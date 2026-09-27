import ccxt
import time
import sys
import json

# =======================================================
# ⚡ CONFIGURATION - IMMEDIATE ACTION REQUIRED ⚡
# =======================================================

# --- Exchange Selection ---
# Match this ID to the exchange you are connecting to.
EXCHANGE_ID = 'binance' 

# --- API Credentials (Required for live trading) ---
API_KEY = "YOUR_API_KEY_HERE"        # <<< *** REPLACE THIS ***
SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # <<< *** REPLACE THIS ***

# --- Trading Parameters (The core of the 'Flash' logic) ---
TRADING_PAIR = 'USDT/BUSD'           # <<< *** REPLACE THIS ***
QTY_TO_TRADE = 0.05                   # <<< *** REPLACE THIS ***
TRADE_ACTION = 'BUY'                  # 'BUY' or 'SELL'
TICKER_LIMIT = 50                     # Number of data points to analyze/fetch

# --- Flash Optimization Settings ---
POLLING_INTERVAL_SEC = 5              # Check market state every 5 seconds
MAX_HISTORY_CHECK = 100               # How far back to check history (if you implement charting/lookback)

# =======================================================
# ⚙️ CORE FUNCTIONS
# =======================================================

def initialize_exchange(exchange_id, api_key, secret_key):
    """Initializes and returns the chosen exchange object."""
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
        })
        print(f"✅ SUCCESS: Initialized {exchange.id} for USDT trading.")
        return exchange
    except AttributeError:
        print(f"❌ ERROR: Exchange ID '{exchange_id}' not recognized by ccxt.")
        return None
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to exchange: {e}")
        return None

def fetch_realtime_data(exchange, symbol):
    """Fetches the latest ticker and order book for fast analysis."""
    try:
        # Fetch Ticker for basic price info
        ticker = exchange.fetch_ticker(symbol)

        # Fetch Order Book for depth analysis (crucial for HFT/Flash)
        order_book = exchange.fetch_order_book(symbol)

        return ticker, order_book
    except Exception as e:
        print(f"🛑 Data Fetch Error: {e}")
        return None, None

def execute_flash_trade(exchange, symbol, action, quantity):
    """Executes a market order trade immediately."""
    try:
        if action.upper() == 'BUY':
            order = exchange.create_market_buy_order(symbol, quantity)
            print(f"\n🔥 [FLASH BUY SUCCESS] Executed Order ID: {order['id']} @ {order.get('price', 'N/A')}")
        elif action.upper() == 'SELL':
            order = exchange.create_market_sell_order(symbol, quantity)
            print(f"\n🔥 [FLASH SELL SUCCESS] Executed Order ID: {order['id']} @ {order.get('price', 'N/A')}")
        else:
            print(f"🚨 ERROR: Invalid trade action '{action}'. Must be 'BUY' or 'SELL'.")
        return order
    except ccxt.InsufficientFunds:
        print("🚨 TRADING ERROR: Insufficient funds to execute the trade.")
    except Exception as e:
        print(f"❌ CRITICAL EXECUTION ERROR: {e}")
    return None

def run_flash_strategy(exchange, symbol, action, quantity):
    """The main loop where the 'Flash' decision-making happens."""

    print("\n" + "="*70)
    print(f"🚀 FLASH TRADER ACTIVATED | Pair: {symbol} | Action: {action} | Rate: {POLLING_INTERVAL_SEC}s")
    print("="*70)

    while True:
        start_time = time.time()

        # 1. Data Acquisition
        ticker, order_book = fetch_realtime_data(exchange, symbol)

        if ticker and order_book:
            print(f"\n--- Snapshot @ {time.strftime('%H:%M:%S')} ---")
            print(f"Last Price: {ticker.get('last')}")
            print(f"Best Ask: {ticker.get('ask')}")
            print(f"Best Bid: {ticker.get('bid')}")

            # 2. Decision Making (THE STRATEGY)
            # === REPLACE THIS LOGIC WITH YOUR ACTUAL TRADING ALGORITHM ===
            should_trade = True # Set this to False to monitor only

            if should_trade:
                print("--&gt; Strategy Triggered: Preparing Flash Trade...")
                execute_flash_trade(exchange, symbol, action, quantity)
            else:
                print("--&gt; Strategy Not Triggered: Monitoring...")
            # ===============================================================

        # 3. Polling Interval Management
        elapsed = time.time() - start_time
        sleep_time = max(0, POLLING_INTERVAL_SEC - elapsed)

        print(f"\n[INFO] Cycle complete. Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

# =======================================================
# 🎯 EXECUTION ENTRY POINT
# =======================================================
if __name__ == "__main__":
    # Run the main loop
    exchange_instance = initialize_exchange(EXCHANGE_ID, API_KEY, SECRET_KEY)

    if exchange_instance:
        run_flash_strategy(
            exchange_instance, 
            TRADING_PAIR, 
            TRADE_ACTION, 
            QTY_TO_TRADE
        )
    else:
        print("\nCannot proceed without a functional exchange connection.")
        sys.exit(1)
