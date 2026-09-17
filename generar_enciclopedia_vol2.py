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
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor("#FFFFFF"), alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica-Bold")
    h1_style = ParagraphStyle('H1Style', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor("#4ade80"), spaceBefore=20, spaceAfter=15, fontName="Helvetica-Bold")
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor("#facc15"), spaceBefore=15, spaceAfter=10, fontName="Helvetica-Bold")
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=12, leading=18, textColor=colors.HexColor("#d0d0d0"), alignment=TA_JUSTIFY, spaceAfter=12)
    highlight_style = ParagraphStyle('HighlightStyle', parent=styles['Normal'], fontSize=12, leading=18, textColor=colors.HexColor("#ffffff"), backColor=colors.HexColor("#1e1e1e"), borderColor=colors.HexColor("#4ade80"), borderWidth=1, borderPadding=10, alignment=TA_JUSTIFY, spaceBefore=15, spaceAfter=20)

    Story = []

    # Portada
    Story.append(Spacer(1, 80))
    Story.append(Paragraph("Enciclopedia Crypto - Vol. II", title_style))
    Story.append(Paragraph("Altcoins de Alta Convicción", ParagraphStyle('Sub', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor("#4ade80"), fontSize=16, fontName="Helvetica-Bold")))
    Story.append(Spacer(1, 40))
    Story.append(Paragraph("Investigación fundamental profunda para oportunidades de acumulación (Hold) en el próximo Bull Run.", ParagraphStyle('Sub2', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor("#a0a0a0"))))
    Story.append(Spacer(1, 40))
    Story.append(Paragraph("Edición Septiembre 2026 - Optimizado para Móvil<br/>Operador: Daniel Sid (Sniper)", ParagraphStyle('Sub3', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor("#666666"))))
    Story.append(PageBreak())

    # Datos
    monedas = [
        {
            "nombre": "ONDO Finance (ONDO)",
            "color": "#42a5f5", 
            "problema": "Las finanzas tradicionales (TradFi) y los bonos del tesoro de EE. UU. están bloqueados geográficamente, requieren grandes capitales e intermediarios ineficientes. Los inversores de DeFi necesitan rendimientos estables y seguros frente a la volatilidad cripto.",
            "solucion": "Ondo Finance tokeniza activos del mundo real (RWA), específicamente bonos del Tesoro de EE. UU. a corto plazo y notas corporativas, permitiendo que cualquier persona con una wallet acceda a estos instrumentos financieros institucionales a través de la blockchain.",
            "tokenomics": "<b>Sector:</b> RWA (Tokenización de activos del mundo real).<br/><b>Asociaciones:</b> Trabajan de la mano con gigantes institucionales como BlackRock.<br/><b>Casos de Uso:</b> Gobernanza (Ondo DAO).",
            "oportunidad": "La narrativa de los RWA es una de las más fuertes para el próximo ciclo. Los grandes fondos tradicionales están buscando entrar en cripto, y puentes legales y técnicos como ONDO son su puerta de entrada. Su integración nativa de bonos del tesoro lo convierte en el estándar de oro de DeFi institucional."
        },
        {
            "nombre": "Fetch.ai (FET / ASI)",
            "color": "#10B981", 
            "problema": "La Inteligencia Artificial (IA) actualmente está monopolizada por gigantes tecnológicos (OpenAI, Google, Meta). Estos modelos son cerrados, centralizados y privatizan los beneficios de la automatización global.",
            "solucion": "Fetch.ai crea una red de aprendizaje automático descentralizada. Su tecnología principal son los 'Agentes Económicos Autónomos' (AEA): programas de IA que pueden negociar, aprender y ejecutar tareas (como reservar vuelos, optimizar logística o trading) en nombre de sus dueños, interactuando entre sí en la blockchain.",
            "tokenomics": "<b>Sector:</b> IA / Machine Learning / DePIN.<br/><b>Evolución:</b> Fusión masiva hacia la Super Inteligencia Artificial (ASI).<br/><b>Casos de Uso:</b> Pagar servicios, desplegar agentes y staking.",
            "oportunidad": "El sector de la IA será el mayor catalizador de la década. Fetch.ai es la columna vertebral de la infraestructura de IA descentralizada. Cualquier avance en IA general (AGI) en el mundo TradFi disparará automáticamente la narrativa de monedas como FET (pronto ASI)."
        },
        {
            "nombre": "Kaspa (KAS)",
            "color": "#14B8A6", 
            "problema": "El Trilema de Blockchain (Seguridad, Descentralización, Escalabilidad). Bitcoin es seguro y descentralizado, pero lento. Solana es rápida, pero menos descentralizada.",
            "solucion": "Kaspa es una Proof of Work (PoW) igual que Bitcoin, pero no usa una cadena de bloques lineal. Usa un <b>BlockDAG</b> (Grafo Acíclico Dirigido). Esto permite que se procesen múltiples bloques en paralelo instantáneamente en lugar de tener que esperar en fila.",
            "tokenomics": "<b>Sector:</b> Capa 1 / PoW.<br/><b>Emisión:</b> Lanzamiento justo, sin VCs.<br/><b>Escalabilidad:</b> Bloques por segundo, no por minutos.",
            "oportunidad": "KAS se considera el 'Bitcoin 2.0'. Al no tener VCs, su crecimiento ha sido orgánico. Su tecnología BlockDAG es un salto evolutivo. Acumular KAS en zonas bajas es apostar por la infraestructura de pagos PoW del futuro."
        },
        {
            "nombre": "Injective (INJ)",
            "color": "#3B82F6", 
            "problema": "Los desarrolladores que construyen apps DeFi enfrentan problemas de latencia, altas comisiones y front-running (manipulación de órdenes) en Ethereum y otras L1.",
            "solucion": "Injective es una Layer 1 construida específicamente para el mundo financiero. Viene con módulos financieros pre-construidos (como un libro de órdenes on-chain). Tiene transacciones ultrarrápidas, 0 comisiones de gas y previene el MEV.",
            "tokenomics": "<b>Sector:</b> DeFi / Capa 1.<br/><b>Deflación:</b> Mecanismos de quema masiva de tokens semanalmente.<br/><b>Casos de Uso:</b> Gobernanza, validación, captura de valor.",
            "oportunidad": "La combinación de tecnología especializada para Wall Street descentralizado y su agresiva tokenomics deflacionaria hace que INJ sea una bomba de tiempo alcista. Cada vez que el ecosistema se usa, INJ se vuelve más escaso."
        },
        {
            "nombre": "Filecoin (FIL)",
            "color": "#06B6D4", 
            "problema": "La humanidad está generando más datos que nunca, pero el almacenamiento está controlado por AWS, Google y Microsoft. Esto crea censura, monopolios y puntos únicos de fallo.",
            "solucion": "Filecoin permite a cualquier persona alquilar su espacio de disco duro sobrante. Es el Airbnb del almacenamiento en la nube. Un mercado descentralizado gigantesco donde el almacenamiento es criptográficamente verificado.",
            "tokenomics": "<b>Sector:</b> DePIN / Almacenamiento.<br/><b>Evolución:</b> Han introducido la FVM (Filecoin Virtual Machine) para contratos inteligentes sobre los datos.<br/><b>Casos de Uso:</b> Pagar por almacenamiento y garantías.",
            "oportunidad": "DePIN será una narrativa clave. A medida que la IA necesite bases de datos inmutables y la Web3 necesite servidores que no puedan ser apagados, Filecoin es la capa de infraestructura base indispensable."
        }
    ]

    for moneda in monedas:
        h1 = ParagraphStyle('H1', parent=h1_style, textColor=colors.HexColor(moneda['color']))
        hl = ParagraphStyle('HL', parent=highlight_style, borderColor=colors.HexColor(moneda['color']))
        
        Story.append(Paragraph(moneda['nombre'], h1))
        
        Story.append(Paragraph("El Problema Real", h2_style))
        Story.append(Paragraph(moneda['problema'], body_style))
        
        Story.append(Paragraph("La Solución Tecnológica", h2_style))
        Story.append(Paragraph(moneda['solucion'], body_style))
        
        Story.append(Paragraph("Tokenomics & Fundamentales", h2_style))
        Story.append(Paragraph(moneda['tokenomics'], body_style))
        
        Story.append(Paragraph("Oportunidad de Sniper (Por qué Holdear)", h2_style))
        Story.append(Paragraph(f"<b>Visión Macro:</b> {moneda['oportunidad']}", hl))
        
        Story.append(PageBreak())

    doc.build(Story, onFirstPage=draw_dark_background, onLaterPages=draw_dark_background)

if __name__ == '__main__':
    print("Generando Enciclopedia Crypto Vol 2 (Versión Móvil A5 con ReportLab)...")
    create_pdf("enciclopedia_crypto_vol2.pdf")
    print("✅ ÉXITO: enciclopedia_crypto_vol2.pdf generado correctamente.")
