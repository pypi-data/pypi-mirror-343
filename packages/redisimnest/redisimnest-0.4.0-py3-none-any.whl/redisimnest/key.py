import json
from typing import Any, Optional
import re

from .exceptions import AccessDeniedError, MissingParameterError

from .utils.de_serialization import SERIALIZED_TYPE_MAP, deserialize, serialize
from .utils.method_maps import DESERIALIZE_COMMANDS, SERIALIZE_COMMANDS, default_methods
from .utils.misc import get_encryption_key, get_pretty_representation, lazy_import
from .utils.prefix import validate_prefix
from .settings import TTL_AUTO_RENEW, SHOW_METHOD_DISPATCH_LOGS






# ====================================================================================================
# ==============             KEY ARGUMENT PASSING             ==============#
# ====================================================================================================
class KeyArgumentPassing:
    """Handles single and multi param passing to format prefix"""

    def __call__(self, *args, **kwargs):
        """Support positional arguments"""
        for key, arg in zip(self._placeholder_keys, args):
            if key not in kwargs:
                kwargs[key] = arg

        # Validate all placeholders provided
        missing = [k for k in self._placeholder_keys if k not in kwargs]
        if missing:
            raise MissingParameterError(
                f"Missing required param(s) {missing} for key prefix '{self.prefix_template}'"
            )

        self._resolved_args = kwargs  # <-- Store the args
        return self



    def __getitem__(self, value):
        """Support single argument"""
        if len(self._placeholder_keys) != 1:
            raise ValueError(
                f"Key with multiple placeholders ({', '.join(self._placeholder_keys)}) "
                "cannot be used with [] syntax. Use .__call__(...) instead."
            )
        return self(**{self._placeholder_keys[0]: value})



