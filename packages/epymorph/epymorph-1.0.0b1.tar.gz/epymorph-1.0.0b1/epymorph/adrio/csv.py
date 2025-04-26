"""ADRIOs that load data from locally available CSV files."""
# ruff: noqa: A005

from datetime import date
from os import PathLike
from pathlib import Path
from typing import Any, Literal

from numpy.typing import DTypeLike, NDArray
from pandas import DataFrame, Series, read_csv
from typing_extensions import override

from epymorph.adrio.adrio import ADRIOLegacy
from epymorph.error import DataResourceError
from epymorph.geography.scope import GeoScope
from epymorph.geography.us_census import CensusScope, CountyScope, StateScope
from epymorph.geography.us_geography import CensusGranularity
from epymorph.geography.us_tiger import get_counties, get_states
from epymorph.time import TimeFrame

KeySpecifier = Literal["state_abbrev", "county_state", "geoid"]


def _parse_label(
    key_type: KeySpecifier,
    scope: GeoScope,
    df: DataFrame,
    key_col: int,
    key_col2: int | None = None,
) -> DataFrame:
    """
    Reads labels from a dataframe according to key type specified and replaces them
    with a uniform value to sort by.
    Returns dataframe with values replaced in the label column.
    """
    match key_type:
        case "state_abbrev":
            result = _parse_abbrev(scope, df, key_col, key_col2)

        case "county_state":
            result = _parse_county_state(scope, df, key_col, key_col2)

        case "geoid":
            result = _parse_geoid(scope, df, key_col, key_col2)

    _validate_result(scope, result[key_col])

    if key_col2 is not None:
        _validate_result(scope, result[key_col2])

    return result


def _parse_abbrev(
    scope: GeoScope, df: DataFrame, key_col: int, key_col2: int | None = None
) -> DataFrame:
    """
    Replaces values in label column containing state abreviations (i.e. AZ) with state
    fips codes and filters out any not in the specified geographic scope.
    """
    if not isinstance(scope, StateScope):
        msg = "State scope is required to use state abbreviation key format."
        raise DataResourceError(msg)

    state_mapping = get_states(scope.year).state_code_to_fips

    result_df = df.copy()
    result_df[key_col] = [state_mapping.get(x) for x in result_df[key_col]]
    if result_df[key_col].isna().any():
        raise DataResourceError("Invalid state code in key column.")
    result_df = result_df[result_df[key_col].isin(scope.node_ids)]

    if key_col2 is not None:
        result_df[key_col2] = [state_mapping.get(x) for x in result_df[key_col2]]
        if result_df[key_col2].isna().any():
            raise DataResourceError("Invalid state code in second key column.")
        result_df = result_df[result_df[key_col2].isin(scope.node_ids)]

    return result_df


def _parse_county_state(
    scope: GeoScope, df: DataFrame, key_col: int, key_col2: int | None = None
) -> DataFrame:
    """
    Replaces values in label column containing county and state names
    (i.e. Maricopa, Arizona) with state county fips codes and filters out
    any not in the specified geographic scope.
    """
    if not isinstance(scope, CountyScope):
        msg = "County scope is required to use county, state key format."
        raise DataResourceError(msg)

    node_ids = scope.node_ids
    geoid_to_name = get_counties(scope.year).county_fips_to_name
    name_to_geoid = {v: k for k, v in geoid_to_name.items() if k in node_ids}

    # filter to scope
    result_df = df[df[key_col].isin(name_to_geoid.keys())]
    if key_col2 is not None:
        result_df = df[df[key_col2].isin(name_to_geoid.keys())]

    # convert keys to geoid
    result_df[key_col] = result_df[key_col].map(name_to_geoid)
    if key_col2 is not None:
        result_df[key_col2] = result_df[key_col2].map(name_to_geoid)

    return result_df


