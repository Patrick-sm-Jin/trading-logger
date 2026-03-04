from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

TRADES_DB_ID = os.getenv("NOTION_TRADES_DB_ID")
SUMMARY_DB_ID = os.getenv("NOTION_SUMMARY_DB_ID")

# 거래 상세 기록 페이지에 데이터 추가
def add_trade(trade):
    notion.pages.create(
        parent={"database_id": TRADES_DB_ID},
        properties={
            "종목": {"title": [{"text": {"content": trade["symbol"]}}]},
            "거래 시간": {"date": {"start": trade["trade_time"]}},
            "방향": {"select": {"name": trade["side"]}},
            "레버리지": {"number": trade["leverage"]},
            "진입 비율": {"number": trade["entry_ratio"]},
            "진입 시 총 자산": {"number": trade["wallet_balance"]},
            "진입가": {"number": trade["entry_price"]},
            "청산가": {"number": trade["exit_price"]},
            "수량": {"number": trade["qty"]},
            "PnL (USDT)": {"number": trade["pnl"]},
            "승패": {"select": {"name": "승" if trade["pnl"] > 0 else "패"}},
        }
    )

# 일간 요약 페이지에 데이터 추가
def add_summary(summary):
    notion.pages.create(
        parent={"database_id": SUMMARY_DB_ID},
        properties={
            "날짜": {"title": [{"text": {"content": summary["date"]}}]},
            "총 거래 횟수": {"number": summary["total_trades"]},
            "승률": {"number": summary["win_rate"]},
            "일 손익 (USDT)": {"number": summary["daily_pnl"]},
            "누적 손익 (USDT)": {"number": summary["total_pnl"]},
            "최대 수익 거래": {"number": summary["max_profit"]},
            "최대 손실 거래": {"number": summary["max_loss"]},
        }
    )

# 일간 요약 페이지에서 가장 최근 누적 손익 가져오기
def get_last_total_pnl():
    response = notion.databases.query(
        **{
            "database_id": SUMMARY_DB_ID,
            "sorts": [{"property": "날짜", "direction": "descending"}],
            "page_size": 1
        }
    )
    results = response["results"]
    if not results:
        return 0
    last = results[0]["properties"]
    return last["누적 손익 (USDT)"]["number"] or 0