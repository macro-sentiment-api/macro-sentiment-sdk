# macro-sentiment-sdk

**宏观高频 × 舆情情绪 数据 API · Python SDK**

用一行代码获取：全市场 A股情绪指数、个股情绪历史、宏观高频指标（PMI/CPI/M2/BDI…）、复合信号与多空极值。

- 数据产品主页：[https://macro-sentiment-api.app.workbuddy.host](https://macro-sentiment-api.app.workbuddy.host)（7 天免费试用，申请即开通）
- 公开信号成绩单：[先登记后验证，样本不足不给胜率](https://macro-sentiment-api.app.workbuddy.host/track-record)
- 每日情报专栏：[每个交易日收盘后自动发布](https://macro-sentiment-api.app.workbuddy.host/insights)

---

## 这个 SDK 给你什么

| 能力 | 说明 |
|---|---|
| 市场情绪指数 | 全市场 5000+ 标的聚合：指数值、情绪温度（0-100）、多空占比、Top 看多/看空名单 |
| 情绪历史 | 每日聚合归档，支持全市场或指定个股，最长 365 天 |
| 宏观高频 | PMI、CPI、M2、BDI 等官方发布指标，多源交叉验证 |
| 复合信号 | 宏观-情绪背离、情绪极值等多空信号（附公开可验证的成绩单） |
| 实时预警 | 热度异动（spike）与突发事件（breaking） |

数据全部来自公开渠道采集加工，**所有信号预测先登记后验证**——成绩单公开可查，样本不足时明说"样本不足"，不给自欺数字。

## 安装

无需安装依赖，单文件、零第三方库（仅用 Python 标准库）：

```bash
git clone https://github.com/macro-sentiment-api/macro-sentiment-sdk.git
cd macro-sentiment-sdk
```

或直接下载 `macro_sentiment_sdk.py` 放进你的项目。

要求：Python 3.8+。

## 快速开始

```python
from macro_sentiment_sdk import Client

# 到产品主页申请试用 Key（7 天免费）；也可以先用内置演示 Key 体验
client = Client(api_key="sk-你的Key")

# 1. 市场情绪指数（全市场聚合）
idx = client.sentiment.index()
print(idx["market_sentiment_index"])   # 情绪指数
print(idx["market_sentiment_gauge"])   # 情绪温度 0-100
print(idx["breadth"])                  # 多空占比

# 2. 宏观高频指标
pmi = client.macro.value("PMI")
m2 = client.macro.value("M2_同比增长")

# 3. 情绪历史（最近 30 天，全市场）
hist = client.sentiment.history(days=30)

# 4. 个股情绪
sz = client.sentiment.symbol("000423")

# 5. 实时预警
alerts = client.sentiment.alerts(level="breaking")
```

也可以用环境变量传 Key，避免写死在代码里：

```bash
export MACRO_SENTIMENT_API_KEY="sk-你的Key"
python macro_sentiment_sdk.py   # 直接运行即自测
```

## API 端点一览

| 方法 | 端点 | 说明 |
|---|---|---|
| `client.sentiment.index()` | `GET /v1/sentiment/index` | 市场情绪指数（聚合） |
| `client.sentiment.realtime()` | `GET /v1/sentiment/realtime` | 实时情绪全量数据 |
| `client.sentiment.symbol(sym)` | `GET /v1/sentiment/symbol` | 指定标的情绪 |
| `client.sentiment.alerts(level)` | `GET /v1/sentiment/alerts` | 预警（spike / breaking） |
| `client.sentiment.history(sym, days)` | `GET /v1/sentiment/history` | 情绪历史（日聚合） |
| `client.sentiment.history_dates()` | `GET /v1/sentiment/history/dates` | 归档日期清单 |
| `client.macro.latest()` | `GET /v1/macro/latest` | 最新全量宏观指标 |
| `client.macro.indicator(name)` | `GET /v1/macro/indicator` | 按指标名查询 |
| `client.macro.value(name)` | 同上 | 取最新值（便捷方法） |
| `client.health()` | `GET /health` | 健康检查 |

鉴权方式：请求头 `X-API-Key: <你的Key>` 或 URL 参数 `?api_key=<你的Key>`（SDK 已自动处理）。

完整文档：[产品主页 /docs](https://macro-sentiment-api.app.workbuddy.host/docs)

## 示例

`examples/` 目录下有三个开箱即用的例子：

```bash
python examples/quickstart.py      # 快速开始：指数+宏观+预警
python examples/daily_report.py    # 每日情绪报告：温度变化+多空极值
python examples/signal_watch.py    # 信号监控：背离信号+极值轮询
```

## 典型用途

- **量化研究**：把市场情绪作为因子输入策略回测（历史数据最长 365 天）
- **盘前盘后复盘**：每日情绪温度变化、多空极值名单，邮件/看板自动推送
- **风控监测**：情绪极值 + 宏观-情绪背离，作为仓位管理的参考信号
- **内容创作**：每日情报的自动化数据底座

## 定价

| 档位 | 价格 | 额度 |
|---|---|---|
| 免费试用 | ¥0（7 天） | 全端点体验 |
| SENT-Lite | ¥99/月 | 500 次/日，舆情全端点+复合信号 |
| 标准版 | 见[产品主页](https://macro-sentiment-api.app.workbuddy.host) | 更高额度 |

试用申请：[产品主页](https://macro-sentiment-api.app.workbuddy.host) 填写邮箱即秒发 Key。

## 数据纪律（为什么可信）

1. **先登记后验证**：每条方向预测带标的、方向、5 交易日持有期，登记时间早于验证时间
2. **可证伪**：到期用真实行情裁定 hit/miss/flat，噪声带（指数 ±0.5%/个股 ±1.5%）以下记平局
3. **样本不足不给胜率**：方向样本 <10 时明示"样本不足"，不出自欺数字
4. **回填与实时分列**：历史快照重建的样本与实时登记分开统计，禁止混算

公开台账：[macro-sentiment-api.app.workbuddy.host/track-record](https://macro-sentiment-api.app.workbuddy.host/track-record)

## 免责声明

本项目提供的数据与信号均为公开信息的数据加工结果，仅供研究参考，**不构成任何投资建议**。市场有风险，决策需独立。

## License

MIT（见 [LICENSE](LICENSE)）
