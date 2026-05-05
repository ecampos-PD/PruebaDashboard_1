import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="PuenteData - Dashboard Demo", layout="wide")

#  --- BASIC LOGIN SYSTEM ---
def check_password():
    """Returns True if the the password"""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"] # Deletes password from memory
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Pantalla de inicio de sesión
        st.text_input("Contraseña de Acceso - PuenteData", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Incorrect password
        st.text_input("Contraseña incorrecta. Intenta de nuevo:", type="password", on_change=password_entered, key="password")
        st.error("😕 Acceso denegado")
        return False
    else:
        return True
    
if not check_password():
    st.stop() # Stops the app if theres not a correct login

st.success("¡Bienvenido Mr. Puenti!")



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

# --- SECCIÓN DE TENDENCIAS (Áreas) ---
st.subheader("📈 Tendencia de Ingresos vs Costos Logísticos")
# Simulamos datos de tendencia
df_trend = pd.DataFrame({
    'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'Ingresos': [100000, 120000, 110000, 140000, 150000, 170000],
    'Costos': [40000, 45000, 42000, 48000, 50000, 52000]
})
fig_area = px.area(df_trend, x='Mes', y=['Ingresos', 'Costos'], 
                   color_discrete_sequence=['#22c55e', '#ef4444'], # Verde y Rojo
                   title="Eficiencia de Margen Operativo")
st.plotly_chart(fig_area, use_container_width=True)

# --- SECCIÓN DE RENDIMIENTO POR RUTA (Barras Horizontales) ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🚛 Eficiencia por Ruta")
    rutas_data = {'Ruta': ['Norte', 'Sur', 'Bajío', 'Occidente'], 'Eficiencia': [95, 82, 88, 75]}
    fig_rutas = px.bar(rutas_data, x='Eficiencia', y='Ruta', orientation='h', 
                       color='Eficiencia', color_continuous_scale='Viridis')
    st.plotly_chart(fig_rutas, use_container_width=True)

with col_b:
    # --- MÉTRICA DE IMPACTO IA (Para el paquete avanzado) ---
    st.subheader("🤖 Optimización con IA")
    st.info("El algoritmo de PuenteData ha sugerido una re-ruta que reduciría el gasto de hoy en:")
    st.metric(label="Ahorro Estimado Hoy", value="$1,250 MXN", delta="12% menos combustible")
    st.success("Sugerencia: Consolidar pedidos de Ruta Occidente con Ruta Bajío.")

# --- TABLA DE ALERTA DE DATOS ---
st.subheader("📋 Auditoría de Calidad de Datos")
st.warning("Se detectaron 3 registros con direcciones incompletas que afectan el cálculo de ruta.")

# 6. Tabla de datos interactiva
st.subheader("Detalle de Operaciones")
st.dataframe(df, use_container_width=True)