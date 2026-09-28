# halving-countdown

Blocks left until the next Bitcoin halving, and when that is likely to happen.

```
$ python halving.py
current height      968,272  (epoch 4, subsidy 3.125 BTC)
next halving        1,050,000  -> subsidy 1.5625 BTC
blocks remaining    81,728
avg block time      10m 17s (difficulty-epoch average)
ETA                 2028-04-29 21:59 UTC  (~584 days)
ETA @ exactly 10m   2028-04-13 02:04 UTC
progress  [##################------------]  61.1% of this epoch
```

The height and the average block time come from mempool.space (`/blocks/tip/height` and
`/v1/difficulty-adjustment`). The subsidy is `50 BTC >> epoch` with `epoch = height // 210000`.

It prints two dates, one from the observed block time and one from the 10 minute target. The
actual halving usually lands between or near them.

`--api` points it at a self-hosted mempool instance.
