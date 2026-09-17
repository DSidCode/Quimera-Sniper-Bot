import re

with open('quimera_terminal.html', 'r', encoding='utf-8') as f:
    q_content = f.read()

# Replace the sniper-section in quimera_terminal with a link
nav_link = '''
            <div class="sniper-section" style="text-align: center; padding: 30px;">
                <h3 style="margin-bottom: 15px; color: var(--accent-blue);">🔍 RADAR DE MONEDAS</h3>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">El escáner de todas las temporalidades ahora se ejecuta en una ventana independiente para mayor comodidad.</p>
                <a href="radar.html" target="_blank" style="display: inline-block; padding: 15px 30px; background: rgba(0, 229, 255, 0.2); border: 2px solid var(--accent-blue); border-radius: 10px; color: #fff; text-decoration: none; font-weight: bold; font-size: 1.1rem; transition: all 0.3s ease; box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);">🚀 ABRIR RADAR EN NUEVA PESTAÑA</a>
            </div>
'''
q_modified = re.sub(r'<!-- SNIPER RADAR MODULE -->.*?<!-- ALERTAS RECIENTES MODULE -->', f'<!-- NAV TO RADAR -->\n{nav_link}\n\n            <!-- ALERTAS RECIENTES MODULE -->', q_content, flags=re.DOTALL)

with open('quimera_terminal.html', 'w', encoding='utf-8') as f:
    f.write(q_modified)

# For radar.html, we remove everything except the radar
with open('radar.html', 'r', encoding='utf-8') as f:
    r_content = f.read()

# Remove Forward Testing, Alertas, Data Cards, Heatmap
r_modified = re.sub(r'<!-- ALERTAS RECIENTES MODULE -->.*?(?=<script>)', '', r_content, flags=re.DOTALL)

# Add a back button to radar.html header
back_link = '<a href="quimera_terminal.html" style="color: var(--accent-blue); text-decoration: none; font-size: 0.9rem;">⬅ Volver a Terminal</a>'
r_modified = r_modified.replace('<div class="app-title">QUIMERA SNIPER TERMINAL</div>', f'<div class="app-title">QUIMERA SNIPER RADAR</div>\n            <div style="text-align: center; margin-bottom: 20px;">{back_link}</div>')

with open('radar.html', 'w', encoding='utf-8') as f:
    f.write(r_modified)

print("HTMLs split successfully.")
