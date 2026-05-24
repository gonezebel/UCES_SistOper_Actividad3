import base64
import math
from dataclasses import dataclass
from pathlib import Path

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
    "Matrícula": "148741",
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
            overflow-y: hidden;
            padding-top: 0;
            padding-left: .72rem;
            padding-right: 1.05rem;
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
            padding-top: .85rem;
            padding-bottom: .25rem;
            margin-bottom: .2rem;
            min-height: 48px;
            overflow: visible !important;
        }

        .page-title {
            color: var(--ink);
            font-size: 2rem;
            font-weight: 850;
            line-height: 1.25;
            padding-top: 0;
            margin: 0;
            overflow: visible !important;
            white-space: normal;
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
            gap: .5rem;
            margin-bottom: .05rem;
            color: var(--uces-dark);
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: .02em;
            font-size: .84rem;
        }

        .brand-mark {
            width: 34px;
            min-width: 34px;
            height: 34px;
            border-radius: 6px;
            background: var(--uces-green);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
            font-size: .68rem;
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

        .context-card.compact-context {
            padding: .72rem .9rem;
            margin: .45rem 0 .55rem;
        }

        .context-card.compact-context p {
            margin: .24rem 0;
            line-height: 1.34;
        }

        .mini-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .7rem;
            margin: .7rem 0 .75rem;
        }

        .isolation-mini-grid {
            gap: .5rem;
            margin: .42rem 0 .5rem;
        }

        .isolation-mini-grid .mini-card {
            padding: .55rem .72rem;
        }

        .isolation-mini-grid .mini-card p {
            margin-top: .24rem;
            line-height: 1.32;
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

        .mmu-infographic {
            border: 1px solid var(--line);
            border-radius: 10px;
            background: #fff;
            padding: .85rem;
            margin-top: .65rem;
        }

        .mmu-flow {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: .45rem;
            margin-bottom: .65rem;
        }

        .mmu-node {
            position: relative;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            padding: .68rem .62rem;
            min-height: 104px;
        }

        .mmu-node:not(:last-child)::after {
            content: "";
            position: absolute;
            right: -.42rem;
            top: 50%;
            width: .38rem;
            height: 2px;
            background: var(--uces-green);
        }

        .mmu-step {
            display: inline-flex;
            width: 24px;
            height: 24px;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: var(--uces-light);
            color: var(--uces-dark);
            font-size: .72rem;
            font-weight: 850;
            margin-bottom: .35rem;
        }

        .mmu-node strong {
            display: block;
            color: var(--ink);
            font-size: .96rem;
            margin-bottom: .16rem;
        }

        .mmu-node span {
            display: block;
            color: var(--muted);
            font-size: .8rem;
            line-height: 1.28;
        }

        .mmu-cases {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .55rem;
        }

        .mmu-case {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .68rem .78rem;
            background: #fbfffd;
        }

        .mmu-case.blocked {
            background: #fffafa;
            border-color: #f0b9b2;
        }

        .mmu-case strong {
            display: block;
            color: var(--uces-dark);
            font-size: .78rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: .24rem;
        }

        .mmu-case p {
            margin: 0;
            color: var(--muted);
            font-size: .84rem;
            line-height: 1.35;
        }

        .mmu-image-only {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: calc(100vh - 130px);
            padding: .3rem 0;
        }

        .mmu-image-only img {
            width: 100%;
            max-height: calc(100vh - 145px);
            object-fit: contain;
            display: block;
            border-radius: 8px;
        }

        .intro-image-only {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: calc(100vh - 165px);
            padding: .3rem 0;
        }

        .intro-image-only img {
            width: 100%;
            max-height: calc(100vh - 190px);
            object-fit: contain;
            display: block;
            border-radius: 8px;
        }

        .intro-source-link {
            margin-top: .18rem;
            font-size: .78rem;
            color: var(--muted);
        }

        .intro-source-link a {
            color: var(--uces-dark);
            font-weight: 700;
            text-decoration: none;
            border-bottom: 1px solid rgba(0, 143, 99, .35);
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

        .isolation-layout {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .75rem;
            margin-top: .7rem;
        }

        .scenario-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            padding: .8rem;
        }

        .scenario-card.risk-panel {
            border-color: #f0b9b2;
            background: #fffafa;
        }

        .scenario-card.safe-panel {
            border-color: #9fd5bc;
            background: #fbfffd;
        }

        .scenario-card strong {
            color: var(--ink);
            display: block;
            font-size: 1rem;
            margin-bottom: .45rem;
        }

        .scenario-card p {
            color: var(--muted);
            font-size: .86rem;
            line-height: 1.35;
            margin: .4rem 0 0;
        }

        .process-map {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .45rem;
            margin-top: .6rem;
        }

        .process-node {
            border: 1px solid var(--line);
            border-radius: 8px;
            min-height: 74px;
            padding: .55rem .35rem;
            text-align: center;
            background: #fff;
            position: relative;
        }

        .process-node b {
            display: block;
            color: var(--ink);
            font-size: .84rem;
        }

        .process-node small {
            display: block;
            color: var(--muted);
            font-size: .72rem;
            margin-top: .2rem;
        }

        .process-node.compromised {
            background: #fde7e3;
            border-color: var(--danger);
        }

        .process-node.affected {
            background: #fff4cf;
            border-color: var(--warn);
        }

        .process-node.protected {
            background: #dff2ea;
            border-color: #72c7a3;
        }

        .status-pill {
            display: inline-block;
            border-radius: 999px;
            padding: .14rem .45rem;
            font-size: .68rem;
            font-weight: 850;
            margin-top: .42rem;
            text-transform: uppercase;
        }

        .status-pill.bad {background: #fde7e3; color: #a3322a;}
        .status-pill.warn {background: #fff4cf; color: #805a00;}
        .status-pill.ok {background: #dff2ea; color: var(--uces-dark);}

        .isolation-layout.compact-isolation {
            gap: .55rem;
            margin-top: .45rem;
        }

        .compact-isolation .scenario-card {
            padding: .62rem .72rem;
        }

        .compact-isolation .scenario-card strong {
            margin-bottom: .28rem;
        }

        .compact-isolation .scenario-card p {
            margin: .26rem 0 0;
            line-height: 1.25;
        }

        .compact-isolation .process-map {
            gap: .32rem;
            margin-top: .38rem;
        }

        .compact-isolation .process-node {
            min-height: 62px;
            padding: .42rem .3rem;
        }

        .compact-isolation .status-pill {
            margin-top: .28rem;
            padding: .1rem .36rem;
        }

        .rr-layout {
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(260px, .65fr);
            gap: .65rem;
            margin-top: .55rem;
            align-items: stretch;
        }

        .rr-table-wrap {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            padding: .55rem;
        }

        .rr-table {
            width: 100%;
            border-collapse: collapse;
        }

        .rr-table th {
            color: var(--uces-dark);
            font-size: .68rem;
            text-transform: uppercase;
            text-align: left;
            padding: .22rem .32rem .42rem;
        }

        .rr-table td {
            border-top: 1px solid var(--line);
            color: var(--ink);
            font-size: .82rem;
            padding: .42rem .32rem;
            vertical-align: middle;
        }

        .turn-cell {
            display: flex;
            flex-wrap: wrap;
            gap: .22rem;
            align-items: center;
        }

        .turn-chip {
            display: inline-flex;
            align-items: center;
            border: 1px solid #9dc4da;
            background: #dcecf5;
            border-radius: 6px;
            padding: .1rem .32rem;
            font-size: .72rem;
            font-weight: 700;
            color: var(--ink);
            white-space: nowrap;
        }

        .turn-count {
            color: var(--muted);
            font-size: .72rem;
            font-weight: 700;
            white-space: nowrap;
        }

        .rr-note-stack {
            display: flex;
            flex-direction: column;
            gap: .55rem;
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
            padding: .42rem .58rem;
            background: #ffffff;
            margin-bottom: .34rem;
            width: calc(100% - .12rem);
        }

        .sidebar-card small {
            display: block;
            color: var(--uces-dark);
            font-size: .65rem;
            font-weight: 800;
            text-transform: uppercase;
        }

        .sidebar-card span {
            display: block;
            color: var(--ink);
            font-weight: 650;
            font-size: .78rem;
            line-height: 1.25;
            margin-top: .05rem;
        }

        .nav-title {
            color: var(--uces-dark);
            font-size: .7rem;
            font-weight: 850;
            text-transform: uppercase;
            margin: .55rem 0 .18rem;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] {
            margin-top: .05rem;
            margin-bottom: .35rem;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            min-height: 1.22rem;
            padding-top: 0;
            padding-bottom: 0;
        }

        [data-testid="stSidebar"] hr {
            margin: .35rem 0 .45rem;
        }

        .apa-list {
            border-top: 1px solid var(--line);
            padding-top: .35rem;
            color: var(--ink);
            font-size: .72rem;
            line-height: 1.22;
        }

        .apa-list p {
            margin: .16rem 0;
        }

        .conclusion-main {
            border-left: 6px solid var(--uces-green);
            background: var(--uces-light);
            border-radius: 8px;
            padding: 1.05rem 1.2rem;
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 700;
            line-height: 1.42;
            margin: .55rem 0 .85rem;
        }

        .conclusion-main strong {
            color: var(--uces-dark);
            text-transform: uppercase;
            font-size: .78rem;
            display: block;
            margin-bottom: .32rem;
        }

        .conclusion-references-title {
            color: var(--uces-dark);
            font-size: .88rem;
            margin: .75rem 0 .2rem;
            font-weight: 850;
        }

        .conclusion-grid {
            margin-bottom: .65rem;
        }

        .part2-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .65rem;
            margin: .75rem 0;
        }

        .part2-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            padding: .78rem .82rem;
            min-height: 118px;
        }

        .part2-card strong {
            display: block;
            color: var(--uces-dark);
            font-size: .82rem;
            text-transform: uppercase;
            margin-bottom: .28rem;
        }

        .part2-card p {
            margin: 0;
            color: var(--muted);
            font-size: .86rem;
            line-height: 1.34;
        }

        .demand-map {
            display: grid;
            grid-template-columns: 1.1fr .7fr 1.1fr;
            gap: .65rem;
            align-items: stretch;
            margin-top: .75rem;
        }

        .demand-zone {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            padding: .85rem;
        }

        .demand-zone strong {
            display: block;
            color: var(--ink);
            margin-bottom: .45rem;
        }

        .terminal-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .34rem;
        }

        .terminal-node, .request-node {
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: .45rem .35rem;
            text-align: center;
            background: var(--soft);
            font-size: .75rem;
            color: var(--ink);
            font-weight: 800;
        }

        .terminal-node.hot, .request-node.hot {
            background: #fde7e3;
            border-color: #e7aaa3;
        }

        .flow-arrow {
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--uces-dark);
            font-weight: 850;
            font-size: 1.35rem;
            min-height: 150px;
        }

        .resource-bars {
            display: grid;
            gap: .45rem;
            margin-top: .65rem;
        }

        .resource-bar {
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
            background: #f8faf9;
        }

        .resource-fill {
            height: 28px;
            display: flex;
            align-items: center;
            padding-left: .55rem;
            color: #fff;
            font-weight: 850;
            font-size: .76rem;
            min-width: 86px;
        }

        .swap-layout {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: .65rem;
            margin-top: .75rem;
        }

        .swap-box {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .75rem;
            background: #fff;
        }

        .swap-box strong {
            color: var(--ink);
            display: block;
            margin-bottom: .35rem;
        }

        .page-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: .3rem;
        }

        .page-pill {
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: .18rem .46rem;
            background: var(--soft);
            color: var(--ink);
            font-size: .74rem;
            font-weight: 800;
        }

        .page-pill.disk {
            background: #fff4cf;
            border-color: #e6c96d;
        }

        .page-pill.fault {
            background: #fde7e3;
            border-color: #e7aaa3;
        }

        .page-table-wrap {
            overflow-x: auto;
            border: 1px solid var(--line);
            border-radius: 8px;
            margin-top: .75rem;
            background: #fff;
        }

        .page-table {
            width: 100%;
            border-collapse: collapse;
            font-size: .78rem;
        }

        .page-table th, .page-table td {
            border-bottom: 1px solid var(--line);
            padding: .45rem .5rem;
            text-align: center;
            white-space: nowrap;
        }

        .page-table th {
            color: var(--uces-dark);
            background: var(--uces-light);
            font-weight: 850;
        }

        .page-table td:first-child, .page-table th:first-child {
            text-align: left;
        }

        .fault-yes {
            color: #b5443a;
            font-weight: 850;
        }

        .fault-no {
            color: var(--uces-dark);
            font-weight: 850;
        }

        .clock-ring {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .45rem;
            margin-top: .6rem;
        }

        .clock-slot {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            padding: .55rem;
            text-align: center;
        }

        .clock-slot.pointer {
            border-color: var(--uces-green);
            box-shadow: inset 0 0 0 2px rgba(0, 140, 90, .18);
        }

        .race-demo {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .65rem;
            margin-top: .75rem;
        }

        .critical-file {
            border: 2px solid var(--uces-green);
            border-radius: 8px;
            padding: .85rem;
            background: #fbfffd;
            color: var(--ink);
            font-weight: 850;
            text-align: center;
            margin-top: .55rem;
        }

        .conflict-file {
            border-color: var(--danger);
            background: #fffafa;
        }

        @media (max-width: 900px) {
            .kpi-grid, .icon-strip, .mini-grid, .pipeline, .isolation-layout, .mmu-flow, .mmu-cases, .rr-layout, .part2-grid, .demand-map, .swap-layout, .race-demo {grid-template-columns: 1fr;}
            .memory-grid {grid-template-columns: repeat(4, 1fr);}
            .process-map {grid-template-columns: repeat(2, 1fr);}
            .pipeline:before, .pipeline:after, .mmu-node:not(:last-child)::after {display: none;}
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


def context_card(title: str, explanation: str, example: str, balance: str, class_name: str = "") -> None:
    balance_html = f"<p><em>Costo / seguridad / eficiencia:</em> {balance}</p>" if balance else ""
    extra_class = f" {class_name}" if class_name else ""
    st.markdown(
        f"""
        <div class="context-card{extra_class}">
            <strong>{title}</strong>
            <p>{explanation}</p>
            <p><em>Ejemplo real:</em> {example}</p>
            {balance_html}
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


def isolation_infographic(scenario: str) -> None:
    scenarios = {
        "Render 3D se bloquea": {
            "trigger": "El motor de render consume memoria y termina con error.",
            "without": "El error puede invadir memoria compartida, afectar el navegador del examen o forzar reinicio.",
            "with": "El sistema operativo limita el daño al proceso de render y permite cerrar solo esa aplicación.",
            "risk": ["Render", "Examen"],
            "safe": ["Examen", "IDE", "Sistema"],
        },
        "Navegador de examen queda comprometido": {
            "trigger": "Una extensión o sitio malicioso intenta leer datos de otros programas.",
            "without": "El navegador podría acceder a información del IDE, archivos temporales o credenciales de otra sesión.",
            "with": "La MMU y los permisos de memoria bloquean el acceso fuera del espacio del navegador.",
            "risk": ["Examen", "IDE", "Datos"],
            "safe": ["IDE", "Datos", "Sistema"],
        },
        "IDE consume memoria en exceso": {
            "trigger": "Una ejecución de código entra en bucle o reserva memoria de forma incorrecta.",
            "without": "El consumo puede degradar toda la terminal y arrastrar servicios que sostienen la clase.",
            "with": "El proceso queda contenido; IT puede finalizarlo y liberar memoria sin reiniciar el equipo.",
            "risk": ["IDE", "Sistema"],
            "safe": ["Examen", "Sistema", "Render"],
        },
    }
    data = scenarios[scenario]
    nodes = ["IDE", "Examen", "Render", "Sistema"]

    def node_html(name: str, mode: str) -> str:
        if mode == "without":
            css = "compromised" if name in data["risk"][:1] else "affected" if name in data["risk"] else ""
            pill = "Falla" if css == "compromised" else "Afectado" if css == "affected" else "Expuesto"
            pill_class = "bad" if css == "compromised" else "warn" if css == "affected" else "warn"
            detail = "Sin límite claro" if css else "Puede recibir impacto"
        else:
            css = "compromised" if name == data["risk"][0] else "protected" if name in data["safe"] else ""
            pill = "Aislado" if css == "compromised" else "Protegido" if css == "protected" else "Estable"
            pill_class = "bad" if css == "compromised" else "ok"
            detail = "Se cierra el proceso" if css == "compromised" else "Memoria separada"
        return (
            f'<div class="process-node {css}">'
            f"<b>{name}</b><small>{detail}</small>"
            f'<span class="status-pill {pill_class}">{pill}</span>'
            "</div>"
        )

    st.markdown(
        f"""
        <div class="isolation-layout compact-isolation">
            <div class="scenario-card risk-panel">
                <strong>Sin aislamiento</strong>
                <p>{data["trigger"]}</p>
                <div class="process-map">{"".join(node_html(node, "without") for node in nodes)}</div>
                <p>{data["without"]}</p>
            </div>
            <div class="scenario-card safe-panel">
                <strong>Con aislamiento de procesos</strong>
                <p>{data["trigger"]}</p>
                <div class="process-map">{"".join(node_html(node, "with") for node in nodes)}</div>
                <p>{data["with"]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def paging_director_cards(page_size: int, process_size: int, frames_needed: int, internal_waste: int) -> str:
    allocated = frames_needed * page_size
    waste_pct = 0 if allocated == 0 else round((internal_waste / allocated) * 100, 1)
    if internal_waste == 0:
        waste_reading = "La división es exacta: no queda desperdicio interno en el último marco."
    elif waste_pct <= 12:
        waste_reading = f"El desperdicio interno es bajo ({internal_waste} MB, {waste_pct}% de lo reservado). Es un costo técnico aceptable."
    else:
        waste_reading = f"El desperdicio interno es visible ({internal_waste} MB, {waste_pct}% de lo reservado). Conviene evaluar un tamaño de página menor."

    if page_size <= 2:
        size_reading = "Páginas chicas reducen desperdicio, pero obligan al SO a administrar más entradas de tabla."
    elif page_size >= 7:
        size_reading = "Páginas grandes simplifican la tabla, pero pueden reservar memoria que el proceso no usa."
    else:
        size_reading = "El tamaño elegido mantiene un balance razonable entre administración y aprovechamiento de RAM."

    if process_size >= 32:
        load_reading = "Es una carga pesada: paginar permite ubicarla en marcos dispersos sin exigir un bloque contiguo grande."
    else:
        load_reading = "Es una carga moderada: la ventaja principal es mantener orden y aislamiento cuando hay varios procesos juntos."

    return (
        '<div class="mini-grid">'
        + mini_card("Asignación de memoria", f"El proceso pide {process_size} MB. El sistema reserva {allocated} MB en {frames_needed} páginas de {page_size} MB.")
        + mini_card("Eficiencia de memoria", waste_reading)
        + mini_card("Tamaño elegido", size_reading)
        + mini_card("Impacto operativo", load_reading)
        + "</div>"
    )


def selection_cost_cards(selected: list[str]) -> str:
    effort_hours = {
        "Usuarios estándar": 0.5,
        "UAC activo": 0.25,
        "BitLocker": 0.75,
        "Defender + Firewall": 0.5,
        "Políticas de grupo": 1.5,
        "Imagen base": 3.0,
    }
    hours = sum(effort_hours[item] for item in selected)
    base = (
        "Windows 11 Pro: referencia retail Microsoft Store USD 199.99 por equipo si debe comprarse licencia nueva. "
        "macOS no se licencia por separado para equipos Apple compatibles; el costo se traslada al hardware. "
        "Si las PC ya traen Windows Pro, el costo incremental de software es USD 0."
    )
    implementation = (
        f"Con {len(selected)} de 6 controles activos: más {hours:.1f} h técnicas de configuración y validación. "
        "Ese esfuerzo se informa separado y no se convierte a USD porque depende del esquema operativo contratado."
    )
    return (
        mini_card("Costo base estimado (USD)", base)
        + mini_card("Esfuerzo técnico", implementation)
    )


def isolation_cost_cards(scenario: str) -> str:
    risks = {
        "Render 3D se bloquea": "Sin aislamiento, el costo probable es tiempo de clase perdido por reinicio o recuperación de sesión. Con aislamiento, se cierra el render y el resto del aula sigue trabajando.",
        "Navegador de examen queda comprometido": "Sin aislamiento, el costo puede escalar a revisión de examen, datos expuestos y soporte urgente. Con aislamiento, se bloquea el acceso a otros procesos.",
        "IDE consume memoria en exceso": "Sin aislamiento, el costo aparece como soporte técnico y demora para recuperar la terminal. Con aislamiento, el incidente se limita al proceso del IDE.",
    }
    base = (
        "Licencias adicionales: USD 0, porque el aislamiento de procesos y memoria virtual ya viene integrado en sistemas modernos. "
        "Más 1-2 h técnicas de validación, pruebas básicas y documentación operativa. Ese esfuerzo se muestra aparte y no se convierte a USD."
    )
    return (
        '<div class="mini-grid isolation-mini-grid">'
        + mini_card("Costo base estimado (USD)", base)
        + mini_card("Costo evitado por escenario", risks[scenario])
        + "</div>"
    )


def mmu_infographic() -> None:
    st.markdown(
        """
        <div class="mmu-infographic">
            <div class="mmu-flow">
                <div class="mmu-node">
                    <div class="mmu-step">1</div>
                    <strong>Dirección virtual</strong>
                    <span>El programa pide página 3 + desplazamiento 128. No conoce la ubicación real en RAM.</span>
                </div>
                <div class="mmu-node">
                    <div class="mmu-step">2</div>
                    <strong>MMU</strong>
                    <span>El hardware intercepta el pedido antes de que llegue a memoria física.</span>
                </div>
                <div class="mmu-node">
                    <div class="mmu-step">3</div>
                    <strong>Tabla de páginas</strong>
                    <span>El sistema indica que la página 3 corresponde al marco físico 2.</span>
                </div>
                <div class="mmu-node">
                    <div class="mmu-step">4</div>
                    <strong>Permisos</strong>
                    <span>Se valida si el proceso puede leer o escribir esa región de memoria.</span>
                </div>
                <div class="mmu-node">
                    <div class="mmu-step">5</div>
                    <strong>RAM o bloqueo</strong>
                    <span>Si el acceso es válido, llega a la dirección física 8320; si no, se corta.</span>
                </div>
            </div>
            <div class="mmu-cases">
                <div class="mmu-case">
                    <strong>Acceso autorizado</strong>
                    <p>El navegador de examen lee solo sus propios datos. La traducción ocurre en hardware y mantiene el rendimiento del aula.</p>
                </div>
                <div class="mmu-case blocked">
                    <strong>Intento indebido bloqueado</strong>
                    <p>Si otra aplicación intenta leer memoria del examen, la MMU genera una falla de protección y el sistema operativo detiene ese acceso.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mmu_image_page() -> None:
    image_path = Path(__file__).parent / "02_Imagenes" / "00_infografia_MMU_sin_encabezado.png"
    if not image_path.exists():
        st.error("No se encontró la imagen de MMU en 02_Imagenes/00_infografia_MMU_sin_encabezado.png.")
        return
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <div class="mmu-image-only">
            <img src="data:image/png;base64,{encoded}" alt="Infografía de MMU y paginación">
        </div>
        """,
        unsafe_allow_html=True,
    )


def phase_header(phase: str, title: str) -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-title">{title}</div>
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


def rr_results_table(processes: list[Process], timeline: list[tuple[str, int, int]], completion: dict[str, int]) -> str:
    turns_by_process: dict[str, list[tuple[int, int]]] = {p.name: [] for p in processes}
    for name, start, end in timeline:
        turns_by_process[name].append((start, end))

    def turn_chips(turns: list[tuple[int, int]]) -> str:
        ranges = [f"{start}-{end}" for start, end in turns]
        if len(ranges) > 5:
            visible = ranges[:3] + ["..."] + [ranges[-1]]
            count = f'<span class="turn-count">{len(ranges)} turnos</span>'
        else:
            visible = ranges
            count = ""
        chips = "".join(f'<span class="turn-chip">{item}</span>' for item in visible)
        return f'<div class="turn-cell">{chips}{count}</div>'

    rows = []
    for process in processes:
        turnaround = completion[process.name] - process.arrival
        waiting = turnaround - process.burst
        rows.append(
            "<tr>"
            f"<td><b>{process.name}</b></td>"
            f"<td>{process.burst}</td>"
            f"<td>{turn_chips(turns_by_process[process.name])}</td>"
            f"<td>{completion[process.name]}</td>"
            f"<td>{waiting}</td>"
            "</tr>"
        )

    return (
        '<div class="rr-table-wrap">'
        '<table class="rr-table">'
        "<thead><tr><th>Proceso</th><th>CPU</th><th>Turnos asignados</th><th>Fin</th><th>Espera</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
        "</div>"
    )


def rr_quantum_reading(quantum: int) -> str:
    if quantum <= 2:
        return "Quantum bajo: mejora la respuesta de procesos cortos, pero aumenta la cantidad de cambios de turno."
    if quantum >= 5:
        return "Quantum alto: reduce cambios de turno, pero los procesos interactivos pueden esperar más antes de responder."
    return "Quantum equilibrado: reparte CPU sin generar demasiados cambios de turno ni esperas largas."


def bounded_percent(value: float) -> int:
    return max(0, min(100, int(value)))


def references_from_text(text: str) -> list[int]:
    refs: list[int] = []
    for item in text.replace(";", ",").split(","):
        item = item.strip()
        if item:
            try:
                refs.append(int(item))
            except ValueError:
                continue
    return refs


def page_replacement_history(references: list[int], frame_count: int, algorithm: str) -> list[dict[str, object]]:
    frames: list[int | None] = [None] * frame_count
    loaded_at: dict[int, int] = {}
    last_used: dict[int, int] = {}
    ref_bits: dict[int, int] = {}
    pointer = 0
    history: list[dict[str, object]] = []

    for step, page in enumerate(references, start=1):
        fault = page not in frames
        victim = None
        if fault:
            if None in frames:
                idx = frames.index(None)
            elif algorithm == "FIFO":
                victim = min((p for p in frames if p is not None), key=lambda p: loaded_at.get(p, 0))
                idx = frames.index(victim)
            elif algorithm == "LRU":
                victim = min((p for p in frames if p is not None), key=lambda p: last_used.get(p, 0))
                idx = frames.index(victim)
            else:
                while True:
                    candidate = frames[pointer]
                    if candidate is None:
                        idx = pointer
                        break
                    if ref_bits.get(candidate, 0) == 0:
                        victim = candidate
                        idx = pointer
                        break
                    ref_bits[candidate] = 0
                    pointer = (pointer + 1) % frame_count
                pointer = (idx + 1) % frame_count

            if victim is not None:
                loaded_at.pop(victim, None)
                last_used.pop(victim, None)
                ref_bits.pop(victim, None)
            frames[idx] = page
            loaded_at[page] = step
            ref_bits[page] = 1
        else:
            ref_bits[page] = 1
        last_used[page] = step
        history.append(
            {
                "step": step,
                "page": page,
                "frames": frames.copy(),
                "fault": fault,
                "victim": victim,
                "pointer": pointer,
                "bits": ref_bits.copy(),
            }
        )
    return history


def render_page_history_table(history: list[dict[str, object]], frame_count: int) -> str:
    rows = []
    for item in history:
        frames = item["frames"]
        cells = "".join(f"<td>{frame if frame is not None else '-'}</td>" for frame in frames)
        status = '<span class="fault-yes">Fallo</span>' if item["fault"] else '<span class="fault-no">Acierto</span>'
        victim = item["victim"] if item["victim"] is not None else "-"
        rows.append(
            "<tr>"
            f"<td>{item['step']}</td>"
            f"<td><b>{item['page']}</b></td>"
            + cells
            + f"<td>{status}</td><td>{victim}</td>"
            "</tr>"
        )
    frame_headers = "".join(f"<th>Marco {i + 1}</th>" for i in range(frame_count))
    return (
        '<div class="page-table-wrap"><table class="page-table">'
        f"<thead><tr><th>Paso</th><th>Pagina</th>{frame_headers}<th>Resultado</th><th>Sale</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def virtual_memory_view() -> None:
    phase_header("Fase 3", "6. Memoria virtual")
    st.markdown(
        """
        <div class="conclusion-main">
            <strong>Respuesta ejecutiva</strong>
            El swapping usa disco como extension temporal de la RAM: mueve paginas menos urgentes fuera de memoria fisica
            y carga las que el render necesita en ese momento. Asi evita el colapso y mantiene las terminales operativas,
            aunque con menor velocidad cuando aumenta el uso de disco.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1.15])
    with c1:
        students = st.slider("Alumnos", 5, 40, 24)
    with c2:
        render_weight = st.slider("Peso render", 1, 10, 7)
    with c3:
        ram = st.slider("RAM fisica", 4, 16, 8)
    with c4:
        demanded = st.slider("Paginas render", 6, 28, 18)
    with c5:
        algorithm = st.selectbox("Metodo", ["FIFO", "LRU", "Clock"])

    algorithm_data = {
        "FIFO": {
            "desc": "Saca la pagina mas antigua en RAM.",
            "factor": 1.08,
            "color": "#2f6f9f",
        },
        "LRU": {
            "desc": "Saca la menos usada recientemente.",
            "factor": .86,
            "color": "#008c5a",
        },
        "Clock": {
            "desc": "Da segunda oportunidad a paginas usadas.",
            "factor": .94,
            "color": "#6c7a31",
        },
    }
    pressure = bounded_percent((students * render_weight * demanded) / (ram * 6))
    in_ram = min(ram, demanded)
    in_swap = max(0, demanded - ram)
    swap_percent = bounded_percent((in_swap / demanded) * 100 if demanded else 0)
    base_faults = max(0, demanded - ram) + max(0, int((students * render_weight) / 18))
    estimated_faults = max(0, math.ceil(base_faults * algorithm_data[algorithm]["factor"]))
    performance = max(18, bounded_percent(100 - (swap_percent * .55) - (estimated_faults * 2.1) - max(0, pressure - 80) * .25))
    continuity = "Operativo" if performance >= 55 else "Degradado" if performance >= 32 else "Critico"
    ram_pages = "".join(f'<span class="page-pill">P{i + 1}</span>' for i in range(min(in_ram, 10)))
    if in_ram > 10:
        ram_pages += '<span class="page-pill">...</span>'
    swap_pages = "".join(f'<span class="page-pill disk">P{i + 1 + in_ram}</span>' for i in range(min(in_swap, 10)))
    if in_swap > 10:
        swap_pages += '<span class="page-pill disk">...</span>'

    st.markdown(
        f"""
        <div class="part2-grid">
            {mini_card("Metodo seleccionado", f"{algorithm}: {algorithm_data[algorithm]['desc']}")}
            {mini_card("Fallos estimados", f"{estimated_faults} eventos de carga desde disco para sostener el render.")}
            {mini_card("Estado del aula", f"{continuity}: rendimiento estimado {performance}%.")}
        </div>
        <div class="swap-layout">
            <div class="swap-box">
                <strong>Demanda total</strong>
                <p>{students} alumnos x peso {render_weight}: presion de memoria {pressure}%.</p>
                <div class="resource-bar"><div class="resource-fill" style="width:{pressure}%; background:#e06a5f;">presion {pressure}%</div></div>
            </div>
            <div class="swap-box">
                <strong>RAM fisica</strong>
                <div class="page-pill-row">{ram_pages}</div>
                <div class="resource-bar"><div class="resource-fill" style="width:{bounded_percent((in_ram / demanded) * 100)}%; background:#008c5a;">{in_ram} paginas</div></div>
            </div>
            <div class="swap-box">
                <strong>Swap en disco</strong>
                <div class="page-pill-row">{swap_pages if swap_pages else '<span class="page-pill">sin uso</span>'}</div>
                <div class="resource-bar"><div class="resource-fill" style="width:{swap_percent}%; background:{algorithm_data[algorithm]['color']};">{in_swap} paginas</div></div>
            </div>
        </div>
        <div class="resource-bars">
            <div class="resource-bar"><div class="resource-fill" style="width:{performance}%; background:{algorithm_data[algorithm]['color']};">rendimiento {performance}%</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_faults_view() -> None:
    phase_header("Parte 2", "Fallos de pagina y reemplazo")
    refs_text = st.text_input("Secuencia de referencias", value="7, 0, 1, 2, 0, 3, 0, 4, 2, 3")
    frame_count = st.slider("Marcos disponibles", 2, 6, 3)
    refs = references_from_text(refs_text)
    history = page_replacement_history(refs, frame_count, "FIFO")
    faults = sum(1 for item in history if item["fault"])
    st.markdown(
        '<div class="part2-grid">'
        + mini_card("Fallo de pagina", "Ocurre cuando el proceso necesita una pagina que no esta cargada en RAM.")
        + mini_card("Victima", "Si no hay marcos libres, el SO decide que pagina sale para hacer lugar.")
        + mini_card("Impacto", f"Con esta secuencia aparecen {faults} fallos usando FIFO como criterio base.")
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(render_page_history_table(history, frame_count), unsafe_allow_html=True)


def replacement_algorithms_view() -> None:
    phase_header("Parte 2", "FIFO, LRU y Clock")
    refs_text = st.text_input("Referencias para comparar", value="1, 2, 3, 1, 4, 5, 1, 2, 3, 4")
    frame_count = st.slider("Cantidad de marcos", 2, 5, 3)
    algorithm = st.selectbox("Algoritmo", ["FIFO", "LRU", "Clock"])
    refs = references_from_text(refs_text)
    history = page_replacement_history(refs, frame_count, algorithm)
    faults = sum(1 for item in history if item["fault"])
    descriptions = {
        "FIFO": "Elimina la pagina que lleva mas tiempo cargada, aunque se haya usado recientemente.",
        "LRU": "Elimina la pagina menos usada recientemente, buscando conservar lo que todavia parece util.",
        "Clock": "Recorre los marcos con un puntero y usa un bit de referencia para dar segunda oportunidad.",
    }
    st.markdown(
        '<div class="part2-grid">'
        + mini_card("FIFO", "Simple: cola de llegada. Puede sacar una pagina activa si entro hace mucho.")
        + mini_card("LRU", "Mas preciso: mira uso reciente. Requiere registrar accesos.")
        + mini_card("Clock", "Equilibrado: aproxima LRU con bajo costo usando bits de referencia.")
        + "</div>",
        unsafe_allow_html=True,
    )
    context_card("Lectura del algoritmo seleccionado", f"<b>{algorithm}:</b> {descriptions[algorithm]}", f"En la secuencia ingresada genera {faults} fallos de pagina.", "")
    if history:
        last = history[-1]
        frames = last["frames"]
        bits = last["bits"]
        pointer = last["pointer"]
        slots = "".join(
            f'<div class="clock-slot {"pointer" if i == pointer else ""}"><b>{frame if frame is not None else "-"}</b><br><small>R={bits.get(frame, 0) if frame is not None else "-"}</small></div>'
            for i, frame in enumerate(frames)
        )
        st.markdown(f'<div class="clock-ring">{slots}</div>', unsafe_allow_html=True)
    st.markdown(render_page_history_table(history, frame_count), unsafe_allow_html=True)


def server_round_robin_view() -> None:
    phase_header("Parte 2", "Round Robin en el servidor de examenes")
    context_card(
        "Procesamiento equitativo",
        "<b>El servidor atiende peticiones por turnos de quantum fijo.</b>",
        "Si un alumno envia una respuesta muy pesada, usa un turno y vuelve a la cola; no bloquea a los envios livianos.",
        "La equidad mejora, aunque un quantum demasiado bajo aumenta cambios de contexto.",
    )
    left, right = st.columns(2)
    with left:
        quantum = st.slider("Quantum del servidor", 1, 6, 2)
        a1 = st.slider("Alumno A", 1, 12, 4)
        a2 = st.slider("Alumno B", 1, 12, 9)
    with right:
        a3 = st.slider("Alumno C", 1, 12, 3)
        a4 = st.slider("Alumno D", 1, 12, 7)
    processes = [Process("Alumno A", a1), Process("Alumno B", a2), Process("Alumno C", a3), Process("Alumno D", a4)]
    timeline, completion = rr_schedule(processes, quantum)
    st.markdown(
        '<div class="rr-layout">'
        + rr_results_table(processes, timeline, completion)
        + '<div class="rr-note-stack">'
        + mini_card("Cola de peticiones", "Cada alumno recibe tiempo de servidor aunque otros envios sigan incompletos.")
        + mini_card("Quantum", rr_quantum_reading(quantum))
        + mini_card("Resultado", "El servidor evita trato injusto y mantiene avance visible para todos.")
        + "</div></div>",
        unsafe_allow_html=True,
    )


def synchronization_view() -> None:
    phase_header("Parte 2", "Semaforos y condiciones de carrera")
    use_semaphore = st.toggle("Usar semaforo para el archivo de calificaciones", value=True)
    students = st.slider("Alumnos escribiendo notas a la vez", 2, 6, 4)
    requests = "".join(f'<div class="request-node {"hot" if not use_semaphore else ""}">Alumno {i + 1}</div>' for i in range(students))
    if use_semaphore:
        result_class = ""
        result = "Archivo consistente: una escritura entra a la seccion critica y las demas esperan turno."
        left_title = "Con semaforo"
        right_title = "Cola ordenada"
    else:
        result_class = "conflict-file"
        result = "Condicion de carrera: dos escrituras pueden pisarse y dejar una nota perdida o inconsistente."
        left_title = "Sin sincronizacion"
        right_title = "Escrituras superpuestas"
    st.markdown(
        f"""
        <div class="race-demo">
            <div class="demand-zone">
                <strong>{left_title}</strong>
                <div class="terminal-grid">{requests}</div>
            </div>
            <div class="demand-zone">
                <strong>{right_title}</strong>
                <div class="critical-file {result_class}">{result}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="part2-grid">'
        + mini_card("Seccion critica", "Es la zona donde se escribe el archivo compartido de calificaciones.")
        + mini_card("Semaforo/mutex", "Permite que un solo proceso escriba mientras los demas esperan.")
        + mini_card("Problema evitado", "La condicion de carrera, donde el resultado depende del orden accidental de ejecucion.")
        + "</div>",
        unsafe_allow_html=True,
    )


def part2_closure_view() -> None:
    phase_header("Parte 2", "Cierre integrador")
    st.markdown(
        """
        <div class="conclusion-main">
            <strong>Conclusion Parte 2</strong>
            La memoria virtual permite sostener renders cuando la RAM fisica no alcanza; los algoritmos de reemplazo
            deciden que paginas salen; Round Robin reparte atencion del servidor; y los semaforos protegen el archivo
            central de calificaciones frente a accesos concurrentes.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="part2-grid">'
        + mini_card("Memoria", "Swapping evita el colapso inmediato, con costo de rendimiento.")
        + mini_card("Reemplazo", "FIFO, LRU y Clock equilibran simpleza, precision y costo.")
        + mini_card("Concurrencia", "RR y semaforos sostienen equidad y consistencia de datos.")
        + "</div>",
        unsafe_allow_html=True,
    )


def introduction_view() -> None:
    phase_header(
        "Inicio",
        "Introducción",
    )
    image_path = Path(__file__).parent / "02_Imagenes" / "05_introduccion_sin_footer.png"
    if not image_path.exists():
        st.error("No se encontró la imagen de introducción en 02_Imagenes/05_introduccion_sin_footer.png.")
        return
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <div class="intro-image-only">
            <img src="data:image/png;base64,{encoded}" alt="Introducción al caso CrowdStrike">
        </div>
        <div class="intro-source-link">
            Fuente:
            <a href="https://www.messageware.com/what-caused-the-crowdstrike-outage-a-detailed-breakdown/" target="_blank" rel="noopener noreferrer">
                Messageware - What caused the CrowdStrike outage
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def selection_security_view() -> None:
    phase_header(
        "Fase 1",
        "1. Selección y Seguridad",
    )

    left, right = st.columns([1.05, .95])
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
            + selection_cost_cards(selected)
            + mini_card("Ejemplo real", "En una clase con Blender, navegadores de examen y proyectores, perder tiempo instalando drivers o resolviendo permisos durante la clase tiene más impacto que el costo de una licencia ya administrable.")
            + "</div>",
            unsafe_allow_html=True,
        )



def process_isolation_view() -> None:
    phase_header(
        "Fase 1",
        "2. Aislamiento de Procesos",
    )
    context_card(
        "Criterio ejecutivo",
        "<b>El aislamiento de procesos convierte errores individuales en fallas contenidas: si una aplicación se bloquea, no arrastra al sistema completo ni compromete datos de otra actividad.</b>",
        "Durante un examen online, un alumno puede tener abierto un IDE o una herramienta de render. Si el render consume memoria o falla, el navegador del examen debe seguir protegido.",
        "",
        "compact-context",
    )

    st.markdown(
        '<div class="mini-grid isolation-mini-grid">'
        + mini_card("Estabilidad", "Un fallo en un render 3D no debe tirar el navegador de examen.")
        + mini_card("Seguridad", "Un proceso no puede leer ni escribir memoria ajena sin autorización.")
        + mini_card("Recuperación", "IT puede cerrar una app problemática sin reiniciar el equipo.")
        + mini_card("Concurrencia", "IDE, navegador, antivirus y servicios del SO conviven sin interferirse.")
        + "</div>",
        unsafe_allow_html=True,
    )

    scenario = st.radio(
        "Escenario de incidente",
        ["Render 3D se bloquea", "Navegador de examen queda comprometido", "IDE consume memoria en exceso"],
        horizontal=True,
    )
    st.markdown(isolation_cost_cards(scenario), unsafe_allow_html=True)
    isolation_infographic(scenario)


def paging_view() -> None:
    phase_header(
        "Fase 2",
        "3. Análisis de Deficiencias: Paginación",
    )
    context_card(
        "Criterio ejecutivo",
        "<b>La paginación se recomienda porque evita depender de bloques contiguos de memoria. El servidor puede cargar partes de procesos en marcos dispersos y sostener varias tareas simultáneas.</b>",
        "Si el servidor atiende archivos, aulas virtuales y renderizados, puede tener RAM libre repartida en huecos. Sin paginación, esos huecos pueden no servir; con paginación, se aprovechan.",
        "Inversión incremental: USD 0 en licencias si el equipo ya soporta memoria virtual. Comprar más RAM o servidor requiere cotización y no resuelve por sí solo la fragmentación ni el aislamiento.",
    )

    c1, c2 = st.columns([.9, 1.1])
    with c1:
        page_size = st.slider("Tamaño de página / marco (MB)", min_value=1, max_value=8, value=4)
        process_size = st.slider("Memoria requerida por proceso (MB)", min_value=5, max_value=48, value=22)
        frames_needed = math.ceil(process_size / page_size)
        internal_waste = frames_needed * page_size - process_size
        metric_left, metric_right = st.columns(2)
        metric_left.metric("Páginas necesarias", frames_needed)
        metric_right.metric("Fragmentación interna", f"{internal_waste} MB")
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
        paging_director_cards(page_size, process_size, frames_needed, internal_waste),
        unsafe_allow_html=True,
    )


def mmu_view() -> None:
    phase_header(
        "Fase 2",
        "4. Rol del Hardware: MMU",
    )
    mmu_image_page()


def round_robin_view() -> None:
    phase_header(
        "Enfoque de consultoría",
        "5. Round Robin para clases 3D y exámenes online",
    )
    context_card(
        "Criterio ejecutivo",
        "<b>Round Robin es una opción adecuada porque reparte CPU en turnos. No maximiza cada tarea individual, pero protege la respuesta percibida cuando conviven actividades pesadas e interactivas.</b>",
        "En una clase, un render 3D puede necesitar mucho CPU. El examen online, el antivirus y el sistema no pueden quedar esperando hasta que termine el render.",
        "",
    )

    left, right = st.columns(2)
    with left:
        quantum = st.slider("Quantum de CPU", min_value=1, max_value=6, value=3)
        p1 = st.slider("Render 3D", min_value=2, max_value=18, value=12)
        p2 = st.slider("Examen online", min_value=2, max_value=18, value=5)
    with right:
        p3 = st.slider("IDE del alumno", min_value=2, max_value=18, value=8)
        p4 = st.slider("Sistema / antivirus", min_value=2, max_value=18, value=4)
    processes = [
        Process("Render", p1),
        Process("Examen", p2),
        Process("IDE", p3),
        Process("Sistema", p4),
    ]
    timeline, completion = rr_schedule(processes, quantum)
    st.markdown(
        '<div class="rr-layout">'
        + rr_results_table(processes, timeline, completion)
        + '<div class="rr-note-stack">'
        + mini_card("Interpretación de turnos", "Cada rango inicio-fin es un turno de CPU. Si un proceso tiene varios rangos, vuelve a la cola porque todavía le falta trabajo.")
        + mini_card("Lectura del quantum", rr_quantum_reading(quantum))
        + mini_card("Criterio ejecutivo", "El examen y el sistema reciben turnos aunque el render siga activo; eso protege la percepción de respuesta del aula.")
        + "</div>"
        + "</div>",
        unsafe_allow_html=True,
    )


def board_view() -> None:
    phase_header(
        "Cierre",
        "Conclusión",
    )

    st.markdown(
        """
        <div class="conclusion-main">
            <strong>Conclusión final</strong>
            La propuesta prioriza continuidad académica. La selección del sistema operativo, los controles de seguridad,
            el aislamiento de procesos, la paginación, la MMU y Round Robin reducen el riesgo de que una tarea pesada
            o defectuosa comprometa clases, exámenes o datos institucionales.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="conclusion-grid">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        card("Fase 1", "Windows + seguridad", "Windows 11 Pro, usuarios estándar y controles nativos reducen cambios no autorizados en el aula.")
    with c2:
        card("Fase 2", "Procesos + memoria", "Aislamiento, paginación y MMU separan fallas, aprovechan RAM y protegen direcciones de memoria.")
    with c3:
        card("Fase 3", "CPU equitativa", "Round Robin reparte turnos para que render, examen y servicios críticos sigan avanzando.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="conclusion-references-title">Referencias bibliográficas</div>', unsafe_allow_html=True)
    st.markdown('<div class="apa-list">', unsafe_allow_html=True)
    for ref in REFERENCIAS:
        st.markdown(f"<p>{ref}</p>", unsafe_allow_html=True)
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
                "Introducción",
                "Fase 1 / 1. Selección y Seguridad",
                "Fase 1 / 2. Aislamiento de Procesos",
                "Fase 2 / 3. Paginación",
                "Fase 2 / 4. MMU",
                "Fase 3 / 5. Round Robin",
                "Fase 3 / 6. Memoria virtual",
                "Parte 2 / Fallos de página",
                "Parte 2 / FIFO, LRU y Clock",
                "Parte 2 / Round Robin en servidor",
                "Parte 2 / Semáforos y carrera",
                "Parte 2 / Cierre integrador",
                "Conclusión",
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

    if section == "Introducción":
        introduction_view()
    elif section == "Fase 1 / 1. Selección y Seguridad":
        selection_security_view()
    elif section == "Fase 1 / 2. Aislamiento de Procesos":
        process_isolation_view()
    elif section == "Fase 2 / 3. Paginación":
        paging_view()
    elif section == "Fase 2 / 4. MMU":
        mmu_view()
    elif section == "Fase 3 / 5. Round Robin":
        round_robin_view()
    elif section == "Fase 3 / 6. Memoria virtual":
        virtual_memory_view()
    elif section == "Parte 2 / Fallos de página":
        page_faults_view()
    elif section == "Parte 2 / FIFO, LRU y Clock":
        replacement_algorithms_view()
    elif section == "Parte 2 / Round Robin en servidor":
        server_round_robin_view()
    elif section == "Parte 2 / Semáforos y carrera":
        synchronization_view()
    elif section == "Parte 2 / Cierre integrador":
        part2_closure_view()
    else:
        board_view()


if __name__ == "__main__":
    main()
