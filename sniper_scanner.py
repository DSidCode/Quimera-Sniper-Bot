import ccxt
import pandas as pd
import time
import os
import json
from datetime import datetime

# Lista global para guardar histórico de alertas
historical_alerts = []

# Configuración del escáner
SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'ZEC/USDT', 'TAO/USDT', 'ADA/USDT', 
    'SUI/USDT', 'SOL/USDT', 'DOT/USDT', 'RENDER/USDT', 'AAVE/USDT', 
    'XRP/USDT', 'UNI/USDT', 'LINK/USDT', 'DOGE/USDT', 'LTC/USDT',
    'INJ/USDT'
]
TIMEFRAMES = {
    '15m': {'tp': 4.0, 'sl': 2.0},
    '30m': {'tp': 6.0, 'sl': 3.0},
    '1h': {'tp': 8.0, 'sl': 4.0}
}

CHECK_INTERVAL_SECONDS = 30
DATA_FILE = 'sniper_data.json'
TRADES_FILE = 'sniper_trades.json'

# Inicializar Binance (API Pública)
exchange = ccxt.binance({
    'enableRateLimit': True,
})

def send_notification(symbol, timeframe, current_price, tipo_cruce="Alcista EMA 9/21"):
    title = f"🎯 SNIPER ALERT: {symbol}"
    message = f"{tipo_cruce} en {timeframe} detectado! Precio actual: ${current_price}"
    
    # Enviar notificación nativa al SO además de guardarla
    os.system(f"notify-send -u critical '{title}' '{message}'")
    
    now_str = datetime.now().strftime('%H:%M:%S')
    alert_obj = {
        "time": now_str,
        "symbol": symbol.replace('/USDT', ''),
        "timeframe": timeframe,
        "price": current_price,
        "message": tipo_cruce
    }
    
    historical_alerts.insert(0, alert_obj)
    # Mantener solo las últimas 15 alertas
    if len(historical_alerts) > 15:
        historical_alerts.pop()
        
    print(f"\n[ALERTA REGISTRADA Y ENVIADA] {now_str} | {title} - {message}")

