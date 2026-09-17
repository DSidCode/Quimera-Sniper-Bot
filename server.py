import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

REAL_TRADES_FILE = "real_trades.json"

def load_real_trades():
    if os.path.exists(REAL_TRADES_FILE):
        try:
            with open(REAL_TRADES_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"open_trades": [], "closed_trades": [], "stats": {"total": 0, "wins": 0, "losses": 0, "win_rate": 0.0}}

def save_real_trades(data):
    with open(REAL_TRADES_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return send_from_directory('.', 'quimera_terminal.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

@app.route('/api/add_real_trade', methods=['POST'])
def add_real_trade():
    req = request.json
    if not req:
        return jsonify({"error": "No data"}), 400
        
    trades = load_real_trades()
    
    clean_symbol = req.get('symbol', '').replace('/USDT', '')
    for t in trades['open_trades']:
        if t['symbol'] == clean_symbol and t.get('direction') == req.get('direction'):
            return jsonify({"error": "Trade already open"}), 400
            
    now_str = datetime.now().strftime('%H:%M:%S')
    
    trade_obj = {
        "symbol": clean_symbol,
        "direction": req.get('direction', 'LONG'),
        "entry_price": float(req.get('entry_price', 0.0)),
        "entry_time": now_str,
        "timeframe": req.get('timeframe', '15m'),
        "take_profit": float(req.get('take_profit', 0.0)),
        "stop_loss": float(req.get('stop_loss', 0.0)),
        "status": "OPEN"
    }
    
    trades['open_trades'].append(trade_obj)
    save_real_trades(trades)
    
    return jsonify({"success": True, "trade": trade_obj})

@app.route('/api/close_real_trade', methods=['POST'])
def close_real_trade():
    req = request.json
    if not req:
        return jsonify({"error": "No data"}), 400
        
    symbol = req.get('symbol')
    direction = req.get('direction')
    result = req.get('result', 'WIN') # WIN or LOSS
    exit_price = float(req.get('exit_price', 0.0))
    
    trades = load_real_trades()
    open_idx = -1
    for i, t in enumerate(trades['open_trades']):
        if t['symbol'] == symbol and t['direction'] == direction:
            open_idx = i
            break
            
    if open_idx == -1:
        return jsonify({"error": "Trade not found in open trades"}), 404
        
    t = trades['open_trades'].pop(open_idx)
    t['status'] = result
    t['exit_price'] = exit_price
    t['exit_time'] = datetime.now().strftime('%d/%m %H:%M:%S')
    
    trades['stats']['total'] += 1
    if result == 'WIN':
        trades['stats']['wins'] += 1
    else:
        trades['stats']['losses'] += 1
        
    trades['stats']['win_rate'] = round((trades['stats']['wins'] / trades['stats']['total']) * 100, 1)
    
    trades['closed_trades'].insert(0, t)
    if len(trades['closed_trades']) > 20:
        trades['closed_trades'] = trades['closed_trades'][:20]
    
    save_real_trades(trades)
    return jsonify({"success": True})


if __name__ == '__main__':
    if not os.path.exists(REAL_TRADES_FILE):
        save_real_trades({"open_trades": [], "closed_trades": [], "stats": {"total": 0, "wins": 0, "losses": 0, "win_rate": 0.0}})
        
    print("Iniciando Flask Server en puerto 8000...")
    app.run(host='0.0.0.0', port=8000, debug=False)
