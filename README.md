# 🎯 Quimera Sniper Bot

**Bot algorítmico de Trading de Alta Frecuencia (HFT) y Escáner 3D Multi-Temporalidad para el mercado de Criptomonedas.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

## 📌 Visión General
Quimera Sniper Bot es una herramienta de análisis cuantitativo diseñada para detectar oportunidades de trading en tiempo real ("sniping") basándose en la convergencia de indicadores técnicos clave (MACD, RSI, Bandas de Bollinger y Volumen). Incorpora un panel de control interactivo (Web UI) para monitorización y gestión de capital.

## 🚀 Características Principales (Core Features)

- **Escáner 3D Multi-Temporalidad:** Analiza simultáneamente los mercados en intervalos de `15m`, `30m` y `1h` para confirmar tendencias sólidas antes de alertar.
- **Detección de "Squeeze" (Bollinger Bands):** Cálculo matemático de la compresión de las bandas (< 1.0% Bandwidth) para anticipar explosiones de volatilidad.
- **Triple Filtro de Señales:** Las alertas solo se disparan ante el cruce perfecto de EMAs + RSI + SMA de Volumen + MACD alineado, filtrando ruido lateral.
- **Gestión de Riesgo Dinámica:** Calculadora integrada que sugiere la inversión de capital ($50, $100, $150-$200) y calcula el Stop Loss (SL) y Take Profit (TP) exactos basado en el Win Rate del Forward Testing.
- **Servidor Flask (Backend):** Gestión asíncrona y orquestación de la captura de datos del exchange (Binance API).
- **Dashboard UI Interactiva:** Terminal de comandos frontend con división de pantallas (`Radar` y `Terminal`) para eliminar la fatiga visual.

## 🛠️ Stack Tecnológico
- **Backend:** Python, Flask, librería CCXT (para interacción con la API de Binance).
- **Frontend:** HTML5, CSS3, JavaScript Vainilla (Fetch API).
- **Datos:** Gestión de estado en memoria y persistencia local (`.json`).
- **Sistema:** Notificaciones nativas (`notify-send`) en entornos Linux.

## ⚙️ Estructura del Proyecto
- `sniper_scanner.py`: Motor de lógica, análisis técnico (indicadores) y orquestación.
- `server.py`: Servidor Flask para comunicación asíncrona con el frontend.
- `quimera_terminal.html` / `radar.html`: Interfaz de usuario (Dashboard).

---
*Desarrollado como proyecto de investigación y demostración técnica End-to-End. Los datos de portafolio y claves de ejecución real se mantienen privados mediante .gitignore.*
