import warnings
warnings.filterwarnings("ignore")

import os
import time
import requests
import json
import pandas as pd
import streamlit as st

from multi_agent_trader.config import settings

tickers = settings.DEFAULT_TICKERS
RAW = settings.RAW_DATA_DIR

def fetch_eod(symbol, start=settings.START_DATE, end=settings.END_DATE):
    params = {"api_token": settings.EODHD_API_KEY, "from": start, "to": end, "period": "d", "fmt": "json"}
    r = requests.get(f"https://eodhd.com/api/eod/{symbol}.US", params=params, timeout=60)
    return r.json()

def to_frame(symbol):
    df = pd.DataFrame(json.loads((RAW / f"{symbol}.json").read_text()))
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date").sort_index()[["close","adjusted_close","volume"]].astype(float)

for s in tickers:
    f = RAW / f"{s}.json"
    if not f.exists():
        f.write_text(json.dumps(fetch_eod(s))); time.sleep(0.3)

df = pd.DataFrame([{"symbol": s, "rows": len(j := json.loads((RAW/f"{s}.json").read_text())),
               "first": j[0]["date"], "last": j[-1]["date"]} for s in tickers])


frames, report = {}, []
for s in settings.DEFAULT_TICKERS:
    d = to_frame(s)
    report.append({"symbol": s, "rows": len(d),
                   "duplicate_dates": int(d.index.duplicated().sum()),
                   "missing": int(d.isna().sum().sum()),
                   "nonpositive_price": int((d[["close","adjusted_close"]] <= 0).sum().sum()),
                   "zero_volume_days": int((d["volume"] <= 0).sum())})
    frames[s] = d[~d.index.duplicated(keep="last")]

report_df = pd.DataFrame(report)

if __name__ == "__main__":
    st.rerun(scope="fragment")