def calculate_ema(df, window):
    return df['close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(df, window=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/window, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/window, adjust=False).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_sma(df, col, window):
    return df[col].rolling(window=window).mean()

def load_trades():
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

def check_sniper_cross():
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
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=50)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
                df['ema9'] = calculate_ema(df, 9)
                df['ema21'] = calculate_ema(df, 21)
                df['rsi'] = calculate_rsi(df, 14)
                df['vol_sma20'] = calculate_sma(df, 'volume', 20)
            
                # MACD
                df['ema12'] = calculate_ema(df, 12)
                df['ema26'] = calculate_ema(df, 26)
                df['macd'] = df['ema12'] - df['ema26']
                df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
            
                # Bollinger Bands
                df['sma20'] = calculate_sma(df, 'close', 20)
                df['std20'] = df['close'].rolling(window=20).std()
                df['upper_band'] = df['sma20'] + (df['std20'] * 2)
                df['lower_band'] = df['sma20'] - (df['std20'] * 2)
                df['bandwidth'] = (df['upper_band'] - df['lower_band']) / df['sma20'] * 100
            
                prev_ema9 = df['ema9'].iloc[-2]
                prev_ema21 = df['ema21'].iloc[-2]
            
                curr_ema9 = df['ema9'].iloc[-1]
                curr_ema21 = df['ema21'].iloc[-1]
                curr_price = df['close'].iloc[-1]
                curr_rsi = df['rsi'].iloc[-1]
                curr_vol = df['volume'].iloc[-1]
                avg_vol = df['vol_sma20'].iloc[-1]
            
                curr_macd = df['macd'].iloc[-1]
                curr_signal = df['signal'].iloc[-1]
                macd_bullish = curr_macd > curr_signal
            
                curr_bandwidth = df['bandwidth'].iloc[-1]
                is_squeeze = curr_bandwidth < 1.0  # Compresión extrema (< 1% en bandas)
            
                # --- FORWARD TESTING LOGIC: Check open trades ---
                open_trade_idx = -1
                clean_symbol = symbol.replace('/USDT', '')
                for i, t in enumerate(trades_data['open_trades']):
                    if t['symbol'] == clean_symbol and t.get('timeframe') == timeframe:
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
            
                # Detectar estado
                estado = "NEUTRAL"
                probabilidad = 50
                direccion = "NEUTRA"
            
                diff_percent = ((curr_ema9 - curr_ema21) / curr_ema21) * 100
                abs_diff = abs(diff_percent)
            
                if curr_ema9 > curr_ema21:
                    estado = "ALCISTA (TENDENCIA)"
                    direccion = "ALZA"
                    if abs_diff < 0.2:
                        probabilidad = 80
                    elif abs_diff < 1.0:
                        probabilidad = 70
                    else:
                        probabilidad = 60 # Sobre-extendido
                else:
                    estado = "BAJISTA (TENDENCIA)"
                    direccion = "BAJA"
                    if abs_diff < 0.2:
                        probabilidad = 80
                    elif abs_diff < 1.0:
                        probabilidad = 70
                    else:
                        probabilidad = 60
                
                cruce_dorado = prev_ema9 <= prev_ema21 and curr_ema9 > curr_ema21
                cruce_bajista = prev_ema9 >= prev_ema21 and curr_ema9 < curr_ema21
            
                # FILTROS ANTIRRUIDO (MERCADO PLANO):
                # 1. El volumen debe ser significativamente mayor a la media (1.5x).
                volumen_valido = curr_vol > (avg_vol * 1.5)
            
                # 2. La vela debe tener un cuerpo mínimo para no ser considerada "plana".
                vela_tamano = abs(df['close'].iloc[-1] - df['open'].iloc[-1]) / df['open'].iloc[-1] * 100
                vela_valida = vela_tamano >= 0.15  # Mínimo 0.15% de movimiento real
            
                rsi_dorado_valido = 50 <= curr_rsi <= 70
                rsi_bajista_valido = 30 <= curr_rsi <= 50

                if cruce_dorado:
                    if volumen_valido and vela_valida:
                        estado = "🚀 ¡CRUCE DORADO AHORA!"
                        direccion = "ALZA"
                        probabilidad = 95 if macd_bullish else 85
                    
                        # FILTRO EXTRA (AFINACIÓN SNIPER):
                        # Solo enviamos la notificación al sistema si el MACD está alineado y el RSI es óptimo.
                        if rsi_dorado_valido and macd_bullish:
                            msg = "Cruce Alcista CONFIRMADO + MACD Verde"
                            if is_squeeze: msg += " + SQUEEZE 💥"
                        
                            # FORWARD TESTING: Open LONG (y Notificar solo 1 vez)
                            if open_trade_idx == -1:
                                tp = curr_price * (1 + risk['tp']/100)
                                sl = curr_price * (1 - risk['sl']/100)
                                # Probabilidad para LONG ya fue asignada arriba (ej. 95 o 85)
                                capital_rec = "$150-$200 🎯" if probabilidad >= 90 else ("$100 🛡️" if probabilidad >= 75 else "$50 ⚠️")
                                msg += f" | SL: ${round(sl,4)} | TP: ${round(tp,4)} | {capital_rec}"
                                
                                send_notification(symbol, timeframe, curr_price, msg)
                                trades_data['open_trades'].append({
                                    'symbol': clean_symbol,
                                    'timeframe': timeframe,
                                    'direction': 'LONG',
                                    'entry_price': curr_price,
                                    'entry_time': now_str,
                                    'take_profit': round(tp, 4),
                                    'stop_loss': round(sl, 4),
                                    'capital': capital_rec,
                                    'status': 'OPEN'
                                })
                                save_trades(trades_data)
                    else:
                        estado = "ALCISTA (RUIDO)"
                        probabilidad = 50
                
                elif cruce_bajista:
                    if volumen_valido and vela_valida:
                        estado = "🩸 ¡CRUCE BAJISTA AHORA!"
                        direccion = "BAJA"
                        probabilidad = 95 if not macd_bullish else 85
                    
                        if rsi_bajista_valido and not macd_bullish:
                            msg = "Cruce Bajista CONFIRMADO + MACD Rojo"
                            if is_squeeze: msg += " + SQUEEZE 💥"
                        
                            # FORWARD TESTING: Open SHORT (y Notificar solo 1 vez)
                            if open_trade_idx == -1:
                                tp = curr_price * (1 - risk['tp']/100)
                                sl = curr_price * (1 + risk['sl']/100)
                                capital_rec = "$150-$200 🎯" if probabilidad >= 90 else ("$100 🛡️" if probabilidad >= 75 else "$50 ⚠️")
                                msg += f" | SL: ${round(sl,4)} | TP: ${round(tp,4)} | {capital_rec}"
                                
                                send_notification(symbol, timeframe, curr_price, msg)
                                trades_data['open_trades'].append({
                                    'symbol': clean_symbol,
                                    'timeframe': timeframe,
                                    'direction': 'SHORT',
                                    'entry_price': curr_price,
                                    'entry_time': now_str,
                                    'take_profit': round(tp, 4),
                                    'stop_loss': round(sl, 4),
                                    'capital': capital_rec,
                                    'status': 'OPEN'
                                })
                                save_trades(trades_data)
                    else:
                        estado = "BAJISTA (RUIDO)"
                        probabilidad = 50
                
                # Calcular capital recomendado basado en probabilidad
                capital = "$50"
                if probabilidad >= 90:
                    capital = "$150-$200 🎯"
                elif probabilidad >= 75:
                    capital = "$100 🛡️"
                else:
                    capital = "$50 ⚠️"
                
                prob_str = f"{probabilidad}%"
            
                vol_status = "🟩" if curr_vol > (avg_vol * 1.5) else "⬜"
            
                if "ALCISTA" in estado or "DORADO" in estado:
                    calc_tp = curr_price * (1 + risk['tp']/100)
                    calc_sl = curr_price * (1 - risk['sl']/100)
                else:
                    calc_tp = curr_price * (1 - risk['tp']/100)
                    calc_sl = curr_price * (1 + risk['sl']/100)
            
                radar_data["coins"].append({
                    "timeframe": timeframe,
                    "symbol": symbol.replace('/USDT', ''),
                    "price": round(curr_price, 4),
                    "ema9": round(curr_ema9, 4),
                    "ema21": round(curr_ema21, 4),
                    "distancia_porcentaje": round(diff_percent, 3),
                    "estado": estado,
                    "probabilidad": prob_str,
                    "capital": capital,
                    "sl": round(calc_sl, 4),
                    "tp": round(calc_tp, 4),
                    "rsi": round(curr_rsi, 1) if not pd.isna(curr_rsi) else 50.0,
                    "volumen": vol_status,
                    "macd_bullish": bool(macd_bullish),
                    "is_squeeze": bool(is_squeeze)
                })
                
                time.sleep(0.5) 
            
            except Exception as e:
                print(f"Error escaneando {symbol}: {e}")
            
    # Guardar en archivo JSON para que la Terminal Web lo lea
    with open(DATA_FILE, 'w') as f:
        json.dump(radar_data, f, indent=4)

if __name__ == "__main__":
    print("========================================")
    print("========================================")
    print("🤖 SNIPER BOT v4 (MACD/SQUEEZE) INICIADO")
    print(f"Monedas: {', '.join(SYMBOLS)}")
    print("========================================")
    print("[INFO] Notificaciones OS Reactivadas (Afinadas con filtro MACD/Squeeze)")
    
    while True:
        check_sniper_cross()
        time.sleep(CHECK_INTERVAL_SECONDS)