def _parse_geoid(
    scope: GeoScope, df: DataFrame, key_col: int, key_col2: int | None = None
) -> DataFrame:
    """
    Replaces values in label column containing state abreviations (i.e. AZ)
    with state fips codes and filters out any not in the specified geographic scope.
    """
    if not isinstance(scope, CensusScope):
        msg = "Census scope is required to use geoid key format."
        raise DataResourceError(msg)

    granularity = CensusGranularity.of(scope.granularity)
    if not all(granularity.matches(x) for x in df[key_col]):
        raise DataResourceError("Invalid geoid in key column.")

    result_df = df.copy()
    result_df = result_df[result_df[key_col].isin(scope.node_ids)]
    if key_col2 is not None:
        result_df = result_df[result_df[key_col2].isin(scope.node_ids)]

    return result_df


def _validate_result(scope: GeoScope, data: Series) -> None:
    """
    Ensures that the key column for an attribute contains at least one entry
    for every node in the scope.
    """
    if set(data) != set(scope.node_ids):
        msg = (
            "Key column missing keys for geographies in scope "
            "or contains unrecognized keys."
        )
        raise DataResourceError(msg)


class CSV(ADRIOLegacy[Any]):
    """Retrieves an N-shaped array of any type from a user-provided CSV file."""

    file_path: PathLike
    """The path to the CSV file containing data."""
    key_col: int
    """Numerical index of the column containing information to identify geographies."""
    data_col: int
    """Numerical index of the column containing the data of interest."""
    data_type: DTypeLike
    """The data type of values in the data column."""
    key_type: KeySpecifier
    """The type of geographic identifier in the key column."""
    skiprows: int | None
    """Number of header rows in the file to be skipped."""

    def __init__(
        self,
        file_path: PathLike,
        key_col: int,
        data_col: int,
        data_type: DTypeLike,
        key_type: KeySpecifier,
        skiprows: int | None,
    ):
        self.file_path = file_path
        self.key_col = key_col
        self.data_col = data_col
        self.data_type = data_type
        self.key_type = key_type
        self.skiprows = skiprows

        if self.key_col == self.data_col:
            msg = "Key column and data column must not be the same."
            raise ValueError(msg)

    @override
    def evaluate_adrio(self) -> NDArray[Any]:
        path = Path(self.file_path)
        # workaround for bad pandas type definitions
        skiprows: int = self.skiprows  # type: ignore
        if path.exists():
            csv_df = read_csv(
                path,
                skiprows=skiprows,
                header=None,
                dtype={self.key_col: str},
            )
            parsed_df = _parse_label(
                self.key_type,
                self.scope,
                csv_df,
                self.key_col,
            )

            if parsed_df[self.data_col].isna().any():
                msg = (
                    "Data for required geographies missing from CSV file "
                    "or could not be found."
                )
                raise DataResourceError(msg)

            sorted_df = parsed_df.rename(columns={self.key_col: "key"}).sort_values(
                by="key"
            )
            return sorted_df[self.data_col].to_numpy(dtype=self.data_type)

        else:
            msg = f"File {self.file_path} not found"
            raise DataResourceError(msg)


