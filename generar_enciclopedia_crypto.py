import sys
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

def draw_dark_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#121212"))
    canvas.rect(0, 0, doc.width + doc.leftMargin + doc.rightMargin, doc.height + doc.topMargin + doc.bottomMargin, fill=1, stroke=0)
    canvas.restoreState()

def create_pdf(output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=A5, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=28, textColor=colors.HexColor("#FFFFFF"), alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica-Bold")
    h1_style = ParagraphStyle('H1Style', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor("#fca311"), spaceBefore=20, spaceAfter=15, fontName="Helvetica-Bold")
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor("#e0e0e0"), spaceBefore=15, spaceAfter=10, fontName="Helvetica-Bold")
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=12, leading=18, textColor=colors.HexColor("#d0d0d0"), alignment=TA_JUSTIFY, spaceAfter=12)
    highlight_style = ParagraphStyle('HighlightStyle', parent=styles['Normal'], fontSize=12, leading=18, textColor=colors.HexColor("#ffffff"), backColor=colors.HexColor("#1e1e1e"), borderColor=colors.HexColor("#fca311"), borderWidth=1, borderPadding=10, alignment=TA_JUSTIFY, spaceBefore=15, spaceAfter=20)

    Story = []

    # Portada
    Story.append(Spacer(1, 100))
    Story.append(Paragraph("Enciclopedia de Fundamentales Cripto", title_style))
    Story.append(Paragraph("Análisis profundo de 12 gigantes tecnológicos", ParagraphStyle('Sub', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor("#a0a0a0"), fontSize=14)))
    Story.append(Spacer(1, 50))
    Story.append(Paragraph("Edición 2026 - Optimizado para Lectura Móvil", ParagraphStyle('Sub2', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor("#666666"))))
    Story.append(PageBreak())

    # Datos de las monedas
    monedas = [
        {
            "nombre": "SUI (Sui Network)",
            "color": "#4A90E2",
            "historia": "Desarrollada por Mysten Labs (ex-ingenieros de Meta/Facebook que trabajaron en el proyecto Libra/Diem). Nace con la premisa de solucionar los cuellos de botella de las blockchains tradicionales mediante un enfoque totalmente nuevo en la estructura de datos.",
            "tecnologia": "A diferencia de Ethereum o Solana, Sui no procesa las transacciones en bloques secuenciales para todo. Utiliza un modelo 'orientado a objetos'. Si dos transacciones no están relacionadas (ej. tú envías tokens a tu amigo y yo minteo un NFT), Sui las procesa en paralelo casi instantáneamente sin necesidad de consenso global. Utiliza el lenguaje de programación 'Move', diseñado para máxima seguridad en contratos inteligentes.",
            "propuesta": "Escalabilidad horizontal infinita. Sui busca ser la infraestructura principal para los juegos Web3 (GameFi) y las finanzas descentralizadas de altísima frecuencia, donde se necesitan cientos de miles de transacciones por segundo (TPS) con latencia de milisegundos.",
            "catalizadores": "Sui se ha posicionado como el 'Asesino de Solana' en términos de arquitectura. La adopción por parte de estudios de videojuegos coreanos y japoneses ha impulsado su TVL masivamente. Su narrativa principal en 2026 es la ejecución paralela determinista."
        },
        {
            "nombre": "RENDER (Render Network)",
            "color": "#D32F2F",
            "historia": "Fundado por Jules Urbach (CEO de OTOY, empresa líder en software de renderizado de Hollywood). Nace para democratizar el poder de procesamiento gráfico (GPU).",
            "tecnologia": "Render es un mercado descentralizado de GPUs. Si tienes una tarjeta gráfica potente ociosa, la conectas a la red y cobras en RENDER. Si eres un artista 3D, un estudio de animación o un investigador de IA, pagas en RENDER para usar esa potencia combinada, ahorrando muchísimo frente a usar Amazon Web Services (AWS) o Google Cloud.",
            "propuesta": "Es el 'Airbnb de las tarjetas gráficas'. Soluciona la escasez global de GPUs (chips de Nvidia).",
            "catalizadores": "Con el boom explosivo de la Inteligencia Artificial Generativa (OpenAI, Sora, Midjourney) y el renderizado espacial para gafas como Apple Vision Pro, Render migró a la red Solana para mayor velocidad. Es el proxy número uno de 'Cripto x Inteligencia Artificial x Hardware'."
        },
        {
            "nombre": "TAO (Bittensor)",
            "color": "#9E9E9E",
            "historia": "Nace de la idea de que la Inteligencia Artificial no debe estar monopolizada por mega-corporaciones como Google o Microsoft. Bittensor crea un cerebro global descentralizado.",
            "tecnologia": "Utiliza un modelo de consenso donde los mineros no resuelven puzzles matemáticos inútiles (como Bitcoin), sino que entrenan modelos de machine learning. Las subredes (subnets) compiten para dar la mejor respuesta (texto, audio, imagen, predicción de mercados). Los validadores premian a los mejores modelos con tokens TAO.",
            "propuesta": "Comoditizar la inteligencia artificial. Bittensor permite que cualquier desarrollador acceda a un enjambre de modelos de IA de código abierto, pagando con TAO.",
            "catalizadores": "TAO es el líder absoluto de la narrativa de 'IA Descentralizada'. A medida que la censura y los sesgos en los modelos corporativos (ChatGPT) aumentan, los desarrolladores y fondos de capital huyen hacia el ecosistema sin permisos de Bittensor."
        },
        {
            "nombre": "SOL (Solana)",
            "color": "#9C27B0",
            "historia": "Creada por Anatoly Yakovenko (ex-Qualcomm). Nació para ser el 'Nasdaq en blockchain', priorizando la velocidad y el bajo coste sobre la extrema descentralización.",
            "tecnologia": "Su gran innovación es el 'Proof of History' (PoH), un reloj criptográfico que permite a los nodos verificar el tiempo sin tener que comunicarse constantemente entre sí. Esto, sumado al procesamiento en paralelo (Sealevel), le permite procesar hasta 65,000 transacciones por segundo en una sola capa (arquitectura monolítica), sin necesidad de Layer 2.",
            "propuesta": "Experiencia de usuario perfecta. Transacciones de fracciones de centavo de dólar que se confirman en 400 milisegundos.",
            "catalizadores": "Solana ha resucitado de las cenizas de FTX y ha dominado el volumen de DEX, la emisión de memecoins y las integraciones de pagos (Solana Pay, Shopify, Visa). Su actualización 'Firedancer' (un nuevo cliente de red) elimina históricas caídas de red, acercándola al millón de TPS teóricas."
        },
        {
            "nombre": "AAVE (Aave)",
            "color": "#00BCD4",
            "historia": "Inició en 2017 como ETHLend por Stani Kulechov, y evolucionó a Aave (fantasma en finés) para convertirse en el Banco Central descentralizado de Web3.",
            "tecnologia": "Es un protocolo de liquidez de código abierto (Smart Contracts). Funciona como una piscina comunitaria: unos usuarios depositan fondos y ganan intereses (proveedores de liquidez), otros piden prestado dejando colateral, pagando intereses. Inventaron los 'Flash Loans' (préstamos sin colateral que deben devolverse en el mismo bloque).",
            "propuesta": "Crédito sin confianza ni intermediarios. No hay banco, ni gestor, ni KYC. El código liquida automáticamente si tu colateral pierde valor.",
            "catalizadores": "Aave es el pilar inamovible (Blue Chip) de DeFi. Con el lanzamiento de su propia stablecoin (GHO) y su despliegue en múltiples redes, Aave captura enormes comisiones. A medida que Wall Street explora tokenizar bonos reales (RWA), Aave es la capa de asentamiento lógica para mercados de deuda."
        },
        {
            "nombre": "OP (Optimism)",
            "color": "#F44336",
            "historia": "Nace ante la imposibilidad de Ethereum de escalar (las tarifas de gas eran prohibitivas de cientos de dólares). OP es un Layer 2 (Capa 2) respaldado por la Fundación Ethereum.",
            "tecnologia": "Utiliza 'Optimistic Rollups'. Coge miles de transacciones, las empaqueta fuera de Ethereum (donde es rápido y barato) y envía un recibo final a Ethereum. Asume 'optimistamente' que las transacciones son válidas, dejando una ventana de 7 días para que cualquiera las impugne mediante pruebas de fraude.",
            "propuesta": "Hacer que Ethereum sea barato (céntimos) manteniendo su seguridad extrema.",
            "catalizadores": "Su mayor innovación no es su red, sino el 'OP Stack': una plantilla de código abierto para que cualquiera cree su propia red. Coinbase usó el OP Stack para crear su red 'Base', y Binance para 'opBNB'. Optimism busca conectar todas estas redes en la 'Superchain'."
        },
        {
            "nombre": "ARB (Arbitrum)",
            "color": "#1976D2",
            "historia": "Desarrollado por Offchain Labs. Al igual que Optimism, es una Capa 2 (Optimistic Rollup), pero con una arquitectura tecnológica distinta y un enfoque altamente pragmático.",
            "tecnologia": "Su arquitectura Nitro compila el código central de Geth (Ethereum) en WebAssembly, lo que lo hace increíblemente rápido. Su mecanismo de resolución de disputas es interactivo y multi-ronda, siendo más eficiente a nivel computacional que OP.",
            "propuesta": "Arbitrum no vende una visión utópica como OP (Superchain), vende tracción brutal. Es el L2 líder indiscutible en DeFi, liquidez y volumen institucional.",
            "catalizadores": "Maneja la mayor cantidad de Valor Total Bloqueado (TVL) entre los L2. Ecosistemas nativos como GMX (DEX de perpetuos) atrajeron miles de millones. La narrativa se basa en métricas frías: es donde está el dinero y la liquidez de Ethereum."
        },
        {
            "nombre": "UNI (Uniswap)",
            "color": "#E91E63",
            "historia": "Creado por Hayden Adams. Fue el primer exchange descentralizado (DEX) en funcionar de forma masiva y fluida, asesinando a los exchanges centralizados de segunda división.",
            "tecnologia": "Inventó el modelo AMM (Automated Market Maker). No hay libro de órdenes (libro de ofertas de compra y venta). En su lugar, hay piscinas de liquidez (Liquidity Pools) reguladas por una fórmula matemática (x * y = k) que determina el precio automáticamente según la demanda.",
            "propuesta": "Intercambio de activos instantáneo, sin permisos y resistente a la censura. Cualquier token de la red Ethereum puede ser listado inmediatamente sin pedir permiso a un CEO.",
            "catalizadores": "Con la llegada de Uniswap v4 y los 'Hooks' (fragmentos de código personalizables para las pools), Uniswap se ha convertido en una plataforma para desarrolladores financieros. Además, las presiones regulatorias (SEC) han reforzado su narrativa como el protocolo más descentralizado e inatacable."
        },
        {
            "nombre": "RUNE (THORChain)",
            "color": "#00E676",
            "historia": "Nació para solucionar la gran muralla entre ecosistemas. Históricamente, no podías cambiar Bitcoin real por Ethereum real de forma descentralizada. Tenías que usar Binance o usar 'Wrapped Tokens' (WBTC), que dependen de un custodio central.",
            "tecnologia": "THORChain es un AMM cross-chain. La red tiene bóvedas descentralizadas controladas por nodos anónimos que observan las cadenas externas. Cuando envías Bitcoin, los nodos lo detectan y te envían el equivalente en ETH real. El token RUNE empareja todos los activos en las piscinas de liquidez (BTC/RUNE, ETH/RUNE).",
            "propuesta": "El Santo Grial de DeFi: liquidez nativa entre cadenas sin puentes (bridges) vulnerables ni custodios centralizados.",
            "catalizadores": "A medida que los hackeos a 'Bridges' tradicionales continúan, el modelo sin envolturas de THORChain es la única alternativa institucional. Además, su modelo económico genera que a mayor TVL, más RUNE debe ser bloqueado y quemado, creando un ciclo alcista estructural."
        },
        {
            "nombre": "DOGE (Dogecoin)",
            "color": "#FFC107",
            "historia": "Creado en 2013 como una broma por Jackson Palmer y Billy Markus para reírse de la especulación de las criptomonedas. Irónicamente, sobrevivió a miles de proyectos 'serios'.",
            "tecnologia": "Es un clon (fork) del código fuente de Litecoin (que a su vez es un fork de Bitcoin). Utiliza Proof of Work. Curiosamente, se mina de forma combinada ('merged mining') con Litecoin, lo que significa que su red es extremadamente segura por el hardware que la respalda.",
            "propuesta": "Dinero de Internet sin pretensiones tecnológicas. Su valor real reside en el efecto Lindy (supervivencia), el reconocimiento de marca universal y el marketing orgánico liderado por figuras como Elon Musk.",
            "catalizadores": "Aunque carece de contratos inteligentes avanzados, su adopción como medio de pago en infraestructuras comerciales (merchandising de Tesla/SpaceX, posibles integraciones en redes sociales (X)) y su naturaleza desinflacionaria fija y predecible la han cimentado como un activo 'Blue Chip' del retail."
        },
        {
            "nombre": "LINK (Chainlink)",
            "color": "#2196F3",
            "historia": "Fundado por Sergey Nazarov. Resolvió el 'Problema del Oráculo'. Los contratos inteligentes en blockchain son ciegos; no pueden consultar Google para ver a cuánto cotiza Apple o qué clima hace hoy.",
            "tecnologia": "Chainlink es una red de oráculos descentralizados. Los nodos extraen datos del mundo exterior, llegan a un consenso sobre la veracidad del dato y lo inyectan en la blockchain para que los contratos (como AAVE) puedan funcionar.",
            "propuesta": "Conectar el mundo real con la blockchain de forma segura e incorruptible.",
            "catalizadores": "La gran narrativa de la década (2025-2030) es la 'Tokenización de RWA' (Activos del Mundo Real: bonos, bienes raíces, acciones). Los fondos como BlackRock necesitan oráculos para mantener actualizados los precios de estos activos on-chain. Además, su protocolo CCIP se ha convertido en el TCP/IP estándar para que los bancos tradicionales se conecten con cualquier blockchain."
        },
        {
            "nombre": "THETA (Theta Network)",
            "color": "#009688",
            "historia": "Asesorado por los cofundadores de YouTube y Twitch. Nace para solucionar los astronómicos costes de CDN (Content Delivery Network) del streaming de video en calidad 4K/8K y VR.",
            "tecnologia": "Red descentralizada de entrega de video (Edge Network). Si estás viendo un directo, tu ordenador comparte tu ancho de banda sobrante a los vecinos de tu bloque que están viendo lo mismo, a cambio, ganas tokens TFUEL. Esto descarga drásticamente la congestión de los servidores centrales.",
            "propuesta": "Reducir costes de infraestructura de vídeo para plataformas y democratizar el streaming de la Web3 (Edge Computing).",
            "catalizadores": "Con su evolución a 'Theta EdgeCloud', combinaron la infraestructura de vídeo con el cómputo de Inteligencia Artificial (similar a Render). Las patentes obtenidas y las asociaciones corporativas pesadas la mantienen relevante en la narrativa de Infraestructura Descentralizada Física (DePIN)."
        }
    ]

    for moneda in monedas:
        h1 = ParagraphStyle('H1', parent=h1_style, textColor=colors.HexColor(moneda['color']))
        hl = ParagraphStyle('HL', parent=highlight_style, borderColor=colors.HexColor(moneda['color']))
        
        Story.append(Paragraph(moneda['nombre'], h1))
        
        Story.append(Paragraph("Historia y Origen", h2_style))
        Story.append(Paragraph(moneda['historia'], body_style))
        
        Story.append(Paragraph("Tecnología Subyacente", h2_style))
        Story.append(Paragraph(moneda['tecnologia'], body_style))
        
        Story.append(Paragraph("Propuesta de Valor Core", h2_style))
        Story.append(Paragraph(moneda['propuesta'], body_style))
        
        Story.append(Paragraph("Catalizadores Macro y Narrativa Actual", h2_style))
        Story.append(Paragraph(f"<b>Contexto Estratégico:</b> {moneda['catalizadores']}", hl))
        
        Story.append(PageBreak())

    doc.build(Story, onFirstPage=draw_dark_background, onLaterPages=draw_dark_background)

if __name__ == "__main__":
    create_pdf("enciclopedia_crypto_2026.pdf")
