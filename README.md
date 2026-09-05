# Institutional Order Flow First-Retest Study

## Overview

This project investigates whether the first retest of an objectively
defined Institutional Order Flow (IOF) supply or demand zone produces
a measurable directional price reaction.

The goal was to take a discretionary trading observation and convert it
into a falsifiable quantitative research problem.

*Note: I am not claiming this strategy actually tracks "institutional" order flow this is simply what the strategy is known as by the discretionary community.*

## Research Question

Does the first retest of an objectively defined IOF supply/demand zone
produce a statistically significant directional price reaction?

### Hypothesis

- Demand-zone retests should exhibit positive forward directional returns.
- Supply-zone retests should exhibit negative forward directional returns.

## Methodology

1. Formalize an objective definition of an IOF formation.
2. Detect qualifying formations programmatically.
3. Identify the first future retest of each zone.
4. Measure directional returns over 1, 3, 5, and 10-hour horizons.
5. Compare observed reactions against random and volatility/time-matched controls.
6. Run a Monte Carlo matched placebo test.

## Data

- Instrument: E-mini S&P 500 futures (ES)
- Timeframe: 1 hour
- Sample: approximately 60 days
- Detected IOF formations: 26
- First retests: 21
- Matched-control observations: 20

## Preliminary Results

IOF first retests exhibited positive average directional reactions across
the tested forward horizons.

Matched placebo tests also suggested that the observed reactions were
unusual relative to historically matched non-IOF observations.

These results are exploratory and should not be interpreted as evidence
of a production-ready trading strategy.

## Key Limitations

- Small sample
- Limited historical data
- Exploratory rather than preregistered analysis
- Multiple forward horizons tested
- Simplified control methodology
- No transaction costs, slippage, or execution modeling
- Results have not yet been validated out-of-sample

## Next Steps

The next stage would be to expand the historical dataset, freeze the
research methodology, and perform true out-of-sample validation.

## Repository Structure

`notebooks/iof_first_retest_study.ipynb`
contains the complete research workflow.

`iof.py`
contains the IOF detection logic.
