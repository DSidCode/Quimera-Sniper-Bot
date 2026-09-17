with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/quimera_terminal.html', 'r') as f:
    html = f.read()

# 1. Add Forward Testing CSS
css_patch = """
        /* --- FORWARD TESTING SECTION --- */
        .ft-section {
            background: rgba(74, 222, 128, 0.05);
            border: 1px solid rgba(74, 222, 128, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 40px;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.8);
        }
        .ft-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .winrate-display { font-size: 2.5rem; font-family: var(--font-mono); font-weight: 800; color: var(--accent-green); text-shadow: 0 0 15px rgba(74, 222, 128, 0.5); }
        .stats-summary { font-size: 0.9rem; color: var(--text-secondary); text-align: right; }
        .ft-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.85rem;}
        .ft-table th, .ft-table td { padding: 8px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .ft-table th { color: var(--text-secondary); font-size: 0.7rem; text-transform: uppercase; }
        .status-win { color: var(--accent-green); font-weight: bold; }
        .status-loss { color: var(--accent-red); font-weight: bold; }
        .status-open { color: var(--accent-yellow); font-weight: bold; }

        @media (max-width: 768px) {
"""
html = html.replace("        @media (max-width: 768px) {", css_patch)

# 2. Add Forward Testing HTML Section after Alerts
html_patch = """
            <!-- FORWARD TESTING (PAPER TRADING) MODULE -->
            <div class="ft-section">
                <div class="ft-header">
                    <div class="sniper-title" style="color: var(--accent-green);">
                        🎯 FORWARD TESTING (SIMULADOR PnL)
                    </div>
                    <div style="display: flex; gap: 20px; align-items: center;">
                        <div class="stats-summary" id="ft-stats-summary">Cargando...</div>
                        <div class="winrate-display" id="ft-winrate">--%</div>
                    </div>
                </div>
                
                <h4 style="color: var(--text-secondary); margin-bottom: 10px; font-size: 0.85rem; text-transform: uppercase;">Operaciones Abiertas</h4>
                <table class="ft-table" style="margin-bottom: 20px;">
                    <thead><tr><th>Token</th><th>Dir</th><th>Entrada</th><th>Hora</th><th>TP</th><th>SL</th><th>Estado</th></tr></thead>
                    <tbody id="ft-open-body"><tr><td colspan="7">No hay operaciones abiertas.</td></tr></tbody>
                </table>

                <h4 style="color: var(--text-secondary); margin-bottom: 10px; font-size: 0.85rem; text-transform: uppercase;">Historial Cerrado</h4>
                <div style="max-height: 200px; overflow-y: auto;">
                    <table class="ft-table">
                        <thead><tr><th>Token</th><th>Dir</th><th>Entrada</th><th>Salida</th><th>Hora</th><th>Resultado</th></tr></thead>
                        <tbody id="ft-closed-body"><tr><td colspan="6">No hay operaciones cerradas.</td></tr></tbody>
                    </table>
                </div>
            </div>

            <!-- DATA CARDS (RELOJES DE LOS MERCADOS) -->
"""
html = html.replace("            <!-- DATA CARDS (RELOJES DE LOS MERCADOS) -->", html_patch)

# 3. Add logic to fetch sniper_trades.json
js_patch = """
        // --- LOGIC FOR FORWARD TESTING ---
        async function fetchTradesData() {
            try {
                const response = await fetch('sniper_trades.json?t=' + new Date().getTime());
                if (!response.ok) return;
                const data = await response.json();
                
                document.getElementById('ft-winrate').textContent = `${data.stats.win_rate}%`;
                document.getElementById('ft-stats-summary').innerHTML = `WIN: <span style="color:#4ade80">${data.stats.wins}</span> | LOSS: <span style="color:#ef4444">${data.stats.losses}</span><br>TOTAL: ${data.stats.total}`;
                
                const openBody = document.getElementById('ft-open-body');
                if (data.open_trades.length > 0) {
                    openBody.innerHTML = data.open_trades.map(t => `
                        <tr style="background: rgba(250,204,21,0.05)">
                            <td style="font-weight:bold">${t.symbol}</td>
                            <td style="color:${t.direction==='LONG'?'#4ade80':'#ef4444'}">${t.direction}</td>
                            <td class="time-cell">$${t.entry_price}</td>
                            <td class="time-cell">${t.entry_time}</td>
                            <td style="color:#4ade80">$${t.take_profit}</td>
                            <td style="color:#ef4444">$${t.stop_loss}</td>
                            <td class="status-open">OPEN</td>
                        </tr>
                    `).join('');
                } else {
                    openBody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:gray">No hay operaciones abiertas.</td></tr>';
                }
                
                const closedBody = document.getElementById('ft-closed-body');
                if (data.closed_trades.length > 0) {
                    closedBody.innerHTML = data.closed_trades.map(t => `
                        <tr>
                            <td style="font-weight:bold">${t.symbol}</td>
                            <td style="color:${t.direction==='LONG'?'#4ade80':'#ef4444'}">${t.direction}</td>
                            <td class="time-cell">$${t.entry_price}</td>
                            <td class="time-cell">$${t.exit_price}</td>
                            <td class="time-cell">${t.exit_time}</td>
                            <td class="${t.status === 'WIN' ? 'status-win' : 'status-loss'}">${t.status}</td>
                        </tr>
                    `).join('');
                } else {
                    closedBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:gray">No hay operaciones cerradas.</td></tr>';
                }
            } catch (error) {
                // Posiblemente no exista el archivo aun
            }
        }

        // INIT
"""
html = html.replace("        // INIT", js_patch)

js_patch2 = """        fetchSniperData(); // Fetch immediate
        fetchTradesData(); // Fetch immediate
        
        // LOOPS
        setInterval(updateDashboard, 1000);
        setInterval(fetchSniperData, 2000); // Fetch sniper data every 2 seconds
        setInterval(fetchTradesData, 2000); // Fetch trades data every 2 seconds"""
html = html.replace("""        fetchSniperData(); // Fetch immediate
        
        // LOOPS
        setInterval(updateDashboard, 1000);
        setInterval(fetchSniperData, 2000); // Fetch sniper data every 2 seconds""", js_patch2)

with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/quimera_terminal.html', 'w') as f:
    f.write(html)

print("HTML Patch applied.")
