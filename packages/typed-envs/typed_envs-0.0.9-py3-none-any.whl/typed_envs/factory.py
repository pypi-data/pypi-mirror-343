import logging
import os
from functools import lru_cache
from contextlib import suppress
from types import new_class
from typing import Any, Callable, Optional, Type, TypeVar

from typed_envs import registry
from typed_envs._env_var import EnvironmentVariable

T = TypeVar("T")


class EnvVarFactory:
    """Factory for creating :class:`EnvironmentVariable` instances with optional prefix."""

    def __init__(self, env_var_prefix: Optional[str] = None) -> None:
        """
        Initializes the :class:`EnvVarFactory` with an optional prefix for environment variables.

        Args:
            env_var_prefix: An optional string prefix to be added to environment variable names.
        """
        self.prefix = env_var_prefix

    def create_env(
        self,
        env_var_name: Optional[str],
        env_var_type: Type[T],
        default: Any,
        *init_args,
        string_converter: Optional[Callable[[str], Any]] = None,
        verbose: bool = True,
        **init_kwargs,
    ) -> "EnvironmentVariable[T]":
        """
        Creates a new :class:`EnvironmentVariable` object with the specified parameters.

        Args:
            env_var_name: The name of the environment variable.
            env_var_type: The type of the environment variable.
            default: The default value for the environment variable.
            *init_args: Additional positional arguments for initialization.
            string_converter: An optional callable to convert the string value from the environment.
            verbose: If True, logs the environment variable details.
            **init_kwargs: Additional keyword arguments for initialization.

        Returns:
            An instance of :class:`EnvironmentVariable` with the specified type and value.

        Example:
            Create an environment variable with an integer type using an `EnvVarFactory` instance:

            ```python
            from typed_envs.factory import EnvVarFactory
            factory = EnvVarFactory()
            some_var = factory.create_env("SET_WITH_THIS_ENV", int, 10)

            >>> isinstance(some_var, int)
            True
            >>> isinstance(some_var, EnvironmentVariable)
            True
            ```

            Differences between `some_var` and `int(10)`:
            - `some_var` will type check as both `int` and :class:`EnvironmentVariable`.
            - `some_var.__repr__()` includes contextual information about the :class:`EnvironmentVariable`.

            ```python
            >>> some_var
            <EnvironmentVariable[name=`SET_WITH_THIS_ENV`, type=int, default_value=10, current_value=10, using_default=True]>
            >>> str(some_var)
            "10"
            >>> some_var + 5
            15
            >>> 20 / some_var
            2
            ```

        See Also:
            - :func:`typed_envs.create_env` for creating environment variables without a prefix.
        """
        if self.prefix:
            env_var_name = f"{self.prefix}_{env_var_name}"
        var_value = os.environ.get(env_var_name)
        using_default = var_value is None
        var_value = var_value or default
        if env_var_type is bool:
            if isinstance(var_value, str) and var_value.lower() == "false":
                var_value = False
            else:
                with suppress(ValueError):
                    # if var_value is "0" or "1"
                    var_value = int(var_value)
                var_value = bool(var_value)
        if any(iter_typ in env_var_type.__bases__ for iter_typ in [list, tuple, set]):
            var_value = var_value.split(",")
        if string_converter and not (
            using_default and isinstance(default, env_var_type)
        ):
            var_value = string_converter(var_value)

        subclass = _create_subclass(env_var_type)
        instance = subclass(var_value, *init_args, **init_kwargs)
        # Set additional attributes
        instance._init_arg0 = var_value
        instance._env_name = env_var_name
        instance._default_value = default
        instance._using_default = using_default

        # Finish up
        if verbose:
            # This code prints envs on script startup for convenience of your users.
            try:
                logger.info(instance.__repr__())
            except RecursionError:
                logger.debug(
                    "unable to properly display your `%s` %s env due to RecursionError",
                    env_var_name,
                    instance.__class__.__base__,
                )
                with suppress(RecursionError):
                    logger.debug(
                        "Here is your `%s` env in string form: %s",
                        env_var_name,
                        str(instance),
                    )
        _register_new_env(env_var_name, instance)
        return instance


@lru_cache(maxsize=None)
def _create_subclass(typ: Type[T]) -> Type["EnvironmentVariable[T]"]:
    """
    Returns a mixed subclass of `typ` and :class:`EnvironmentVariable` that does 2 things:
     - modifies the __repr__ method so its clear an object's value was set with an env var while when inspecting variables
     - ensures the instance will type check as an :class:`EnvironmentVariable` object without losing information about its actual type

    Aside from these two things, subclass instances will function exactly the same as any other instance of `typ`.
    """
    subclass_name = f"EnvironmentVariable_{typ.__name__}"
    # You can't subclass a boolean but its just an int anyway
    subclass_bases = (int if typ is bool else typ, EnvironmentVariable[typ])
    cls = new_class(subclass_name, subclass_bases, {})
    cls.__repr__ = EnvironmentVariable.__repr__
    cls.__str__ = EnvironmentVariable.__str__
    cls._base_type = typ
    return cls


def _register_new_env(name: str, instance: EnvironmentVariable) -> None:
    registry.ENVIRONMENT[name] = instance
    if instance._using_default:
        registry._ENVIRONMENT_VARIABLES_USING_DEFAULTS[name] = instance
    else:
        registry._ENVIRONMENT_VARIABLES_SET_BY_USER[name] = instance


# NOTE: While we create the TYPEDENVS_SHUTUP object in the ENVIRONMENT_VARIABLES file as an example,
#       we cannot use it here without creating a circular import.

logger = logging.getLogger("typed_envs")

from typed_envs import ENVIRONMENT_VARIABLES

if ENVIRONMENT_VARIABLES.SHUTUP:
    logger.disabled = True
else:
    if not logger.hasHandlers():
        logger.addHandler(logging.StreamHandler())
    if not logger.isEnabledFor(logging.INFO):
        logger.setLevel(logging.INFO)


default_factory = EnvVarFactory()
