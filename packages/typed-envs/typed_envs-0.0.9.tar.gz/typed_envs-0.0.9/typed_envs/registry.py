from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from typed_envs._env_var import EnvironmentVariable

_EnvsRegistry = Dict[str, "EnvironmentVariable"]

ENVIRONMENT: _EnvsRegistry = {}
_ENVIRONMENT_VARIABLES_SET_BY_USER: _EnvsRegistry = {}
_ENVIRONMENT_VARIABLES_USING_DEFAULTS: _EnvsRegistry = {}
