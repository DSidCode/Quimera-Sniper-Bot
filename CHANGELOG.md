# CHANGELOG: Quimera Sniper Bot

## [v4.0.0] - Sniper In-App & Afinación Extrema
*Despliegue del panel de control web centralizado y filtros avanzados.*

### Añadido (Backend - Python)
- **Cálculo MACD (12, 26, 9):** Integrado de forma manual utilizando EMAs para medir la dirección del momentum del precio.
- **Detector de Squeeze (Bandas de Bollinger):** Añadido cálculo matemático de Bandas de Bollinger (20 periodos) y su Bandwidth. Detecta estados de compresión extrema (< 1.0%) que preceden explosiones de volatilidad.
- **Log Centralizado en Memoria:** Las notificaciones generadas ya no se pierden en el sistema; el bot almacena un histórico local de las últimas 15 alertas confirmadas para exportarlas en `sniper_data.json`.
- **Filtro Estricto de Notificaciones Nativas:** El sistema operativo solo lanza un pop-up (`notify-send`) si se cumple un escenario perfecto: Cruce Dorado/Bajista + Volumen Validado + Acción de Precio + MACD alineado a favor del cruce.

### Modificado (Frontend - HTML/JS)
- **Panel In-App "Últimas Alertas":** Añadida una nueva sección en la interfaz web de `quimera_terminal.html` para consultar el historial de alertas del bot sin depender de pop-ups del SO.
- **Columna Momentum Condensada:** Se agrupó RSI, Volumen y el nuevo estado del MACD (Alcista/Bajista) en una sola columna para reducir el ruido visual.
- **Indicador Visual de Squeeze:** Si un token entra en zona de alta compresión, se muestra un icono dinámico (💥) al lado de su ticker para señalar riesgo de latigazo de precio.
- **Limpieza de Tokens:** Eliminado el par FET/USDT por no estar soportado en exchanges operados (Quantfury), enfocando recursos en tokens con alta liquidez.

## [v3.0.0] - Triple Filtro (RSI + Vol)
*Implementación de filtros contra lateralizaciones y ruido de mercado.*
- RSI Wilder de 14 periodos.
- SMA de volumen de 20 periodos para descartar cruces con volumen falso.
- Etiquetado de probabilidades basado en la separación (divergencia) de las EMAs rápida y lenta.

## [v6.0] - 2026-09-15
### Añadido
- **Módulo de Multi-Temporalidad (Scanner 3D)**: El bot ahora analiza de manera concurrente `15m`, `30m` y `1h` para cada token, y consolida las alertas por nivel de riesgo.
- **Ratios Riesgo/Beneficio Específicos por TF**:
  - `15m`: TP +2.0%, SL -1.0% (Ratio 2:1)
  - `30m`: TP +3.5%, SL -1.5% (Ratio 2.3:1)
  - `1h`:  TP +5.0%, SL -2.5% (Ratio 2:1)
- **Upgrade de Servidor (Flask)**: Transición del servidor estático `http.server` a un servidor Flask (`server.py`) para permitir interactividad bidireccional en el frontend.
- **Panel Portafolio Real (LIVE)**:
  - Nueva sección visual separada del Forward Testing para registrar y trackear operaciones reales.
  - Interfaz interactiva: Botones `[+ REAL]`, `[🏆 WIN]` y `[💀 LOSS]` integrados directamente en el Dashboard HTML para la gestión manual del portafolio.

### Arreglado
- Corrección de un conflicto en clases de CSS (`status-open`) que sobrescribía los colores del reloj de los mercados (restaurado verde neón `#4ade80`).
- Corrección de indentación en el bucle principal de `sniper_scanner.py` (bloque `try/except`).
- Restauración de variables globales de configuración (`CHECK_INTERVAL_SECONDS`, `DATA_FILE`, `TRADES_FILE`) borradas accidentalmente durante un parcheo.

## [v7.0] - 2026-09-17 (Optimización de Volatilidad y UX)
### Añadido
- **Calculadora de Capital (Gestión de Riesgo):** El bot ahora calcula y sugiere dinámicamente el capital a invertir ($50, $100, $150-$200) según la probabilidad de éxito de la señal.
- **Split de Interfaz (Multi-Page):** Se dividió la Terminal monolítica en dos páginas (`quimera_terminal.html` para operaciones y `radar.html` para el escáner global) para eliminar la fatiga visual.
- **Navegación por Pestañas:** Añadidos filtros por temporalidad (Todas, 15m, 30m, 1h) en el Radar Snipper.
- **Nuevas Columnas de Datos:** Se agregaron columnas de "Capital" y "SL / TP exactos" a las tablas del Forward Testing.

### Modificado (Afinación Estratégica)
- **Expansión de Rango (SL / TP):** Tras analizar el *Forward Testing* (Win Rate: 10%), se detectó asfixia por volatilidad. Se han ensanchado los márgenes para permitir respiración al precio:
  - `15m`: SL 2.0% / TP 4.0%
  - `30m`: SL 3.0% / TP 6.0%
  - `1h`:  SL 4.0% / TP 8.0%
