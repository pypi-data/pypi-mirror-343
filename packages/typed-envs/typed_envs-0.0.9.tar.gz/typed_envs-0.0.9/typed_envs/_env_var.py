from typing import Generic, TypeVar, Type, Any

T = TypeVar("T")


class EnvironmentVariable(Generic[T]):
    """
    Base class for creating custom wrapper subclasses on the fly.

    Note:
        This is just a base class used to create custom wrapper subclasses on the fly.
        You must never initialize these directly.
        You must use the :func:`create_env` function either on the main module or on an :class:`EnvVarFactory` to initialize your env vars.

    Example:
        Useful for enhancing type hints and __repr__ of variables that hold values you set with env vars.
        Note: This is just a helper class to create custom wrapper classes on the fly.
        You should never initialize these directly.

        Functionally, :class:`EnvironmentVariable` objects will work exactly the same as any instance of specified `typ`.

        In the example below, `some_var` can be used just like any other `int` object.

        .. code-block:: python

            import typed_envs
            some_var = typed_envs.create_env("SET_WITH_THIS_ENV", int, 10)

            >>> isinstance(some_var, int)
            True
            >>> isinstance(some_var, EnvironmentVariable)
            True

        There are only 2 differences between `some_var` and `int(10)`:
        - `some_var` will properly type check as an instance of both `int` and :class:`EnvironmentVariable`
        - `some_var.__repr__()` will include contextual information about the :class:`EnvironmentVariable`.

        .. code-block:: python

            >>> some_var
            <EnvironmentVariable[name=`SET_WITH_THIS_ENV`, type=int, default_value=10, current_value=10, using_default=True]>
            >>> str(some_var)
            "10"
            >>> some_var + 5
            15
            >>> 20 / some_var
            2

    See Also:
        :func:`create_env`, :class:`EnvVarFactory`
    """

    # TODO: give these docstrings
    _base_type: Type[T]
    _default_value: Any
    _using_default: bool
    _env_name: str
    _init_arg0: Any

    def __str__(self) -> str:
        base_type = self._base_type
        string_from_base = base_type.__str__(self)
        # NOTE: If this returns True, base type's `__str__` method calls `__repr__` and our custom `__repr__` breaks it.
        if string_from_base == self.__repr__():
            # We broke it but it's all good, we can fix it with some special case logic.
            return (
                str(bool(self)) if base_type is bool else self._base_type.__repr__(self)
            )
        return (
            self._base_type.__str__(self)
            if "object at 0x" in string_from_base
            else string_from_base
        )

    def __repr__(self) -> str:
        return "<EnvironmentVariable[name=`{}`, type={}, default_value={}, current_value={}, using_default={}]>".format(
            self._env_name,
            self._base_type.__qualname__,
            self._default_value,
            self._init_arg0,
            self._using_default,
        )
