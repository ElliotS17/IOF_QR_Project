import numpy as np
import pandas as pd


def body_size(row: pd.Series) -> float:
    return abs(float(row["Close"]) - float(row["Open"]))


def candle_range(row: pd.Series) -> float:
    return float(row["High"]) - float(row["Low"])


def body_ratio(row: pd.Series) -> float:
    r = candle_range(row)
    if r <= 0:
        return np.nan
    return body_size(row) / r


def direction(row: pd.Series) -> int:
    """+1 bullish, -1 bearish, 0 doji."""
    c = float(row["Close"])
    o = float(row["Open"])
    return int(c > o) - int(c < o)


def _body_low(frame: pd.DataFrame) -> float:
    return float(np.minimum(frame["Open"], frame["Close"]).min())


def _body_high(frame: pd.DataFrame) -> float:
    return float(np.maximum(frame["Open"], frame["Close"]).max())


def detect_iof(
    df: pd.DataFrame,
    impulse_body_ratio: float = 0.50,
    consolidation_body_ratio: float = 0.50,
    max_consolidation_bars: int = 3,
    second_impulse_zone_multiple: float = 2.0,
) -> pd.DataFrame:
    """
    Detect candidate IOF formations using the current research definition.

    Rules:
    1. Initial impulse body/range >= 50%.
    2. Consolidation contains 1-3 consecutive candles.
       Each consolidation candle has body/range <= 50%.
    3. Combined consolidation range <= initial impulse range.
    4. Second impulse body/range >= 50%.
    5. Second impulse body >= 2x the resulting zone width.
    6. The second impulse may not be gap-displaced outside the consolidation
       range in this MVP. Gap-displaced candidates are excluded.
    7. Continuation:
         second impulse has the same direction as the initial impulse.
    8. Reversal:
         second impulse has the opposite direction AND closes beyond the
         initial impulse close in the direction of the reversal.
         Bullish reversal: second close > initial close.
         Bearish reversal: second close < initial close.
    9. Zone definition for multiple consolidation candles:
         Demand = lowest consolidation low -> highest consolidation body.
         Supply = lowest consolidation body -> highest consolidation high.

    Important:
    This function deliberately freezes the current hypothesis. Do not tune
    these parameters after looking at outcome data and then report the tuned
    result as the original test.
    """
    required = {"Open", "High", "Low", "Close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    data = df.copy()
    data["Body"] = (data["Close"] - data["Open"]).abs()
    data["Range"] = data["High"] - data["Low"]
    data["BodyRatio"] = data["Body"] / data["Range"].replace(0, np.nan)

    events = []
    n_rows = len(data)

    for i in range(n_rows):
        initial = data.iloc[i]

        if not (initial["BodyRatio"] >= impulse_body_ratio):
            continue

        initial_dir = direction(initial)
        if initial_dir == 0:
            continue

        init_range = float(initial["Range"])

        for n_cons in range(1, max_consolidation_bars + 1):
            second_pos = i + n_cons + 1
            if second_pos >= n_rows:
                break

            cons = data.iloc[i + 1 : second_pos]

            if not (cons["BodyRatio"] <= consolidation_body_ratio).all():
                break

            cons_range = float(cons["High"].max() - cons["Low"].min())
            if cons_range > init_range:
                continue

            second = data.iloc[second_pos]
            if not (second["BodyRatio"] >= impulse_body_ratio):
                continue

            second_dir = direction(second)
            if second_dir == 0:
                continue

            # Exclude gap-displaced second impulses in the MVP.
            cons_high = float(cons["High"].max())
            cons_low = float(cons["Low"].min())
            gap_up = float(second["Open"]) > cons_high
            gap_down = float(second["Open"]) < cons_low

            if gap_up or gap_down:
                continue

            if second_dir > 0:
                zone_type = "demand"
                zone_low = cons_low
                zone_high = _body_high(cons)
            else:
                zone_type = "supply"
                zone_low = _body_low(cons)
                zone_high = cons_high

            zone_width = zone_high - zone_low
            if zone_width <= 0:
                continue

            if float(second["Body"]) < second_impulse_zone_multiple * zone_width:
                continue

            # Classify the relationship using the actual reversal rule.
            if initial_dir == second_dir:
                relationship = "continuation"
            elif initial_dir == -second_dir:
                valid_reversal = (
                    # Bullish reversal
                    (second_dir > 0 and float(second["Close"]) > float(initial["Open"]))
                    or
                    # Bearish reversal
                    (second_dir < 0 and float(second["Close"]) < float(initial["Open"]))
                )
                if not valid_reversal:
                    # Opposite-direction impulse, but it did not close beyond
                    # the initial impulse close. Not an IOF reversal.
                    continue
                relationship = "reversal"
            else:
                continue

            events.append(
                {
                    "initial_time": data.index[i],
                    "consolidation_start": cons.index[0],
                    "consolidation_end": cons.index[-1],
                    "second_impulse_time": data.index[second_pos],
                    "consolidation_bars": n_cons,
                    "zone_type": zone_type,
                    "zone_low": zone_low,
                    "zone_high": zone_high,
                    "zone_width": zone_width,
                    "initial_direction": initial_dir,
                    "second_direction": second_dir,
                    "relationship": relationship,
                    "initial_body_ratio": float(initial["BodyRatio"]),
                    "second_body_ratio": float(second["BodyRatio"]),
                    "initial_range": init_range,
                    "consolidation_range": cons_range,
                    "second_body": float(second["Body"]),
                    "second_body_zone_multiple": float(second["Body"]) / zone_width,
                    "second_pos": second_pos,
                }
            )

    return pd.DataFrame(events)
