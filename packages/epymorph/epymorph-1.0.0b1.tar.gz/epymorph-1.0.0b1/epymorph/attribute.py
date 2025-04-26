from dataclasses import dataclass, field
from typing import Generic, Self, TypeVar

from epymorph.data_shape import DataShape
from epymorph.data_type import AttributeType, AttributeValue, dtype_as_np, dtype_check
from epymorph.util import acceptable_name

########################
# Names and Namespaces #
########################


def _validate_pattern_segments(*names: str) -> None:
    for n in names:
        if len(n) == 0:
            raise ValueError("Invalid pattern: cannot use empty strings.")
        if "::" in n:
            raise ValueError("Invalid pattern: cannot contain '::'.")


def _validate_name_segments(*names: str) -> None:
    for n in names:
        if len(n) == 0:
            raise ValueError("Invalid name: cannot use empty strings.")
        if n == "*":
            raise ValueError("Invalid name: cannot use wildcards (*).")
        if "::" in n:
            raise ValueError("Invalid name: cannot contain '::'.")


@dataclass(frozen=True)
class ModuleNamespace:
    """A namespace with a specified strata and module."""

    strata: str
    module: str

    def __post_init__(self):
        _validate_name_segments(self.strata, self.module)

    @classmethod
    def parse(cls, name: str) -> Self:
        """Parse a module name from a ::-delimited string."""
        parts = name.split("::")
        if len(parts) != 2:
            raise ValueError("Invalid number of parts for namespace.")
        return cls(*parts)

    def __str__(self) -> str:
        return f"{self.strata}::{self.module}"

    def to_absolute(self, attrib_id: str) -> "AbsoluteName":
        """Creates an absolute name by providing the attribute ID."""
        return AbsoluteName(self.strata, self.module, attrib_id)


@dataclass(frozen=True)
class AbsoluteName:
    """A fully-specified name (strata, module, and attribute ID)."""

    strata: str
    module: str
    id: str

    def __post_init__(self):
        _validate_name_segments(self.strata, self.module, self.id)

    @classmethod
    def parse(cls, name: str) -> Self:
        """Parse a module name from a ::-delimited string."""
        parts = name.split("::")
        if len(parts) != 3:
            raise ValueError("Invalid number of parts for absolute name.")
        return cls(*parts)

    def __str__(self) -> str:
        return f"{self.strata}::{self.module}::{self.id}"

    def in_strata(self, new_strata: str) -> "AbsoluteName":
        """
        Creates a new AbsoluteName that is a copy of this name
        but with the given strata.
        """
        return AbsoluteName(new_strata, self.module, self.id)

    def with_id(self, new_id: str) -> "AbsoluteName":
        """
        Creates a new AbsoluteName that is a copy of this name
        but with the given ID.
        """
        return AbsoluteName(self.strata, self.module, new_id)

    def to_namespace(self) -> ModuleNamespace:
        """Extracts the module namespace of this name."""
        return ModuleNamespace(self.strata, self.module)

    def to_pattern(self) -> "NamePattern":
        """Converts this name to a pattern that is an exact match for this name."""
        return NamePattern(self.strata, self.module, self.id)


STRATA_PLACEHOLDER = "(unspecified)"
MODULE_PLACEHOLDER = "(unspecified)"
ID_PLACEHOLDER = "(unspecified)"
NAMESPACE_PLACEHOLDER = ModuleNamespace(STRATA_PLACEHOLDER, MODULE_PLACEHOLDER)
"""A namespace to use when we don't need to be specific."""
NAME_PLACEHOLDER = NAMESPACE_PLACEHOLDER.to_absolute(ID_PLACEHOLDER)
"""An absolute name to use when we don't need to be specific."""


@dataclass(frozen=True)
class ModuleName:
    """A partially-specified name with module and attribute ID."""

    module: str
    id: str

    def __post_init__(self):
        _validate_name_segments(self.module, self.id)

    @classmethod
    def parse(cls, name: str) -> Self:
        """Parse a module name from a ::-delimited string."""
        parts = name.split("::")
        if len(parts) != 2:
            raise ValueError("Invalid number of parts for module name.")
        return cls(*parts)

    def __str__(self) -> str:
        return f"{self.module}::{self.id}"

    def to_absolute(self, strata: str) -> AbsoluteName:
        """Creates an absolute name by providing the strata."""
        return AbsoluteName(strata, self.module, self.id)


@dataclass(frozen=True)
class AttributeName:
    """A partially-specified name with just an attribute ID."""

    id: str

    def __post_init__(self):
        _validate_name_segments(self.id)

    def __str__(self) -> str:
        return self.id


