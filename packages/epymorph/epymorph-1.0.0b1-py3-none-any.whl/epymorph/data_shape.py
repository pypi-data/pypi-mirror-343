"""
Utility classes to verify the shape of data as numpy arrays
whose dimensions can be relative to the simulation context,
and to adapt equivalent shapes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypeVar

import numpy as np
from numpy.typing import NDArray
from typing_extensions import override

from epymorph.error import DimensionError
from epymorph.util import Matcher


class Dimensions(Protocol):
    """A class to store the lengths of dimensions which are supported by DataShapes.
    It is possible to create Dimensions instances which contain a subset of the
    available dimensions, for cases where the other dimensions aren't known and
    aren't needed."""

    @property
    @abstractmethod
    def T(self) -> int:
        """The number of days."""

    @property
    @abstractmethod
    def N(self) -> int:
        """The number of nodes."""

    @property
    @abstractmethod
    def C(self) -> int:
        """The number of compartments."""

    @property
    @abstractmethod
    def E(self) -> int:
        """The number of events."""

    @staticmethod
    def of(
        *,
        T: int | None = None,
        N: int | None = None,
        C: int | None = None,
        E: int | None = None,
    ) -> "Dimensions":
        if T is not None and N is not None and C is not None and E is not None:
            return CompleteDimensions(T=T, N=N, C=C, E=E)
        return PartialDimensions(T=T, N=N, C=C, E=E)


class PartialDimensions(Dimensions):
    """A Dimensions instance where some dimensions are unknown.
    If code accesses an unknown dimension, a DimensionError is raised."""

    _T: int | None
    _N: int | None
    _C: int | None
    _E: int | None

    def __init__(
        self,
        *,
        T: int | None = None,
        N: int | None = None,
        C: int | None = None,
        E: int | None = None,
    ):
        self._T = T
        self._N = N
        self._C = C
        self._E = E

    @property
    @override
    def T(self):
        if self._T is None:
            raise DimensionError("We need dimension T but it was not provided.")
        return self._T

    @property
    @override
    def N(self):
        if self._N is None:
            raise DimensionError("We need dimension N but it was not provided.")
        return self._N

    @property
    @override
    def C(self):
        if self._C is None:
            raise DimensionError("We need dimension C but it was not provided.")
        return self._C

    @property
    @override
    def E(self):
        if self._E is None:
            raise DimensionError("We need dimension E but it was not provided.")
        return self._E


class CompleteDimensions(Dimensions):
    """A Dimensions instance where all dimensions are known."""

    _T: int
    _N: int
    _C: int
    _E: int

    def __init__(
        self,
        *,
        T: int,
        N: int,
        C: int,
        E: int,
    ):
        self._T = T
        self._N = N
        self._C = C
        self._E = E

    @property
    @override
    def T(self):
        return self._T

    @property
    @override
    def N(self):
        return self._N

    @property
    @override
    def C(self):
        return self._C

    @property
    @override
    def E(self):
        return self._E


DataT = TypeVar("DataT", bound=np.generic)


class DataShape(ABC):
    """Description of a data attribute's shape relative to a simulation context."""

    @abstractmethod
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        """Returns a tuple with the lengths of the dimensions in this shape.
        If an axis is of indeterminate length, that axis is represented as -1."""

    @abstractmethod
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        """Does the given value match this shape expression?"""

    @abstractmethod
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        """Adapt the given value to this shape; raise ValueError if we can't."""


@dataclass(frozen=True)
class Scalar(DataShape):
    """A scalar value."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return ()

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        return value.shape == tuple()

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        if not self.matches(dim, value):
            raise ValueError("Not able to adapt shape.")
        return value

    def __str__(self):
        return "S"


@dataclass(frozen=True)
class Time(DataShape):
    """An array of at least size T (the number of simulation days)."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (dim.T,)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        if value.ndim == 1 and value.shape[0] >= dim.T:
            return True
        if value.shape == tuple():
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        if value.ndim == 1 and value.shape[0] >= dim.T:
            return value[: dim.T]
        if value.shape == tuple():
            return np.broadcast_to(value, shape=(dim.T,))
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "T"


@dataclass(frozen=True)
class Node(DataShape):
    """An array of size N (the number of simulation nodes)."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (dim.N,)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        if value.ndim == 1 and value.shape[0] == dim.N:
            return True
        if value.shape == tuple():
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        if value.ndim == 1 and value.shape[0] == dim.N:
            return value
        if value.shape == tuple():
            return np.broadcast_to(value, shape=(dim.N,))
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "N"


@dataclass(frozen=True)
class NodeAndNode(DataShape):
    """An array of size NxN."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (dim.N, dim.N)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        shape = self.to_tuple(dim)
        if value.shape == shape:
            return True
        if value.shape == tuple():
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        shape = self.to_tuple(dim)
        if value.shape == shape:
            return value
        if value.shape == tuple():
            return np.broadcast_to(value, shape=shape)
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "NxN"


