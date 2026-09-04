# IOF Zone Research

## Research question

Does the first retest of an objectively defined Institutional Order Flow (IOF)
supply/demand zone produce a directional price reaction?

This repository is intentionally a **research prototype**, not a production
trading system.

## MVP scope

- Instrument: SPY
- Timeframe: 1 hour
- Consolidation length: 1–3 candles
- Initial impulse body/range >= 0.50
- Every consolidation candle body/range <= 0.50
- Combined consolidation range <= initial impulse range
- Second impulse body/range >= 0.50
- Second impulse body >= 2x zone width
- Bullish second impulse => demand zone
- Bearish second impulse => supply zone
- Only the first retest is considered in the initial experiment

## Zone definition

For 1–3 consolidation candles:

- Demand zone:
  - lower boundary = lowest consolidation low
  - upper boundary = highest open/close value among consolidation candles

- Supply zone:
  - lower boundary = lowest open/close value among consolidation candles
  - upper boundary = highest consolidation high

This encodes the discretionary definition supplied before looking at results.
It can later be compared against a "last consolidation candle only" definition
as a separate robustness test.

## Important methodological rule

Do **not** tune the 50%, 2x, or 1–3 candle thresholds after seeing the first
results and then report the tuned result as if it were the original hypothesis.
Any parameter changes should be labeled exploratory and later validated
out-of-sample.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/01_iof_detection.ipynb`.

## Next milestone

After validating that the detector correctly identifies visual examples:

1. Find the first retest of each zone.
2. Measure 1-, 3-, 5-, and 10-bar forward directional returns.
3. Measure maximum favorable/adverse excursion.
4. Construct a baseline/control.
5. Compare continuation vs reversal IOF formations.
