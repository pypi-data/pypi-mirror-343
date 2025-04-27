"""
Checking types based on the type hints of the function arguments. This saves
a lot of boilerplate tests, since the type hints will automatically be checked.
"""

import beartype

__all__ = ["typecheck"]

# type check a function call based on its type hints, but only print warnings
# this is separated out into its own module so that changing it in one place
# will affect all modules that use it
typecheck = beartype.beartype(
    conf=beartype.BeartypeConf(
        violation_type=UserWarning,
    )
)

typecheck.__doc__ = """
Type check a function call based on its type hints.
If a violation is detected, a warning is printed.

Parameters
----------
func : Callable
    The function to type check.

Returns
-------
func
    The function with the type hints checked.
"""
