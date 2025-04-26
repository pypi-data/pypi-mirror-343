# XNO API Library

**XNO API** is a Python package for retrieving financial data and performing quantitative analysis, specifically optimized for the **Vietnamese financial market**. It provides a clean, modular interface to access data on stocks, derivatives, and backtesting tools for PnL and performance metrics.

---

## 📌 Key Features

- 🔎 Simple interface to retrieve **real-time and historical data** for Vietnamese stocks and derivatives  
- 📈 Built-in support for **performance metrics**: Sharpe, Sortino, Max Drawdown, and more  
- 📊 Optimized **PnL backtesting tools** for derivatives with **Vietnam-specific fee structures**  
- 🧪 Compatible with pandas, NumPy for custom strategies and analysis  
- 🖼️ Easily extensible for **visual output of strategies and metrics**

---

## 📦 Installation

Install via pip:

```sh
pip install xnoapi
```

Or clone this repo:

```sh
git clone https://github.com/xnoproject/xnoapi.git
pip install ./xnoapi
```

After installation:

```python
from xnoapi import client
from xnoapi.vn.data import stocks, derivatives
from xnoapi.vn.metrics import Metrics, Backtest_Derivates

client(apikey="your_api_key")
```

---

## 📚 Documentation

- Online Docs: [https://xnoapi.readthedocs.io](https://xnoapi.readthedocs.io/en/latest/)
- ![Documentation Status](https://readthedocs.org/projects/xnoapi/badge/?version=latest)
- [📄 PDF version](https://buildmedia.readthedocs.org/media/pdf/xnoapi/latest/xnoapi.pdf)

---

## 🚀 Usage Example

Retrieve and analyze Vietnamese stock & derivative data:

```python
from xnoapi import client
from xnoapi.vn.data import stocks, derivatives

client(apikey="your_api_key")

# List of liquid stocks
stocks.list_liquid_asset()

# Historical data for VIC (Vingroup)
vic = stocks.get_hist("VIC", "1D")

# Historical data for VN30F1M derivative
vn30f1m = derivatives.get_hist("VN30F1M", "1m")
```

---

## 🧠 Available Modules

### 📊 Financial Data

- `xnoapi.vn.data.stocks`
  - `list_liquid_asset()`: List of high-liquidity Vietnamese stocks.
  - `get_hist(asset, frequency)`: Historical OHLCV data.

- `xnoapi.vn.data.derivatives`
  - `get_hist(asset, frequency)`: Derivative market data (e.g., VN30F1M).

### 📈 Metrics & Analytics

- `xnoapi.vn.metrics.Metrics`: 
  - Includes: Sharpe Ratio, Sortino Ratio, Max Drawdown, Avg Gain/Loss, Hit Ratio...
- `xnoapi.vn.metrics.Backtest_Derivates`: 
  - Backtesting logic for trading strategies with support for fee modeling.

---

## 🧪 Examples

### Strategy Evaluation with Metrics

```python
from xnoapi.vn.metrics import Metrics, Backtest_Derivates
from xnoapi.vn.data import derivatives
import numpy as np

def gen_position(df):
    # Volume-based signal generation
    return df.assign(
        position=np.sign(df["Close"] - df["Close"].rolling(20).median())
    )

# Get 1-minute historical data
df = derivatives.get_hist("VN30F1M", "1m")
df_pos = gen_position(df)

# Run backtest
backtest = Backtest_Derivates(df_pos, pnl_type="raw")
metrics = Metrics(backtest)

# Print Sharpe Ratio
print(metrics.sharpe())

# Plot PNL
backtest.daily_PNL().plot()
```

---

## 🤝 Credits

Maintained by the **XNO Team**.  
Special thanks to contributors and financial data providers supporting the Vietnamese retail quant community.

---

## 📄 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).  
See [LICENSE](https://github.com/xnoproject/xnoapi/blob/main/LICENSE) for full details.
