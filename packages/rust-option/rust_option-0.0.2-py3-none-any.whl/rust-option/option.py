from typing import Callable, TypeVar, Generic, cast

T = TypeVar('T')


class Option(Generic[T]):
    """
    A type representing a value that is either present or None.

    # How To Use
    ## Creation
    Creating a None Option:
    ```python
    Option[T].none()
    ```
    Creating a Some Option:
    ```python
    Option[T].some(value) # type :: Option[type(value)]
    ```
    Creating an Option from a value of type `T | None`:
    ```python
    Option[T].new_maybe(value) # will return either a None or Some Option depending on the value.
    ```
    ## Usage
    Checking for a Some Option:
    ```python
    some_Option = Option[T].some(value)
    some_Option.is_some() # returns True
    ```
    Checking for a None Option:
    ```python
    none_Option = Option[T].none()
    none_Option.is_none() # returns True
    ```
    Getting the value out of an Option:
    ```python
    x = Option[T].some(value)
    x.unwrap() # returns value
    y = Option[U].none()
    y.unwrap_or(value2) # returns value2 as y is a None Option
    ```
    """
    _value: T | None
    _filled: bool

    def __init__(self, value: T | None = None) -> None:
        self._value = value
        self._filled = not value is None

    @staticmethod
    def none() -> 'Option[T]':
        """Creates a new none `Option`."""
        return Option()

    @staticmethod
    def some(value: T) -> 'Option[T]':
        """Creates a new some `Option` with the given `value` inside."""
        return Option(value)

    @staticmethod
    def new_maybe(value: T | None) -> 'Option[T]':
        """Returns a new `Option` created with the given `value` which may be some(type(value)) or none."""
        if value is None:
            return Option()
        else:
            return Option(value)

    def is_some(self) -> bool:
        """Checks that a value is present."""
        return self._filled

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """Returns true if the `Option` is some, and the inner value satisfies the given predicate."""
        if self.is_some():
            return f(self.unwrap())
        else:
            return False

    def then[R](self, op: Callable[[T], R]) -> 'Option[R]':
        """
        Applies the function `op` to the inner value and returns a new `Option` with the result.

        # Examples
        ```python
        Option.some(4).then(lambda value: str(value * 2)) # Option.some('8')
        Option.none().then(lambda value: str(value * 2)) # Option.none()
        ```
        """
        if self.is_some():
            return Option[R].some(op(self.unwrap()))
        else:
            return Option[R].none()

    def is_none(self) -> bool:
        """Checks that the `Option` doesn't have a value."""
        return not self._filled

    def is_none_or(self, f: Callable[[T], bool]) -> bool:
        """Returns true if the `Option` is none, or the inner value satisfies the given predicate."""
        if self.is_some():
            return f(self.unwrap())
        else:
            return True

    def otherwise(self, optb: 'Option[T]') -> 'Option[T]':
        """Returns the `Option` if it's some, otherwise return `optb`."""
        if self.is_some():
            return self
        else:
            return optb

    def unwrap(self) -> T:
        """Returns the inner value if this `Option` is some, otherwise throws an `OptionError` if it's none."""
        if self.is_none():
            raise OptionError("Option is empty")

        return cast(T, self._value)

    def unwrap_or(self, other: T) -> T:
        """Returns the inner value if one exists, otherwise returns the `other` value."""
        if self.is_some():
            return cast(T, self._value)
        else:
            return other

    def take(self) -> 'Option[T]':
        """Takes the value out of the `Option`, leaving a None in its place."""
        if self.is_some():
            tmp = self.unwrap()
            self = Option[T].none()
            return Option[T].some(tmp)
        else:
            return self

    def __str__(self) -> str:
        if self.is_some():
            return f"Option.some({self._value})"
        else:
            return "Option.none()"


class OptionError(RuntimeError):
    def __init__(self, text: str):
        super().__init__(text)