@dataclass(frozen=True)
class NodeAndCompartment(DataShape):
    """An array of size NxC."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (dim.N, dim.C)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        N, C = self.to_tuple(dim)
        if value.shape == (N, C):
            return True
        if value.shape == tuple():
            return True
        if value.shape == (N,):
            return True
        if value.shape == (C,):
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        N, C = self.to_tuple(dim)
        if value.shape == (N, C):
            return value
        if value.shape == tuple():
            return np.broadcast_to(value, shape=(N, C))
        if value.shape == (N,):
            return np.broadcast_to(value[:, np.newaxis], shape=(N, C))
        if value.shape == (C,):
            return np.broadcast_to(value, shape=(N, C))
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "NxC"


@dataclass(frozen=True)
class TimeAndNode(DataShape):
    """An array of size at-least-T by exactly-N."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (dim.T, dim.N)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        T, N = self.to_tuple(dim)
        if value.ndim == 2 and value.shape[0] >= T and value.shape[1] == N:
            return True
        if value.shape == tuple():
            return True
        if value.shape == (N,):
            return True
        if value.ndim == 1 and value.shape[0] >= T:
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        T, N = self.to_tuple(dim)
        if value.ndim == 2 and value.shape[0] >= T and value.shape[1] == N:
            return value[:T, :]
        if value.shape == tuple():
            return np.broadcast_to(value, shape=(T, N))
        if value.shape == (N,):
            return np.broadcast_to(value, shape=(T, N))
        if value.ndim == 1 and value.shape[0] >= T:
            return np.broadcast_to(value[:T, np.newaxis], shape=(T, N))
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "TxN"


@dataclass(frozen=True)
class NodeAndArbitrary(DataShape):
    """An array of size exactly-N by any dimension."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (dim.N, -1)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        if value.ndim == 2 and value.shape[0] == dim.N:
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        if self.matches(dim, value):
            return value
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "NxA"


@dataclass(frozen=True)
class ArbitraryAndNode(DataShape):
    """An array of size any dimension by exactly-N."""

    @override
    def to_tuple(self, dim: Dimensions) -> tuple[int, ...]:
        return (-1, dim.N)

    @override
    def matches(self, dim: Dimensions, value: NDArray) -> bool:
        if value.ndim == 2 and value.shape[1] == dim.N:
            return True
        return False

    @override
    def adapt(self, dim: Dimensions, value: NDArray[DataT]) -> NDArray[DataT]:
        if self.matches(dim, value):
            return value
        raise ValueError("Not able to adapt shape.")

    def __str__(self):
        return "AxN"


@dataclass(frozen=True)
class Shapes:
    """Static instances for all available shapes."""

    # Data can be in any of these shapes, where:
    # - Scalar is a single scalar value
    # - T is the number of days
    # - N is the number of nodes
    # - C is the number of IPM compartments
    # - A is any length (arbitrary; this dimension is effectively unchecked)

    Scalar = Scalar()
    T = Time()
    N = Node()
    NxC = NodeAndCompartment()
    NxN = NodeAndNode()
    TxN = TimeAndNode()
    NxA = NodeAndArbitrary()
    AxN = ArbitraryAndNode()


def parse_shape(shape: str) -> DataShape:
    """Attempt to parse an AttributeShape from a string."""
    match shape:
        case "Scalar":
            return Shapes.Scalar
        case "T":
            return Shapes.T
        case "N":
            return Shapes.N
        case "NxC":
            return Shapes.NxC
        case "NxN":
            return Shapes.NxN
        case "TxN":
            return Shapes.TxN
        case "NxA":
            return Shapes.NxA
        case "AxN":
            return Shapes.AxN
        case _:
            raise ValueError(f"'{shape}' is not a valid shape specification.")


class DataShapeMatcher(Matcher[NDArray]):
    """Matches an array as adaptable to `shape` under the given Dimensions (`dim`)."""

    _shape: DataShape
    _dim: Dimensions
    _exact: bool

    def __init__(self, shape: DataShape, dim: Dimensions, *, exact: bool = False):
        self._shape = shape
        self._dim = dim
        self._exact = exact

    def expected(self) -> str:
        """Describes what the expected value is."""
        return str(self._shape)

    def __call__(self, value: NDArray) -> bool:
        if self._exact:
            # If making an exact match, convert the expected shape to a tuple
            # then see that the expected shape matches the value shape.
            # They must have the same number of dimensions.
            # A value of -1 in the expected tuple matches any value,
            # this is to support shapes with Arbitrary dimensions.
            expected = self._shape.to_tuple(self._dim)
            return len(value.shape) == len(expected) and all(
                True if exp == -1 else exp == act
                for exp, act in zip(expected, value.shape)
            )
        return self._shape.matches(self._dim, value)
