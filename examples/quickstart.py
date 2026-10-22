#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速开始：情绪指数 + 宏观指标 + 实时预警"""
import os
from macro_sentiment_sdk import Client

client = Client(api_key=os.environ.get("MACRO_SENTIMENT_API_KEY", "sk-demo-trial-0002"))

print("=== 健康检查 ===")
print(client.health())

print("\n=== 市场情绪指数 ===")
idx = client.sentiment.index()
print(f"情绪指数: {idx.get('market_sentiment_index')}")
print(f"情绪温度: {idx.get('market_sentiment_gauge')}（0-100，50 为多空分界）")
b = idx.get("breadth", {})
print(f"看多占比: {b.get('bullish', 0):.1%} · 看空占比: {b.get('bearish', 0):.1%}")
print("Top 看多:", [(t["symbol"], f"{t['sentiment_score']:+.2f}") for t in (idx.get("top_bullish") or [])[:5]])
print("Top 看空:", [(t["symbol"], f"{t['sentiment_score']:+.2f}") for t in (idx.get("top_bearish") or [])[:5]])

print("\n=== 宏观高频 ===")
for name in ["PMI_制造业", "CPI_当月同比", "M2_同比增长", "BDI_综合运价"]:
    print(f"{name}: {client.macro.value(name)}")

print("\n=== 实时预警 ===")
for a in client.sentiment.alerts(level="breaking")[:5]:
    print(f"  {a.get('symbol', '-')}: {a.get('message', a)}")
