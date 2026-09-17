with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/quimera_terminal.html', 'r') as f:
    html = f.read()

# 1. Update Sniper Table Headers
html = html.replace("<th>TOKEN</th>", "<th>TOKEN</th><th>TF</th>")

# 2. Update Sniper Table Rows
row_patch = """                            <td data-label="Token" style="font-weight: 800; font-size: 1.1em;">${coin.symbol} ${squeezeHtml}</td>
                            <td data-label="TF" style="color: #4ade80; font-family: var(--font-mono); font-weight: bold;">${coin.timeframe}</td>"""
html = html.replace("""                            <td data-label="Token" style="font-weight: 800; font-size: 1.1em;">${coin.symbol} ${squeezeHtml}</td>""", row_patch)

# 3. Update Alerts display
alert_patch = """                        <div class="alert-item">
                            <span class="alert-time">${a.time} <br><span style="color:#4ade80; font-size: 0.8em">${a.timeframe}</span></span>"""
html = html.replace("""                        <div class="alert-item">
                            <span class="alert-time">${a.time}</span>""", alert_patch)

# 4. Update Forward Testing Open Trades Table Headers
html = html.replace("<th>Token</th><th>Dir</th><th>Entrada</th>", "<th>Token</th><th>TF</th><th>Dir</th><th>Entrada</th>")

# 5. Update Forward Testing Open Trades Rows
open_row_patch = """                        <tr style="background: rgba(250,204,21,0.05)">
                            <td style="font-weight:bold">${t.symbol}</td>
                            <td style="color: #4ade80; font-family: var(--font-mono); font-weight: bold;">${t.timeframe}</td>"""
html = html.replace("""                        <tr style="background: rgba(250,204,21,0.05)">
                            <td style="font-weight:bold">${t.symbol}</td>""", open_row_patch)
html = html.replace('<td colspan="7">No hay operaciones', '<td colspan="8">No hay operaciones')

# 6. Update Forward Testing Closed Trades Table Headers
html = html.replace("<th>Token</th><th>Dir</th><th>Entrada</th><th>Salida</th>", "<th>Token</th><th>TF</th><th>Dir</th><th>Entrada</th><th>Salida</th>")

# 7. Update Forward Testing Closed Trades Rows
closed_row_patch = """                        <tr>
                            <td style="font-weight:bold">${t.symbol}</td>
                            <td style="color: #4ade80; font-family: var(--font-mono); font-weight: bold;">${t.timeframe}</td>"""
html = html.replace("""                        <tr>
                            <td style="font-weight:bold">${t.symbol}</td>""", closed_row_patch)
html = html.replace('<td colspan="6" style="text-align:center; color:gray">No hay', '<td colspan="7" style="text-align:center; color:gray">No hay')

with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/quimera_terminal.html', 'w') as f:
    f.write(html)

print("HTML multi-timeframe patch applied.")
