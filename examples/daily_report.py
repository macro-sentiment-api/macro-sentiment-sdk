#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日情绪报告：情绪温度变化 + 多空极值 + 成绩单快照"""
import os
from datetime import datetime
from macro_sentiment_sdk import Client

client = Client(api_key=os.environ.get("MACRO_SENTIMENT_API_KEY", "sk-demo-trial-0002"))


def build_report() -> str:
    idx = client.sentiment.index()
    hist = client.sentiment.history(days=7)
    lines = []
    lines.append(f"宏观舆情日报 · {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"数据截至最近收盘 · 全市场 {idx.get('total_symbols', '-')} 只标的舆情快照")
    lines.append("")
    gauge = idx.get("market_sentiment_gauge", "-")
    lines.append(f"【情绪温度】{gauge}（0-100，50 为多空分界）")
    lines.append(f"【情绪指数】{idx.get('market_sentiment_index', '-')}")
    b = idx.get("breadth", {})
    lines.append(f"【多空占比】看多 {b.get('bullish', 0):.1%} / 看空 {b.get('bearish', 0):.1%}")

    if len(hist) >= 2:
        g_prev = hist[-2].get("gauge")
        g_now = hist[-1].get("gauge")
        if g_prev is not None and g_now is not None:
            lines.append(f"【较前一日】{g_now - g_prev:+.1f}")

    lines.append("")
    lines.append("【情绪多头极值 Top5】（均值回归假设下警惕回落）")
    for t in (idx.get("top_bullish") or [])[:5]:
        lines.append(f"  {t['symbol']}  {t['sentiment_score']:+.2f}")
    lines.append("【情绪空头极值 Top5】（均值回归假设下关注修复）")
    for t in (idx.get("top_bearish") or [])[:5]:
        lines.append(f"  {t['symbol']}  {t['sentiment_score']:+.2f}")

    lines.append("")
    lines.append("数据来源：公开市场行情与官方宏观发布 · 仅供研究，不构成投资建议")
    return "\n".join(lines)


if __name__ == "__main__":
    report = build_report()
    print(report)
    # 如需落盘：
    # with open(f"daily_report_{datetime.now():%Y%m%d}.txt", "w", encoding="utf-8") as f:
    #     f.write(report)
