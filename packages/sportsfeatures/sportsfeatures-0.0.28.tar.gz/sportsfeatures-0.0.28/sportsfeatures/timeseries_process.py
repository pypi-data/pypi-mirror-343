"""Processing for time series features."""

# pylint: disable=duplicate-code,too-many-branches,too-many-nested-blocks

import datetime

import pandas as pd
from pandarallel import pandarallel  # type: ignore
from tqdm import tqdm

from .columns import DELIMITER
from .entity_type import EntityType
from .identifier import Identifier

_LAGS = [1, 2, 4, 8]
_COUNT_FUNC = "count"
_SUM_FUNC = "sum"
_MEAN_FUNC = "mean"
_MEDIAN_FUNC = "median"
_VAR_FUNC = "var"
_STD_FUNC = "std"
_MIN_FUNC = "min"
_MAX_FUNC = "max"
_SKEW_FUNC = "skew"
_KURT_FUNC = "kurt"
_SEM_FUNC = "sem"
_RANK_FUNC = "rank"
_WINDOW_FUNCS = [
    _COUNT_FUNC,
    _SUM_FUNC,
    _MEAN_FUNC,
    _MEDIAN_FUNC,
    _VAR_FUNC,
    _STD_FUNC,
    _MIN_FUNC,
    _MAX_FUNC,
    _SKEW_FUNC,
    _KURT_FUNC,
    _SEM_FUNC,
    _RANK_FUNC,
]


def timeseries_process(
    df: pd.DataFrame,
    identifiers: list[Identifier],
    windows: list[datetime.timedelta | None],
    dt_column: str,
) -> pd.DataFrame:
    """Process a dataframe for its timeseries features."""
    # pylint: disable=too-many-locals,consider-using-dict-items,too-many-statements,duplicate-code
    pandarallel.initialize(progress_bar=True)
    tqdm.pandas(desc="Timeseries Progress")

    # For each entity type
    for entity_type in EntityType:
        # Isolate the identifiers
        entity_type_identifiers = [
            x for x in identifiers if x.entity_type == entity_type
        ]
        # Find the columns
        columns = set()
        for identifier in entity_type_identifiers:
            for feature_column in identifier.feature_columns + (
                [identifier.points_column]
                if identifier.points_column is not None
                else []
            ):
                columns.add(feature_column[len(identifier.column_prefix) :])
                # Add the new columns to the dataframe
                for lag in _LAGS:
                    df[DELIMITER.join([feature_column, "lag", str(lag)])] = None
                for window in windows:
                    window_col = (
                        str(window.days) + "days" if window is not None else "all"
                    )
                    for window_func in _WINDOW_FUNCS:
                        df[
                            DELIMITER.join([feature_column, window_func, window_col])
                        ] = None

        # Find the unique IDs
        dfs = [df[x.column] for x in entity_type_identifiers]
        if dfs:
            unique_ids = pd.unique(pd.concat(dfs))
            for unique_id in unique_ids:
                # Find all column values
                for column in columns:
                    id_df = pd.concat(
                        [
                            df.loc[
                                df[x.column] == unique_id,
                                [
                                    dt_column,
                                    x.column_prefix + column,
                                ],
                            ].rename(
                                columns={
                                    x.column_prefix + column: column,
                                }
                            )
                            for x in entity_type_identifiers
                        ]
                    ).sort_values(dt_column)
                    for identifier in entity_type_identifiers:
                        entity_dt_df = df.loc[
                            (df[identifier.column] == unique_id)
                            & (df[dt_column].isin(id_df[dt_column]))
                        ]
                        # Process the lags
                        for lag in _LAGS:
                            lag_df = id_df.copy()
                            lag_df[column] = lag_df[column].shift(lag)
                            df.loc[
                                (df[identifier.column] == unique_id)
                                & (df[dt_column].isin(id_df[dt_column])),
                                [
                                    DELIMITER.join(
                                        [
                                            identifier.column_prefix + column,
                                            "lag",
                                            str(lag),
                                        ]
                                    )
                                ],
                            ] = id_df.loc[
                                id_df[dt_column].isin(entity_dt_df[dt_column]),
                                [column],
                            ].to_numpy()
                        # Process the window functions
                        for window in windows:
                            window_df = (
                                id_df.rolling(window, on=dt_column)
                                if window is not None
                                else id_df.expanding()
                            )
                            window_col = (
                                str(window.days) + "days"
                                if window is not None
                                else "all"
                            )
                            for window_func in _WINDOW_FUNCS:
                                window_func_df = id_df.copy()
                                if window_func == _COUNT_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].count().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _SUM_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].sum().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _MEAN_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].mean().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _MEDIAN_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].median().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _VAR_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].var().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _STD_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].std().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _MIN_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].min().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _MAX_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].max().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _SKEW_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].skew().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _KURT_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].kurt().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _SEM_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].sem().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
                                elif window_func == _RANK_FUNC:
                                    window_func_df[column] = (
                                        window_df[column].rank().shift(1)
                                    )
                                    df.loc[
                                        (df[identifier.column] == unique_id)
                                        & (df[dt_column].isin(id_df[dt_column])),
                                        [
                                            DELIMITER.join(
                                                [
                                                    identifier.column_prefix + column,
                                                    window_func,
                                                    window_col,
                                                ]
                                            )
                                        ],
                                    ] = window_func_df.loc[
                                        window_func_df[dt_column].isin(
                                            entity_dt_df[dt_column]
                                        ),
                                        [column],
                                    ].to_numpy()
    return df
