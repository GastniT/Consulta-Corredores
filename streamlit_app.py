import streamlit as st
import pandas as pd

# Definición de estructura para identifi.txt
identifi_colspecs = [
    (1, 10),     # rut
    (10, 11),    # dv
    (11, 111),   # nombre
    (112, 120),  # telefono
    (121, 160),  # domicilio
    (161, 180),  # ciudad
    (182, 183),  # region
    (183, 184)   # tipo_persona
]

identifi_colnames = ['rut', 'dv', 'nombre', 'telefono', 'domicilio', 'ciudad', 'region', 'tipo_persona']

# Definición de estructura para intercia.txt
intercia_colspecs = [
    (1, 7),      # periodo
    (8, 17),     # rut
    (17, 18),    # dv
    (19, 20),    # grupo
    (21, 23),    # num_secuencia
    (24, 33),    # rut_cia
    (33, 34),    # dv_cia
    (34, 54),    # nombre_cia
    (55, 55),    # signo
    (56, 66),    # monto
]

intercia_colnames = ['periodo', 'rut', 'dv', 'grupo', 'num_secuencia', 'rut_cia', 'dv_cia', 'nombre_cia', 'signo', 'monto']

st.title("Consulta simple de Corredores de Seguros")
idfile = st.file_uploader("Sube el archivo identifi.txt", type='txt')
intfile = st.file_uploader("Sube el archivo intercia.txt", type='txt')

if idfile and intfile:
    identifi = pd.read_fwf(idfile, colspecs=identifi_colspecs, names=identifi_colnames, encoding='latin1', dtype=str)
    intercia = pd.read_fwf(intfile, colspecs=intercia_colspecs, names=intercia_colnames, encoding='latin1', dtype=str)
    consulta = st.text_input("Buscar por nombre o RUT:")
    if consulta:
        mask = identifi['nombre'].str.contains(consulta.upper(), na=False) | identifi['rut'].str.contains(consulta)
        resultados = identifi[mask]
        st.write("Corredores encontrados:", resultados)
        if not resultados.empty:
            # ver intermediación por RUT
            ruts = resultados['rut'].tolist()
            int_filtrada = intercia[intercia['rut'].isin(ruts)]
            st.write("Intermediaciones relacionadas:", int_filtrada)
    else:
        st.write("Ingrese un nombre o RUT para comenzar la búsqueda.")

else:
    st.info("Primero sube ambos archivos .txt para habilitar la búsqueda.")
