import urllib.request
import json
import time

coins = ['bitcoin', 'ethereum', 'solana']
url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    
    print("\n=== RESUMEN MERCADO CRIPTO (24H) ===")
    for coin in coins:
        if coin in data:
            price = data[coin]['usd']
            change = data[coin]['usd_24h_change']
            vol = data[coin]['usd_24h_vol']
            trend = "🟢 SUBIENDO" if change > 0 else "🔴 BAJANDO"
            print(f"{coin.upper()}:")
            print(f"  Precio: ${price:,.2f}")
            print(f"  Cambio 24h: {change:+.2f}% {trend}")
            print(f"  Volumen 24h: ${vol:,.0f}")
            print("-" * 30)
except Exception as e:
    print("Error consultando CoinGecko:", e)
