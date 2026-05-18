import math
from dataclasses import dataclass

import streamlit as st


st.set_page_config(
    page_title="UCES | Sistemas Operativos",
    page_icon="UCES",
    layout="wide",
)


REFERENCIAS = [
    "Botaro, A. E., & Jiménez, J. J. (2001). *Sistemas operativos fundamentales*. Universidad de Cádiz.",
    "Grimaldi, C. (2026). *Introducción a los sistemas operativos* [Material de cátedra]. UCES.",
    "Grimaldi, C. (2026). *Gestión de procesos* [Material de cátedra]. UCES.",
    "Grimaldi, C. (2026). *Gestión de memoria* [Material de cátedra]. UCES.",
    "Silberschatz, A., Galvin, P. B., & Gagne, G. (2006). *Fundamentos de sistemas operativos* (7.ª ed.). McGraw-Hill.",
    "Stallings, W. (1997). *Sistemas operativos* (2.ª ed.). Prentice Hall.",
    "Tanenbaum, A. S. (2009). *Sistemas operativos modernos* (3.ª ed.). Pearson Educación.",
]


ACADEMIC_DATA = {
    "Universidad": "UCES",
    "Programa": "Tecnicatura Universitaria en Programación de Software",
    "Asignatura": "Sistemas Operativos",
    "Actividad": "Integrador, Parte 1",
    "Profesor/a": "Grimaldi, Camila",
    "Alumno/a": "Beloqui, Gonzalo",
    "Fecha entrega": "2026/05/21",
}


