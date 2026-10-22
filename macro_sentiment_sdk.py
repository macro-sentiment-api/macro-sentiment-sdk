#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macro-sentiment-sdk —— 宏观高频 × 舆情情绪 数据 API 的 Python SDK

数据产品主页：https://macro-sentiment-api.app.workbuddy.host （7 天免费试用，申请即开通）

用法:
    from macro_sentiment_sdk import Client
    client = Client(api_key="sk-xxxx")  # 默认指向公网数据服务
    idx = client.sentiment.index()      # 市场情绪指数
    pmi = client.macro.value("PMI")     # 宏观高频指标
    hist = client.sentiment.history(days=30)  # 情绪历史
"""

import json
import urllib.request
import urllib.error
from urllib.parse import quote_plus
from typing import Dict, List, Optional


class APIError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"[{status}] {message}")


class _HTTPClient:
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{path}"
        if params:
            qs = "&".join(f"{quote_plus(str(k))}={quote_plus(str(v))}" for k, v in params.items())
            url = f"{url}?{qs}"
        req = urllib.request.Request(url, headers={
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        })
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            try:
                msg = json.loads(body).get("error", body)
            except Exception:
                msg = body
            raise APIError(e.code, msg)
        except urllib.error.URLError as e:
            raise APIError(0, f"连接失败: {e.reason}")

    def post(self, path: str, data: Dict) -> Dict:
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(data).encode("utf-8"),
            headers={"X-API-Key": self.api_key, "Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            raise APIError(e.code, body)


class MacroAPI:
    """宏观高频数据端点"""
    def __init__(self, http: _HTTPClient):
        self._http = http

    def latest(self) -> List[Dict]:
        """最新全量宏观指标"""
        return self._http.get("/v1/macro/latest")["data"]

    def indicator(self, name: str, days: int = 90) -> List[Dict]:
        """按指标名查询（如 PMI/CPI/M2/社融）"""
        return self._http.get("/v1/macro/indicator", {"name": name, "days": days})["data"]

    def value(self, name: str) -> Optional[float]:
        """取某指标最新值（便捷方法）"""
        rows = self.indicator(name)
        if not rows:
            return None
        return rows[0].get("value")


class SentimentAPI:
    """舆情情绪端点"""
    def __init__(self, http: _HTTPClient):
        self._http = http

    def realtime(self) -> List[Dict]:
        """实时情绪全量数据"""
        return self._http.get("/v1/sentiment/realtime")["data"]

    def symbol(self, symbol: str) -> List[Dict]:
        """指定标的情绪数据"""
        return self._http.get("/v1/sentiment/symbol", {"symbol": symbol})["data"]

    def alerts(self, level: str = "spike") -> List[Dict]:
        """预警（spike=热度异动, breaking=突发事件）"""
        return self._http.get("/v1/sentiment/alerts", {"level": level})["data"]

    def index(self) -> Dict:
        """市场情绪指数（全市场聚合：指数值/多空占比/Top 看多看空标的）"""
        return self._http.get("/v1/sentiment/index")

    def history(self, symbol: str = "", days: int = 30) -> List[Dict]:
        """情绪历史（每日聚合；symbol 可省略=全市场；days 默认 30，最大 365）"""
        params = {"days": days}
        if symbol:
            params["symbol"] = symbol
        return self._http.get("/v1/sentiment/history", params)["data"]

    def history_dates(self) -> List[Dict]:
        """历史归档日期清单（数据深度证明）"""
        return self._http.get("/v1/sentiment/history/dates")["dates"]


class Client:
    """统一客户端"""
    def __init__(self, api_key: str, base_url: str = "https://macro-sentiment-api.app.workbuddy.host", timeout: int = 30):
        self._http = _HTTPClient(api_key, base_url, timeout)
        self.macro = MacroAPI(self._http)
        self.sentiment = SentimentAPI(self._http)

    def health(self) -> Dict:
        """服务健康检查"""
        return self._http.get("/health")


# ============== 快速自测（需要有效 api_key） ==============
if __name__ == "__main__":
    import os
    client = Client(api_key=os.environ.get("MACRO_SENTIMENT_API_KEY", "sk-demo-trial-0002"))
    print("健康检查:", client.health())
    idx = client.sentiment.index()
    print(f"市场情绪指数: {idx.get('market_sentiment_index')} · 温度: {idx.get('market_sentiment_gauge')}")
    pmi = client.macro.value("PMI")
    print(f"PMI 最新值: {pmi}")
    m2 = client.macro.value("M2_同比增长")
    print(f"M2 同比: {m2}%")
    alerts = client.sentiment.alerts("breaking")
    print(f"突发事件预警: {len(alerts)} 条")