class CSVTimeSeries(ADRIOLegacy[Any]):
    """Retrieves a TxN-shaped array of any type from a user-provided CSV file."""

    file_path: PathLike
    """The path to the CSV file containing data."""
    key_col: int
    """Numerical index of the column containing information to identify geographies."""
    data_col: int
    """Numerical index of the column containing the data of interest."""
    data_type: DTypeLike
    """The data type of values in the data column."""
    key_type: KeySpecifier
    """The type of geographic identifier in the key column."""
    skiprows: int | None
    """Number of header rows in the file to be skipped."""
    file_time_frame: TimeFrame
    """The time period encompassed by data in the file."""
    time_col: int
    """The numerical index of the column containing time information."""

    def __init__(
        self,
        file_path: PathLike,
        key_col: int,
        data_col: int,
        data_type: DTypeLike,
        key_type: KeySpecifier,
        skiprows: int | None,
        time_frame: TimeFrame,
        time_col: int,
    ):
        self.file_path = file_path
        self.key_col = key_col
        self.data_col = data_col
        self.data_type = data_type
        self.key_type = key_type
        self.skiprows = skiprows
        self.file_time_frame = time_frame
        self.time_col = time_col

        if self.key_col == self.data_col:
            msg = "Key column and data column must not be the same."
            raise ValueError(msg)

    @override
    def evaluate_adrio(self) -> NDArray[Any]:
        path = Path(self.file_path)
        skiprows: int = self.skiprows  # type: ignore
        if path.exists():
            csv_df = read_csv(
                path,
                skiprows=skiprows,
                header=None,
                dtype={self.key_col: str},
            )
            parsed_df = _parse_label(
                self.key_type,
                self.scope,
                csv_df,
                self.key_col,
            )

            if parsed_df[self.data_col].isna().any():
                msg = (
                    "Data for required geographies missing from CSV file "
                    "or could not be found."
                )
                raise DataResourceError(msg)

            parsed_df[self.time_col] = parsed_df[self.time_col].apply(
                date.fromisoformat
            )

            is_before = parsed_df[self.time_col] < self.file_time_frame.start_date
            is_after = parsed_df[self.time_col] > self.file_time_frame.end_date
            if any(is_before | is_after):
                msg = "Found time column value(s) outside of provided date range."
                raise DataResourceError(msg)

            sorted_df = (
                parsed_df.rename(
                    columns={
                        self.key_col: "key",
                        self.data_col: "data",
                        self.time_col: "time",
                    },
                )
                .sort_values(by=["time", "key"])
                .pivot_table(index="time", columns="key", values="data")
            )
            return sorted_df.to_numpy(dtype=self.data_type)

        else:
            msg = f"File {self.file_path} not found"
            raise DataResourceError(msg)


class CSVMatrix(ADRIOLegacy[Any]):
    """Retrieves an NxN-shaped array of any type from a user-provided CSV file."""

    file_path: PathLike
    """The path to the CSV file containing data."""
    from_key_col: int
    """Index of the column identifying source geographies."""
    to_key_col: int
    """Index of the column identifying destination geographies."""
    data_col: int
    """Index of the column containing the data of interest."""
    data_type: DTypeLike
    """The data type of values in the data column."""
    key_type: KeySpecifier
    """The type of geographic identifier in the key columns."""
    skiprows: int | None
    """Number of header rows in the file to be skipped."""

    def __init__(
        self,
        file_path: PathLike,
        from_key_col: int,
        to_key_col: int,
        data_col: int,
        data_type: DTypeLike,
        key_type: KeySpecifier,
        skiprows: int | None,
    ):
        self.file_path = file_path
        self.from_key_col = from_key_col
        self.to_key_col = to_key_col
        self.data_col = data_col
        self.data_type = data_type
        self.key_type = key_type
        self.skiprows = skiprows

        if len({self.from_key_col, self.to_key_col, self.data_col}) != 3:
            msg = "From key column, to key column, and data column must all be unique."
            raise ValueError(msg)

    @override
    def evaluate_adrio(self) -> NDArray[Any]:
        path = Path(self.file_path)
        if not path.exists():
            msg = f"File {self.file_path} not found"
            raise DataResourceError(msg)

        skiprows: int = self.skiprows  # type: ignore
        csv_df = read_csv(
            path,
            skiprows=skiprows,
            header=None,
            dtype={self.from_key_col: str, self.to_key_col: str},
        )
        parsed_df = _parse_label(
            self.key_type,
            self.scope,
            csv_df,
            self.from_key_col,
            self.to_key_col,
        )
        return (
            parsed_df.pivot_table(
                index=parsed_df.columns[self.from_key_col],
                columns=parsed_df.columns[self.to_key_col],
                values=parsed_df.columns[self.data_col],
            )
            .sort_index(axis=0)
            .sort_index(axis=1)
            .fillna(0)
            .to_numpy(dtype=self.data_type)
        )
