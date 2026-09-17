import sys
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfgen import canvas

# Función para dibujar el fondo oscuro en cada página
def draw_dark_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#121212")) # Fondo oscuro profundo
    canvas.rect(0, 0, doc.width + doc.leftMargin + doc.rightMargin, doc.height + doc.topMargin + doc.bottomMargin, fill=1, stroke=0)
    canvas.restoreState()

def create_pdf(output_filename):
    # Optimizar para lectura móvil
    doc = SimpleDocTemplate(
        output_filename, 
        pagesize=A5,
        rightMargin=20, 
        leftMargin=20, 
        topMargin=20, 
        bottomMargin=20
    )
    
    styles = getSampleStyleSheet()
    
    # Estilo de Título Principal
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#fca311"), # Zcash Orange
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold"
    )
    
    # Estilo de Subtítulos (H2)
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor("#fca311"), # Zcash Orange
        spaceBefore=20,
        spaceAfter=10,
        fontName="Helvetica-Bold"
    )
    
    # Estilo de Subtítulos Menores (H3)
    h3_style = ParagraphStyle(
        'H3Style',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor("#e0e0e0"), # Gris muy claro
        spaceBefore=15,
        spaceAfter=8,
        fontName="Helvetica-Bold"
    )
    
    # Estilo de Párrafo Normal
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=18, 
        textColor=colors.HexColor("#d0d0d0"), # Gris claro para evitar contraste extremo con negro
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Estilo para Cajas Destacadas
    highlight_style = ParagraphStyle(
        'HighlightStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        textColor=colors.HexColor("#e0e0e0"),
        backColor=colors.HexColor("#1e1e1e"), # Gris oscuro
        borderColor=colors.HexColor("#fca311"),
        borderWidth=1,
        borderPadding=10,
        alignment=TA_JUSTIFY,
        spaceBefore=15,
        spaceAfter=20
    )

    Story = []

    Story.append(Paragraph("Zcash (ZEC) y la Guerra por la Soberanía Financiera", title_style))
    Story.append(Paragraph("<i>Estudio Macro para Lectura Móvil - Septiembre 2026</i>", ParagraphStyle('Sub', parent=body_style, alignment=TA_CENTER, textColor=colors.gray)))
    Story.append(Spacer(1, 20))

    Story.append(Paragraph("Para entender el explosivo crecimiento de Zcash (ZEC) entre 2024 y 2026, no basta con mirar los gráficos. Es necesario comprender la colisión de dos fuerzas titánicas: la evolución de la tecnología criptográfica y el avance sin precedentes del control financiero estatal. Zcash se ha posicionado exactamente en el epicentro de este conflicto.", body_style))

    Story.append(Paragraph("Parte 1: El Catalizador Interno (Proof-of-Stake)", h2_style))
    Story.append(Paragraph("Hasta hace poco, Zcash utilizaba el modelo Proof-of-Work (PoW), el mismo que usa Bitcoin. Este modelo requiere que 'mineros' resuelvan problemas matemáticos complejos utilizando granjas gigantescas de ordenadores. El problema económico del PoW es la <b>hemorragia constante de capital</b>.", body_style))
    Story.append(Paragraph("Los mineros operan para ganar dinero. Cuando recibían ZEC como recompensa, tenían que venderlo casi inmediatamente en el mercado para poder pagar sus inmensas facturas de electricidad y mantenimiento. Esto inyectaba una presión de venta diaria en el mercado que asfixiaba el precio de ZEC.", body_style))
    
    Story.append(Paragraph("El Cambio de Paradigma: Staking", h3_style))
    Story.append(Paragraph("Con la exitosa transición a Proof-of-Stake (PoS), la minería física desapareció. La red ahora es asegurada por 'Validadores'. Para participar, los usuarios deben comprar ZEC y 'bloquearlos' en la red a cambio de ganar intereses.", body_style))
    
    Story.append(Paragraph("<b>El Efecto Económico del PoS:</b> La presión de venta de los mineros desapareció de la noche a la mañana. Al mismo tiempo, miles de inversores empezaron a comprar ZEC en el mercado abierto para bloquearlo y ganar intereses. Esto provocó un <i>Shock de Oferta</i> brutal: altísima demanda persiguiendo monedas que ya no estaban a la venta.", highlight_style))

    Story.append(KeepTogether([
        Paragraph("Parte 2: El Catalizador Externo (Las CBDC)", h2_style),
        Paragraph("Mientras Zcash solucionaba sus problemas internos de emisión, el mundo tradicional preparaba la infraestructura de vigilancia más grande de la historia humana: las Monedas Digitales de Bancos Centrales (CBDCs).", body_style)
    ]))

    Story.append(Paragraph("¿Qué es una CBDC?", h3_style))
    Story.append(Paragraph("A simple vista, parece lo mismo que usar tu tarjeta de crédito o Apple Pay. Sin embargo, bajo el capó, es revolucionario. Cuando usas el banco tradicional, tu dinero es un pasivo de tu banco privado comercial. Con una CBDC, tu dinero es un pasivo directo del Estado. Y lo más importante: <b>es dinero programable</b>.", body_style))

    Story.append(Paragraph("Los 3 Pilares del Control con CBDCs", h3_style))
    Story.append(Paragraph("<b>1. Erradicación del Efectivo (Control Fiscal)</b><br/>El dinero físico es la última trinchera del anonimato. Con una CBDC, cada transacción, sin importar lo pequeña que sea, es registrada en la base de datos del Banco Central. La evasión fiscal se vuelve matemáticamente imposible.", body_style))
    Story.append(Paragraph("<b>2. Tipos de Interés Negativos (Control Monetario)</b><br/>Con las CBDCs, el dinero físico no existe. El Banco Central puede programar una tasa del -3% anual en todas las cuentas de los ciudadanos. Te obligan a gastar tu dinero o invertirlo, controlando el consumo a voluntad.", body_style))
    Story.append(Paragraph("<b>3. Bloqueo Selectivo (Control Social)</b><br/>Al ser código programable, los burócratas pueden decidir qué puedes comprar y qué no. El dinero puede ser bloqueado si asistes a una protesta no autorizada o si excedes cuotas de CO2.", body_style))

    Story.append(KeepTogether([
        Paragraph("Parte 3: Zcash como el Búnker Institucional", h2_style),
        Paragraph("¿Por qué todo este contexto macroeconómico beneficia a Zcash y no a otras criptomonedas?", body_style),
        Paragraph("Bitcoin es inconfiscable, sí. Pero es <b>público</b>. Cualquiera puede ver cuánto Bitcoin tienes y a dónde lo envías.", body_style),
        Paragraph("Zcash soluciona esto usando criptografía alienígena: los <b>zk-SNARKs (Pruebas de Conocimiento Cero)</b>. Esta tecnología permite confirmar que una transacción es válida sin revelar quién envió el dinero, quién lo recibió, ni cuánto se envió. Es dinero digital en la sombra.", body_style)
    ]))

    Story.append(Paragraph("<b>La Supervivencia de Zcash frente a Monero:</b> A diferencia de Monero (XMR), que es privado por defecto y fue expulsado de los exchanges, Zcash tiene <i>privacidad opcional</i>. Esto ha permitido que Zcash sea aceptado legalmente en Wall Street, permitiendo que fondos institucionales billonarios inyecten capital en él, usándolo como refugio seguro contra las CBDCs.", highlight_style))

    Story.append(Paragraph("Conclusión Estratégica", h2_style))
    Story.append(Paragraph("Cuando observas el gráfico hiper-alcista de Zcash, estás viendo la reacción en cadena de la economía global. Millonarios y fondos de cobertura se han dado cuenta de que el dinero tradicional está siendo convertido en una herramienta de vigilancia. Zcash se ha posicionado como la única bóveda digital privada con la liquidez institucional necesaria para absorber esa fuga masiva de capitales hacia la libertad financiera.", body_style))

    doc.build(Story, onFirstPage=draw_dark_background, onLaterPages=draw_dark_background)

if __name__ == "__main__":
    create_pdf("estudio_zcash_color.pdf")
