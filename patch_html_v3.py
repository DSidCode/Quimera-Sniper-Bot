with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/quimera_terminal.html', 'r') as f:
    html = f.read()

# 1. Add API functions at the beginning of the script tag
api_funcs = """        // --- API FUNCTIONS FOR REAL TRADES ---
        async function addRealTrade(symbol, direction, entry_price, timeframe, tp, sl) {
            try {
                let res = await fetch('/api/add_real_trade', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        symbol: symbol, direction: direction, entry_price: entry_price, 
                        timeframe: timeframe, take_profit: tp, stop_loss: sl
                    })
                });
                let data = await res.json();
                if(data.success) {
                    alert('✅ Trade añadido al Portafolio Real');
                } else {
                    alert('❌ Error: ' + data.error);
                }
            } catch(e) {
                alert('Error de conexión con el servidor local');
            }
        }
        
        async function closeRealTrade(symbol, direction, result, exit_price) {
            try {
                let res = await fetch('/api/close_real_trade', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        symbol: symbol, direction: direction, result: result, exit_price: exit_price
                    })
                });
                let data = await res.json();
                if(data.success) {
                    alert('✅ Trade cerrado en el Portafolio Real');
                } else {
                    alert('❌ Error: ' + data.error);
                }
            } catch(e) {
                alert('Error de conexión con el servidor local');
            }
        }
        
        async function fetchData() {"""
html = html.replace("        async function fetchData() {", api_funcs)

# 2. Add Add to Real Trade button in Radar Alerts
radar_btn_patch = """                        <div class="alert-item">
                            <span class="alert-time">${a.time} <br><span style="color:#4ade80; font-size: 0.8em">${a.timeframe}</span></span>
                            <div class="alert-content">
                                <span class="alert-symbol">${a.symbol} <span style="font-size: 0.6em; color:gray">$${a.price}</span></span>
                                <span class="alert-msg">${a.message}</span>
                            </div>
                            <button onclick="addRealTrade('${a.symbol}', '${a.message.includes('Alcista') ? 'LONG' : 'SHORT'}', ${a.price}, '${a.timeframe}', ${a.message.includes('Alcista') ? a.price * 1.02 : a.price * 0.98}, ${a.message.includes('Alcista') ? a.price * 0.99 : a.price * 1.01})" style="background:var(--accent-green); color:#000; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:0.7rem; font-weight:bold; margin-left:10px;">+ REAL</button>
                        </div>"""
html = html.replace("""                        <div class="alert-item">
                            <span class="alert-time">${a.time} <br><span style="color:#4ade80; font-size: 0.8em">${a.timeframe}</span></span>
                            <div class="alert-content">
                                <span class="alert-symbol">${a.symbol} <span style="font-size: 0.6em; color:gray">$${a.price}</span></span>
                                <span class="alert-msg">${a.message}</span>
                            </div>
                        </div>""", radar_btn_patch)


# 3. Add fetching for real trades
fetch_real = """                // Fetch Real Trades
                try {
                    let resReal = await fetch('real_trades.json?t=' + Date.now());
                    if(resReal.ok) {
                        let realData = await resReal.json();
                        renderRealTrades(realData);
                    }
                } catch(e) { console.log('Sin real_trades.json aún'); }"""
html = html.replace("setTimeout(fetchData, 2000);", fetch_real + "\n            setTimeout(fetchData, 2000);")


