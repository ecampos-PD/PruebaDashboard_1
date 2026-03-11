import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="PuenteData - Dashboard Demo", layout="wide")

# 2. Título y Estética
st.title("📊 Panel de Control Logístico | PuenteData")
st.markdown("---")

# 3. Datos de Ejemplo (Simulando una base de datos de PyME)
# En el futuro, aquí conectarás tu SQL o Google Sheets

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSvLJ45rzlyN5HS6jtMelQDnHZ_8seuy5jGpcInXW9UnYNgM8GNfxGqmfkv0yld2sI8BQCv2a5msnD1/pub?output=csv"

try:
    # LA CORRECCIÓN: Usamos read_csv en lugar de DataFrame()
    df = pd.read_csv(sheet_url)
    
    # Limpieza básica: Aseguramos que las columnas numéricas sean números
    df['Costo_Envio'] = pd.to_numeric(df['Costo_Envio'], errors='coerce')
    df['Tiempo_Entrega_Dias'] = pd.to_numeric(df['Tiempo_Entrega_Dias'], errors='coerce')
    
except Exception as e:
    st.error(f"No pude conectar con Google Sheets. Revisa el link. Error: {e}")
    st.stop() # Detiene la ejecución si no hay datos

# 4. Métricas Clave (Los KPIs que "atrapan" al cliente)
col1, col2, col3 = st.columns(3)

with col1:
    otif_meta = 90
    otif_actual = 70 # Simulando un cálculo
    st.metric(label="OTIF (Entregas a Tiempo)", value=f"{otif_actual}%", delta=f"{otif_actual - otif_meta}% vs Meta")

with col2:
    costo_total = df['Costo_Envio'].sum()
    st.metric(label="Gasto Logístico Total", value=f"${costo_total} USD")

with col3:
    promedio_dias = df['Tiempo_Entrega_Dias'].mean()
    st.metric(label="Promedio Días de Entrega", value=f"{promedio_dias} días")

st.markdown("---")

# 5. Gráficos Visuales
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Estado de los Pedidos")
    fig_pie = px.pie(df, names='Estado', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Costo de Envío por Pedido")
    fig_bar = px.bar(df, x='Pedido_ID', y='Costo_Envio', color='Estado', text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. Tabla de datos interactiva
st.subheader("Detalle de Operaciones")
st.dataframe(df, use_container_width=True)