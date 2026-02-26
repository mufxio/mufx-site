#!/usr/bin/env python3
"""
muFX Signal Check — Daily Price Fetcher
========================================
Pulls all market data needed for the daily signal check.
Uses free APIs (no key required): Yahoo Finance via yfinance.

Usage:
    python3 fetch_prices.py              # Current / last close
    python3 fetch_prices.py --json       # Output as JSON for automation
    python3 fetch_prices.py --csv        # Output as CSV

Requires: pip install yfinance requests
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
# INSTRUMENT MAP
# ═══════════════════════════════════════════════════════════
INSTRUMENTS = {
    # Primary (price strip)
    "DXY":     {"ticker": "DX-Y.NYB",  "decimals": 2, "category": "primary"},
    "EUR/USD": {"ticker": "EURUSD=X",  "decimals": 4, "category": "primary"},
    "XAU/USD": {"ticker": "GC=F",      "decimals": 0, "category": "primary", "note": "Gold futures front month"},
    "USD/JPY": {"ticker": "JPY=X",     "decimals": 2, "category": "primary"},
    # Secondary (extended table)
    "GBP/USD": {"ticker": "GBPUSD=X",  "decimals": 4, "category": "secondary"},
    "AUD/USD": {"ticker": "AUDUSD=X",  "decimals": 4, "category": "secondary"},
    "USD/CHF": {"ticker": "CHF=X",     "decimals": 4, "category": "secondary"},
    "US10Y":   {"ticker": "^TNX",      "decimals": 3, "category": "secondary", "note": "10Y yield, divide by 1 (already %)"},
    "Brent":   {"ticker": "BZ=F",      "decimals": 2, "category": "secondary", "note": "Brent front month"},
    # Supplementary
    "S&P500":  {"ticker": "^GSPC",     "decimals": 2, "category": "supplementary"},
    "VIX":     {"ticker": "^VIX",      "decimals": 2, "category": "supplementary"},
    "BTC/USD": {"ticker": "BTC-USD",   "decimals": 0, "category": "supplementary"},
}


def fetch_all():
    """Fetch latest prices for all instruments."""
    results = {}
    tickers = {name: info["ticker"] for name, info in INSTRUMENTS.items()}
    
    # Batch download — single API call for all tickers
    print("Fetching market data...\n", file=sys.stderr)
    data = yf.download(
        list(tickers.values()),
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=True,
    )
    
    for name, info in INSTRUMENTS.items():
        ticker = info["ticker"]
        decimals = info["decimals"]
        
        try:
            # Get last two trading days
            close_col = ("Close", ticker) if isinstance(data.columns, type(data.columns)) else "Close"
            
            try:
                closes = data["Close"][ticker].dropna()
            except (KeyError, TypeError):
                # Fallback: fetch individually
                single = yf.Ticker(ticker).history(period="5d")
                closes = single["Close"].dropna()
            
            if len(closes) < 2:
                results[name] = {"error": "Insufficient data"}
                continue
                
            current = closes.iloc[-1]
            previous = closes.iloc[-2]
            change_pct = ((current - previous) / previous) * 100
            
            # Direction
            if abs(change_pct) < 0.01:
                direction = "flat"
                arrow = "●"
            elif change_pct > 0:
                direction = "up"
                arrow = "▲"
            else:
                direction = "down"
                arrow = "▼"
            
            results[name] = {
                "price": round(float(current), decimals),
                "prev_close": round(float(previous), decimals),
                "change_pct": round(float(change_pct), 2),
                "change_str": f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%",
                "direction": direction,
                "arrow": arrow,
                "category": info["category"],
                "date": str(closes.index[-1].date()),
            }
            
        except Exception as e:
            results[name] = {"error": str(e), "category": info["category"]}
    
    return results


def print_table(results):
    """Pretty-print results as a terminal table."""
    print(f"\n{'═' * 72}")
    print(f"  muFX SIGNAL CHECK — PRICE DATA")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'═' * 72}\n")
    
    for category in ["primary", "secondary", "supplementary"]:
        label = {"primary": "▌ PRIMARY (Price Strip)", 
                 "secondary": "▌ SECONDARY (Extended Table)",
                 "supplementary": "▌ SUPPLEMENTARY"}[category]
        print(f"  {label}")
        print(f"  {'─' * 66}")
        
        for name, data in results.items():
            if data.get("category") != category:
                continue
            if "error" in data:
                print(f"  {name:<12} ERROR: {data['error']}")
                continue
            
            price_str = f"{data['price']:>12}" if data["price"] >= 100 else f"{data['price']:>12}"
            chg_str = f"{data['arrow']} {data['change_str']:>8}"
            dir_indicator = {"up": "🟢", "down": "🔴", "flat": "🟡"}[data["direction"]]
            
            print(f"  {name:<12} {price_str}   {chg_str}  {dir_indicator}   (prev: {data['prev_close']})")
        
        print()
    
    print(f"{'═' * 72}")
    print(f"  Data date: {next(iter(results.values())).get('date', 'N/A')}")
    print(f"  Source: Yahoo Finance via yfinance")
    print(f"{'═' * 72}\n")


def print_json(results):
    """Output as JSON for automation."""
    output = {
        "generated": datetime.now().isoformat(),
        "source": "Yahoo Finance",
        "instruments": results,
    }
    print(json.dumps(output, indent=2))


def print_csv(results):
    """Output as CSV."""
    print("instrument,price,prev_close,change_pct,direction,category,date")
    for name, data in results.items():
        if "error" in data:
            print(f"{name},ERROR,,,,,")
            continue
        print(f"{name},{data['price']},{data['prev_close']},{data['change_pct']},{data['direction']},{data['category']},{data['date']}")


def main():
    parser = argparse.ArgumentParser(description="muFX Daily Price Fetcher")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--csv", action="store_true", help="Output as CSV")
    args = parser.parse_args()
    
    results = fetch_all()
    
    if args.json:
        print_json(results)
    elif args.csv:
        print_csv(results)
    else:
        print_table(results)


if __name__ == "__main__":
    main()
