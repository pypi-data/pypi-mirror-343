import inspect
import re
from typing import Any, Dict

from .exceptions import MissingParameterError, ParameterValidationError

from .settings import REDIS_DELETE_CHUNK_SIZE, SHOW_METHOD_DISPATCH_LOGS
from .utils.misc import get_pretty_representation
from .utils.prefix import validate_prefix
from .utils.redis import scan_keys




# ==============______CLUSTER ACCESSOR______=========================================================================================== CLUSTER ACCESSOR
class ClusterAccessor:
    def __init__(self, cls):
        self.cls = cls

    def __get__(self, instance, owner):
        if instance is None:
            return self.cls
        
        instance.get_full_prefix()
        
        return BoundClusterFactory(instance, self.cls)
    def __repr__(self):
        return f"<ClusterAccessor for {self.cls.__name__}>"







# ==============______BOUDN CLUSTER FACTORY______=========================================================================================== BOUDN CLUSTER FACTORY
class BoundClusterFactory:
    def __init__(self, parent_instance, cluster_cls):
        self.parent = parent_instance
        self.cluster_cls = cluster_cls

    def __call__(self, *args, **kwargs):
        if not issubclass(self.cluster_cls, BaseCluster):
            self.cluster_cls = type(
                self.cluster_cls.__name__,
                (BaseCluster, self.cluster_cls),
                dict(self.cluster_cls.__dict__)
            )

        # Extract placeholder keys from __prefix__
        prefix_template = getattr(self.cluster_cls, "__prefix__", "")
        placeholder_keys = re.findall(r"\{(.*?)\}", prefix_template)

        # Map args to keys in order if kwargs not already provided
        for key, arg in zip(placeholder_keys, args):
            if key not in kwargs:
                kwargs[key] = arg

        return self.cluster_cls(
            inherited_params={**self.parent._inherited_params, **kwargs},
            _parent=self.parent
        )

    def __getattr__(self, name):
        return getattr(self(), name)
    
    def __getitem__(self, value):
        # Infer key name from __prefix__ placeholders
        prefix_template = getattr(self.cluster_cls, "__prefix__", "")
        placeholder_keys = re.findall(r"\{(.*?)\}", prefix_template)

        if not placeholder_keys:
            raise ValueError("No placeholders in prefix to apply item access")
        if len(placeholder_keys) > 1:
            raise ValueError(
                f"Cluster '{self.cluster_cls.__name__}' has multiple placeholders "
                f"({', '.join(placeholder_keys)}); use explicit keyword arguments instead."
            )

        return self.__call__(**{placeholder_keys[0]: value})
    def __repr__(self):
        cls_name = self.cluster_cls.__name__
        parent = repr(self.parent)
        return f"<BoundClusterFactory cluster='{cls_name}' parent={parent}>"

    






