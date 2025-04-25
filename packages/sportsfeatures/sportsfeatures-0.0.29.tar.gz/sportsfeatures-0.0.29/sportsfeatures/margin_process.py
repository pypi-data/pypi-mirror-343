"""Calculate margin features."""

# pylint: disable=too-many-branches,too-many-locals

import pandas as pd
from tqdm import tqdm

from .columns import DELIMITER
from .entity_type import EntityType
from .identifier import Identifier


def margin_process(
    df: pd.DataFrame, identifiers: list[Identifier], dt_column: str
) -> pd.DataFrame:
    """Process margins between teams."""
    tqdm.pandas(desc="Margins Features")

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
        # Process the margins for each column
        drop_columns = set()
        for column in columns:
            column_df = df[[x.column_prefix + column for x in entity_type_identifiers]]
            max_val = column_df.max(axis="columns")
            for identifier in entity_type_identifiers:
                margin_absolute_column = DELIMITER.join(
                    [identifier.column_prefix + column, "margin", "absolute"]
                )
                margin_relative_column = DELIMITER.join(
                    [identifier.column_prefix + column, "margin", "relative"]
                )
                current_val = column_df[identifier.column_prefix + column]
                df[margin_absolute_column] = max_val - current_val
                df[margin_relative_column] = current_val / max_val
                drop_columns.add(margin_absolute_column)
                drop_columns.add(margin_relative_column)
        # Find the unique IDs
        dfs = [df[x.column] for x in entity_type_identifiers]
        if dfs:
            unique_ids = pd.unique(pd.concat(dfs))
            # Process each ID
            for unique_id in tqdm(unique_ids, desc=f"Margin {entity_type} IDs"):
                # Find all column values
                for column in columns:
                    # Calculate metric list
                    margin_absolute_column = DELIMITER.join(
                        [column, "margin", "absolute"]
                    )
                    margin_relative_column = DELIMITER.join(
                        [column, "margin", "relative"]
                    )
                    id_df = pd.concat(
                        [
                            df.loc[
                                df[x.column] == unique_id,
                                [
                                    dt_column,
                                    x.column_prefix
                                    + DELIMITER.join([column, "margin", "absolute"]),
                                    x.column_prefix
                                    + DELIMITER.join([column, "margin", "relative"]),
                                ],
                            ].rename(
                                columns={
                                    x.column_prefix
                                    + DELIMITER.join(
                                        [column, "margin", "absolute"]
                                    ): margin_absolute_column,
                                    x.column_prefix
                                    + DELIMITER.join(
                                        [column, "margin", "relative"]
                                    ): margin_relative_column,
                                }
                            )
                            for x in entity_type_identifiers
                        ]
                    ).sort_values(dt_column)
                    id_df[[margin_absolute_column, margin_relative_column]] = id_df[
                        [margin_absolute_column, margin_relative_column]
                    ].shift(periods=1)
                    for identifier in entity_type_identifiers:
                        margin_cols = [
                            identifier.column_prefix + margin_absolute_column,
                            identifier.column_prefix + margin_relative_column,
                        ]
                        entity_id_df = df.loc[
                            (df[identifier.column] == unique_id)
                            & (df[dt_column].isin(id_df[dt_column]))
                        ]
                        df.loc[
                            (df[identifier.column] == unique_id)
                            & (df[dt_column].isin(id_df[dt_column])),
                            margin_cols,
                        ] = id_df.loc[
                            id_df[dt_column].isin(entity_id_df[dt_column]),
                            [margin_absolute_column, margin_relative_column],
                        ].to_numpy()

    return df
