import re

with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/sniper_scanner.py', 'r') as f:
    content = f.read()

# 1. Add TRADES_FILE and config at the top
config_block = """DATA_FILE = 'sniper_data.json'
TRADES_FILE = 'sniper_trades.json'
DEFAULT_TP_PCT = 2.0
DEFAULT_SL_PCT = 1.0
"""
content = content.replace("DATA_FILE = 'sniper_data.json'", config_block)

# 2. Add load_trades and save_trades functions before check_sniper_cross
functions_block = """def load_trades():
    if os.path.exists(TRADES_FILE):
        try:
            with open(TRADES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"open_trades": [], "closed_trades": [], "stats": {"total": 0, "wins": 0, "losses": 0, "win_rate": 0.0}}

def save_trades(trades_data):
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades_data, f, indent=4)

def check_sniper_cross():"""
content = content.replace("def check_sniper_cross():", functions_block)

# 3. In check_sniper_cross, load trades_data
load_trades_block = """    radar_data = {
        "last_updated": now_str,
        "timeframe": TIMEFRAME,
        "alerts": historical_alerts,
        "coins": []
    }
    
    trades_data = load_trades()
"""
content = content.replace("""    radar_data = {
        "last_updated": now_str,
        "timeframe": TIMEFRAME,
        "alerts": historical_alerts,
        "coins": []
    }""", load_trades_block)

# 4. Check open trades logic inside the loop, after getting curr_price
open_trades_logic = """            curr_bandwidth = df['bandwidth'].iloc[-1]
            is_squeeze = curr_bandwidth < 1.0  # Compresión extrema (< 1% en bandas)
            
            # --- FORWARD TESTING LOGIC: Check open trades ---
            open_trade_idx = -1
            clean_symbol = symbol.replace('/USDT', '')
            for i, t in enumerate(trades_data['open_trades']):
                if t['symbol'] == clean_symbol:
                    open_trade_idx = i
                    break
            
            if open_trade_idx != -1:
                t = trades_data['open_trades'][open_trade_idx]
                closed = False
                win = False
                if t['direction'] == 'LONG':
                    if curr_price >= t['take_profit']:
                        closed, win = True, True
                    elif curr_price <= t['stop_loss']:
                        closed, win = True, False
                else: # SHORT
                    if curr_price <= t['take_profit']:
                        closed, win = True, True
                    elif curr_price >= t['stop_loss']:
                        closed, win = True, False
                
                if closed:
                    t['status'] = 'WIN' if win else 'LOSS'
                    t['exit_price'] = curr_price
                    t['exit_time'] = datetime.now().strftime('%d/%m %H:%M:%S')
                    
                    # Update stats
                    trades_data['stats']['total'] += 1
                    if win: trades_data['stats']['wins'] += 1
                    else: trades_data['stats']['losses'] += 1
                    trades_data['stats']['win_rate'] = round((trades_data['stats']['wins'] / trades_data['stats']['total']) * 100, 1)
                    
                    # Move to closed
                    trades_data['closed_trades'].insert(0, t)
                    if len(trades_data['closed_trades']) > 20:
                        trades_data['closed_trades'] = trades_data['closed_trades'][:20]
                    trades_data['open_trades'].pop(open_trade_idx)
                    save_trades(trades_data)
                    print(f"[{now_str}] TRADE CERRADO: {clean_symbol} -> {t['status']}")
            
            # ------------------------------------------------
            
            # Detectar estado"""
content = content.replace("""            curr_bandwidth = df['bandwidth'].iloc[-1]
            is_squeeze = curr_bandwidth < 1.0  # Compresión extrema (< 1% en bandas)
            
            # Detectar estado""", open_trades_logic)

# 5. Open new trade logic when alert is fired
open_long_logic = """                    # FILTRO EXTRA (AFINACIÓN SNIPER):
                    # Solo enviamos la notificación al sistema si el MACD está alineado y el RSI es óptimo.
                    if rsi_dorado_valido and macd_bullish:
                        msg = "Cruce Alcista CONFIRMADO + MACD Verde"
                        if is_squeeze: msg += " + SQUEEZE 💥"
                        send_notification(symbol, TIMEFRAME, curr_price, msg)
                        
                        # FORWARD TESTING: Open LONG
                        if open_trade_idx == -1:
                            tp = curr_price * (1 + DEFAULT_TP_PCT/100)
                            sl = curr_price * (1 - DEFAULT_SL_PCT/100)
                            trades_data['open_trades'].append({
                                'symbol': clean_symbol,
                                'direction': 'LONG',
                                'entry_price': curr_price,
                                'entry_time': now_str,
                                'take_profit': round(tp, 4),
                                'stop_loss': round(sl, 4),
                                'status': 'OPEN'
                            })
                            save_trades(trades_data)"""
content = content.replace("""                    # FILTRO EXTRA (AFINACIÓN SNIPER):
                    # Solo enviamos la notificación al sistema si el MACD está alineado y el RSI es óptimo.
                    if rsi_dorado_valido and macd_bullish:
                        msg = "Cruce Alcista CONFIRMADO + MACD Verde"
                        if is_squeeze: msg += " + SQUEEZE 💥"
                        send_notification(symbol, TIMEFRAME, curr_price, msg)""", open_long_logic)

open_short_logic = """                    if rsi_bajista_valido and not macd_bullish:
                        msg = "Cruce Bajista CONFIRMADO + MACD Rojo"
                        if is_squeeze: msg += " + SQUEEZE 💥"
                        send_notification(symbol, TIMEFRAME, curr_price, msg)
                        
                        # FORWARD TESTING: Open SHORT
                        if open_trade_idx == -1:
                            tp = curr_price * (1 - DEFAULT_TP_PCT/100)
                            sl = curr_price * (1 + DEFAULT_SL_PCT/100)
                            trades_data['open_trades'].append({
                                'symbol': clean_symbol,
                                'direction': 'SHORT',
                                'entry_price': curr_price,
                                'entry_time': now_str,
                                'take_profit': round(tp, 4),
                                'stop_loss': round(sl, 4),
                                'status': 'OPEN'
                            })
                            save_trades(trades_data)"""
content = content.replace("""                    if rsi_bajista_valido and not macd_bullish:
                        msg = "Cruce Bajista CONFIRMADO + MACD Rojo"
                        if is_squeeze: msg += " + SQUEEZE 💥"
                        send_notification(symbol, TIMEFRAME, curr_price, msg)""", open_short_logic)


with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/sniper_scanner.py', 'w') as f:
    f.write(content)

print("Patch applied.")