# 4. Add Render Real Trades function
render_real_func = """        function renderRealTrades(data) {
            const openBody = document.getElementById('rt-open-body');
            const closedBody = document.getElementById('rt-closed-body');
            const wrSpan = document.getElementById('rt-wr');
            
            if (data.stats) {
                wrSpan.textContent = data.stats.win_rate + '%';
                wrSpan.style.color = data.stats.win_rate >= 50 ? 'var(--accent-green)' : 'var(--accent-red)';
            }
            
            if (data.open_trades && data.open_trades.length > 0) {
                openBody.innerHTML = data.open_trades.map(t => `
                    <tr style="background: rgba(168,85,247,0.05)">
                        <td style="font-weight:bold">${t.symbol}</td>
                        <td style="color: #a855f7; font-family: var(--font-mono); font-weight: bold;">${t.timeframe}</td>
                        <td style="color:${t.direction==='LONG'?'#4ade80':'#ef4444'}">${t.direction}</td>
                        <td class="time-cell">$${t.entry_price}</td>
                        <td class="time-cell">${t.entry_time}</td>
                        <td style="color:#4ade80">$${t.take_profit}</td>
                        <td style="color:#ef4444">$${t.stop_loss}</td>
                        <td>
                            <button onclick="closeRealTrade('${t.symbol}', '${t.direction}', 'WIN', prompt('Precio de Salida (WIN):', ${t.take_profit}))" style="background:var(--accent-green); color:#000; border:none; padding:2px 6px; border-radius:3px; cursor:pointer; font-size:0.7rem; font-weight:bold;">🏆 WIN</button>
                            <button onclick="closeRealTrade('${t.symbol}', '${t.direction}', 'LOSS', prompt('Precio de Salida (LOSS):', ${t.stop_loss}))" style="background:var(--accent-red); color:#000; border:none; padding:2px 6px; border-radius:3px; cursor:pointer; font-size:0.7rem; font-weight:bold;">💀 LOSS</button>
                        </td>
                    </tr>
                `).join('');
            } else {
                openBody.innerHTML = '<tr><td colspan="8" style="text-align:center; color:gray">No hay operaciones reales abiertas.</td></tr>';
            }
            
            if (data.closed_trades && data.closed_trades.length > 0) {
                closedBody.innerHTML = data.closed_trades.map(t => `
                    <tr>
                        <td style="font-weight:bold">${t.symbol}</td>
                        <td style="color: #a855f7; font-family: var(--font-mono); font-weight: bold;">${t.timeframe}</td>
                        <td style="color:${t.direction==='LONG'?'#4ade80':'#ef4444'}">${t.direction}</td>
                        <td class="time-cell">$${t.entry_price}</td>
                        <td class="time-cell">$${t.exit_price || t.take_profit}</td>
                        <td class="time-cell">${t.exit_time || '-'}</td>
                        <td class="${t.status === 'WIN' ? 'status-win' : 'status-loss'}">${t.status}</td>
                    </tr>
                `).join('');
            } else {
                closedBody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:gray">No hay operaciones reales cerradas.</td></tr>';
            }
        }"""
html = html.replace("        // Iniciar reloj global", render_real_func + "\n        // Iniciar reloj global")


# 5. Add RT panel to HTML body
rt_panel = """
            <div class="panel">
                <div class="panel-header">
                    <h2>🟣 PORTAFOLIO REAL (LIVE)</h2>
                    <div style="font-size: 1.2rem; font-weight: 800;" id="rt-wr">- - %</div>
                </div>
                
                <h3 style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 15px;">OPERACIONES ABIERTAS</h3>
                <table class="ft-table">
                    <thead>
                        <tr>
                            <th>Token</th>
                            <th>TF</th>
                            <th>Dir</th>
                            <th>Entrada</th>
                            <th>Hora</th>
                            <th>TP</th>
                            <th>SL</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody id="rt-open-body">
                        <tr><td colspan="8" style="text-align:center; color:gray">Cargando...</td></tr>
                    </tbody>
                </table>

                <h3 style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 25px;">HISTORIAL CERRADO</h3>
                <table class="ft-table">
                    <thead>
                        <tr>
                            <th>Token</th>
                            <th>TF</th>
                            <th>Dir</th>
                            <th>Entrada</th>
                            <th>Salida</th>
                            <th>Hora</th>
                            <th>Resultado</th>
                        </tr>
                    </thead>
                    <tbody id="rt-closed-body">
                        <tr><td colspan="7" style="text-align:center; color:gray">Cargando...</td></tr>
                    </tbody>
                </table>
            </div>"""
html = html.replace('<!-- FIN MÓDULO FORWARD TESTING -->', '<!-- FIN MÓDULO FORWARD TESTING -->' + rt_panel)

# Update layout grid to fit the new panel properly (e.g. 1fr 1fr or full width below)
html = html.replace('grid-template-columns: 2fr 1fr;', 'grid-template-columns: 2fr 1.5fr;')

with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/quimera_terminal.html', 'w') as f:
    f.write(html)
print("Patch applied")