@dataclass(frozen=True)
class NamePattern:
    """
    A name with a strata, module, and attribute ID that allows wildcards (*) so it can
    act as a pattern to match against AbsoluteNames.
    """

    strata: str
    module: str
    id: str

    def __post_init__(self):
        _validate_pattern_segments(self.strata, self.module, self.id)

    @classmethod
    def parse(cls, name: str) -> Self:
        """
        Parse a pattern from a ::-delimited string. As a shorthand, you can omit
        preceding wildcard segments and they will be automatically filled in,
        e.g., "a" will become "*::*::a" and "a::b" will become "*::a::b".
        """
        parts = name.split("::")
        match len(parts):
            case 1:
                return cls("*", "*", *parts)
            case 2:
                return cls("*", *parts)
            case 3:
                return cls(*parts)
            case _:
                raise ValueError("Invalid number of parts for name pattern.")

    @staticmethod
    def of(name: "str | NamePattern") -> "NamePattern":
        """Coerce the given value to a NamePattern.
        If it's already a NamePattern, return it; if it's a string, parse it."""
        return name if isinstance(name, NamePattern) else NamePattern.parse(name)

    def match(self, name: "AbsoluteName | NamePattern") -> bool:
        """
        Test this pattern to see if it matches the given AbsoluteName or NamePattern.
        The ability to match against NamePatterns is useful to see if two patterns
        conflict with each other and would create ambiguity.
        """
        match name:
            case AbsoluteName(s, m, i):
                if self.strata != "*" and self.strata != s:
                    return False
                if self.module != "*" and self.module != m:
                    return False
                if self.id != "*" and self.id != i:
                    return False
                return True
            case NamePattern(s, m, i):
                if self.strata != "*" and s != "*" and self.strata != s:
                    return False
                if self.module != "*" and m != "*" and self.module != m:
                    return False
                if self.id != "*" and i != "*" and self.id != i:
                    return False
                return True
            case _:
                raise ValueError(f"Unsupported match: {type(name)}")

    def __str__(self) -> str:
        return f"{self.strata}::{self.module}::{self.id}"


@dataclass(frozen=True)
class ModuleNamePattern:
    """
    A name with a module and attribute ID that allows wildcards (*).
    Mostly this is useful to provide parameters to GPMs, which don't have
    a concept of which strata they belong to. A ModuleNamePattern can be
    transformed into a full NamePattern by adding the strata.
    """

    module: str
    id: str

    def __post_init__(self):
        _validate_pattern_segments(self.module, self.id)

    @classmethod
    def parse(cls, name: str) -> Self:
        """
        Parse a pattern from a ::-delimited string. As a shorthand, you can omit
        a preceding wildcard segment and it will be automatically filled in,
        e.g.,"a" will become "*::a".
        """
        if len(name) == 0:
            raise ValueError("Empty string is not a valid name.")
        parts = name.split("::")
        match len(parts):
            case 1:
                return cls("*", *parts)
            case 2:
                return cls(*parts)
            case _:
                raise ValueError("Invalid number of parts for module name pattern.")

    def to_absolute(self, strata: str) -> NamePattern:
        """Creates a full name pattern by providing the strata."""
        return NamePattern(strata, self.module, self.id)

    def __str__(self) -> str:
        return f"{self.module}::{self.id}"


##############
# Attributes #
##############


AttributeT = TypeVar("AttributeT", bound=AttributeType)
"""The data type of an attribute; maps to the numpy type of the attribute array."""


@dataclass(frozen=True)
class AttributeDef(Generic[AttributeT]):
    """
    The definition of a data attribute.

    AttributeDef is a frozen dataclass.

    AttributeDef is generic on the [`AttributeType`](`epymorph.data_type.AttributeType`)
    which describes the type of the data (`AttributeT`).
    """

    name: str
    """The name used to identify the attribute."""
    type: AttributeT
    """The type of the data."""
    shape: DataShape
    """The expected array shape of the data."""
    default_value: AttributeValue | None = field(default=None, compare=False)
    """An optional default value."""
    comment: str | None = field(default=None, compare=False)
    """An optional description of the attribute."""

    def __post_init__(self):
        if acceptable_name.match(self.name) is None:
            raise ValueError(f"Invalid attribute name: {self.name}")
        try:
            dtype_as_np(self.type)
        except Exception as e:
            msg = (
                f"AttributeDef's type is not correctly specified: {self.type}\n"
                "See documentation for appropriate type designations."
            )
            raise ValueError(msg) from e

        if (
            self.default_value is not None  #
            and not dtype_check(self.type, self.default_value)
        ):
            msg = (
                "AttributeDef's default value does not align with its dtype "
                f"('{self.name}')."
            )
            raise ValueError(msg)
