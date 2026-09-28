"""Bitcoin halving countdown."""
import argparse
import json
import urllib.request
from datetime import datetime, timedelta, timezone

INTERVAL = 210_000
COIN = 100_000_000


def get(api, path):
    req = urllib.request.Request(api + path, headers={"User-Agent": "halving-countdown"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def subsidy_sats(height: int) -> int:
    epoch = height // INTERVAL
    return (50 * COIN) >> epoch if epoch < 64 else 0


def fmt_btc(sats: int) -> str:
    return f"{sats / COIN:.8f}".rstrip("0").rstrip(".")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api", default="https://mempool.space/api")
    a = ap.parse_args()

    height = int(get(a.api, "/blocks/tip/height"))
    avg_ms = get(a.api, "/v1/difficulty-adjustment").get("timeAvg", 600_000)
    epoch = height // INTERVAL
    nxt = (epoch + 1) * INTERVAL
    left = nxt - height
    now = datetime.now(timezone.utc)
    eta = now + timedelta(milliseconds=avg_ms * left)
    eta10 = now + timedelta(minutes=10 * left)
    done = (height - epoch * INTERVAL) / INTERVAL
    bar = "#" * int(done * 30) + "-" * (30 - int(done * 30))

    print(f"current height      {height:,}  (epoch {epoch}, subsidy {fmt_btc(subsidy_sats(height))} BTC)")
    print(f"next halving        {nxt:,}  -> subsidy {fmt_btc(subsidy_sats(nxt))} BTC")
    print(f"blocks remaining    {left:,}")
    print(f"avg block time      {int(avg_ms // 60000)}m {int(avg_ms % 60000 // 1000)}s (difficulty-epoch average)")
    print(f"ETA                 {eta:%Y-%m-%d %H:%M} UTC  (~{(eta - now).days} days)")
    print(f"ETA @ exactly 10m   {eta10:%Y-%m-%d %H:%M} UTC")
    print(f"progress  [{bar}]  {done:.1%} of this epoch")


if __name__ == "__main__":
    main()
