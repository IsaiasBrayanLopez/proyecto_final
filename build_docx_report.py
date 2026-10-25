import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from PIL import Image

def build_report():
    doc = Document()
    
    # Page setup - Margins 2.5 cm (approx 0.984 inches)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        
    media_dir = r"c:\proyecto_final\proyecto_final\extracted_media"
    output_docx = r"c:\proyecto_final\proyecto_final\Reporte_Proyecto_Final_Catalogo_Automotriz.docx"
    
    # Colors
    NAVY = RGBColor(0x1A, 0x52, 0x76)       # Primary Tech Navy
    SLATE = RGBColor(0x2E, 0x40, 0x53)      # Secondary Dark Slate
    MUTED = RGBColor(0x5D, 0x6D, 0x7E)      # Subtitle Gray
    TEXT = RGBColor(0x21, 0x2F, 0x3D)       # Dark Charcoal body
    BORDER_HEX = "2980B9"
    CODE_BG_HEX = "F8F9FA"
    CALLOUT_BG_HEX = "EBF5FB"

    # Helpers
    def set_cell_background(cell, fill_hex):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._element.get_or_add_tcPr()
        tcMar = parse_xml(f'''
            <w:tcMar {nsdecls("w")}>
                <w:top w:w="{top}" w:type="dxa"/>
                <w:bottom w:w="{bottom}" w:type="dxa"/>
                <w:left w:w="{left}" w:type="dxa"/>
                <w:right w:w="{right}" w:type="dxa"/>
            </w:tcMar>
        ''')
        tcPr.append(tcMar)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=3, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(11)
            r.font.color.rgb = TEXT
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(16)
        r.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.color.rgb = SLATE
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(11.5)
        r.font.color.rgb = NAVY
        return p

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, CALLOUT_BG_HEX)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="30" w:space="0" w:color="{BORDER_HEX}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"{title}: ")
        r_t.bold = True
        r_t.font.name = "Arial"
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = NAVY
        
        r_b = p.add_run(text)
        r_b.font.name = "Arial"
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = TEXT
        
        # Add empty spacing after table
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    def add_code_box(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, CODE_BG_HEX)
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="D5D8DC"/>
                <w:left w:val="single" w:sz="18" w:space="0" w:color="{BORDER_HEX}"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="D5D8DC"/>
                <w:right w:val="single" w:sz="6" w:space="0" w:color="D5D8DC"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(code_text)
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x1C, 0x28, 0x33)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    def add_image_with_caption(img_filename, caption_text, width_inches=5.6):
        img_path = os.path.join(media_dir, img_filename)
        if not os.path.exists(img_path):
            print(f"Warning: {img_path} not found")
            return
            
        # Check aspect ratio
        try:
            im = Image.open(img_path)
            w, h = im.size
            ratio = h / w
            
            # If it's a mobile vertical screenshot (ratio > 1.8), limit width
            actual_width = width_inches
            if ratio > 1.5:
                actual_width = min(width_inches, 2.7)
            elif w < 400:
                actual_width = min(width_inches, 3.5)
                
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            
            run = p_img.add_run()
            run.add_picture(img_path, width=Inches(actual_width))
            
            # Caption
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            
            r_num = p_cap.add_run(caption_text.split(":")[0] + ": ")
            r_num.bold = True
            r_num.font.name = "Arial"
            r_num.font.size = Pt(9.5)
            r_num.font.color.rgb = NAVY
            
            rest = ":".join(caption_text.split(":")[1:]) if ":" in caption_text else ""
            r_txt = p_cap.add_run(rest)
            r_txt.italic = True
            r_txt.font.name = "Arial"
            r_txt.font.size = Pt(9.5)
            r_txt.font.color.rgb = MUTED
        except Exception as e:
            print(f"Error adding image {img_filename}: {e}")

    # ==========================================
    # 1. PORTADA INSTITUCIONAL
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("TECNOLÓGICO NACIONAL DE MÉXICO")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.color.rgb = NAVY

    p_itt = doc.add_paragraph()
    p_itt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_itt.paragraph_format.space_before = Pt(0)
    p_itt.paragraph_format.space_after = Pt(12)
    r = p_itt.add_run("INSTITUTO TECNOLÓGICO DE TLAXIACO\nDEPARTAMENTO DE SISTEMAS Y COMPUTACIÓN")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.color.rgb = SLATE

    # Centered Logo
    logo_path = os.path.join(media_dir, "image1.jpeg")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(12)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.6))

    # Project Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    r = p_title.add_run("PROYECTO FINAL: CATÁLOGO AUTOMOTRIZ INTERACTIVO")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(17)
    r.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    r = p_sub.add_run("UNIDAD 3: MANEJO DE ESTADOS, ARQUITECTURA Y SERVICIOS")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.color.rgb = MUTED

    # Metadata Table
    tbl_meta = doc.add_table(rows=7, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Carrera:", "Ingeniería en Sistemas Computacionales"),
        ("Materia:", "Desarrollo de Aplicaciones Móviles"),
        ("Asesor / Docente:", "Mtro. Vasquez Martínez Josué Israel"),
        ("Alumnos (Bina):", "López Domínguez Isaías Brayan (Programador A)\nBarrios Velasco Jazlynn (Programador B)"),
        ("Grupo:", "7US"),
        ("Producto:", "Reporte Técnico de Práctica Integral"),
        ("Fecha de Entrega:", "17 de Octubre de 2026")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = tbl_meta.rows[idx]
        cell_l = row.cells[0]
        cell_r = row.cells[1]
        
        set_cell_margins(cell_l, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_r, top=60, bottom=60, left=100, right=100)
        set_cell_background(cell_l, "F4F6F7")
        set_cell_background(cell_r, "FFFFFF")
        
        p_l = cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_l = p_l.add_run(label)
        r_l.bold = True
        r_l.font.name = "Arial"
        r_l.font.size = Pt(10.5)
        r_l.font.color.rgb = NAVY
        
        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_r = p_r.add_run(val)
        r_r.font.name = "Arial"
        r_r.font.size = Pt(10.5)
        r_r.font.color.rgb = TEXT
        
    p_lem = doc.add_paragraph()
    p_lem.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lem.paragraph_format.space_before = Pt(20)
    p_lem.paragraph_format.space_after = Pt(0)
    r = p_lem.add_run("Tlaxiaco, Oax., Octubre de 2026.\n“Educación, Ciencia y Tecnología, Progreso día con día” ®")
    r.italic = True
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = MUTED

    doc.add_page_break()

    # ==========================================
    # 2. ÍNDICES
    # ==========================================
    add_h1("ÍNDICE GENERAL")
    
    indices = [
        ("1. INTRODUCCIÓN", "2"),
        ("    1.1 Contexto y Objetivos del Proyecto", "2"),
        ("    1.2 Pilares Técnicos y Arquitectura", "2"),
        ("2. DESARROLLO DE LA PRÁCTICA", "3"),
        ("    2.1 Fase 1: Creación del Repositorio e Invitación (Programador A)", "3"),
        ("    2.2 Fase 2: Configuración del Entorno de Trabajo (Programador B)", "4"),
        ("    2.3 Fase 3: Modelo de Datos y Fuente JSON (Programador A)", "5"),
        ("    2.4 Fase 4: Servicios Asíncronos y Sistema de Temas (Programador B)", "7"),
        ("    2.5 Fase 5: Construcción de Widgets Modulares - Bloque 1 (Programador A)", "9"),
        ("    2.6 Fase 6: Construcción de Widgets Modulares - Bloque 2 (Programador B)", "11"),
        ("    2.7 Fase 7: Implementación de Pantallas Principales (Programador A)", "12"),
        ("    2.8 Fase 8: Pantallas Finales e Integración Global (Programador B)", "15"),
        ("    2.9 Fase 9: Pruebas y Resultados de Ejecución (Web y Móvil)", "18"),
        ("3. CONCLUSIONES", "21"),
        ("4. FUENTES BIBLIOGRÁFICAS", "22")
    ]
    for item, page in indices:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item)
        r1.font.name = "Arial"
        r1.font.size = Pt(10.5)
        if not item.startswith("    "):
            r1.bold = True
            r1.font.color.rgb = NAVY
        else:
            r1.font.color.rgb = TEXT
        # Dots
        dots_count = max(5, 75 - len(item))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Arial"
        r_dots.font.size = Pt(9)
        r_dots.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)
        r2 = p.add_run(page)
        r2.bold = True
        r2.font.name = "Arial"
        r2.font.size = Pt(10)
        r2.font.color.rgb = SLATE

    add_h1("ÍNDICE DE ILUSTRACIONES")
    
    ilustraciones = [
        ("Ilustración 1", "Creación de un nuevo repositorio público en GitHub", "3"),
        ("Ilustración 2", "Gestión de acceso e inclusión del colaborador Jazlynn22", "3"),
        ("Ilustración 3", "Estructura del proyecto Flutter generado en Visual Studio Code", "3"),
        ("Ilustración 4", "Organización de paquetes en lib y directorio assets/data", "4"),
        ("Ilustración 5", "Comandos git init, git add y git commit en la terminal local", "4"),
        ("Ilustración 6", "Vinculación con origen remoto y push a la rama main", "4"),
        ("Ilustración 7", "Repositorio en GitHub con el primer commit y arquitectura", "4"),
        ("Ilustración 8", "Creación de la carpeta de trabajo en la estación del Programador B", "4"),
        ("Ilustración 9", "Notificación de acceso concedido en GitHub para el Programador B", "5"),
        ("Ilustración 10", "Clonación del repositorio mediante comando git clone", "5"),
        ("Ilustración 11", "Verificación y descarga de cambios mediante git pull origin main", "5"),
        ("Ilustración 12", "Creación y cambio a la rama de desarrollo isaias", "5"),
        ("Ilustración 13", "Declaración de la ruta del asset JSON en pubspec.yaml", "6"),
        ("Ilustración 14", "Definición del conjunto de datos en assets/data/vehiculos.json", "6"),
        ("Ilustración 15", "Implementación del modelo Vehiculo y constructor Factory fromJson", "6"),
        ("Ilustración 16", "Registro de commit y push hacia la rama remota isaias", "7"),
        ("Ilustración 17", "Apertura de la Solicitud de Extracción (Pull Request #1)", "7"),
        ("Ilustración 18", "Fusión exitosa del Pull Request #1 en la rama main", "7"),
        ("Ilustración 19", "Programador B actualiza su entorno local mediante git pull", "7"),
        ("Ilustración 20", "Creación y conmutación hacia la rama Jazlynn", "8"),
        ("Ilustración 21", "Definición de paleta de colores y tema en lib/theme/app_theme.dart", "8"),
        ("Ilustración 22", "Implementación del servicio asíncrono lib/services/vehiculo_service.dart", "8"),
        ("Ilustración 23", "Commit local de tema y servicio en la rama Jazlynn", "8"),
        ("Ilustración 24", "GitHub detecta actualizaciones recientes en la rama Jazlynn", "9"),
        ("Ilustración 25", "Creación de Solicitud de Extracción (Pull Request #2)", "9"),
        ("Ilustración 26", "Validación automática de ausencia de conflictos para fusión", "9"),
        ("Ilustración 27", "Pull Request #2 cerrado y fusionado satisfactoriamente", "9"),
        ("Ilustración 28", "Programador A descarga las modificaciones de tema y servicio", "10"),
        ("Ilustración 29", "Estructura del directorio lib/widgets/ con 5 nuevos widgets", "10"),
        ("Ilustración 30", "Código fuente del widget interactivo category_chip.dart", "10"),
        ("Ilustración 31", "Código fuente del widget de barra superior custom_app_bar.dart", "10"),
        ("Ilustración 32", "Código fuente del componente de precio price_tag.dart", "11"),
        ("Ilustración 33", "Código fuente del encabezado estructurado section_header.dart", "11"),
        ("Ilustración 34", "Código fuente de la tarjeta de especificaciones spec_badge.dart", "11"),
        ("Ilustración 35", "Commit y subida de los 5 widgets personalizados a la rama isaias", "11"),
        ("Ilustración 36", "Apertura de Pull Request #3 para incorporación del Bloque 1 de widgets", "12"),
        ("Ilustración 37", "Fusión confirmada del Pull Request #3 en la rama main", "12"),
        ("Ilustración 38", "Repositorio consolidado en GitHub con 7 commits en main", "12"),
        ("Ilustración 39", "Programador B confirma la creación del Bloque 2 de widgets", "12"),
        ("Ilustración 40", "Envío de la rama Jazlynn hacia el repositorio remoto en GitHub", "12"),
        ("Ilustración 41", "Fusión del Pull Request #4 con los widgets del Bloque 2", "13"),
        ("Ilustración 42", "Programador A sincroniza los widgets del Bloque 2 mediante git pull", "13"),
        ("Ilustración 43", "Estructura del directorio lib/screens con las pantallas base", "13"),
        ("Ilustración 44", "Código de CatalogScreen: definición de estado y filtros", "13"),
        ("Ilustración 45", "Código de CatalogScreen: mapeo de chips y render condicional", "14"),
        ("Ilustración 46", "Código de CatalogScreen: navegación con paso de objeto completo", "14"),
        ("Ilustración 47", "Código de DetailScreen: estructura CustomScrollView y SliverAppBar", "14"),
        ("Ilustración 48", "Código de DetailScreen: ficha técnica y precio", "14"),
        ("Ilustración 49", "Código de DetailScreen: mapeo de lista de equipamiento y revisión", "15"),
        ("Ilustración 50", "Código de DetailScreen: procedimiento numerado y botón de retroceso", "15"),
        ("Ilustración 51", "Código de HomeScreen: estado reactivo y colección de favoritos", "15"),
        ("Ilustración 52", "Código de HomeScreen: renderizado asíncrono con FutureBuilder", "16"),
        ("Ilustración 53", "Código de HomeScreen: botones de navegación hacia pantallas secundarias", "16"),
        ("Ilustración 54", "Commit y push de las pantallas principales en la rama isaias", "16"),
        ("Ilustración 55", "Fusión del Pull Request #5 en la rama main", "16"),
        ("Ilustración 56", "Programador B sincroniza las pantallas desarrolladas", "17"),
        ("Ilustración 57", "Código de about_screen.dart con presentación de la bina", "17"),
        ("Ilustración 58", "Código de favorites_screen.dart: filtrado dinámico de favoritos", "17"),
        ("Ilustración 59", "Código de favorites_screen.dart: renderizado de tarjeta y navegación", "18"),
        ("Ilustración 60", "Código del punto de entrada lib/main.dart con CatalogoAutosApp", "18"),
        ("Ilustración 61", "Confirmación y push de las pantallas finales por el Programador B", "18"),
        ("Ilustración 62", "Creación de Pull Request #6 para pantallas finales y main", "19"),
        ("Ilustración 63", "Fusión definitiva del Pull Request #6 en main", "19"),
        ("Ilustración 64", "Programador A ejecuta la sincronización final con git pull", "19"),
        ("Ilustración 65", "Ejecución Web: Pantalla de inicio Directorio Automotriz", "19"),
        ("Ilustración 66", "Ejecución Web: Vista de Catálogo con filtrado interactivo", "20"),
        ("Ilustración 67", "Ejecución Web: Vista de Vehículos Guardados como favoritos", "20"),
        ("Ilustración 68", "Ejecución Web: Vista informativa del proyecto y miembros de la bina", "20"),
        ("Ilustración 69", "Ejecución Móvil: Pantalla principal en emulador Android", "20"),
        ("Ilustración 70", "Ejecución Móvil: Exploración del catálogo en smartphone", "21"),
        ("Ilustración 71", "Ejecución Móvil: Pantalla de vehículos guardados en smartphone", "21"),
        ("Ilustración 72", "Ejecución Móvil: Información del proyecto y bina en smartphone", "21")
    ]
    for tag, desc, page in ilustraciones:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"{tag}: ")
        r1.bold = True
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = NAVY
        
        r2 = p.add_run(desc)
        r2.font.name = "Arial"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT
        
        dots_count = max(4, 78 - len(tag) - len(desc))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Arial"
        r_dots.font.size = Pt(8.5)
        r_dots.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)
        
        r3 = p.add_run(page)
        r3.bold = True
        r3.font.name = "Arial"
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = SLATE

    doc.add_page_break()

    # ==========================================
    # 3. INTRODUCCIÓN
    # ==========================================
    add_h1("1. INTRODUCCIÓN")
    
    add_h2("1.1 Contexto y Objetivos del Proyecto")
    add_p("El presente proyecto consiste en el desarrollo integral de un Catálogo Automotriz interactivo construido con el framework multiplataforma Flutter y el lenguaje de programación fuertemente tipado Dart. Esta aplicación móvil permite a los usuarios finales explorar un inventario dinámico de vehículos, consultar fichas técnicas exhaustivas, visualizar especificaciones de motorización y transmisión, revisar listas de equipamiento de serie, inspeccionar guías paso a paso de mantenimiento preventivo y gestionar una colección personalizada de vehículos favoritos.")
    add_p("Este desarrollo se enmarca dentro de las actividades prácticas de la Unidad 3: Manejo de Estados, Arquitectura y Servicios de la asignatura Desarrollo de Aplicaciones Móviles. El propósito medular de esta etapa académica es guiar a los estudiantes en la transición desde la construcción de interfaces puramente estáticas hacia el diseño de aplicaciones móviles dinámicas, escalables, reactivas y estructuradas bajo estándares profesionales de ingeniería de software.")
    
    add_h2("1.2 Pilares Técnicos y Arquitectura del Sistema")
    add_p("Para alcanzar un nivel de calidad profesional y facilitar la mantenibilidad del código fuente, el proyecto se cimentó sobre cinco conceptos técnicos fundamentales:")
    
    add_callout("Arquitectura por Capas Limpia", "Separación modular del código en paquetes especializados: models (entidades del dominio), services (lógica de acceso a datos), theme (estilos y reglas de diseño Material 3), widgets (componentes atómicos reutilizables) y screens (vistas de usuario de alto nivel).")
    add_callout("Consumo y Deserialización de JSON Local", "Simulación fidedigna de una fuente de datos estructurada mediante el archivo assets/data/vehiculos.json, transformado a objetos de Dart a través del patrón de diseño Factory con conversiones de tipos seguras.")
    add_callout("Renderizado Reactivo y Asíncrono con FutureBuilder", "Gestión fluida del estado de las peticiones de datos (espera, completado o error), impidiendo cualquier tipo de bloqueo o congelamiento en el hilo principal de la interfaz de usuario (UI thread).")
    add_callout("Sistema Robusto de Rutas y Navegación", "Implementación de Navigator.push y Navigator.pop mediante transiciones fluidas de MaterialPageRoute, garantizando el paso bidireccional de parámetros y la sincronización reactiva de colecciones de favoritos.")
    add_callout("Flujo Colaborativo con Git y GitHub", "Adopción de un esquema de trabajo en bina (Programador A y Programador B) basado en ramificación por funcionalidades (feature branching), emisión formal de Pull Requests y resolución sistemática de fusiones sin conflictos en la rama main.")

    doc.add_page_break()

    # ==========================================
    # 4. DESARROLLO DE LA PRÁCTICA
    # ==========================================
    add_h1("2. DESARROLLO DE LA PRÁCTICA")

    # 2.1 Fase 1
    add_h2("2.1 Fase 1: Creación del Repositorio e Invitación a Colaborador")
    add_callout("Rol Responsable", "Programador A (López Domínguez Isaías Brayan)")
    add_p("El proyecto dio inicio con la configuración de la infraestructura de control de versiones remota. En la plataforma GitHub, el Programador A creó un repositorio público denominado 'proyecto_final'. Para posibilitar el desarrollo concurrente y coordinado en equipo, se accedió al panel de configuración del repositorio y se envió la invitación formal de colaboración al usuario del Programador B (Jazlynn22).")
    
    add_image_with_caption("image4.png", "Ilustración 1: Creación de un nuevo repositorio público en GitHub")
    add_image_with_caption("image5.png", "Ilustración 2: Gestión de acceso e inclusión del colaborador Jazlynn22")

    add_p("Posteriormente, en la estación local del Programador A, se generó el proyecto Flutter mediante la instrucción 'flutter create proyecto_final'. Se organizó la estructura inicial del código fuente y se creó la carpeta 'assets/data' para alojar los recursos de datos locales, además de los directorios especializados dentro de 'lib/' (models, screens, services, theme, widgets).")
    
    add_image_with_caption("image6.png", "Ilustración 3: Estructura del proyecto Flutter generado en Visual Studio Code")
    add_image_with_caption("image7.png", "Ilustración 4: Organización de paquetes en lib y directorio assets/data")

    add_p("A continuación, se inicializó el repositorio Git local en PowerShell, se añadieron todos los archivos al área de preparación (staging) y se realizó el primer commit de la arquitectura limpia, subiendo el proyecto a la rama remota 'main':")
    add_code_box("git init\ngit add .\ngit commit -m \"Creación de proyecto en flutter con arquitectura limpia\"\ngit branch -M main\ngit remote add origin https://github.com/IsaiasBrayanLopez/proyecto_final.git\ngit push -u origin main")

    add_image_with_caption("image8.png", "Ilustración 5: Comandos git init, git add y git commit en la terminal local")
    add_image_with_caption("image9.png", "Ilustración 6: Vinculación con origen remoto y push a la rama main")
    add_image_with_caption("image10.png", "Ilustración 7: Repositorio en GitHub con el primer commit y arquitectura")

    # 2.2 Fase 2
    add_h2("2.2 Fase 2: Configuración del Entorno de Trabajo del Programador B")
    add_callout("Rol Responsable", "Programador B (Barrios Velasco Jazlynn)")
    add_p("En la estación de trabajo secundaria, el Programador B preparó su entorno local creando la carpeta 'C:\\proyecto_final'. Tras recibir y aceptar la invitación de colaboración en GitHub, obtuvo acceso de escritura directo al repositorio central.")
    
    add_image_with_caption("image11.png", "Ilustración 8: Creación de la carpeta de trabajo en la estación del Programador B")
    add_image_with_caption("image12.png", "Ilustración 9: Notificación de acceso concedido en GitHub para el Programador B")

    add_p("A través del Símbolo del sistema (CMD) y PowerShell, el Programador B procedió a clonar el repositorio y sincronizar la rama principal 'main':")
    add_code_box("cd C:\\proyecto_final\ngit clone https://github.com/IsaiasBrayanLopez/proyecto_final.git\ncd proyecto_final\ngit pull origin main")

    add_image_with_caption("image13.png", "Ilustración 10: Clonación del repositorio mediante comando git clone")
    add_image_with_caption("image14.png", "Ilustración 11: Verificación y descarga de cambios mediante git pull origin main")

    # 2.3 Fase 3
    add_h2("2.3 Fase 3: Modelo de Datos y Fuente JSON (Programador A)")
    add_callout("Rol Responsable", "Programador A (López Domínguez Isaías Brayan)")
    add_p("Para dar inicio a la capa de datos sin interferir con la rama productiva, el Programador A creó la rama de trabajo 'isaias' mediante el comando 'git checkout -b isaias'.")
    
    add_image_with_caption("image15.png", "Ilustración 12: Creación y cambio a la rama de desarrollo isaias")

    add_p("En primer lugar, se editó el manifiesto 'pubspec.yaml' para activar las fuentes de Material Design y registrar el archivo 'assets/data/vehiculos.json' dentro de la sección de assets del paquete:")
    add_code_box("flutter:\n  uses-material-design: true\n  assets:\n    - assets/data/vehiculos.json")
    
    add_image_with_caption("image16.png", "Ilustración 13: Declaración de la ruta del asset JSON en pubspec.yaml")

    add_p("En seguida, se construyó el archivo 'assets/data/vehiculos.json', definiendo un conjunto de registros vehiculares con campos como id, marca, modelo, anio, categoria, precio, motor, transmision, imageUrl, equipamiento y pasosRevision.")
    
    add_image_with_caption("image17.png", "Ilustración 14: Definición del conjunto de datos en assets/data/vehiculos.json")

    add_p("Para manipular estos datos como entidades tipadas de Dart, se programó la clase 'Vehiculo' en 'lib/models/vehiculo.dart'. Esta clase cuenta con variables inmutables y un constructor de tipo Factory ('Vehiculo.fromJson') que deserializa el mapa dynamic de forma segura, convirtiendo tipos numéricos a double y listas dinámicas a 'List<String>'.")
    
    add_image_with_caption("image18.png", "Ilustración 15: Implementación del modelo Vehiculo y constructor Factory fromJson")

    add_p("Con estos archivos validados, el Programador A confirmó los cambios en su rama local, ejecutó el push y creó el Pull Request #1 en GitHub, el cual fue revisado y fusionado a 'main':")
    add_code_box("git add .\ngit commit -m \"Se agregó modelo y JSON de vehículos\"\ngit push -u origin isaias")

    add_image_with_caption("image19.png", "Ilustración 16: Registro de commit y push hacia la rama remota isaias")
    add_image_with_caption("image20.png", "Ilustración 17: Apertura de la Solicitud de Extracción (Pull Request #1)")
    add_image_with_caption("image21.png", "Ilustración 18: Fusión exitosa del Pull Request #1 en la rama main")

    # 2.4 Fase 4
    add_h2("2.4 Fase 4: Servicios Asíncronos y Sistema de Temas (Programador B)")
    add_callout("Rol Responsable", "Programador B (Barrios Velasco Jazlynn)")
    add_p("El Programador B descargó el nuevo modelo de datos y el JSON mediante 'git pull origin main', y procedió a crear su rama de trabajo 'Jazlynn'.")
    
    add_image_with_caption("image22.png", "Ilustración 19: Programador B actualiza su entorno local mediante git pull")
    add_image_with_caption("image23.png", "Ilustración 20: Creación y conmutación hacia la rama Jazlynn")

    add_p("En esta fase se implementaron dos módulos estructurales críticos:")
    add_p("1. 'lib/theme/app_theme.dart': Define la paleta de colores institucional (primaryColor: 0xFF34495E, accentColor: 0xFF5D6D7E, backgroundColor: 0xFFF4F6F8) y el objeto ThemeData con compatibilidad Material 3.")
    add_p("2. 'lib/services/vehiculo_service.dart': Clase de servicio encargada de cargar asíncronamente el archivo JSON mediante 'rootBundle.loadString', parsearlo con 'jsonDecode' y convertirlo a una lista de objetos 'Vehiculo'.")

    add_image_with_caption("image24.png", "Ilustración 21: Definición de paleta de colores y tema en lib/theme/app_theme.dart")
    add_image_with_caption("image25.png", "Ilustración 22: Implementación del servicio asíncrono lib/services/vehiculo_service.dart")

    add_p("El Programador B realizó el commit, subió la rama 'Jazlynn' a GitHub y abrió el Pull Request #2 ('Cree app_theme.dart y vehiculo_service.dart'), fusionándolo a 'main' sin ningún conflicto:")
    add_code_box("git add .\ngit commit -m \"Cree app_theme.dart y vehiculo_service.dart\"\ngit push -u origin Jazlynn")

    add_image_with_caption("image26.png", "Ilustración 23: Commit local de tema y servicio en la rama Jazlynn")
    add_image_with_caption("image27.png", "Ilustración 24: GitHub detecta actualizaciones recientes en la rama Jazlynn")
    add_image_with_caption("image28.png", "Ilustración 25: Creación de Solicitud de Extracción (Pull Request #2)")
    add_image_with_caption("image29.png", "Ilustración 26: Validación automática de ausencia de conflictos para fusión")
    add_image_with_caption("image30.png", "Ilustración 27: Pull Request #2 cerrado y fusionado satisfactoriamente")

    # 2.5 Fase 5
    add_h2("2.5 Fase 5: Construcción de Widgets Modulares - Bloque 1 (Programador A)")
    add_callout("Rol Responsable", "Programador A (López Domínguez Isaías Brayan)")
    add_p("El Programador A sincronizó los cambios de tema y servicio vía 'git pull origin main'. Posteriormente, dentro del directorio 'lib/widgets/', construyó cinco componentes de interfaz altamente reutilizables:")
    add_p("• 'category_chip.dart': Chip interactivo basado en ChoiceChip para filtrado por categoría.")
    add_p("• 'custom_app_bar.dart': Barra de aplicación superior homogénea que implementa PreferredSizeWidget.")
    add_p("• 'price_tag.dart': Contenedor estilizado para el precio formateado en pesos mexicanos (MXN).")
    add_p("• 'section_header.dart': Encabezado con título prominente y subtítulo descriptivo para vistas.")
    add_p("• 'spec_badge.dart': Tarjeta con icono y etiquetas para resaltar especificaciones de motor y transmisión.")

    add_image_with_caption("image31.png", "Ilustración 28: Programador A descarga las modificaciones de tema y servicio")
    add_image_with_caption("image32.png", "Ilustración 29: Estructura del directorio lib/widgets/ con 5 nuevos widgets")
    add_image_with_caption("image33.png", "Ilustración 30: Código fuente del widget interactivo category_chip.dart")
    add_image_with_caption("image34.png", "Ilustración 31: Código fuente del widget de barra superior custom_app_bar.dart")
    add_image_with_caption("image35.png", "Ilustración 32: Código fuente del componente de precio price_tag.dart")
    add_image_with_caption("image36.png", "Ilustración 33: Código fuente del encabezado estructurado section_header.dart")
    add_image_with_caption("image37.png", "Ilustración 34: Código fuente de la tarjeta de especificaciones spec_badge.dart")

    add_p("El Programador A envió los 5 widgets a su rama remota y formalizó el Pull Request #3, completando la fusión exitosa en la rama principal:")
    add_code_box("git add .\ngit commit -m \"Se agregaron 5 widgets personalizados\"\ngit push -u origin isaias")

    add_image_with_caption("image38.png", "Ilustración 35: Commit y subida de los 5 widgets personalizados a la rama isaias")
    add_image_with_caption("image39.png", "Ilustración 36: Apertura de Pull Request #3 para incorporación del Bloque 1 de widgets")
    add_image_with_caption("image40.png", "Ilustración 37: Fusión confirmada del Pull Request #3 en la rama main")
    add_image_with_caption("image41.png", "Ilustración 38: Repositorio consolidado en GitHub con 7 commits en main")

    # 2.6 Fase 6
    add_h2("2.6 Fase 6: Construcción de Widgets Modulares - Bloque 2 (Programador B)")
    add_callout("Rol Responsable", "Programador B (Barrios Velasco Jazlynn)")
    add_p("De manera coordinada, el Programador B implementó el segundo bloque de cinco componentes en 'lib/widgets/':")
    add_p("• 'custom_action_button.dart': Botón de acción destacado con elevación e icono integrado.")
    add_p("• 'empty_state_view.dart': Vista que se despliega cuando una búsqueda o lista de favoritos carece de registros.")
    add_p("• 'stat_counter_card.dart': Tarjeta para desplegar estadísticas numéricas con iconos en la pantalla de bienvenida.")
    add_p("• 'team_member_tile.dart': Tarjeta informativa con avatar, nombre, rol y usuario Git de los integrantes.")
    add_p("• 'vehiculo_card.dart': Tarjeta completa para el catálogo con imagen de fondo, marca, modelo, precio e interacción de favoritos.")

    add_p("El Programador B registró el commit 'Agregué 5 widget', realizó el push a la rama 'Jazlynn' y fusionó el Pull Request #4 en la rama 'main':")
    add_code_box("git add .\ngit commit -m \"Agregué 5 widget\"\ngit push origin Jazlynn")

    add_image_with_caption("image42.png", "Ilustración 39: Programador B confirma la creación del Bloque 2 de widgets")
    add_image_with_caption("image43.png", "Ilustración 40: Envío de la rama Jazlynn hacia el repositorio remoto en GitHub")
    add_image_with_caption("image44.png", "Ilustración 41: Fusión del Pull Request #4 con los widgets del Bloque 2")

    # 2.7 Fase 7
    add_h2("2.7 Fase 7: Implementación de Pantallas Principales (Programador A)")
    add_callout("Rol Responsable", "Programador A (López Domínguez Isaías Brayan)")
    add_p("El Programador A descargó los widgets del Bloque 2 mediante 'git pull origin main' y procedió a crear las tres pantallas fundamentales en 'lib/screens/':")
    
    add_image_with_caption("image45.png", "Ilustración 42: Programador A sincroniza los widgets del Bloque 2 mediante git pull")
    add_image_with_caption("image46.png", "Ilustración 43: Estructura del directorio lib/screens con las pantallas base")

    add_p("1. 'CatalogScreen' ('catalog_screen.dart'): Administra el listado de vehículos, permitiendo filtrar en memoria según la categoría seleccionada mediante una lista horizontal de CategoryChip. Al seleccionar una unidad, invoca 'Navigator.push' transfiriendo el objeto 'Vehiculo' a la vista de detalles.")
    add_image_with_caption("image47.png", "Ilustración 44: Código de CatalogScreen: definición de estado y filtros")
    add_image_with_caption("image48.png", "Ilustración 45: Código de CatalogScreen: mapeo de chips y render condicional")
    add_image_with_caption("image49.png", "Ilustración 46: Código de CatalogScreen: navegación con paso de objeto completo")

    add_p("2. 'DetailScreen' ('detail_screen.dart'): Diseñada con un 'CustomScrollView' y 'SliverAppBar' con imagen responsiva, ficha técnica, lista de equipamiento mapeada con iconos y el procedimiento numerado de revisión mecánica con botón de retroceso.")
    add_image_with_caption("image50.png", "Ilustración 47: Código de DetailScreen: estructura CustomScrollView y SliverAppBar")
    add_image_with_caption("image51.png", "Ilustración 48: Código de DetailScreen: ficha técnica y precio")
    add_image_with_caption("image52.png", "Ilustración 49: Código de DetailScreen: mapeo de lista de equipamiento y revisión")
    add_image_with_caption("image53.png", "Ilustración 50: Código de DetailScreen: procedimiento numerado y botón de retroceso")

    add_p("3. 'HomeScreen' ('home_screen.dart'): Pantalla principal que carga los datos asíncronos mediante 'FutureBuilder<List<Vehiculo>>', muestra el indicador de progreso mientras se procesa la lectura, despliega las tarjetas estadísticas ('StatCounterCard') con el total de unidades y vehículos guardados, y proporciona botones para navegar a las demás secciones.")
    add_image_with_caption("image54.png", "Ilustración 51: Código de HomeScreen: estado reactivo y colección de favoritos")
    add_image_with_caption("image55.png", "Ilustración 52: Código de HomeScreen: renderizado asíncrono con FutureBuilder")
    add_image_with_caption("image56.png", "Ilustración 53: Código de HomeScreen: botones de navegación hacia pantallas secundarias")

    add_p("El Programador A realizó el commit 'Se agregaron 3 pantallas, home, catalogo y detalles', subió su rama y completó la fusión del Pull Request #5 en GitHub:")
    add_code_box("git add .\ngit commit -m \"Se agregaron 3 pantallas, home, catalogo y detalles\"\ngit push -u origin isaias")

    add_image_with_caption("image57.png", "Ilustración 54: Commit y push de las pantallas principales en la rama isaias")
    add_image_with_caption("image58.png", "Ilustración 55: Fusión del Pull Request #5 en la rama main")

    # 2.8 Fase 8
    add_h2("2.8 Fase 8: Pantallas Finales e Integración Global (Programador B)")
    add_callout("Rol Responsable", "Programador B (Barrios Velasco Jazlynn)")
    add_p("El Programador B descargó las pantallas implementadas mediante 'git pull origin main' e implementó los componentes finales de la aplicación:")
    
    add_image_with_caption("image59.png", "Ilustración 56: Programador B sincroniza las pantallas desarrolladas")

    add_p("1. 'AboutScreen' ('about_screen.dart'): Pantalla que documenta la institución, materia, unidad y miembros de la bina mediante tarjetas TeamMemberTile.")
    add_image_with_caption("image60.png", "Ilustración 57: Código de about_screen.dart con presentación de la bina")

    add_p("2. 'FavoritesScreen' ('favorites_screen.dart'): Pantalla que filtra los vehículos cuyos IDs estén contenidos en el conjunto 'Set<int> favoritosIds'. Si no hay favoritos, renderiza 'EmptyStateView'; en caso contrario, despliega la lista con tarjetas interactivas.")
    add_image_with_caption("image61.png", "Ilustración 58: Código de favorites_screen.dart: filtrado dinámico de favoritos")
    add_image_with_caption("image62.png", "Ilustración 59: Código de favorites_screen.dart: renderizado de tarjeta y navegación")

    add_p("3. 'main.dart': Configuración de la clase de entrada 'CatalogoAutosApp' con desactivación del banner de depuración, asignación del tema 'AppTheme.lightTheme' y establecimiento de 'HomeScreen' como vista inicial.")
    add_image_with_caption("image63.png", "Ilustración 60: Código del punto de entrada lib/main.dart con CatalogoAutosApp")

    add_p("El Programador B confirmó estos archivos finales, realizó el push a la rama 'Jazlynn' y fusionó el Pull Request #6 en 'main':")
    add_code_box("git add .\ngit commit -m \"Agregué en la carpeta screens los archivos about_screen.dart, favorites_screen.dart e hice el main.dart\"\ngit push -u origin Jazlynn")

    add_image_with_caption("image64.png", "Ilustración 61: Confirmación y push de las pantallas finales por el Programador B")
    add_image_with_caption("image65.png", "Ilustración 62: Creación de Pull Request #6 para pantallas finales y main")
    add_image_with_caption("image66.png", "Ilustración 63: Fusión definitiva del Pull Request #6 en main")

    add_p("Finalmente, el Programador A ejecutó 'git pull origin main' en su terminal, dejando ambas estaciones de desarrollo con la versión final idéntica y lista para pruebas:")
    add_image_with_caption("image67.png", "Ilustración 64: Programador A ejecuta la sincronización final con git pull")

    # 2.9 Fase 9
    add_h2("2.9 Fase 9: Pruebas y Resultados de Ejecución (Web y Móvil)")
    add_p("La aplicación fue sometida a pruebas exhaustivas en dos entornos de ejecución: navegador web (Google Chrome) y emulador móvil (Android).")
    
    add_h3("A. Pruebas de Ejecución en Entorno Web (localhost:59219)")
    add_p("En el navegador se verificó la correcta distribución del diseño responsivo, las transiciones fluidas de los botones de navegación, la persistencia en memoria de los favoritos marcados y el comportamiento ágil del filtrado por categorías:")
    
    add_image_with_caption("image68.png", "Ilustración 65: Ejecución Web: Pantalla de inicio Directorio Automotriz")
    add_image_with_caption("image69.png", "Ilustración 66: Ejecución Web: Vista de Catálogo con filtrado interactivo")
    add_image_with_caption("image70.png", "Ilustración 67: Ejecución Web: Vista de Vehículos Guardados como favoritos")
    add_image_with_caption("image71.png", "Ilustración 68: Ejecución Web: Vista informativa del proyecto y miembros de la bina")

    add_h3("B. Pruebas de Ejecución en Emulador Móvil Android")
    add_p("En el dispositivo móvil virtual se comprobó la adaptabilidad al factor de forma vertical y al recorte de pantalla (notch/punch hole), así como la fluidez del scroll táctil y la carga de imágenes remotas:")
    
    add_image_with_caption("image72.png", "Ilustración 69: Ejecución Móvil: Pantalla principal en emulador Android", width_inches=2.7)
    add_image_with_caption("image73.png", "Ilustración 70: Ejecución Móvil: Exploración del catálogo en smartphone", width_inches=2.7)
    add_image_with_caption("image74.png", "Ilustración 71: Ejecución Móvil: Pantalla de vehículos guardados en smartphone", width_inches=2.7)
    add_image_with_caption("image75.png", "Ilustración 72: Ejecución Móvil: Información del proyecto y bina en smartphone", width_inches=2.7)

    doc.add_page_break()

    # ==========================================
    # 5. CONCLUSIONES
    # ==========================================
    add_h1("3. CONCLUSIONES")
    add_p("El desarrollo exitoso del Catálogo Automotriz interactivo permitió consolidar de manera práctica y rigurosa los objetivos de aprendizaje de la Unidad 3: Manejo de Estados, Arquitectura y Servicios. A través de este proyecto se obtuvieron las siguientes conclusiones técnicas y metodológicas:")
    
    add_p("1. Eficiencia y Robustez en la Deserialización de Datos: La implementación del patrón Factory mediante el método 'Vehiculo.fromJson' evidenció las ventajas del sistema de tipos estricto de Dart. Realizar conversiones explícitas de tipos primitivos y listas dinámicas garantizó la inmutabilidad y solidez del modelo de datos frente a variaciones imprevistas en la carga del archivo JSON.")
    
    add_p("2. Programación Reactiva y Asíncrona sin Congelamientos: El empleo conjunto de 'FutureBuilder' y 'async/await' demostró ser la estrategia idónea para coordinar el ciclo de vida de peticiones asíncronas con la interfaz visual. El control de estados de conexión ('ConnectionState.waiting' y 'hasError') aseguró que el hilo principal (UI thread) permaneciera totalmente desbloqueado, ofreciendo una experiencia de usuario fluida e indicadores visuales de progreso.")

    add_p("3. Modularidad y Reutilización con Arquitectura Limpia: La descomposición de la interfaz en diez widgets especializados e independientes (categorizados en dos bloques de trabajo colaborativo) redujo drásticamente la duplicidad de código fuente, facilitó el mantenimiento correctivo y garantizó una rigurosa consistencia visual bajo las pautas de diseño de Material Design 3.")

    add_p("4. Trabajo Colaborativo Profesional con Git y GitHub: El esquema de trabajo en bina mediante ramas de características independientes ('isaias' y 'Jazlynn'), la integración mediante Pull Requests formales y la verificación continua de compatibilidad permitieron un flujo de desarrollo paralelo sin conflictos de fusión (merge conflicts), simulando con absoluta fidelidad las prácticas de la industria de software.")

    add_p("5. Escalabilidad y Proyección Futura: La arquitectura por capas implementada en este proyecto establece las bases para evolucionar la aplicación hacia el consumo de APIs RESTful remotas, la persistencia en bases de datos locales (como Hive o SQLite) y la incorporación de gestores de estado avanzados (Provider, Riverpod o BLoC), constituyendo un producto de software robusto, mantenible y listo para producción.")

    doc.add_page_break()

    # ==========================================
    # 6. FUENTES BIBLIOGRÁFICAS
    # ==========================================
    add_h1("4. FUENTES BIBLIOGRÁFICAS Y DOCUMENTALES")
    
    fuentes = [
        "Chacon, S., & Straub, B. (2014). Pro Git: Everything you need to know about Git (2da ed.). Apress. https://git-scm.com/book/es/v2",
        "Dart Language Team. (2024). Asynchronous Programming: Futures and async-await. Google Developers. https://dart.dev/codelabs/async-await",
        "Google LLC. (2024). Flutter Architectural Overview & State Management. Flutter Documentation. https://docs.flutter.dev",
        "Material Design. (2023). Material 3 Design Guidelines for Mobile Applications. Google Design. https://m3.material.io",
        "Tecnológico Nacional de México. (2026). Programa de Estudios de la Asignatura: Desarrollo de Aplicaciones Móviles. Instituto Tecnológico de Tlaxiaco.",
        "Windmill, E. (2020). Flutter in Action (1ra ed.). Manning Publications."
    ]
    for fuente in fuentes:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        r = p.add_run(fuente)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT

    # Save document
    doc.save(output_docx)
    print("Document successfully created and saved at:", output_docx)
    print("File size:", os.path.getsize(output_docx), "bytes")

if __name__ == "__main__":
    build_report()
