# 📊 Trading Logger

바이비트 자동매매 거래 내역을 매일 자동으로 노션에 기록하는 시스템

## 📌 프로젝트 개요

바이비트에서 발생한 당일 거래 내역을 자동으로 수집 및 분석하여
노션 데이터베이스에 정리해주는 자동화 툴입니다.

## ⚙️ 주요 기능

- 바이비트 API로 당일 거래 내역 자동 수집
- 승률, PnL, 진입 비율, 누적 손익 자동 계산
- 노션 DB에 거래 상세 기록 및 일간 요약 자동 저장
- 매일 KST 09:00 자동 실행 스케줄러

## 🗂️ 노션 DB 구조

**거래 상세 기록**
| 컬럼 | 설명 |
|---|---|
| 종목 | 거래 코인 (예: BTCUSDT) |
| 거래시간 | 포지션 청산 시간 |
| 방향 | 롱 / 숏 |
| 레버리지 | 사용 레버리지 |
| 진입 비율 | 총 자산 대비 진입 비율 (%) |
| 진입 시 총 자산 | 진입 시점 지갑 잔고 (USDT) |
| PnL (USDT) | 손익 |
| 승패 | 승 / 패 |

**일간 요약**
| 컬럼 | 설명 |
|---|---|
| 날짜 | 거래 날짜 |
| 총 거래 횟수 | 당일 거래 건수 |
| 승률 | 당일 승률 (%) |
| 일 손익 (USDT) | 당일 손익 합계 |
| 누적 손익 (USDT) | 전체 누적 손익 |
| 최대 수익 거래 | 당일 최대 수익 |
| 최대 손실 거래 | 당일 최대 손실 |

## 🛠️ 기술 스택

- Python
- pybit (바이비트 API)
- notion-client (노션 API)
- APScheduler (스케줄러)
- python-dotenv

## 🚀 실행 방법

1. 패키지 설치
\```bash
pip install pybit notion-client python-dotenv apscheduler
\```

2. `.env` 파일 설정
\```
BYBIT_API_KEY=your_key
BYBIT_API_SECRET=your_secret
NOTION_TOKEN=your_token
NOTION_TRADES_DB_ID=your_db_id
NOTION_SUMMARY_DB_ID=your_db_id
\```

3. 실행
\```bash
# 수동 실행
python main.py

# 자동 스케줄러 실행
python scheduler.py
\```