from shining_pebbles import get_yesterday
import pandas as pd
from .portfolio_fetcher import fetch_df_menu2205


class Portfolio:
    def __init__(self, fund_code, date_ref=None):
        self.fund_code = fund_code
        self.date_ref = date_ref
        self.raw_portfolio = None
        self.df = None
        self._load_pipeline()
    
    def get_raw_portfolio(self):
        if self.raw_portfolio is None:
            df = fetch_df_menu2205(fund_code=self.fund_code, date_ref=self.date_ref).set_index('일자')
            dfs = dict(tuple(df.groupby('자산')))
            valid_assets = ['국내주식', '국내채권', '국내선물', '국내수익증권', '국내수익증권(ETF)', '외화주식', '외화스왑']
            dfs_portfolio = []
            for asset in valid_assets:
                if asset in dfs.keys():
                    dfs_portfolio.append(dfs[asset])
            if len(dfs_portfolio) == 0:
                raw_portfolio = pd.DataFrame()
            else:
                raw_portfolio = pd.concat(dfs_portfolio, axis=0)
                raw_portfolio = raw_portfolio[raw_portfolio['종목명']!='소계']
            self.raw_portfolio = raw_portfolio
        return self.raw_portfolio
    
    def get_df(self):
        if self.df is None:
            cols_for_comparison = ['종목명', '종목', '비중: 자산대비']
            self.df = self.get_raw_portfolio()[cols_for_comparison].set_index('종목')
        return self.df

    def _load_pipeline(self):
        try:
            self.get_raw_portfolio()
            self.get_df()
            return True
        except Exception as e:
            print(f'PortfolioVector _load_pipeline error: {e}')
            return False
    