# PlayerStats45M

Python utility that polls FiveM server player lists and logs player joins, leaves, and session durations.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python runner.py
```

Configure monitored servers in `runner.py`. Logs are written under `logs/YYYYMM/`.
