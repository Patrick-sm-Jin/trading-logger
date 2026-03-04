from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

session = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

def get_yesterday_trades():
    # 어제 날짜 시작/끝 타임스탬프 계산
    yesterday = datetime.utcnow() - timedelta(days=1)
    start = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    end = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)

    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)

    response = session.get_closed_pnl(
        category="linear",
        startTime=start_ms,
        endTime=end_ms,
        limit=100
    )

    trades = response["result"]["list"]
    return trades
def get_wallet_balance():
    """실제 계좌 잔고 조회"""
    response = session.get_wallet_balance(
        accountType="UNIFIED",
        coin="USDT"
    )
    balance = response["result"]["list"][0]["totalEquity"]
    return float(balance)