# ====================================================================================================
# ==============             BASE CLUSTER             ==============#
# ====================================================================================================
class BaseCluster:
    __prefix__ = "base"
    __ttl__ = None  # Optional TTL in seconds
    ENABLE_CACHING = True  # Default is ON; override per class if needed

    
    def __init__(self, redis_client=None, inherited_params: Dict[str, Any] = None, _parent=None):
        self._inherited_params = inherited_params or {}
        self._parent = _parent
        self._apply_validators()
        self._bind_subclusters()
        # self._collect_runtime_structure()

        self.__doc__ = get_pretty_representation(self.describe())
        self._redis = redis_client or getattr(_parent, "_redis", None)

    def _apply_validators(self):
        validators = getattr(self.__class__, "__validators__", {})
        for key, validator in validators.items():
            if key in self._inherited_params:
                value = self._inherited_params[key]
                if not validator(value):
                    raise ParameterValidationError(
                        f"Validation failed for '{key}' with value '{value}' in cluster '{self.__class__.__name__}'"
                    ) from None
    def _bind_subclusters(self):
        for name, attr in self.__class__.__dict__.items():
            if inspect.isclass(attr):
                # Enforce that all subclusters declare __prefix__
                if not hasattr(attr, "__prefix__"):
                    raise ValueError(
                        f"Cluster '{attr.__name__}' must define a '__prefix__' attribute "
                        f"to be used as a subcluster of '{self.__class__.__name__}'"
                    )

                # Promote non-BaseCluster classes into BaseCluster subclasses
                if not issubclass(attr, BaseCluster):
                    attr = type(
                        attr.__name__,
                        (BaseCluster, attr),
                        dict(attr.__dict__)
                    )

                validate_prefix(attr.__prefix__, attr.__name__)
                setattr(self.__class__, name, ClusterAccessor(attr))

    def _collect_prefix_parts(self):
        parts = []
        required_keys = set()
        cluster = self

        while cluster:
            prefix_template = getattr(cluster.__class__, "__prefix__", "")
            keys = re.findall(r"\{(.*?)\}", prefix_template)
            required_keys.update(keys)
            try:
                parts.insert(0, prefix_template.format(**cluster._inherited_params))
            except KeyError:
                parts.insert(0, prefix_template)
            cluster = cluster._parent

        return parts, required_keys
    
    def _compute_full_prefix(self):
        parts = []
        required_keys = set()
        cluster = self

        while cluster:
            prefix_template = getattr(cluster.__class__, "__prefix__", "")
            keys = re.findall(r"\{(.*?)\}", prefix_template)
            required_keys.update(keys)

            try:
                # Ensure this line is awaited if it's making Redis calls or coroutines
                parts.insert(0, prefix_template.format(**cluster._inherited_params))
            except KeyError as e:
                missing_key = e.args[0]
                raise MissingParameterError(
                    f"Missing required param '{missing_key}' for prefix '{prefix_template}' "
                    f"in cluster '{cluster.__class__.__name__}'"
                ) from None

            cluster = cluster._parent

        return ":".join(p for p in parts if p)

    def get_full_prefix(self):
        if self.ENABLE_CACHING:
            if not hasattr(self, "_cached_prefix"):
                self._cached_prefix = self._compute_full_prefix()
            return self._cached_prefix
        return self._compute_full_prefix()
    


    def with_params(self, **params):
        new_instance = self.__class__({**self._inherited_params, **params}, _parent=self._parent)
        # Clear cached prefix if it exists
        if hasattr(new_instance, "_cached_prefix"):
            del new_instance._cached_prefix
        return new_instance
    
    def describe(self):
        prefix = getattr(self.__class__, "__prefix__", "")
        params = re.findall(r"\{(.*?)\}", prefix)
        missing = [p for p in params if p not in self._inherited_params]

        subclusters = []
        keys = []

        for name, value in self.__class__.__dict__.items():
            if name.startswith("__"):
                continue
            from .key import Key
            if isinstance(value, ClusterAccessor):
                subclusters.append(name)
            elif isinstance(value, Key):
                keys.append(name)

        return {
            "prefix": prefix,
            "params": params,
            "missing_params": missing,
            "subclusters": subclusters,
            "keys": keys
        }
    
    async def clear(self) -> None:
        """
        Deletes all keys under this cluster by scanning with the cluster prefix.
        """
        cluster_prefix = self.get_full_prefix() + '*'
        keys = await scan_keys(self._redis, cluster_prefix)
        
        if not keys:
            return
        chunks = []
        for i in range(0, len(keys), REDIS_DELETE_CHUNK_SIZE):
            chunk = keys[i:i + REDIS_DELETE_CHUNK_SIZE]
            result = await self._redis.delete(*chunk)
            chunks.append(f"[redisimnest] CLEAR → Cluster: {self.__class__.__name__} | chunk: {i+1} | deleted: {result} | keys: {chunk}")

        if SHOW_METHOD_DISPATCH_LOGS:
            print('\n'.join(chunks))
            
        return True
    
    async def subkeys(self) -> None:
        """
        Returns all keys under this cluster by scanning with the cluster prefix.
        """
        cluster_prefix = self.get_full_prefix() + '*'
        keys = await scan_keys(self._redis, cluster_prefix)
        
        return keys or []


    
    def __repr__(self):
        cls_name = self.__class__.__name__
        params = ", ".join(f"{k}={v}" for k, v in self._inherited_params.items())
        return f"<{cls_name}({params})>"

