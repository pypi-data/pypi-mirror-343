import numpy as np
import pandas as pd


class TradingBacktest:
    """
    A class for backtesting derivatives trading strategies.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing historical data with columns ['date', 'time', 'close', 'position'].
    pnl_type : str, optional
        Type of PNL calculation ('raw' or 'after_fees'), by default 'after_fees'.

    Raises
    ------
    ValueError
        If pnl_type is not 'raw' or 'after_fees'.
    """

    def __init__(self, df, pnl_type="raw"):
        """
        Initializes the BacktestDerivates class.

        Parameters
        ----------
        df : pd.DataFrame
            Data containing trade details.
        pnl_type : str, optional
            Type of PNL calculation ('raw' or 'after_fees'), by default 'after_fees'.
        """
        if pnl_type not in ["raw", "after_fees"]:
            raise ValueError("Invalid pnl_type. Choose 'raw' or 'after_fees'.")

        self.df = df.copy()
        self.pnl_type = pnl_type
        self.df["datetime"] = pd.to_datetime(self.df["date"] + " " + self.df["time"])
        self.df = self.df.set_index("datetime")
        self.df = self.df.sort_index()

        # Calculate raw PNL
        self.df["pnl_raw"] = self.df["close"].diff().shift(-1) * self.df["position"]
        self.df["pnl_raw"] = self.df["pnl_raw"].fillna(0)

        # Calculate daily PNL
        self.daily_pnl = self.daily_PNL()

    def cumulative_PNL(self):
        """
        Calculate cumulative PNL based on selected pnl_type.

        Returns
        -------
        pandas.Series
            Cumulative PNL.
        """
        return self.df[f"pnl_{self.pnl_type}"].cumsum()

    def daily_PNL(self):
        """
        Calculate daily PNL based on selected pnl_type.

        Returns
        -------
        pandas.Series
            Daily PNL.
        """
        return self.df.groupby(self.df["date"])[f"pnl_{self.pnl_type}"].sum()

    def estimate_minimum_capital(self):
        """
        Estimate the minimum capital required to run the strategy.

        Returns
        -------
        float
            Minimum capital required.
        """
        self.df["cumulative_pnl"] = self.cumulative_PNL()
        self.df["capital_required"] = (
            self.df["position"].abs() * self.df["close"]
        ) - self.df["cumulative_pnl"]

        return max(self.df["capital_required"].max(), 0)

    def PNL_percentage(self):
        """
        Calculate PNL percentage relative to minimum required capital.

        Returns
        -------
        float
            PNL percentage.
        """
        min_capital = self.estimate_minimum_capital()
        if min_capital == 0:
            return np.nan  # Avoid division by zero
        return self.daily_pnl / min_capital

    def avg_loss(self, initial_capital=1):
        """
        Compute the average loss (percentage) from daily PNL.

        Returns
        -------
        float
            Average loss.
        """
        losses = self.daily_pnl[self.daily_pnl < 0]
        return losses.mean() / initial_capital

    def avg_return(self, initial_capital=1):
        """
        Compute the average return (percentage) from daily PNL.

        Returns
        -------
        float
            Average return.
        """
        return self.daily_pnl.mean() / initial_capital

    def avg_win(self, initial_capital=1):
        """
        Compute the average win (percentage) from daily PNL.

        Returns
        -------
        float
            Average win.
        """
        wins = self.daily_pnl[self.daily_pnl > 0]
        return wins.mean() / initial_capital

    def max_drawdown(self):
        """
        Compute the maximum drawdown.

        Returns
        -------
        float
            Maximum drawdown as a percentage of minimum capital.
        """
        cumulative_daily_pnl = self.daily_pnl.cumsum()
        peak = cumulative_daily_pnl.cummax()
        drawdown = cumulative_daily_pnl - peak
        return drawdown.min() / self.estimate_minimum_capital()

    def win_rate(self):
        """
        Compute the win rate.

        Returns
        -------
        float
            Win rate.
        """
        wins = (self.daily_pnl > 0).sum()
        total = len(self.daily_pnl)
        return wins / total if total > 0 else 0

    def volatility(self):
        """
        Compute the standard deviation of daily PNL.

        Returns
        -------
        float
            Volatility.
        """
        return self.daily_pnl.std()

    def sharpe(self, risk_free_rate=0.0):
        """
        Compute the Sharpe ratio. Assume risk free rate is daily

        Returns
        -------
        float
            Sharpe ratio.
        """
        return (self.avg_return() - risk_free_rate) / self.volatility() * np.sqrt(252)

    def sortino(self, risk_free_rate=0.0):
        """
        Compute the Sortino ratio. Assume risk free rate is daily

        Returns
        -------
        float
            Sortino ratio.
        """
        downside_std = self.daily_pnl[self.daily_pnl < 0].std()
        return (
            (self.avg_return() - risk_free_rate) / downside_std * np.sqrt(252)
            if downside_std > 0
            else np.nan
        )

    def calmar(self, risk_free_rate=0.0):
        """
        Compute the Calmar ratio. Assume risk free rate is daily

        Returns
        -------
        float
            Calmar ratio.
        """
        return (
            (self.avg_return() - risk_free_rate)
            / abs(self.max_drawdown())
            * np.sqrt(252)
            if self.max_drawdown() != 0
            else np.nan
        )

    def profit_factor(self):
        """
        Compute the profit factor.

        Returns
        -------
        float
            Profit factor.
        """
        total_gain = self.daily_pnl[self.daily_pnl > 0].sum()
        total_loss = abs(self.daily_pnl[self.daily_pnl < 0].sum())
        return total_gain / total_loss if total_loss != 0 else np.nan

    def risk_of_ruin(self):
        """
        Compute risk of ruin.

        Returns
        -------
        float
            Risk of ruin.
        """
        win_rate = self.win_rate()
        loss_rate = 1 - win_rate
        return (
            (loss_rate / win_rate) ** (1 / self.avg_loss())
            if self.avg_loss() != 0
            else np.nan
        )

    def value_at_risk(self, confidence_level=0.05):
        """
        Compute Value at Risk (VaR).

        Parameters
        ----------
        confidence_level : float, optional
            Confidence level for VaR, by default 0.05.

        Returns
        -------
        float
            Value at Risk (VaR).
        """
        return self.daily_pnl.quantile(confidence_level)
