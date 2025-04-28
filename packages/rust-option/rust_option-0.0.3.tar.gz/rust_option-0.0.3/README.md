# rust-option

rust-like option type for python

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
