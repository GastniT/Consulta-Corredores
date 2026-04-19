"""
FECU Corredores · Securicom
Análisis competitivo multi-año 2017-2025
CMF Chile
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FECU Corredores · Securicom",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

AÑOS = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
AÑO_DEFAULT = "2025"

# ──────────────────────────────────────────────────────────────
# DICCIONARIO RAMOS (completo, desde el código original)
# ──────────────────────────────────────────────────────────────
RAMOS = {
    "99": "TOTAL SEG. GENERALES",
    "1": "Incendio",
    "2": "Pérdida de Beneficios por Incendio",
    "3": "Otros Riesgos Adicionales a Incendio",
    "4": "Terremoto y Tsunami",
    "5": "Pérdida de Beneficios por Terremoto",
    "6": "Otros Riesgos de la Naturaleza",
    "7": "Terrorismo",
    "8": "Robo",
    "9": "Cristales",
    "10": "Daños Vehículos Motorizados",
    "11": "Casco Marítimo",
    "12": "Casco Aéreo",
    "13": "RC Hogar y Condominios",
    "14": "RC Profesional",
    "15": "RC Industria/Infraestructura/Comercio",
    "16": "RC Vehículos Motorizados",
    "17": "Transporte Terrestre",
    "18": "Transporte Marítimo",
    "19": "Transporte Aéreo",
    "20": "Equipo Contratista",
    "21": "Todo Riesgo Construcción y Montaje",
    "22": "Avería Maquinaria",
    "23": "Equipo Electrónico",
    "24": "Garantía",
    "25": "Fidelidad",
    "26": "Extensión y Garantía",
    "27": "Crédito por Ventas a Plazo",
    "28": "Crédito a la Exportación",
    "29": "Otros Seguros de Crédito",
    "30": "Salud",
    "31": "Accidentes Personales",
    "32": "SOAP",
    "33": "Cesantía",
    "34": "Título",
    "35": "Agrícola",
    "36": "Asistencia",
    "50": "Otros Seguros Gen.",
    "999": "TOTAL VIDA",
    "100": "Vida Individual",
    "101": "Vida Entera Individual",
    "102": "Temporal de Vida Individual",
    "103": "Cuenta Única de Inversión Individual",
    "104": "Mixto/Dotal Individual",
    "105": "Rentas Privadas/Otras Rentas Individuales",
    "106": "Dotal/Capt. Diferido Individual",
    "107": "Protección Familiar Individual",
    "108": "Incapacidad/Invalidez Individual",
    "109": "Salud Individual",
    "110": "Accidentes Personales Individual",
    "111": "Asistencia Individual",
    "112": "Desgravamen Hipotecario Individual",
    "113": "Desgravamen Consumos/Otros Individual",
    "114": "SOAP Individual",
    "150": "Otros Vida Individual",
    "200": "Colectivos Tradicionales",
    "201": "Vida Entera Colectivo",
    "202": "Temporal de Vida Colectivo",
    "203": "Cuenta Única de Inversión Colectivo",
    "204": "Mixto/Dotal Colectivo",
    "205": "Rentas Privadas/Otras Rentas Colectivo",
    "206": "Dotal/Capt. Diferido Colectivo",
    "207": "Protección Familiar Colectivo",
    "208": "Incapacidad/Invalidez Colectivo",
    "209": "Salud Colectivo",
    "210": "Accidentes Personales Colectivo",
    "211": "Asistencia Colectivo",
    "212": "Desgravamen Hipotecario Colectivo",
    "213": "Desgravamen Consumos/Otros Colectivo",
    "214": "SOAP Colectivo",
    "250": "Otros Vida Colectivo",
    "300": "Banca Seguros y Retail",
    "301": "Vida Entera Banca/Retail",
    "302": "Temporal de Vida Banca/Retail",
    "303": "Cuenta Única de Inversión Banca",
    "304": "Mixto/Dotal Banca/Retail",
    "305": "Rentas Privadas/Otras Rentas Banca/Retail",
    "306": "Dotal/Capt. Diferido Banca/Retail",
    "307": "Protección Familiar Banca/Retail",
    "308": "Incapacidad/Invalidez Banca/Retail",
    "309": "Salud Banca/Retail",
    "310": "Accidentes Personales Banca/Retail",
    "311": "Asistencia Banca/Retail",
    "312": "Desgravamen Hipotecario Banca/Retail",
    "313": "Desgravamen Consumos/Otros Banca/Retail",
    "314": "SOAP Banca/Retail",
    "350": "Otros Banca/Retail",
    "400": "Seguros Previsionales",
    "420": "Invalidez y Sobrevivencia SIS",
    "421": "Renta Vitalicia Vejez",
    "422": "Renta Vitalicia de Invalidez",
    "423": "Vitalicia Sobrevivencia",
    "424": "Invalidez y Sobrevivencia C-528",
    "425": "Seguro Ahorro Previsional APV",
    "426": "Seguro Ahorro Previsional Colectivo APVC",
}

REGIONES = {
    "1": "Tarapacá", "01": "Tarapacá",
    "2": "Antofagasta", "02": "Antofagasta",
    "3": "Atacama", "03": "Atacama",
    "4": "Coquimbo", "04": "Coquimbo",
    "5": "Valparaíso", "05": "Valparaíso",
    "6": "O'Higgins", "06": "O'Higgins",
    "7": "Maule", "07": "Maule",
    "8": "Biobío", "08": "Biobío",
    "9": "La Araucanía", "09": "La Araucanía",
    "10": "Los Lagos",
    "11": "Aysén",
    "12": "Magallanes",
    "13": "Metropolitana",
    "14": "Los Ríos",
    "15": "Arica y Parinacota",
    "16": "Ñuble",
}

# ──────────────────────────────────────────────────────────────
# CARGA DE DATOS (cacheada)
# ──────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent

@st.cache_data(show_spinner="Cargando datos FECU…")
def load_data():
    identifi = pd.read_csv(DATA_DIR / "identifi.csv.gz", compression="gzip")
    intercia = pd.read_csv(DATA_DIR / "intercia.csv.gz", compression="gzip")
    prodramo = pd.read_csv(DATA_DIR / "prodramo.csv.gz", compression="gzip")
    # Normalizar RUTs: int → string sin ceros a la izquierda
    for df in [identifi, intercia, prodramo]:
        if "rut" in df.columns:
            df["rut"] = df["rut"].astype(str).str.strip().str.lstrip("0")
    # RUT compañía
    if "rut_cia" in intercia.columns:
        intercia["rut_cia"] = intercia["rut_cia"].astype(str).str.strip().str.lstrip("0")
    # anio como string
    for df in [intercia, prodramo]:
        if "anio" in df.columns:
            df["anio"] = df["anio"].astype(str)
    # codigo_ramo como string (sin ceros a la izquierda, igual que las claves del dict RAMOS)
    if "codigo_ramo" in prodramo.columns:
        prodramo["codigo_ramo"] = prodramo["codigo_ramo"].astype(str).str.strip().str.lstrip("0")
    # grupo como string
    for df in [intercia, prodramo]:
        if "grupo" in df.columns:
            df["grupo"] = df["grupo"].astype(str).str.strip()
    # dv como string
    for df in [identifi, intercia, prodramo]:
        if "dv" in df.columns:
            df["dv"] = df["dv"].astype(str).str.strip()
    return identifi, intercia, prodramo

identifi, intercia, prodramo = load_data()

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
def uf(v):
    """Formatea un monto en miles de pesos (M$)."""
    if pd.isna(v):
        return "—"
    return f"$ {v:,.0f}".replace(",", ".")

def delta_pct(new, old):
    if not old or old == 0:
        return None
    return (new - old) / abs(old) * 100

def color_delta(pct):
    if pct is None:
        return ""
    if pct > 0:
        return f"🟢 +{pct:.1f}%"
    if pct < 0:
        return f"🔴 {pct:.1f}%"
    return f"⚪ {pct:.1f}%"

def rut_display(rut, dv):
    """Formatea RUT con puntos y guión: 12.345.678-9"""
    try:
        n = int(rut)
        s = f"{n:,}".replace(",", ".")
        return f"{s}-{dv}"
    except:
        return f"{rut}-{dv}"

def get_totales_corredor(rut):
    """Tabla de totales por año para un corredor dado."""
    rows = []
    for anio in AÑOS:
        ci = intercia[(intercia["rut"] == rut) & (intercia["anio"] == anio)]
        if ci.empty:
            rows.append({"Año": anio, "Generales (M$)": 0, "Vida (M$)": 0, "Total (M$)": 0})
            continue
        # Totales: num_sec == '99' para generales, '999' para vida (o cualquier TOTAL)
        # En la FECU: nombre_cia == 'TOTAL' es el subtotal por grupo
        # grupo 1 = generales, grupo 2 = vida
        gen = ci[(ci["grupo"] == "1") & (ci["nombre_cia"].str.upper().str.strip() == "TOTAL")]["monto"].sum()
        vid = ci[(ci["grupo"] == "2") & (ci["nombre_cia"].str.upper().str.strip() == "TOTAL")]["monto"].sum()
        rows.append({
            "Año": anio,
            "Generales (M$)": gen,
            "Vida (M$)": vid,
            "Total (M$)": gen + vid,
        })
    return pd.DataFrame(rows)

# ──────────────────────────────────────────────────────────────
# CSS PERSONALIZADO
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Header de la app */
[data-testid="stAppViewContainer"] { background: #0f1117; }
.main-header {
    background: linear-gradient(135deg, #0d8f96 0%, #076e75 100%);
    padding: 1.2rem 2rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1rem;
}
.main-header h1 { color: white; margin: 0; font-size: 1.5rem; font-weight: 700; }
.main-header p { color: rgba(255,255,255,0.75); margin: 0; font-size: 0.85rem; }

/* Cards de KPI */
.kpi-card {
    background: #1e2128;
    border: 1px solid #3a4050;
    border-radius: 0.625rem;
    padding: 1rem 1.25rem;
    text-align: center;
}
.kpi-label { color: #aab; font-size: 0.72rem; text-transform: uppercase; letter-spacing: .05em; }
.kpi-value { color: #4dd6e0; font-size: 1.35rem; font-weight: 700; font-family: monospace; margin: 4px 0; }
.kpi-delta { font-size: 0.75rem; }

/* Ficha corredor */
.corredor-card {
    background: #1a1d23;
    border: 1px solid #2a2d35;
    border-left: 4px solid #4dd6e0;
    border-radius: 0.625rem;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
}
.corredor-nombre { font-size: 1.3rem; font-weight: 700; color: #f0ede8; margin: 0; }
.corredor-rut { font-family: monospace; font-size: 0.9rem; color: #888; }
.corredor-meta { display: flex; gap: 2rem; flex-wrap: wrap; margin-top: 0.5rem; }
.corredor-meta span { font-size: 0.82rem; color: #bbb; }
.corredor-meta strong { color: #e8e8e8; }

/* Tablas */
.stDataFrame { border-radius: 0.5rem; overflow: hidden; }

/* Divisor */
.fecu-divider { border-top: 1px solid #2a2d35; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <div>
    <h1>📋 FECU Corredores · Securicom</h1>
    <p>Análisis competitivo · CMF Chile 2017–2025 · Valores en M$ (miles de pesos)</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# BÚSQUEDA
# ──────────────────────────────────────────────────────────────
col_search, col_año = st.columns([3, 1])

with col_search:
    consulta = st.text_input(
        "🔍 Buscar corredor por nombre o RUT:",
        placeholder="Ej: MARSH   o   025959302",
        key="busqueda_principal",
    )

with col_año:
    año_seleccionado = st.selectbox(
        "Año base:",
        options=AÑOS[::-1],  # Descendente: 2025 primero
        index=0,
        key="año_base",
    )

# ──────────────────────────────────────────────────────────────
# RESULTADOS DE BÚSQUEDA
# ──────────────────────────────────────────────────────────────
if not consulta:
    st.info("Ingresá nombre o RUT de un corredor para ver su ficha FECU.")
    st.stop()

q = consulta.strip().upper()
mask = (
    identifi["nombre"].str.upper().str.contains(q, na=False) |
    identifi["rut"].str.contains(consulta.strip(), na=False)
)
resultados = identifi[mask].reset_index(drop=True)

if resultados.empty:
    st.warning(f"No se encontraron corredores para: **{consulta}**")
    st.stop()

# Selector de corredor
opciones = resultados.apply(
    lambda r: f"{r['nombre'].strip()}  [{rut_display(r['rut'], r['dv'])}]",
    axis=1
).tolist()

elegido_idx = st.selectbox(
    f"Resultados ({len(resultados)}):",
    range(len(opciones)),
    format_func=lambda i: opciones[i],
    key="selector_corredor",
)

corredor = resultados.iloc[elegido_idx]
rut = corredor["rut"]
dv = corredor["dv"]
nombre = str(corredor["nombre"]).strip() if pd.notna(corredor["nombre"]) else ""
ciudad = str(corredor["ciudad"]).strip() if pd.notna(corredor["ciudad"]) else ""
_region_raw = str(corredor["region"]).strip() if pd.notna(corredor["region"]) else ""
region = REGIONES.get(_region_raw, _region_raw)
tipo = "Persona Natural" if corredor["tipo_persona"] == "N" else "Persona Jurídica"

# ──────────────────────────────────────────────────────────────
# FICHA DEL CORREDOR
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="corredor-card">
  <div class="corredor-nombre">{nombre}</div>
  <div class="corredor-rut">RUT {rut_display(rut, dv)}</div>
  <div class="corredor-meta">
    <span>📍 <strong>{ciudad}</strong></span>
    <span>🗺 <strong>Región {region}</strong></span>
    <span>👤 <strong>{tipo}</strong></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# TABLA DE EVOLUCIÓN MULTI-AÑO (siempre visible)
# ──────────────────────────────────────────────────────────────
st.subheader("📈 Evolución FECU 2017–2025")

df_evol = get_totales_corredor(rut)
df_evol_display = df_evol.copy()

# Agregar columna de variación
totales = df_evol["Total (M$)"].tolist()
variaciones = [None] + [
    delta_pct(totales[i], totales[i-1]) for i in range(1, len(totales))
]
df_evol_display["Var. anual"] = [color_delta(v) for v in variaciones]

# Formatear montos
for col in ["Generales (M$)", "Vida (M$)", "Total (M$)"]:
    df_evol_display[col] = df_evol[col].apply(lambda v: uf(v) if v != 0 else "—")

# Destacar el año seleccionado
def highlight_year(row):
    if row["Año"] == año_seleccionado:
        return ["background-color: #1a3538"] * len(row)
    if all(v == "—" for v in [row["Generales (M$)"], row["Vida (M$)"], row["Total (M$)"]]):
        return ["color: #555"] * len(row)
    return [""] * len(row)

st.dataframe(
    df_evol_display.style.apply(highlight_year, axis=1),
    use_container_width=True,
    hide_index=True,
    height=380,
)

# Gráfico de evolución
df_graf = df_evol[df_evol["Total (M$)"] > 0].copy()
if not df_graf.empty:
    fig_evol = go.Figure()
    fig_evol.add_trace(go.Bar(
        x=df_graf["Año"], y=df_graf["Generales (M$)"],
        name="Generales", marker_color="#4dd6e0",
        hovertemplate="<b>%{x}</b><br>Generales: $ %{y:,.0f}<extra></extra>",
    ))
    fig_evol.add_trace(go.Bar(
        x=df_graf["Año"], y=df_graf["Vida (M$)"],
        name="Vida", marker_color="#f5c842",
        hovertemplate="<b>%{x}</b><br>Vida: $ %{y:,.0f}<extra></extra>",
    ))
    fig_evol.update_layout(
        barmode="stack",
        plot_bgcolor="#0f1117",
        paper_bgcolor="#0f1117",
        font_color="#ccc",
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
        height=260,
        xaxis=dict(gridcolor="#2a2d35"),
        yaxis=dict(gridcolor="#3a3d45", tickformat=",.0f", color="#ccc"),
    )
    # Línea de total
    fig_evol.add_trace(go.Scatter(
        x=df_graf["Año"], y=df_graf["Total (M$)"],
        name="Total", mode="lines+markers",
        line=dict(color="#ffffff", width=2, dash="dot"),
        marker=dict(size=4),
        hovertemplate="<b>%{x}</b><br>Total: $ %{y:,.0f}<extra></extra>",
    ))
    st.plotly_chart(fig_evol, use_container_width=True)

st.markdown('<div class="fecu-divider"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# DETALLE DEL AÑO SELECCIONADO
# ──────────────────────────────────────────────────────────────
st.subheader(f"🔎 Detalle FECU {año_seleccionado}")

ci_año = intercia[(intercia["rut"] == rut) & (intercia["anio"] == año_seleccionado)].copy()
pr_año = prodramo[(prodramo["rut"] == rut) & (prodramo["anio"] == año_seleccionado)].copy()

if ci_año.empty and pr_año.empty:
    st.warning(f"Sin datos FECU para este corredor en {año_seleccionado}.")
else:
    # KPIs del año
    total_gen = df_evol[df_evol["Año"] == año_seleccionado]["Generales (M$)"].values
    total_vid = df_evol[df_evol["Año"] == año_seleccionado]["Vida (M$)"].values
    total_tot = df_evol[df_evol["Año"] == año_seleccionado]["Total (M$)"].values

    total_gen = float(total_gen[0]) if len(total_gen) else 0
    total_vid = float(total_vid[0]) if len(total_vid) else 0
    total_tot = float(total_tot[0]) if len(total_tot) else 0

    # Calcular delta respecto al año anterior
    prev_idx = AÑOS.index(año_seleccionado) - 1
    prev_año = AÑOS[prev_idx] if prev_idx >= 0 else None
    prev_total = df_evol[df_evol["Año"] == prev_año]["Total (M$)"].values if prev_año else []
    prev_total = float(prev_total[0]) if len(prev_total) else None
    var_total = delta_pct(total_tot, prev_total)

    # Número de aseguradoras
    n_cias = ci_año[
        (ci_año["nombre_cia"].str.upper().str.strip() != "TOTAL") & (ci_año["monto"] != 0)
    ]["rut_cia"].nunique()

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Generales</div>
        <div class="kpi-value">{uf(total_gen)}</div>
    </div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Vida</div>
        <div class="kpi-value">{uf(total_vid)}</div>
    </div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total</div>
        <div class="kpi-value">{uf(total_tot)}</div>
        <div class="kpi-delta">{color_delta(var_total)} vs {prev_año or "—"}</div>
    </div>""", unsafe_allow_html=True)
    k4.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Aseguradoras</div>
        <div class="kpi-value" style="color:#e8b340">{n_cias}</div>
    </div>""", unsafe_allow_html=True)

    st.write("")

    col_cia, col_ramo = st.columns(2)

    # ── Producción por Compañía ──────────────────────────────
    with col_cia:
        st.markdown("**Producción por Compañía**")
        if ci_año.empty:
            st.write("Sin datos.")
        else:
            # Excluir filas TOTAL y agrupar por aseguradora
            df_cia = ci_año[
                ci_año["nombre_cia"].str.upper().str.strip() != "TOTAL"
            ].copy()
            df_cia = (
                df_cia.groupby(["rut_cia", "dv_cia", "nombre_cia"])["monto"]
                .sum()
                .reset_index()
                .sort_values("monto", ascending=False)
            )
            df_cia = df_cia[df_cia["monto"] != 0].copy()
            df_cia["RUT Cía."] = df_cia.apply(
                lambda r: rut_display(r["rut_cia"], r["dv_cia"]), axis=1
            )
            df_cia["Monto (M$)"] = df_cia["monto"].apply(uf)
            df_cia["Monto_num"] = df_cia["monto"]

            # Porcentaje
            total_abs = df_cia["monto"].abs().sum()
            df_cia["Share"] = df_cia["monto"].apply(
                lambda v: f"{v/total_abs*100:.1f}%" if total_abs else "—"
            )

            st.dataframe(
                df_cia[["nombre_cia", "RUT Cía.", "Monto (M$)", "Share"]].rename(
                    columns={"nombre_cia": "Compañía"}
                ),
                use_container_width=True,
                hide_index=True,
                height=min(35 + len(df_cia) * 35, 420),
            )

            # Donut
            if len(df_cia) > 0:
                df_pie = df_cia[df_cia["monto"] > 0].nlargest(10, "monto")
                if len(df_pie) > 0:
                    fig_pie = px.pie(
                        df_pie,
                        values="monto",
                        names="nombre_cia",
                        hole=0.55,
                        color_discrete_sequence=px.colors.qualitative.Set2,
                    )
                    fig_pie.update_layout(
                        plot_bgcolor="#0f1117",
                        paper_bgcolor="#0f1117",
                        font_color="#ccc",
                        margin=dict(l=0, r=0, t=0, b=0),
                        height=220,
                        showlegend=True,
                        legend=dict(font=dict(size=10)),
                    )
                    fig_pie.update_traces(
                        textposition="inside",
                        textinfo="percent",
                        hovertemplate="<b>%{label}</b><br>$ %{value:,.0f}<br>%{percent}<extra></extra>",
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

    # ── Producción por Ramo ──────────────────────────────────
    with col_ramo:
        st.markdown("**Producción por Ramo**")
        if pr_año.empty:
            st.write("Sin datos.")
        else:
            df_ramo = pr_año.copy()
            df_ramo["ramo_desc"] = df_ramo["codigo_ramo"].map(RAMOS).fillna(
                df_ramo["codigo_ramo"].apply(lambda c: f"Ramo {c}")
            )
            df_agg = (
                df_ramo.groupby("ramo_desc")["monto"]
                .sum()
                .reset_index()
                .sort_values("monto", ascending=False)
            )
            df_agg = df_agg[df_agg["monto"] != 0].copy()
            df_agg["Monto (M$)"] = df_agg["monto"].apply(uf)

            # Porcentaje
            total_r = df_agg["monto"].abs().sum()
            df_agg["Share"] = df_agg["monto"].apply(
                lambda v: f"{v/total_r*100:.1f}%" if total_r else "—"
            )

            st.dataframe(
                df_agg[["ramo_desc", "Monto (M$)", "Share"]].rename(
                    columns={"ramo_desc": "Ramo"}
                ),
                use_container_width=True,
                hide_index=True,
                height=min(35 + len(df_agg) * 35, 420),
            )

            # Barras horizontales (top 10 ramos)
            df_bar = df_agg[df_agg["monto"] > 0].head(10).sort_values("monto")
            if not df_bar.empty:
                fig_bar = go.Figure(go.Bar(
                    x=df_bar["monto"],
                    y=df_bar["ramo_desc"],
                    orientation="h",
                    marker_color="#4dd6e0",
                    hovertemplate="<b>%{y}</b><br>$ %{x:,.0f}<extra></extra>",
                ))
                fig_bar.update_layout(
                    plot_bgcolor="#0f1117",
                    paper_bgcolor="#0f1117",
                    font_color="#ccc",
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=220,
                    xaxis=dict(gridcolor="#2a2d35", tickformat=",.0f"),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

st.markdown('<div class="fecu-divider"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# EVOLUCIÓN DE COMPAÑÍAS AÑO A AÑO
# ──────────────────────────────────────────────────────────────
st.subheader("🏢 Evolución por Compañía (todos los años)")

ci_all = intercia[
    (intercia["rut"] == rut) &
    (~intercia["nombre_cia"].str.upper().str.strip().isin(["TOTAL"]))
].copy()

if not ci_all.empty:
    df_cia_evol = (
        ci_all.groupby(["anio", "nombre_cia"])["monto"]
        .sum()
        .reset_index()
    )
    df_cia_evol = df_cia_evol[df_cia_evol["monto"] != 0]

    # Top 8 compañías por monto total
    top_cias = (
        df_cia_evol.groupby("nombre_cia")["monto"]
        .sum()
        .nlargest(8)
        .index.tolist()
    )
    df_cia_evol_top = df_cia_evol[df_cia_evol["nombre_cia"].isin(top_cias)]

    fig_cia_evol = px.line(
        df_cia_evol_top,
        x="anio", y="monto", color="nombre_cia",
        markers=True,
        labels={"anio": "Año", "monto": "Prima (M$)", "nombre_cia": "Compañía"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_cia_evol.update_layout(
        plot_bgcolor="#0f1117",
        paper_bgcolor="#0f1117",
        font_color="#ccc",
        margin=dict(l=0, r=0, t=10, b=0),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1, font=dict(size=10)),
        xaxis=dict(gridcolor="#2a2d35"),
        yaxis=dict(gridcolor="#2a2d35", tickformat=",.0f"),
    )
    fig_cia_evol.update_traces(
        hovertemplate="<b>%{x}</b> · %{fullData.name}<br>$ %{y:,.0f}<extra></extra>"
    )
    st.plotly_chart(fig_cia_evol, use_container_width=True)

    # Tabla pivot compañías × años
    df_pivot = df_cia_evol[df_cia_evol["nombre_cia"].isin(top_cias)].pivot_table(
        index="nombre_cia", columns="anio", values="monto", aggfunc="sum", fill_value=0
    ).reset_index()
    df_pivot.columns.name = None
    # Formatear
    año_cols = [c for c in df_pivot.columns if c != "nombre_cia"]
    for c in año_cols:
        df_pivot[c] = df_pivot[c].apply(lambda v: uf(v) if v != 0 else "—")
    df_pivot = df_pivot.rename(columns={"nombre_cia": "Compañía"})
    st.dataframe(df_pivot, use_container_width=True, hide_index=True)

st.markdown('<div class="fecu-divider"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center;color:#555;font-size:0.78rem;padding-top:0.5rem'>"
    "Fuente: <b>CMF Chile</b> — FECU Corredores de Seguros · Diciembre 2017–2025 · "
    "Valores en M$ (miles de pesos) · Uso interno Securicom"
    "</div>",
    unsafe_allow_html=True,
)