@dataclass
class Process:
    name: str
    burst: int
    arrival: int = 0


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;650;750;850&display=swap');

        :root {
            --uces-green: #008c5a;
            --uces-dark: #005b3f;
            --uces-light: #e9f7f0;
            --ink: #14213d;
            --muted: #526070;
            --line: #d7e2dc;
            --panel: #ffffff;
            --soft: #f5f8f7;
            --warn: #f6c343;
            --danger: #e06a5f;
            --blue: #2f6f9f;
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", Arial, sans-serif;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 1.25rem;
            padding-left: 1.4rem;
            padding-right: 1.4rem;
            max-width: 1380px;
        }

        [data-testid="stSidebar"] {
            min-width: 330px !important;
            max-width: 330px !important;
            width: 330px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            min-width: 330px !important;
            max-width: 330px !important;
            width: 330px !important;
            overflow-x: hidden;
            padding-top: .75rem;
            padding-left: .75rem;
            padding-right: .75rem;
        }

        [data-testid="stSidebarResizer"],
        [data-testid="stSidebarResizeHandle"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebar"] [style*="cursor: col-resize"] {
            display: none !important;
        }

        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--ink);
        }

        h1 {
            font-size: 2rem !important;
            margin-bottom: .35rem !important;
            line-height: 1.32 !important;
            padding-top: .35rem;
            overflow: visible !important;
        }

        h2 {
            font-size: 1.55rem !important;
            margin-top: .55rem !important;
            margin-bottom: .45rem !important;
        }

        [data-testid="stCaptionContainer"] {
            font-size: .78rem;
            margin-bottom: .45rem;
        }

        [data-testid="stHorizontalBlock"] {
            gap: .75rem;
        }

        [data-testid="stHeading"] {
            overflow: visible !important;
        }

        .page-header {
            display: block;
            padding-top: 1rem;
            padding-bottom: .65rem;
            margin-bottom: .35rem;
            min-height: 78px;
            overflow: visible !important;
        }

        .page-title {
            color: var(--ink);
            font-size: 2rem;
            font-weight: 850;
            line-height: 1.25;
            padding-top: 0;
            margin: 0 0 .55rem;
            overflow: visible !important;
            white-space: normal;
        }

        .page-subtitle {
            color: var(--muted);
            font-size: .82rem;
            margin: 0;
        }

        .stMultiSelect [data-baseweb="select"] {
            min-height: 40px;
        }

        [data-testid="stRadio"] > label {
            display: none !important;
        }

        .hero {
            border-top: 6px solid var(--uces-green);
            padding: 1.4rem 1.5rem 1.25rem;
            background: linear-gradient(90deg, var(--uces-light) 0%, #ffffff 70%);
            border-radius: 8px;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }

        .brand-row {
            display: flex;
            align-items: center;
            gap: .6rem;
            margin-bottom: .45rem;
            color: var(--uces-dark);
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: .02em;
            font-size: .9rem;
        }

        .brand-mark {
            width: 44px;
            min-width: 44px;
            height: 44px;
            border-radius: 6px;
            background: var(--uces-green);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
            font-size: .86rem;
            line-height: 1;
            overflow: visible;
        }

        .hero h1 {
            font-size: clamp(2rem, 4vw, 3.45rem);
            margin: 0 0 .4rem 0;
            line-height: 1.04;
        }

        .hero p {
            font-size: 1.05rem;
            color: var(--muted);
            margin: 0;
            max-width: 830px;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .55rem;
            margin: .7rem 0;
        }

        .metric-card, .mini-card, .justification-card {
            padding: .72rem .82rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
        }

        .metric-card {
            min-height: 104px;
        }

        .metric-card strong, .mini-card strong, .justification-card strong {
            display: block;
            font-size: .72rem;
            color: var(--uces-dark);
            text-transform: uppercase;
            font-weight: 800;
        }

        .metric-card span {
            display: block;
            font-size: 1.35rem;
            color: var(--ink);
            font-weight: 850;
            margin-top: .32rem;
        }

        .metric-card p, .mini-card p, .justification-card p {
            font-size: .86rem;
            color: var(--muted);
            margin: .38rem 0 0;
            line-height: 1.42;
        }

        .context-card {
            border: 1px solid var(--line);
            border-left: 5px solid var(--uces-green);
            border-radius: 8px;
            background: #fff;
            padding: 1rem 1.1rem;
            margin: .75rem 0 1rem;
        }

        .context-card strong {
            color: var(--uces-dark);
            display: block;
            font-size: .82rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: .25rem;
        }

        .context-card p {
            color: var(--ink);
            margin: .35rem 0;
            line-height: 1.45;
        }

        .context-card em {
            color: var(--muted);
            font-style: normal;
        }

        .mini-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .7rem;
            margin: .7rem 0 .75rem;
        }

        .stack-cards {
            display: flex;
            flex-direction: column;
            gap: .7rem;
            margin-top: .7rem;
        }

        .icon-strip {
            display: grid;
            grid-template-columns: repeat(5, minmax(120px, 1fr));
            gap: .65rem;
            margin: 1rem 0 1.2rem;
        }

        .icon-step {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .85rem;
            background: var(--panel);
            min-height: 118px;
        }

        .icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--uces-light);
            color: var(--uces-dark);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
            margin-bottom: .55rem;
        }

        .icon-step b {
            display: block;
            color: var(--ink);
            font-size: .96rem;
        }

        .icon-step small {
            color: var(--muted);
            font-size: .84rem;
        }

        .pipeline {
            position: relative;
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: .55rem;
            margin: .8rem 0 1rem;
        }

        .pipeline:before {
            content: "";
            position: absolute;
            left: 8%;
            right: 8%;
            top: 28px;
            height: 3px;
            background: var(--line);
        }

        .pipeline:after {
            content: "";
            position: absolute;
            top: 20px;
            left: 8%;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--uces-green);
            animation: travel 5s linear infinite;
        }

        @keyframes travel {
            0% {left: 8%;}
            100% {left: 88%;}
        }

        .pipe-node {
            position: relative;
            z-index: 1;
            text-align: center;
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .75rem .45rem;
            min-height: 86px;
        }

        .pipe-node b {
            display: block;
            color: var(--ink);
        }

        .pipe-node small {
            color: var(--muted);
        }

        .memory-grid {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: .35rem;
            margin: .75rem 0;
        }

        .frame {
            min-height: 56px;
            border-radius: 6px;
            border: 1px solid var(--line);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: var(--ink);
            background: var(--soft);
        }

        .used {background: #dff2ea; border-color: #8acdb2;}
        .waste {background: #fff4cf; border-color: var(--warn);}
        .risk {background: #fde7e3; border-color: var(--danger);}
        .free {background: #f8faf9; color: #9aa8a2;}

        .gantt {
            display: flex;
            overflow-x: auto;
            gap: 3px;
            padding: .35rem 0 .8rem;
        }

        .slice {
            min-width: 74px;
            padding: .58rem .45rem;
            text-align: center;
            border-radius: 6px;
            background: #dcecf5;
            border: 1px solid #9dc4da;
            font-size: .9rem;
            color: var(--ink);
        }

        .decision {
            border-left: 5px solid var(--uces-green);
            background: var(--uces-light);
            border-radius: 8px;
            padding: .78rem .9rem;
            color: var(--ink);
            font-weight: 600;
            margin-top: .55rem;
            margin-bottom: .7rem;
        }

        .security-scale {
            margin: .32rem 0 .28rem;
        }

        .security-labels {
            display: flex;
            justify-content: space-between;
            color: var(--muted);
            font-size: .72rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: .18rem;
        }

        .security-track {
            height: 15px;
            border-radius: 999px;
            background: #e8eeeb;
            border: 1px solid var(--line);
            overflow: hidden;
            position: relative;
        }

        .security-fill {
            height: 100%;
            border-radius: 999px;
            transition: width .25s ease, background .25s ease;
        }

        .security-marker {
            position: absolute;
            top: -4px;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            border: 3px solid #fff;
            box-shadow: 0 2px 8px rgba(20,33,61,.22);
            transform: translateX(-50%);
        }

        .control-detail {
            border: 1px solid var(--line);
            background: #fff;
            border-radius: 8px;
            padding: .5rem .65rem;
            margin-bottom: .52rem;
        }

        .mini-card,
        .control-detail,
        .sidebar-card {
            box-sizing: border-box;
        }

        .control-detail b {
            font-size: .9rem;
        }

        .control-detail b {
            color: var(--ink);
        }

        .control-detail small {
            color: var(--muted);
            display: block;
            line-height: 1.28;
            margin-top: .16rem;
            font-size: .78rem;
        }

        .sidebar-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .55rem .65rem;
            background: #ffffff;
            margin-bottom: .55rem;
        }

        .sidebar-card small {
            display: block;
            color: var(--uces-dark);
            font-size: .66rem;
            font-weight: 800;
            text-transform: uppercase;
        }

        .sidebar-card span {
            display: block;
            color: var(--ink);
            font-weight: 650;
            font-size: .8rem;
            margin-top: .08rem;
        }

        .nav-title {
            color: var(--uces-dark);
            font-size: .7rem;
            font-weight: 850;
            text-transform: uppercase;
            margin: .55rem 0 .18rem;
        }

        .apa-list {
            border-top: 1px solid var(--line);
            padding-top: .5rem;
            color: var(--ink);
            font-size: .95rem;
        }

        @media (max-width: 900px) {
            .kpi-grid, .icon-strip, .mini-grid, .pipeline {grid-template-columns: 1fr;}
            .memory-grid {grid-template-columns: repeat(4, 1fr);}
            .pipeline:before, .pipeline:after {display: none;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, value: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <strong>{title}</strong>
            <span>{value}</span>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mini_card(title: str, body: str) -> str:
    return f'<div class="mini-card"><strong>{title}</strong><p>{body}</p></div>'


def context_card(title: str, explanation: str, example: str, balance: str) -> None:
    st.markdown(
        f"""
        <div class="context-card">
            <strong>{title}</strong>
            <p>{explanation}</p>
            <p><em>Ejemplo real:</em> {example}</p>
            <p><em>Costo / seguridad / eficiencia:</em> {balance}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def icon_step(number: str, title: str, body: str) -> str:
    return (
        '<div class="icon-step">'
        f'<div class="icon">{number}</div>'
        f"<b>{title}</b>"
        f"<small>{body}</small>"
        "</div>"
    )


def pipeline(nodes: list[tuple[str, str]]) -> None:
    html = '<div class="pipeline">'
    for title, body in nodes:
        html += f'<div class="pipe-node"><b>{title}</b><small>{body}</small></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def decision(text: str) -> None:
    st.markdown(f'<div class="decision">{text}</div>', unsafe_allow_html=True)


def security_bar(active_count: int, total: int) -> None:
    ratio = active_count / total if total else 0
    percent = int(ratio * 100)
    if ratio < 0.34:
        marker_color = "#e06a5f"
        level = "Riesgo alto"
    elif ratio < 0.67:
        marker_color = "#f6c343"
        level = "Riesgo medio"
    else:
        marker_color = "#008c5a"
        level = "Riesgo bajo"

    st.markdown(
        f"""
            <div class="security-scale">
                <div class="security-labels"><span>Inseguro</span><span>{level}</span><span>Seguro</span></div>
                <div class="security-track">
                <div class="security-fill" style="width:{percent}%; background:{marker_color};"></div>
                <div class="security-marker" style="left:{percent}%; background:{marker_color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def control_details(selected: list[str]) -> None:
    details = {
        "Usuarios estándar": {
            "active": "Impide que los alumnos instalen software, cambien drivers o modifiquen la seguridad del equipo.",
            "inactive": "Riesgo: un alumno con privilegios puede cambiar configuraciones, instalar software no autorizado o afectar a otros usuarios.",
        },
        "UAC activo": {
            "active": "Exige confirmación elevada para cambios administrativos y frena instalaciones o ajustes accidentales.",
            "inactive": "Riesgo: un instalador o clic malicioso puede modificar el sistema sin una barrera de confirmación.",
        },
        "BitLocker": {
            "active": "Cifra el disco y protege datos académicos si se pierde el equipo o se retira la unidad.",
            "inactive": "Riesgo: ante robo, extravío o extracción del disco, los archivos locales podrían leerse sin autorización.",
        },
        "Defender + Firewall": {
            "active": "Reduce malware y conexiones no autorizadas sin sumar costo de una herramienta externa.",
            "inactive": "Riesgo: aumenta la exposición a malware, descargas inseguras y conexiones entrantes no deseadas.",
        },
        "Políticas de grupo": {
            "active": "Bloquean paneles, instalaciones, herramientas críticas y cambios de configuración del aula.",
            "inactive": "Riesgo: cada equipo queda más dependiente del buen uso del alumno y se vuelve más difícil sostener una política común.",
        },
        "Imagen base": {
            "active": "Permite restaurar una terminal a estado conocido si un perfil se degrada o una práctica deja fallas.",
            "inactive": "Riesgo: recuperar un equipo roto lleva más tiempo y puede afectar el inicio de una clase o examen.",
        },
    }
    for name, messages in details.items():
        is_active = name in selected
        status = "Activo" if is_active else "Pendiente"
        body = messages["active"] if is_active else messages["inactive"]
        st.markdown(
            f"""
            <div class="control-detail">
                <b>{status}: {name}</b>
                <small>{body}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


def phase_header(phase: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def rr_schedule(processes: list[Process], quantum: int) -> tuple[list[tuple[str, int, int]], dict[str, int]]:
    remaining = {p.name: p.burst for p in processes}
    completion: dict[str, int] = {}
    time = 0
    queue = [p.name for p in processes if p.arrival <= 0]
    arrivals = sorted([p for p in processes if p.arrival > 0], key=lambda p: p.arrival)
    timeline: list[tuple[str, int, int]] = []

    while queue or arrivals:
        while arrivals and arrivals[0].arrival <= time:
            queue.append(arrivals.pop(0).name)
        if not queue:
            time = arrivals[0].arrival
            continue
        current = queue.pop(0)
        run = min(quantum, remaining[current])
        start, end = time, time + run
        timeline.append((current, start, end))
        time = end
        remaining[current] -= run
        while arrivals and arrivals[0].arrival <= time:
            queue.append(arrivals.pop(0).name)
        if remaining[current] > 0:
            queue.append(current)
        else:
            completion[current] = time
    return timeline, completion


def executive_view() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Infraestructura académica sin colapsos</h1>
            <p>Propuesta de IT para una academia tecnológica: estaciones seguras, procesos aislados, memoria paginada y CPU repartida de forma equitativa.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        card("Fase 1", "Windows + control", "Plataforma de escritorio con cuentas sin privilegios y herramientas nativas.")
    with c2:
        card("Fase 2", "Paginación + MMU", "Memoria en bloques fijos, traducción de direcciones y protección.")
    with c3:
        card("Directorio", "Round Robin", "El render 3D no bloquea exámenes ni servicios críticos.")

    pipeline(
        [
            ("Alumno", "Aplicación"),
            ("Proceso", "Aislamiento"),
            ("MMU", "Traducción"),
            ("RAM", "Páginas"),
            ("CPU", "Turnos"),
        ]
    )

    decision(
        "Mensaje central: la continuidad académica depende de separar permisos, memoria y CPU para que una carga pesada no comprometa la clase completa."
    )


def selection_security_view() -> None:
    phase_header(
        "Fase 1",
        "1. Selección y Seguridad",
        "Sistema base monousuario de escritorio y controles para impedir cambios administrativos.",
    )

    left, right = st.columns([1.05, .95])
    with left:
        st.subheader("Criterio ejecutivo")
        decision("Windows 11 Pro como sistema base para estaciones del profesor y alumnos.")
        st.markdown(
            '<div class="mini-grid">'
            + mini_card("Compatibilidad", "Reduce riesgo operativo con navegadores de examen, software 3D, drivers y periféricos.")
            + mini_card("Administración", "Permite separar cuenta de IT/profesor y usuarios estándar para alumnos.")
            + mini_card("Seguridad nativa", "UAC, Defender, Firewall, BitLocker, permisos NTFS y actualizaciones.")
            + mini_card("Soporte del aula", "Facilita restaurar perfiles, aplicar imagen base y mantener una política común.")
            + "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="stack-cards">'
            + mini_card("Costo / seguridad / eficiencia", "El costo inicial es moderado; la seguridad sube por cuentas estándar, cifrado y políticas; la eficiencia mejora porque IT puede administrar y restaurar equipos sin rediseñar todo el entorno.")
            + mini_card("Ejemplo real", "En una clase con Blender, navegadores de examen y proyectores, perder tiempo instalando drivers o resolviendo permisos durante la clase tiene más impacto que el costo de una licencia ya administrable.")
            + "</div>",
            unsafe_allow_html=True,
        )
    with right:
        st.subheader("Controles de aula")
        selected = st.multiselect(
            "Seleccionar controles activos",
            ["Usuarios estándar", "UAC activo", "BitLocker", "Defender + Firewall", "Políticas de grupo", "Imagen base"],
            default=["Usuarios estándar", "UAC activo", "Defender + Firewall", "Políticas de grupo"],
        )
        security_bar(len(selected), 6)
        st.caption(f"{len(selected)} de 6 controles activos. Cada control agrega seguridad, pero también administración y mantenimiento.")
        control_details(selected)



def process_isolation_view() -> None:
    phase_header(
        "Fase 1",
        "2. Aislamiento de Procesos",
        "Cada aplicación debe ejecutar en su propio espacio de memoria virtual protegido.",
    )
    context_card(
        "Criterio ejecutivo",
        "El aislamiento de procesos convierte errores individuales en fallas contenidas. Para el Directorio, esto significa continuidad: si una aplicación se bloquea, no arrastra al sistema completo ni compromete datos de otra actividad.",
        "Durante un examen online, un alumno puede tener abierto un IDE o una herramienta de render. Si el render consume memoria o falla, el navegador del examen debe seguir protegido.",
        "El costo es el overhead normal de memoria virtual y cambios de contexto; la seguridad aumenta por separación de espacios; la eficiencia mejora porque se evitan reinicios y pérdida de tiempo de clase.",
    )

    st.markdown(
        '<div class="mini-grid">'
        + mini_card("Estabilidad", "Un fallo en un render 3D no debe tirar el navegador de examen.")
        + mini_card("Seguridad", "Un proceso no puede leer ni escribir memoria ajena sin autorización.")
        + mini_card("Recuperación", "IT puede cerrar una app problemática sin reiniciar el equipo.")
        + mini_card("Concurrencia", "IDE, navegador, antivirus y servicios del SO conviven sin interferirse.")
        + "</div>",
        unsafe_allow_html=True,
    )

    app_a, app_b = st.columns(2)
    with app_a:
        st.subheader("Riesgo sin aislamiento")
        st.markdown(
            """
            <div class="memory-grid">
                <div class="frame used">IDE</div><div class="frame used">IDE</div><div class="frame risk">Error</div><div class="frame used">Examen</div>
                <div class="frame used">Render</div><div class="frame risk">Daño</div><div class="frame used">SO</div><div class="frame used">Datos</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.error("Una falla puede contaminar otras tareas.")
    with app_b:
        st.subheader("Modelo recomendado")
        st.markdown(
            """
            <div class="memory-grid">
                <div class="frame used">IDE</div><div class="frame used">IDE</div><div class="frame free">Límite</div><div class="frame used">Examen</div>
                <div class="frame used">Examen</div><div class="frame free">Límite</div><div class="frame used">Render</div><div class="frame used">Render</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.success("El SO bloquea accesos indebidos.")

    pipeline(
        [
            ("App", "Solicita memoria"),
            ("Proceso", "Espacio propio"),
            ("SO", "Tabla de páginas"),
            ("MMU", "Valida acceso"),
            ("RAM", "Marco físico"),
        ]
    )

    decision("Resultado operativo: una aplicación defectuosa se trata como incidente aislado, no como caída general del aula.")


def paging_view() -> None:
    phase_header(
        "Fase 2",
        "3. Análisis de Deficiencias: Paginación",
        "El servidor presenta fragmentación y bajo aprovechamiento de RAM.",
    )
    context_card(
        "Criterio ejecutivo",
        "La paginación se recomienda porque evita depender de bloques contiguos de memoria. El servidor puede cargar partes de procesos en marcos dispersos y sostener varias tareas simultáneas.",
        "Si el servidor atiende archivos, aulas virtuales y renderizados, puede tener RAM libre repartida en huecos. Sin paginación, esos huecos pueden no servir; con paginación, se aprovechan.",
        "El costo es gestionar tablas de páginas y aceptar una pequeña fragmentación interna; la seguridad mejora por separación de páginas; la eficiencia sube al reducir fragmentación externa y fallos de asignación.",
    )

    c1, c2 = st.columns([.9, 1.1])
    with c1:
        page_size = st.slider("Tamaño de página / marco (MB)", min_value=1, max_value=8, value=4)
        process_size = st.slider("Memoria requerida por proceso (MB)", min_value=5, max_value=48, value=22)
        frames_needed = math.ceil(process_size / page_size)
        internal_waste = frames_needed * page_size - process_size
        st.metric("Páginas necesarias", frames_needed)
        st.metric("Fragmentación interna", f"{internal_waste} MB")
    with c2:
        cells = []
        for i in range(24):
            if i < frames_needed:
                label = f"P{i}"
                cls = "used"
            elif i < frames_needed + internal_waste:
                label = "int."
                cls = "waste"
            else:
                label = "libre"
                cls = "free"
            cells.append(f'<div class="frame {cls}">{label}</div>')
        st.markdown(f'<div class="memory-grid">{"".join(cells)}</div>', unsafe_allow_html=True)
        st.caption("Los marcos libres pueden estar dispersos; la paginación los aprovecha igual.")

    st.markdown(
        '<div class="mini-grid">'
        + mini_card("Problema", "La asignación variable deja huecos que no siempre sirven para nuevos procesos.")
        + mini_card("Solución", "Páginas y marcos de tamaño fijo evitan buscar un bloque contiguo grande.")
        + mini_card("Costo aceptado", "Puede quedar fragmentación interna en el último marco.")
        + mini_card("Beneficio", "Mejor aprovechamiento de RAM y menos fallos por falta de espacio contiguo.")
        + "</div>",
        unsafe_allow_html=True,
    )

    decision("Resultado operativo: el servidor usa mejor la RAM disponible y reduce el riesgo de quedarse sin bloques contiguos útiles.")


def mmu_view() -> None:
    phase_header(
        "Fase 2",
        "4. Rol del Hardware: MMU",
        "La Unidad de Gestión de Memoria traduce direcciones virtuales y protege accesos.",
    )
    context_card(
        "Criterio ejecutivo",
        "La MMU es el componente que vuelve práctica y segura la memoria virtual: traduce direcciones en hardware, verifica permisos y habilita fallos de página controlados por el sistema operativo.",
        "Cuando un navegador de examen pide leer memoria, la MMU valida si esa dirección pertenece a su proceso. Si una app intenta leer memoria del examen, el acceso se bloquea.",
        "El costo viene incluido en el hardware moderno; la seguridad aumenta por control de accesos; la eficiencia mejora porque la traducción ocurre en hardware y no por software lento.",
    )

    virtual_page = st.number_input("Página virtual solicitada", min_value=0, max_value=7, value=3)
    offset = st.number_input("Desplazamiento", min_value=0, max_value=4095, value=128)
    table = {0: 5, 1: 1, 2: 7, 3: 2, 4: 9, 5: 4, 6: 12, 7: 6}
    frame = table[int(virtual_page)]
    physical = frame * 4096 + int(offset)

    st.markdown(
        '<div class="icon-strip">'
        + icon_step("CPU", f"Página {virtual_page}", f"Offset {offset}")
        + icon_step("MMU", "Consulta", "Tabla de páginas")
        + icon_step("TAB", f"Marco {frame}", "Traducción válida")
        + icon_step("RAM", f"{physical}", "Dirección física")
        + icon_step("OK", "Permisos", "Lectura / escritura")
        + "</div>",
        unsafe_allow_html=True,
    )

    pipeline(
        [
            ("Dirección virtual", "Programa"),
            ("MMU", "Hardware"),
            ("Tabla", "Mapeo"),
            ("Permisos", "Protección"),
            ("Dirección física", "RAM"),
        ]
    )

    decision("Resultado operativo: la traducción y protección de memoria ocurren a velocidad de hardware.")


def round_robin_view() -> None:
    phase_header(
        "Enfoque de consultoría",
        "5. Round Robin para clases 3D y exámenes online",
        "Planificación equitativa para que ninguna tarea monopolice la CPU.",
    )
    context_card(
        "Criterio ejecutivo",
        "Round Robin se defiende porque reparte CPU en turnos. No maximiza cada tarea individual, pero protege la respuesta percibida cuando conviven actividades pesadas e interactivas.",
        "En una clase, un render 3D puede necesitar mucho CPU. El examen online, el antivirus y el sistema no pueden quedar esperando hasta que termine el render.",
        "El costo es mayor cantidad de cambios de contexto si el quantum es bajo; la seguridad operativa sube porque servicios críticos siguen respondiendo; la eficiencia del aula mejora porque todos los procesos avanzan.",
    )

    quantum = st.slider("Quantum de CPU", min_value=1, max_value=6, value=3)
    p1 = st.slider("Render 3D", min_value=2, max_value=18, value=12)
    p2 = st.slider("Examen online", min_value=2, max_value=18, value=5)
    p3 = st.slider("IDE del alumno", min_value=2, max_value=18, value=8)
    p4 = st.slider("Sistema / antivirus", min_value=2, max_value=18, value=4)
    processes = [
        Process("Render", p1),
        Process("Examen", p2),
        Process("IDE", p3),
        Process("Sistema", p4),
    ]
    timeline, completion = rr_schedule(processes, quantum)
    slices = "".join([f'<div class="slice"><b>{name}</b><br>{start}-{end}</div>' for name, start, end in timeline])
    st.markdown(f'<div class="gantt">{slices}</div>', unsafe_allow_html=True)

    rows = []
    for p in processes:
        turnaround = completion[p.name] - p.arrival
        waiting = turnaround - p.burst
        rows.append({"Proceso": p.name, "CPU requerida": p.burst, "Finaliza en": completion[p.name], "Espera total": waiting})
    st.dataframe(rows, hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="mini-grid">'
        + mini_card("Equidad", "Todos los procesos reciben turnos de CPU.")
        + mini_card("Respuesta", "El examen conserva interacción aunque haya renderizado.")
        + mini_card("Riesgo", "Quantum demasiado bajo aumenta cambios de contexto.")
        + mini_card("Criterio", "Ajustar quantum para balancear fluidez y eficiencia.")
        + "</div>",
        unsafe_allow_html=True,
    )

    decision("Resultado operativo: el render avanza sin bloquear exámenes, navegadores ni servicios del sistema.")


def board_view() -> None:
    phase_header(
        "Cierre",
        "Decisión integrada para el Directorio",
        "Síntesis técnica presentada como defensa ejecutiva.",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        card("Fase 1", "Control de aula", "Windows Pro, usuarios estándar y políticas de seguridad.")
    with c2:
        card("Fase 2", "Memoria estable", "Paginación y MMU para aislamiento y aprovechamiento de RAM.")
    with c3:
        card("Operación", "CPU equitativa", "Round Robin evita monopolios de procesos pesados.")

    decision(
        "Decisión final: priorizar continuidad académica. La arquitectura propuesta evita que una tarea pesada o defectuosa comprometa clases, exámenes o datos institucionales."
    )

    st.subheader("Referencias bibliográficas")
    st.markdown('<div class="apa-list">', unsafe_allow_html=True)
    for ref in REFERENCIAS:
        st.markdown(f"- {ref}")
    st.markdown("</div>", unsafe_allow_html=True)


def sidebar() -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-row"><div class="brand-mark">UCES</div><div>Sistemas Operativos</div></div>
            """,
            unsafe_allow_html=True,
        )
        section = st.radio(
            "",
            [
                "Resumen ejecutivo",
                "Fase 1 / 1. Selección y Seguridad",
                "Fase 1 / 2. Aislamiento de Procesos",
                "Fase 2 / 3. Paginación",
                "Fase 2 / 4. MMU",
                "Directorio / 5. Round Robin",
                "Directorio / Cierre y bibliografía",
            ],
        )
        st.divider()
        for key, value in ACADEMIC_DATA.items():
            st.markdown(
                f"""
                <div class="sidebar-card">
                    <small>{key}</small>
                    <span>{value}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    return section


def main() -> None:
    inject_css()
    section = sidebar()

    if section == "Resumen ejecutivo":
        executive_view()
    elif section == "Fase 1 / 1. Selección y Seguridad":
        selection_security_view()
    elif section == "Fase 1 / 2. Aislamiento de Procesos":
        process_isolation_view()
    elif section == "Fase 2 / 3. Paginación":
        paging_view()
    elif section == "Fase 2 / 4. MMU":
        mmu_view()
    elif section == "Directorio / 5. Round Robin":
        round_robin_view()
    else:
        board_view()


if __name__ == "__main__":
    main()
