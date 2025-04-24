"""
Calculate max pain from open interest data.
"""

import pandas as pd
from pandas.api.types import CategoricalDtype


right = CategoricalDtype(categories=["put", "call"], ordered=False)

columns = {
    "contractID": str,
    "symbol": str,
    "expiration": str,
    "strike": float,
    "type": right,
    "open_interest": int,
}

na_values = ["", " ", "N/A", "NaN", "nan", "None", None, "null", "-"]


def calculate_loss(row, current_price):
    strike_price = row["strike"]
    call_oi = row["call_open_interest"]
    put_oi = row["put_open_interest"]

    # Call loss
    call_loss = max(0, current_price - strike_price) * call_oi

    # Put loss
    put_loss = max(0, strike_price - current_price) * put_oi

    # Add to total loss
    return call_loss + put_loss


def calculate_max_pain(records, expiration_date=None, min_records=10):
    """
    Calculate the max pain point for an options chain.

    Parameters:
    - option_data: DataFrame with columns ['strike', 'type', 'open_interest', 'expiration']

    Returns:
    - max_pain_strike: Strike price corresponding to max pain
    """
    if records is None or len(records) == 0:
        return None
    if not isinstance(records, pd.DataFrame):
        df = pd.DataFrame(records)
        # Define the columns and their data types
        columns = {
            "expiration": str,
            "strike": float,
            "type": str,
            "open_interest": int,
        }

        # Convert the DataFrame columns to the appropriate data types
        df.fillna(0, inplace=True)
        df = df.astype(columns)
    else:
        df = records
    if len(df) < min_records:
        raise ValueError(
            f"calculate_max_pain: Insufficient data to calculate max pain."
        )
    if expiration_date is not None:
        options = df[df["expiration"] == expiration_date]
        if options.empty:
            raise ValueError(
                "No records found for the specified options expiration date."
            )
    else:
        options = (
            df.groupby(["type", "strike"]).agg({"open_interest": "sum"}).reset_index()
        )

    option_data = options.pivot(
        index="strike", columns="type", values="open_interest"
    ).reset_index()
    # Fill missing put/call columns with 0
    if "put" not in option_data.columns:
        option_data["put"] = 0
    if "call" not in option_data.columns:
        option_data["call"] = 0

    option_data.rename(
        columns={"put": "put_open_interest", "call": "call_open_interest"}, inplace=True
    )

    def apply_price(row):
        current_price = row["strike"]
        calculated_loss = option_data.apply(
            lambda row: calculate_loss(row, current_price), axis=1
        ).sum()
        return pd.Series({"strike": current_price, "loss": calculated_loss})

    calculated_total_loss = option_data.apply(apply_price, axis=1)
    index = calculated_total_loss["loss"].idxmin()
    max_pain_strike = calculated_total_loss.loc[index]["strike"]

    return max_pain_strike
