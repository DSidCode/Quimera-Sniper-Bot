import re

with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/sniper_scanner.py', 'r') as f:
    content = f.read()

# 1. Replace TIMEFRAME config with TIMEFRAMES dictionary
config_block = """TIMEFRAMES = {
    '15m': {'tp': 2.0, 'sl': 1.0},
    '30m': {'tp': 3.5, 'sl': 1.5},
    '1h': {'tp': 5.0, 'sl': 2.5}
}"""
content = re.sub(r"TIMEFRAME = '15m'.*?DEFAULT_SL_PCT = 1.0\n", config_block + "\n", content, flags=re.DOTALL)

# 2. Add TIMEFRAME to alert storage (historical_alerts)
alert_obj_block = """    alert_obj = {
        "time": now_str,
        "symbol": symbol.replace('/USDT', ''),
        "timeframe": timeframe,
        "price": current_price,
        "message": tipo_cruce
    }"""
content = re.sub(r"    alert_obj = \{.*?\}", alert_obj_block, content, flags=re.DOTALL)

# 3. Update check_sniper_cross to loop over timeframes
check_cross_logic = """def check_sniper_cross():
    now_str = datetime.now().strftime('%H:%M:%S')
    print(f"[{now_str}] Escaneando mercados en múltiples temporalidades...")
    
    radar_data = {
        "last_updated": now_str,
        "timeframes": list(TIMEFRAMES.keys()),
        "alerts": historical_alerts,
        "coins": []
    }
    
    trades_data = load_trades()
    
    for timeframe, risk in TIMEFRAMES.items():
        print(f"[{now_str}] Procesando {timeframe}...")
        for symbol in SYMBOLS:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=50)"""

content = re.sub(r"def check_sniper_cross\(\):.*?ohlcv = exchange\.fetch_ohlcv\(symbol, TIMEFRAME, limit=50\)", check_cross_logic, content, flags=re.DOTALL)

# 4. Modify open trades check to match timeframe
open_trades_logic = """            # --- FORWARD TESTING LOGIC: Check open trades ---
            open_trade_idx = -1
            clean_symbol = symbol.replace('/USDT', '')
            for i, t in enumerate(trades_data['open_trades']):
                if t['symbol'] == clean_symbol and t.get('timeframe') == timeframe:
                    open_trade_idx = i
                    break"""
content = re.sub(r"            # --- FORWARD TESTING LOGIC: Check open trades ---.*?break", open_trades_logic, content, flags=re.DOTALL)

# 5. Modify send_notification call and trade opening parameters
# For LONG
send_notif_long = """                        send_notification(symbol, timeframe, curr_price, msg)
                        
                        # FORWARD TESTING: Open LONG
                        if open_trade_idx == -1:
                            tp = curr_price * (1 + risk['tp']/100)
                            sl = curr_price * (1 - risk['sl']/100)
                            trades_data['open_trades'].append({
                                'symbol': clean_symbol,
                                'timeframe': timeframe,
                                'direction': 'LONG',"""
content = re.sub(r"                        send_notification\(symbol, TIMEFRAME, curr_price, msg\).*?'direction': 'LONG',", send_notif_long, content, flags=re.DOTALL)

# For SHORT
send_notif_short = """                        send_notification(symbol, timeframe, curr_price, msg)
                        
                        # FORWARD TESTING: Open SHORT
                        if open_trade_idx == -1:
                            tp = curr_price * (1 - risk['tp']/100)
                            sl = curr_price * (1 + risk['sl']/100)
                            trades_data['open_trades'].append({
                                'symbol': clean_symbol,
                                'timeframe': timeframe,
                                'direction': 'SHORT',"""
content = re.sub(r"                        send_notification\(symbol, TIMEFRAME, curr_price, msg\).*?'direction': 'SHORT',", send_notif_short, content, flags=re.DOTALL)


# 6. Append timeframe to radar_data
radar_append = """            radar_data["coins"].append({
                "timeframe": timeframe,
                "symbol": symbol.replace('/USDT', ''),"""
content = re.sub(r"            radar_data\[\"coins\"\].append\(\{.*?\"symbol\": symbol.replace\('/USDT', ''\),", radar_append, content, flags=re.DOTALL)


with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/sniper_scanner.py', 'w') as f:
    f.write(content)

print("Scanner multi-timeframe patch applied.")
