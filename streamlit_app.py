import streamlit as st
import pandas as pd

# Diccionario RAMOS completo. Puedes separarlo en un ramos.py si prefieres y hacer from ramos import RAMOS 
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
    "421.1": "Vejez Normal",
    "421.2": "Vejez Anticipada",
    "422": "Renta Vitalicia de Invalidez",
    "422.1": "Invalidez Total",
    "422.2": "Invalidez Parcial",
    "423": "Vitalicia Sobrevivencia",
    "424": "Invalidez y Sobrevivencia C-528",
    "425": "Seguro Ahorro Previsional APV",
    "426": "Seguro Ahorro Previsional Colectivo APVC"
}

identifi_colspecs = [
    (1, 10), (10, 11), (11, 111), (112, 120), (121, 160), (161, 180), (182, 183), (183, 184)
]
identifi_colnames = ['rut', 'dv', 'nombre', 'telefono', 'domicilio', 'ciudad', 'region', 'tipo_persona']

intercia_colspecs = [
    (1, 7), (8, 17), (17, 18), (19, 20), (21, 23), (24, 33), (33, 34), (34, 54), (55, 55), (56, 66),
]
intercia_colnames = ['periodo', 'rut', 'dv', 'grupo', 'num_secuencia', 'rut_cia', 'dv_cia', 'nombre_cia', 'signo', 'monto']

prodramo_colspecs = [
    (1, 7), (8, 17), (17, 18), (19, 20), (22, 25), (26, 36),
]
prodramo_colnames = ['periodo', 'rut', 'dv', 'grupo', 'codigo_ramo', 'monto']

st.title("Consulta Intermediarios con Producción por Ramo y Compañía")
idfile = st.file_uploader("Sube identifi.txt", type='txt')
intfile = st.file_uploader("Sube intercia.txt", type='txt')
prodfile = st.file_uploader("Sube prodramo.txt", type='txt')

if idfile and intfile and prodfile:
    identifi = pd.read_fwf(idfile, colspecs=identifi_colspecs, names=identifi_colnames, encoding='latin1', dtype=str)
    intercia = pd.read_fwf(intfile, colspecs=intercia_colspecs, names=intercia_colnames, encoding='latin1', dtype=str)
    prodramo = pd.read_fwf(prodfile, colspecs=prodramo_colspecs, names=prodramo_colnames, encoding='latin1', dtype=str)
    consulta = st.text_input("Buscar por nombre o RUT:")

    if consulta:
        mask = identifi['nombre'].str.contains(consulta.upper(), na=False) | identifi['rut'].str.contains(consulta)
        resultados = identifi[mask].reset_index(drop=True)
        if not resultados.empty:
            corredor_opciones = resultados['nombre'] + " [" + resultados['rut'] + "-" + resultados['dv'] + "]"
            elegido_idx = st.selectbox(
                "Selecciona un corredor:",
                range(len(corredor_opciones)),
                format_func=lambda i: corredor_opciones[i],
            )
            elegido_rut = resultados.loc[elegido_idx, 'rut']
            st.write("Ficha:", resultados.loc[[elegido_idx]])

            # Filtrar datos por el seleccionado
            ruts = [elegido_rut]
            int_filtrada = intercia[intercia['rut'].isin(ruts)].copy()
            int_filtrada['monto'] = int_filtrada['monto'].astype(float) * 1000
            int_filtrada['monto'] = int_filtrada['monto'].map('${:,.0f}'.format)
            st.write("Producción por Compañía", int_filtrada[['nombre_cia', 'monto']])

            # Tabla por ramo
            prod_ramos = prodramo[prodramo['rut'].isin(ruts)].copy()
            prod_ramos['codigo_ramo'] = prod_ramos['codigo_ramo'].astype(str).str.lstrip('0')
            prod_ramos['monto'] = prod_ramos['monto'].astype(float) * 1000
            prod_agg = prod_ramos.groupby('codigo_ramo')['monto'].sum().reset_index()
            prod_agg['ramo'] = prod_agg['codigo_ramo'].map(RAMOS)
            prod_agg['ramo'] = prod_agg['ramo'].fillna(prod_agg['codigo_ramo'])
            prod_agg['monto'] = prod_agg['monto'].map('${:,.0f}'.format)
            prod_agg = prod_agg[['ramo', 'monto']]
            st.write("Producción por Ramo", prod_agg)
        else:
            st.write("No se encontraron corredores.")
    else:
        st.write("Ingrese nombre o RUT para la búsqueda.")

else:
    st.info("Sube los tres archivos .txt para habilitar la búsqueda.")