# ============================================================================================================================================
# ============================================================================================================================================
# ===========================                         BASE KEY                         ===========================#
# ============================================================================================================================================
# ============================================================================================================================================
class Key(KeyArgumentPassing):
    def __init__(
        self, 
        prefix_template: str, 
        default: Optional[Any] = None,
        ttl: Optional[int] = None,
        ttl_auto_renew: bool = TTL_AUTO_RENEW,
        is_secret: bool = False,
        is_password: bool = False
    ):
        self.prefix_template = prefix_template
        self.default = default
        self._own_ttl = ttl  # Changed from self.ttl
        self._placeholder_keys = re.findall(r"\{(.*?)\}", prefix_template) if prefix_template else []
        self.ttl_auto_renew = ttl_auto_renew

        if is_secret and is_password:
            raise ValueError(
                "A Key cannot be both 'secret' and 'password'. "
                "'is_secret' is for generic sensitive data, while 'is_password' implies credentials. "
                "Choose only one."
            )
        self.is_secret = is_secret
        self.is_password = is_password

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        cls._generate_methods()
        return instance

    def _resolve_ttl(self):
        # Key-level TTL
        if getattr(self, '_own_ttl', None) is not None:
            return self._own_ttl

        # Subcluster → parent TTLs
        cluster = self._parent
        while cluster:
            ttl = getattr(cluster.__class__, '__ttl__', None)
            if ttl is not None:
                return ttl
            cluster = cluster._parent

        return None  # No TTL found
    
    async def raw(self):
        """Returns the data as is as stored in redis"""
        return await self._parent._redis.get(self.key)

    
    @property
    def key(self) -> str:
        """Returns the final, resolved key for this key instance."""
        if self._placeholder_keys:
            if not hasattr(self, "_resolved_args"):
                raise MissingParameterError(
                    f"Key '{self._name}' was accessed without required params: {self._placeholder_keys}"
                )
            formatted_key = self.prefix_template.format(**self._resolved_args)
            return f"{self._parent.get_full_prefix()}:{formatted_key}"
        else:
            return f"{self._parent.get_full_prefix()}:{self.prefix_template}"
    
    @property
    async def the_type(self):
        """
        Returns the Python `type` object of the value stored at this key, if available.
        """
        the_key = self.key
        raw_value = await self._parent._redis.get(the_key)

        if raw_value is None:
            return None  # No value present at key

        try:
            if isinstance(raw_value, bytes):
                raw_value = raw_value.decode()
            data = json.loads(raw_value)

            if isinstance(data, dict) and "__type__" in data:
                return SERIALIZED_TYPE_MAP.get(data["__type__"], None)
        except Exception:
            pass  # Not serialized with our method


    async def delete(self):
        """Deletes the current key itself"""
        the_key = self.key
        return await self._parent._redis.delete(the_key)


    async def verify_password(self, plain_password: str) -> bool:
        """Verifies given password with original"""
        if not self.is_password:
            raise TypeError("This key does not store a password hash.")
        
        print(f'{plain_password=}')
        hashed = await self._parent._redis.get(self.key)
        if not hashed:
            return None
        
        deserialized = deserialize(hashed)

        print(f'{deserialized}')
        if not isinstance(deserialized, str):
            print('even did not try to check')
            return False

        try:
            bcrypt = lazy_import('bcrypt')
            return bcrypt.checkpw(plain_password.encode(), deserialized.encode())
        except Exception:
            return False


    @property
    def the_ttl(self):
        """Returns the current resolved ttl that is about to be applied"""
        return self._resolve_ttl()
    
    def _resolve_value(self, payload):
        if not self.is_secret and not self.is_password:
            return payload
        
        if payload is None:
            return None
        
        if not isinstance(payload, str):
            raise TypeError("Passwords and secrets must be strings.")
        
        
        if self.is_secret and isinstance(payload, str) and payload.startswith("gAAAA"):
            return payload  # already encrypted


        if self.is_password and isinstance(payload, str) and payload.startswith("$2b$"):
            return payload  # already hashed

        if self.is_password:
            bcrypt = lazy_import('bcrypt')
            payload = bcrypt.hashpw(payload.encode(), bcrypt.gensalt()).decode()
        elif self.is_secret:
            ENCRYPTION_KEY = get_encryption_key()
            fernet = lazy_import('cryptography.fernet').Fernet(ENCRYPTION_KEY)

            payload = fernet.encrypt(payload.encode()).decode()
        return payload

    async def _dispatch_method(self, method: str, *args, **kwargs) -> Any:
        if method not in default_methods:
            raise AttributeError(f"Unsupported method: '{method}'.")

        redis_method = getattr(self._parent._redis, method, None)
        if not callable(redis_method):
            raise AttributeError(f"Redis client does not support method: '{method}'.")
        
        reveal = kwargs.pop('reveal', False)

        full_key_path = self.key
        if SHOW_METHOD_DISPATCH_LOGS:
            print(f"[redisimnest] {method.upper():<8} → {full_key_path} | args={args} kwargs={kwargs}")


        if method in SERIALIZE_COMMANDS:
            
            payload = args[0] if args else kwargs["value"] if 'value' in kwargs else None
            payload = self._resolve_value(payload)

            if args:
                args = (serialize(payload), *args[1:])
            elif 'value' in kwargs:
                kwargs['value'] = serialize(payload)

        # Inject TTL inline where supported
        if method == "set" and self.the_ttl is not None:
            kwargs.setdefault("ex", self.the_ttl)
        
        if method == "restore":
            ttl_ms = (self.the_ttl or 0) * 1000
            result = await redis_method(full_key_path, ttl_ms, *args, **kwargs)

            # Also apply TTL again if needed (usually redundant with ttl_ms but keep it if needed)
            if self.the_ttl:
                await self._parent._redis.expire(self._name, self.the_ttl)

            return result  # ✅ Early return here

        if method == 'get' and self.is_password:
            Warning("Passwords cannot be accessed directly. Use `verify_password` instead.")
        result = await redis_method(full_key_path, *args, **kwargs)

        # Apply TTL manually if method doesn't support it inline
        if method in {"restore"} and self.the_ttl is not None:
            await self._parent._redis.expire(self._name, self.the_ttl)

        # Handle auto-renew on read if enabled
        if self.ttl_auto_renew and method in DESERIALIZE_COMMANDS and self.the_ttl is not None:
            await self._parent._redis.expire(self._name, self.the_ttl)

        # Deserialize result for read operations
        if method in DESERIALIZE_COMMANDS:
            # Fallback to default if result is None
            if result is None:
                return self.default if self.default is not None else None
            
            result = deserialize(result)
            print(f'deserialized result in get: {result}')

            print(f"{self.is_secret=}")

            if result is None:
                return result
            
            
            if self.is_secret:
                print('key is secret trying to encode with fernet')
                try:
                    ENCRYPTION_KEY = get_encryption_key()
                    fernet = lazy_import('cryptography').fernet.Fernet(ENCRYPTION_KEY)
                    fernet_result =  fernet.decrypt(result.encode()).decode()
                    print(f'fernet result: {fernet_result}')
                    return fernet_result
                except Exception:
                    return "[decryption-error]"

            # Password hashes should never be returned
            print(f'{self.is_password=}')
            if self.is_password:
                if reveal:
                    return result
                raise AccessDeniedError("To access secrets, set ALLOW_SECRET_ACCESS=1.")

        return result

    def __set_name__(self, owner, name: str):
        self._name = name

    
    def __get__(self, instance, owner):
        self._parent = instance
        validate_prefix(self.prefix_template, instance.__class__.__name__)
        return self
    
    
    @classmethod
    def _generate_methods(cls):
        """
        Dynamically generate all supported Redis methods for this key class.
        Each generated method will automatically invoke `_dispatch_method`.
        """
        supported_methods = default_methods
        # print(f"KEY_TYPE: {key_type}")
        # pprint(supported_methods)

        for method in supported_methods:
            def make_wrapper(method_name):
                def method_wrapper(self, *args, **kwargs):
                    return self._dispatch_method(method_name, *args, **kwargs)
                return method_wrapper
            setattr(cls, method, make_wrapper(method))
    
    
    def describe(self):
        """Returns key description as dict (name, prefix, params, key, ttl)"""
        return {
            "name": self._name,
            "prefix": self.prefix_template,
            "params": self._placeholder_keys,
            "key": self.key,
            "ttl": self.the_ttl,
            "is_secret": self.is_secret,
            "is_password": self.is_password
        }

    @property
    def __doc__(self):
        return get_pretty_representation(self.describe())
    
    def __repr__(self):
        tag = ' (secret)' if self.is_secret else ' (password)' if self.is_password else ''
        return f"<Key(name='{self._name}' template='{self.prefix_template}'){tag}>"



