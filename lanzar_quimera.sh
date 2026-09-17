#!/bin/bash
echo "Iniciando Servidor Web Local en puerto 8000..."
# Iniciar servidor silenciosamente en segundo plano
python3 -m http.server 8000 > /dev/null 2>&1 &
SERVER_PID=$!

echo "Iniciando Francotirador (Sniper Bot v2)..."
# Iniciar el bot en segundo plano
python3 sniper_scanner.py &
BOT_PID=$!

echo ""
echo "========================================================"
echo " 🎯 QUIMERA ALCHEMIST TERMINAL ESTÁ ONLINE"
echo " 🌐 Abre tu navegador web y entra en este enlace:"
echo "    http://localhost:8000/quimera_terminal.html"
echo "========================================================"
echo " El bot está corriendo. Presiona Ctrl+C aquí para apagar todo."
echo ""

# Esperar a que el usuario presione Ctrl+C para matar ambos procesos
trap "echo -e '\nApagando sistemas...'; kill $SERVER_PID; kill $BOT_PID; exit" INT
wait
