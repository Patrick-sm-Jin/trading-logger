from bybit_client import get_yesterday_trades
from notion_api import add_trade, add_summary
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
from notion_api import add_trade, add_summary, get_last_total_pnl
from bybit_client import get_yesterday_trades, get_wallet_balance

load_dotenv()

def process_trades():
    trades = get_yesterday_trades()
    
    if not trades:
        print("어제 거래 내역 없음")
        return

    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    pnl_list = []
    win_count = 0

    for t in trades:
        pnl = float(t["closedPnl"])
        entry_price = float(t["avgEntryPrice"])
        exit_price = float(t["avgExitPrice"])
        qty = float(t["qty"])
        leverage = float(t["leverage"])
        wallet_balance = get_wallet_balance()
        entry_ratio = round((entry_price * qty) / wallet_balance * 100, 2) if wallet_balance else 0
        trade_time = datetime.fromtimestamp(int(t["updatedTime"]) / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        side = "롱" if t["side"] == "Buy" else "숏"

        trade_data = {
            "symbol": t["symbol"],
            "trade_time": trade_time,
            "side": side,
            "leverage": leverage,
            "entry_ratio": entry_ratio,
            "wallet_balance": wallet_balance,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "qty": qty,
            "pnl": pnl,
        }

        add_trade(trade_data)
        pnl_list.append(pnl)
        if pnl > 0:
            win_count += 1

    total_trades = len(pnl_list)
    win_rate = round(win_count / total_trades * 100, 2)
    daily_pnl = round(sum(pnl_list), 4)
    max_profit = round(max(pnl_list), 4)
    max_loss = round(min(pnl_list), 4)

    summary_data = {
        "date": yesterday,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "daily_pnl": daily_pnl,
        "total_pnl": round(get_last_total_pnl() + daily_pnl, 4),  # 누적은 나중에 개선
        "max_profit": max_profit,
        "max_loss": max_loss,
    }

    add_summary(summary_data)
    print(f"완료! {total_trades}건 기록됨")

if __name__ == "__main__":
    process_trades()