### Sumary of changes

No breaking changes are introduced, and all existing APIs remain unchanged

#### In `record-data.py`

- The function `flushInput()` immediately preceding `readline()`, which could discard incoming serial frames and cause read timeouts

- Replaced bare `try/except` with exceptions (`ValueError`, `IndexError`)  and up to 10 retries for malformed or noisy serial frames, preventing unexpected script termination during calibration

- Entering an unrecognized key no longer aborts and saves prematurely

#### In `plot-calibration-data.py`

- Replaced the per-point `for` loop calling `ax.scatter` N times with single vectorized calls

- File resolution for the example dataset is now relative to the scripts directory

#### In `README.md`

Added missing `pyserial` to pip and conda installation instructions
