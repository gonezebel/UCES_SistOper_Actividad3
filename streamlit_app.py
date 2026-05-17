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
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1260px;
        }

        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--ink);
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

        .hero:after {
            content: "";
            position: absolute;
            right: -40px;
            top: -70px;
            width: 220px;
            height: 220px;
            border: 28px solid rgba(0, 140, 90, .12);
            border-radius: 50%;
        }

        .brand-row {
            display: flex;
            align-items: center;
            gap: .8rem;
            margin-bottom: .7rem;
            color: var(--uces-dark);
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: .02em;
        }

        .brand-mark {
            width: 54px;
            height: 54px;
            border-radius: 6px;
            background: var(--uces-green);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
            font-size: 1rem;
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
            max-width: 790px;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .75rem;
            margin: 1rem 0;
        }

        .metric-card, .mini-card {
            padding: 1rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
        }

        .metric-card {
            min-height: 126px;
        }

        .metric-card strong, .mini-card strong {
            display: block;
            font-size: .78rem;
            color: var(--uces-dark);
            text-transform: uppercase;
            font-weight: 800;
        }

        .metric-card span {
            display: block;
            font-size: 1.55rem;
            color: var(--ink);
            font-weight: 850;
            margin-top: .32rem;
        }

        .metric-card p, .mini-card p {
            font-size: .92rem;
            color: var(--muted);
            margin: .5rem 0 0;
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
            padding: 1rem;
            color: var(--ink);
            font-weight: 600;
        }

        .sidebar-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .78rem;
            background: #ffffff;
            margin-bottom: .65rem;
        }

        .sidebar-card small {
            display: block;
            color: var(--uces-dark);
            font-size: .72rem;
            font-weight: 800;
            text-transform: uppercase;
        }

        .sidebar-card span {
            display: block;
            color: var(--ink);
            font-weight: 650;
            font-size: .9rem;
            margin-top: .12rem;
        }

        .apa-list {
            border-top: 1px solid var(--line);
            padding-top: .5rem;
            color: var(--ink);
            font-size: .95rem;
        }

        @media (max-width: 900px) {
            .kpi-grid, .icon-strip {grid-template-columns: 1fr;}
            .memory-grid {grid-template-columns: repeat(4, 1fr);}
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


def icon_step(number: str, title: str, body: str) -> str:
    return (
        '<div class="icon-step">'
        f'<div class="icon">{number}</div>'
        f"<b>{title}</b>"
        f"<small>{body}</small>"
        "</div>"
    )


def decision(text: str) -> None:
    st.markdown(f'<div class="decision">{text}</div>', unsafe_allow_html=True)


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
            <div class="brand-row"><div class="brand-mark">UCES</div><div>Sistemas Operativos</div></div>
            <h1>Infraestructura académica sin colapsos</h1>
            <p>Propuesta de IT para una academia tecnológica: estaciones seguras, memoria estable y CPU repartida por prioridad operativa.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        card("Plataforma", "Windows 11 Pro", "Compatibilidad, administración y seguridad nativa.")
    with c2:
        card("Control operativo", "Memoria aislada", "Cada app trabaja en su espacio protegido.")
    with c3:
        card("Continuidad", "Paginación + RR", "RAM aprovechada y CPU por turnos.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="icon-strip">'
        + icon_step("01", "Alumno", "Abre IDE, navegador o render 3D.")
        + icon_step("02", "Proceso", "El SO lo aísla del resto.")
        + icon_step("03", "MMU", "Traduce direcciones y valida permisos.")
        + icon_step("04", "RAM", "Páginas en marcos fijos.")
        + icon_step("05", "CPU", "Round Robin evita monopolios.")
        + "</div>",
        unsafe_allow_html=True,
    )

    decision(
        "Recomendación al Directorio: adoptar una base Windows administrada, con cuentas sin privilegios, paginación activa y planificación equitativa para proteger clases, exámenes y trabajos pesados."
    )


def os_choice_view() -> None:
    st.header("Decisión 1: plataforma y seguridad")
    c1, c2 = st.columns([1.05, .95])
    with c1:
        st.markdown(
            '<div class="icon-strip">'
            + icon_step("A", "Compatibilidad", "Software educativo, navegadores y drivers.")
            + icon_step("B", "Gobierno", "Usuarios estándar y políticas locales.")
            + icon_step("C", "Protección", "UAC, Defender, Firewall y BitLocker.")
            + "</div>",
            unsafe_allow_html=True,
        )
        decision("Elección ejecutiva: Windows 11 Pro en las estaciones de trabajo.")
    with c2:
        selected = st.multiselect(
            "Controles de aula",
            ["Usuarios estándar", "UAC activo", "BitLocker", "Defender + Firewall", "Políticas de grupo", "Imagen base"],
            default=["Usuarios estándar", "UAC activo", "Defender + Firewall", "Políticas de grupo"],
        )
        st.progress(min(len(selected) / 6, 1.0), text=f"{len(selected)} de 6 controles activos")
        st.caption("Objetivo: alumnos operan, IT administra.")


def process_isolation_view() -> None:
    st.header("Decisión 2: aislamiento de procesos")
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

    decision(
        "Impacto directivo: si un render 3D se bloquea, el examen online y el sistema siguen operativos."
    )


def paging_view() -> None:
    st.header("Decisión 3: paginación contra fragmentación")
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
        st.caption("La RAM se usa en marcos fijos; no requiere bloques contiguos.")

    decision(
        "Resultado esperado: menos fragmentación externa, mejor aprovechamiento de RAM y menor probabilidad de colapso por huecos inutilizables."
    )


def mmu_view() -> None:
    st.header("Decisión 4: MMU como control de acceso")
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
    decision(
        "La MMU convierte direcciones virtuales en físicas, valida permisos y dispara fallos de página cuando falta información en RAM."
    )


def round_robin_view() -> None:
    st.header("Decisión 5: Round Robin para cargas mixtas")
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
    decision(
        "Round Robin mantiene respuesta visible: el render avanza, pero no bloquea el examen ni los servicios del sistema."
    )


def board_view() -> None:
    st.header("Cierre para Directorio")
    st.markdown(
        '<div class="kpi-grid">',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        card("Riesgo reducido", "Aula controlada", "Permisos, cifrado y antimalware.")
    with c2:
        card("Memoria estable", "Paginación", "Sin depender de bloques contiguos.")
    with c3:
        card("Respuesta", "Round Robin", "Turnos de CPU para cargas mixtas.")
    st.markdown("</div>", unsafe_allow_html=True)

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
            <div class="brand-row"><div class="brand-mark">UCES</div><div>Entrega universitaria</div></div>
            """,
            unsafe_allow_html=True,
        )
        section = st.radio(
            "Recorrido ejecutivo",
            [
                "Apertura",
                "Plataforma",
                "Aislamiento",
                "Paginación",
                "MMU",
                "Round Robin",
                "Cierre",
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

    if section == "Apertura":
        executive_view()
    elif section == "Plataforma":
        os_choice_view()
    elif section == "Aislamiento":
        process_isolation_view()
    elif section == "Paginación":
        paging_view()
    elif section == "MMU":
        mmu_view()
    elif section == "Round Robin":
        round_robin_view()
    else:
        board_view()


if __name__ == "__main__":
    main()
