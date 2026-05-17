import math
from dataclasses import dataclass

import streamlit as st


st.set_page_config(
    page_title="Actividad 3 | Sistemas Operativos",
    page_icon="SO",
    layout="wide",
)


REFERENCIAS = [
    "Unidad 1 - Introduccion al Sistema Operativo: definicion del SO, objetivos, Windows/macOS, seguridad y componentes.",
    "Guia Unidad 2 - Gestion de Procesos: procesos, hilos, estados, planificacion Round Robin y proteccion.",
    "Guia Unidad 3 - Gestion de Memoria: memoria virtual, paginacion, MMU, fragmentacion, reemplazo y rendimiento.",
    "Silberschatz, Galvin y Gagne. Fundamentos de Sistemas Operativos, 7ma ed.",
    "Tanenbaum. Sistemas Operativos Modernos, 3ra ed.",
    "Stallings. Sistemas Operativos, 2da ed.",
]


@dataclass
class Process:
    name: str
    burst: int
    arrival: int = 0


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem;}
        h1, h2, h3 {letter-spacing: 0;}
        .hero {
            border-left: 6px solid #2563eb;
            padding: 1.25rem 1.5rem;
            background: linear-gradient(90deg, #eff6ff 0%, #ffffff 72%);
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .hero h1 {font-size: clamp(2rem, 4vw, 3.6rem); margin: 0 0 .35rem 0;}
        .hero p {font-size: 1.05rem; color: #374151; margin: 0;}
        .metric-card {
            padding: 1rem;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: #ffffff;
            min-height: 132px;
        }
        .metric-card strong {display:block; font-size: .82rem; color:#475569; text-transform: uppercase;}
        .metric-card span {display:block; font-size: 1.45rem; font-weight: 750; margin-top:.35rem;}
        .metric-card p {font-size:.94rem; color:#4b5563; margin:.55rem 0 0 0;}
        .flow {
            display: grid;
            grid-template-columns: repeat(5, minmax(110px, 1fr));
            gap: .65rem;
            align-items: stretch;
            margin: .75rem 0 1rem 0;
        }
        .flow-step {
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: .8rem;
            background: #fff;
            text-align: center;
            min-height: 94px;
        }
        .flow-step b {display:block; color:#0f172a;}
        .flow-step small {color:#475569;}
        .memory-grid {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: .35rem;
            margin: .7rem 0;
        }
        .frame {
            min-height: 54px;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight: 700;
            color:#0f172a;
            background:#f1f5f9;
        }
        .used {background:#dbeafe; border-color:#60a5fa;}
        .waste {background:#fee2e2; border-color:#fca5a5;}
        .free {background:#f8fafc; color:#94a3b8;}
        .gantt {
            display:flex;
            overflow-x:auto;
            gap:2px;
            padding:.35rem 0 .8rem 0;
        }
        .slice {
            min-width: 72px;
            padding:.55rem .4rem;
            text-align:center;
            border-radius: 6px;
            background:#e0f2fe;
            border:1px solid #7dd3fc;
            font-size:.9rem;
        }
        .callout {
            border: 1px solid #bfdbfe;
            background:#eff6ff;
            border-radius:8px;
            padding: 1rem;
        }
        @media (max-width: 900px) {
            .flow {grid-template-columns: 1fr;}
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
            <h1>Academia Tecnologica: Infraestructura sin Colapsos</h1>
            <p>Defensa ejecutiva de decisiones de sistema operativo, memoria y planificacion para clases de renderizado 3D y examenes online.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        card("Decision base", "Windows 11 Pro", "Entorno monousuario de escritorio, compatible con software educativo, drivers y herramientas de administracion.")
    with c2:
        card("Riesgo controlado", "Aislamiento", "Cada aplicacion corre en su propio espacio de memoria virtual para evitar interferencias entre alumnos.")
    with c3:
        card("Servidor estable", "Paginacion + RR", "La memoria se administra en bloques fijos y la CPU se reparte por turnos para sostener respuesta interactiva.")

    st.subheader("Tesis para el Directorio")
    st.write(
        "La academia necesita equipos faciles de operar, seguros para usuarios no administradores y capaces de sostener carga mixta: "
        "renderizado 3D, navegadores, IDEs y examenes online. La propuesta combina Windows 11 Pro en las estaciones, politicas de "
        "restriccion, memoria virtual con paginacion y planificacion Round Robin para que ningun proceso monopolice el sistema."
    )

    st.markdown(
        """
        <div class="flow">
            <div class="flow-step"><b>1. Usuario alumno</b><small>Ejecuta navegador, IDE o motor 3D.</small></div>
            <div class="flow-step"><b>2. Proceso aislado</b><small>El SO crea espacio de direcciones propio.</small></div>
            <div class="flow-step"><b>3. MMU</b><small>Traduce direcciones virtuales a fisicas.</small></div>
            <div class="flow-step"><b>4. Paginacion</b><small>RAM en marcos fijos, sin huecos inutiles grandes.</small></div>
            <div class="flow-step"><b>5. Round Robin</b><small>Turnos de CPU para respuesta pareja.</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def os_choice_view() -> None:
    st.header("Fase 1: Seleccion y Seguridad")
    st.write(
        "El sistema recomendado para la estacion del profesor y las terminales de alumnos es Windows 11 Pro. "
        "La bibliografia de Unidad 1 destaca que Windows ofrece amplia compatibilidad de hardware/software, herramientas nativas "
        "de seguridad, administracion de cuentas, BitLocker, UAC, Defender y politicas de grupo. Para una academia nueva, esa "
        "compatibilidad reduce friccion operativa y facilita soporte."
    )

    left, right = st.columns([1.15, .85])
    with left:
        st.subheader("Justificacion ejecutiva")
        st.markdown(
            """
            - **Compatibilidad:** drivers, impresoras, proyectores, suites educativas, navegadores de examen y software 3D suelen estar mejor cubiertos.
            - **Administracion:** usuarios estandar para alumnos, cuenta administradora separada para IT/profesor y politicas locales o de grupo.
            - **Seguridad:** Microsoft Defender, Firewall, BitLocker, UAC, Windows Update y permisos NTFS.
            - **Continuidad:** si un alumno rompe su perfil, no compromete al equipo ni al resto de usuarios.
            """
        )
    with right:
        st.subheader("Controles nativos")
        selected = st.multiselect(
            "Armar politica de aula",
            ["Usuarios estandar", "UAC activo", "BitLocker", "Defender + Firewall", "Politicas de grupo", "Restauracion/imagen base"],
            default=["Usuarios estandar", "UAC activo", "Defender + Firewall", "Politicas de grupo"],
        )
        st.progress(min(len(selected) / 6, 1.0), text=f"{len(selected)} de 6 controles seleccionados")

    st.info(
        "Respuesta sintetica: se elige Windows 11 Pro porque es un entorno monousuario de escritorio adecuado para puestos individuales, "
        "pero permite control administrativo centralizado. Los alumnos usan cuentas sin privilegios; IT conserva administracion, cifrado, "
        "antimalware, politicas y auditoria."
    )


def process_isolation_view() -> None:
    st.header("Fase 1: Aislamiento de Procesos")
    st.write(
        "Segun la Unidad 2, un proceso es un programa en ejecucion con recursos propios; segun la Unidad 3, la memoria virtual y los "
        "espacios de direcciones mantienen separados a los procesos. Esa separacion es indispensable en un aula: si un render, un IDE "
        "o un navegador falla, no debe corromper la memoria de un examen online ni del sistema."
    )
    app_a, app_b = st.columns(2)
    with app_a:
        st.subheader("Sin aislamiento")
        st.markdown(
            """
            <div class="memory-grid">
                <div class="frame used">IDE</div><div class="frame used">IDE</div><div class="frame waste">Error</div><div class="frame used">Examen</div>
                <div class="frame used">Render</div><div class="frame waste">Corrupcion</div><div class="frame used">SO</div><div class="frame used">Datos</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning("Un proceso podria escribir donde no corresponde y afectar a otros.")
    with app_b:
        st.subheader("Con memoria virtual protegida")
        st.markdown(
            """
            <div class="memory-grid">
                <div class="frame used">IDE</div><div class="frame used">IDE</div><div class="frame free">Limite</div><div class="frame used">Examen</div>
                <div class="frame used">Examen</div><div class="frame free">Limite</div><div class="frame used">Render</div><div class="frame used">Render</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.success("La MMU y el SO bloquean accesos no autorizados.")

    st.markdown(
        """
        <div class="callout">
        <b>Respuesta para la consigna:</b> el aislamiento evita que errores, malware o consumos excesivos de una aplicacion afecten a las demas.
        Tambien permite aplicar permisos, terminar procesos problematicos y sostener estabilidad en equipos compartidos por alumnos.
        </div>
        """,
        unsafe_allow_html=True,
    )


def paging_view() -> None:
    st.header("Fase 2: Fragmentacion y Paginacion")
    st.write(
        "La fragmentacion aparece cuando la memoria queda dividida en huecos dificiles de reutilizar. La paginacion, explicada en la "
        "Unidad 3, divide memoria virtual y fisica en bloques de tamano fijo: paginas y marcos. Asi, un proceso no necesita ocupar "
        "un bloque contiguo grande; sus paginas pueden ubicarse en marcos libres dispersos."
    )
    c1, c2 = st.columns([.9, 1.1])
    with c1:
        page_size = st.slider("Tamano de pagina / marco (MB)", min_value=1, max_value=8, value=4)
        process_size = st.slider("Memoria requerida por proceso (MB)", min_value=5, max_value=48, value=22)
        frames_needed = math.ceil(process_size / page_size)
        internal_waste = frames_needed * page_size - process_size
        st.metric("Paginas necesarias", frames_needed)
        st.metric("Fragmentacion interna", f"{internal_waste} MB")
    with c2:
        st.subheader("Asignacion paginada")
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
        st.caption("El diagrama muestra marcos de memoria: usados, libres y desperdicio interno del ultimo marco.")

    st.subheader("Informe breve a la directiva")
    st.write(
        "Implementar paginacion corrige la fragmentacion externa porque elimina la necesidad de encontrar espacios contiguos de tamano variable. "
        "La RAM se administra como marcos iguales y cada programa se divide en paginas del mismo tamano. Si hay marcos libres dispersos, el "
        "proceso puede usarlos igual. El costo aceptable es una pequena fragmentacion interna en la ultima pagina y la necesidad de tablas de "
        "paginas, pero a cambio el servidor aprovecha mejor la memoria y reduce fallos por falta de bloques grandes."
    )


def mmu_view() -> None:
    st.header("Rol Critico de la MMU")
    st.write(
        "La Unidad 3 define a la MMU como hardware encargado de traducir direcciones virtuales a direcciones fisicas usando tablas de paginas. "
        "Sin esa traduccion, un programa solo tendria numeros virtuales sin correspondencia confiable con la RAM real."
    )
    virtual_page = st.number_input("Pagina virtual solicitada por un proceso", min_value=0, max_value=7, value=3)
    offset = st.number_input("Desplazamiento dentro de la pagina", min_value=0, max_value=4095, value=128)
    table = {0: 5, 1: 1, 2: 7, 3: 2, 4: 9, 5: 4, 6: 12, 7: 6}
    frame = table[int(virtual_page)]
    physical = frame * 4096 + int(offset)
    st.markdown(
        f"""
        <div class="flow">
            <div class="flow-step"><b>CPU</b><small>Direccion virtual: pag. {virtual_page}, off. {offset}</small></div>
            <div class="flow-step"><b>MMU</b><small>Consulta tabla de paginas</small></div>
            <div class="flow-step"><b>Tabla</b><small>Pagina {virtual_page} -> marco {frame}</small></div>
            <div class="flow-step"><b>RAM</b><small>Direccion fisica {physical}</small></div>
            <div class="flow-step"><b>Proteccion</b><small>Valida permisos y presencia</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "Respuesta sintetica: la MMU hace que la memoria virtual funcione en tiempo real. Traduce direcciones, aplica proteccion, detecta "
        "fallos de pagina y evita que un proceso acceda a memoria que no le pertenece."
    )


def round_robin_view() -> None:
    st.header("Round Robin para Clases 3D y Examenes Online")
    st.write(
        "La consigna pide defender Round Robin ante el Directorio. La Unidad 2 lo presenta como un algoritmo equitativo: cada proceso recibe "
        "un quantum fijo de CPU y luego vuelve al final de la cola si no termino. Esto evita que una tarea pesada, como renderizado 3D, "
        "deje sin respuesta al navegador de examen."
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
    st.success(
        "Mensaje ejecutivo: Round Robin sacrifica algo de eficiencia por cambios de contexto, pero compra equidad y respuesta. "
        "Eso es lo correcto cuando conviven examenes interactivos y trabajos pesados."
    )


def final_answer_view() -> None:
    st.header("Respuesta Integrada para Entregar")
    st.subheader("1. Seleccion y seguridad")
    st.write(
        "Se propone Windows 11 Pro por compatibilidad, soporte de hardware/software educativo y herramientas nativas de seguridad. "
        "Los alumnos trabajaran con usuarios estandar; el responsable de IT mantendra privilegios administrativos. Se usaran UAC, "
        "Defender, Firewall, BitLocker, permisos NTFS, Windows Update y politicas de grupo/locales para impedir cambios administrativos."
    )
    st.subheader("2. Aislamiento de procesos")
    st.write(
        "Cada aplicacion debe ejecutarse en su propio espacio de memoria virtual protegido. Esto impide que un error de un programa, "
        "un navegador comprometido o una aplicacion de renderizado afecte la memoria de otro proceso. El resultado es estabilidad, "
        "seguridad y posibilidad de cerrar un proceso fallido sin reiniciar toda la terminal."
    )
    st.subheader("3. Paginacion contra fragmentacion")
    st.write(
        "La paginacion divide la memoria en paginas y marcos de tamano fijo. Al no exigir bloques contiguos, aprovecha huecos dispersos "
        "de RAM y reduce la fragmentacion externa. Puede existir fragmentacion interna en la ultima pagina, pero el balance es favorable "
        "para servidores con multiples procesos de distinto tamano."
    )
    st.subheader("4. Rol de la MMU")
    st.write(
        "La MMU traduce direcciones virtuales a fisicas usando tablas de paginas. Tambien colabora con la proteccion de memoria: valida "
        "si una pagina esta presente, si el proceso tiene permisos y si debe generarse un fallo de pagina para que el sistema operativo actue."
    )
    st.subheader("5. Round Robin")
    st.write(
        "Round Robin asigna turnos de CPU mediante un quantum. Es adecuado para la academia porque evita monopolios: el renderizado 3D "
        "progresa, pero los examenes online y el sistema conservan respuesta. El quantum debe calibrarse: muy bajo aumenta cambios de "
        "contexto; muy alto se parece a FIFO y perjudica la interactividad."
    )
    st.subheader("Bibliografia usada")
    for ref in REFERENCIAS:
        st.write(f"- {ref}")


def main() -> None:
    inject_css()
    with st.sidebar:
        st.title("Actividad 3")
        st.caption("Sistemas Operativos | UCES")
        section = st.radio(
            "Navegacion",
            [
                "Resumen ejecutivo",
                "Seleccion y seguridad",
                "Aislamiento",
                "Paginacion",
                "MMU",
                "Round Robin",
                "Respuesta final",
            ],
        )
        st.divider()
        st.write("Rol: Responsable de IT")
        st.write("Escenario: academia tecnologica")
        st.write("Formato: web interactiva")

    if section == "Resumen ejecutivo":
        executive_view()
    elif section == "Seleccion y seguridad":
        os_choice_view()
    elif section == "Aislamiento":
        process_isolation_view()
    elif section == "Paginacion":
        paging_view()
    elif section == "MMU":
        mmu_view()
    elif section == "Round Robin":
        round_robin_view()
    else:
        final_answer_view()


if __name__ == "__main__":
    main()
