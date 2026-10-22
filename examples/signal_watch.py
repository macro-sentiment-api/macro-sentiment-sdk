#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""信号监控：情绪指数轮询 + 极值变化告警（可挂 cron / 计划任务）"""
import os
import time
from macro_sentiment_sdk import Client

client = Client(api_key=os.environ.get("MACRO_SENTIMENT_API_KEY", "sk-demo-trial-0002"))

# 告警阈值：温度进入极端区（>75 过热 / <25 过冷）时提示
OVERHEAT, OVERCOLD = 75, 25
# 轮询间隔（秒）：盘中建议 60-300，盘后 3600
POLL_INTERVAL = 300


def watch_once() -> None:
    idx = client.sentiment.index()
    gauge = idx.get("market_sentiment_gauge")
    if gauge is None:
        print("未获取到情绪温度，跳过")
        return
    tag = ""
    if gauge > OVERHEAT:
        tag = "⚠️ 过热区——情绪透支风险，警惕回调"
    elif gauge < OVERCOLD:
        tag = "💡 过冷区——情绪受压，关注修复"
    else:
        tag = "中性区"
    print(f"[{time.strftime('%H:%M:%S')}] 温度 {gauge:.1f} · {tag}")
    top_b = (idx.get("top_bullish") or [])[:3]
    top_s = (idx.get("top_bearish") or [])[:3]
    if top_b:
        print("  多头极值:", " ".join(f"{t['symbol']}({t['sentiment_score']:+.2f})" for t in top_b))
    if top_s:
        print("  空头极值:", " ".join(f"{t['symbol']}({t['sentiment_score']:+.2f})" for t in top_s))


if __name__ == "__main__":
    print(f"信号监控启动（间隔 {POLL_INTERVAL}s，Ctrl+C 退出）")
    try:
        while True:
            watch_once()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("监控已停止")
