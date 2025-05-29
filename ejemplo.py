import streamlit as st
import pandas as pd

# 1. Crear un DataFrame de ejemplo
data = {
    'ID Producto': [101, 102, 103, 104, 105],
    'Nombre': ['Laptop Pro', 'Mouse Gamer', 'Teclado Mecánico', 'Monitor 4K', 'Webcam HD'],
    'Categoría': ['Electrónica', 'Accesorios', 'Accesorios', 'Monitores', 'Periféricos'],
    'Precio ($)': [1200.00, 45.50, 89.99, 350.00, 60.75],
    'Stock': [15, 50, 30, 10, 25]
}
df = pd.DataFrame(data)

# Definimos una clave para nuestro DataFrame para acceder a su estado
DATAFRAME_WIDGET_KEY = "df_con_callback"

# 2. Función Callback para manejar la selección
def procesar_seleccion_df():
    """
    Esta función es el 'callable'. Se ejecuta cuando la selección en el DataFrame cambia.
    Actualiza st.session_state con los detalles de la fila seleccionada.
    """
    # El estado de la selección está en st.session_state usando la clave del widget
    if DATAFRAME_WIDGET_KEY in st.session_state:
        estado_seleccion = st.session_state[DATAFRAME_WIDGET_KEY].selection

        if estado_seleccion.rows: # .rows contiene los índices de las filas seleccionadas
            # Para 'single-row', tomamos el primer (y único) índice
            indice_fila = estado_seleccion.rows[0]
            fila_datos = df.iloc[indice_fila] # Obtiene la Serie de Pandas para la fila

            # Guardamos los datos de la fila y su índice en st.session_state
            # para que el resto del script pueda acceder a ellos después del rerun.
            st.session_state.datos_fila_seleccionada_callback = fila_datos
            st.session_state.indice_fila_seleccionada_callback = indice_fila
            # print(f"Callback ejecutado: Fila seleccionada con índice {indice_fila}") # Para depuración en consola
        else:
            # Si no hay filas seleccionadas, limpiamos el estado
            st.session_state.datos_fila_seleccionada_callback = None
            st.session_state.indice_fila_seleccionada_callback = None
            # print("Callback ejecutado: Selección eliminada") # Para depuración en consola
    # Streamlit re-ejecutará el script después de que este callback termine.

# 3. Inicializar variables en st.session_state si no existen
# Esto es importante para evitar errores en la primera ejecución antes de cualquier selección.
if 'datos_fila_seleccionada_callback' not in st.session_state:
    st.session_state.datos_fila_seleccionada_callback = None
if 'indice_fila_seleccionada_callback' not in st.session_state:
    st.session_state.indice_fila_seleccionada_callback = None


# --- Interfaz de Usuario de Streamlit ---
st.title("📄 DataFrame con Selección (usando `callable`)")

st.markdown("""
Haz clic en una fila de la tabla de abajo. La selección activará una función **callback**
que procesará los datos. La información de la fila seleccionada se mostrará
debajo de la tabla, leída desde `st.session_state` después de que el callback la actualice.
""")

# 4. Mostrar el DataFrame, pasando la función como 'callable' a on_select
st.subheader("Tabla de Productos:")
st.dataframe(
    df,
    key=DATAFRAME_WIDGET_KEY, # Muy importante para que el callback acceda al estado correcto
    on_select=procesar_seleccion_df, # Aquí se pasa la función directamente
    selection_mode="single-row", # Modo de selección (puede ser "multi-row")
    hide_index=True
)

# 5. Mostrar la información de la fila seleccionada
# Esta parte del script se ejecuta después del rerun (que es disparado por la selección).
# Lee los datos que el callback 'procesar_seleccion_df' guardó en st.session_state.
st.subheader("Información de la Fila Seleccionada:")
if st.session_state.datos_fila_seleccionada_callback is not None:
    st.write(f"Índice de la fila en el DataFrame original: `{st.session_state.indice_fila_seleccionada_callback}`")

    # st.session_state.datos_fila_seleccionada_callback es una Serie de Pandas
    # La convertimos a un DataFrame de una fila y la transponemos para mejor visualización.
    st.dataframe(st.session_state.datos_fila_seleccionada_callback.to_frame().T, hide_index=True)

    # También podrías imprimirlo como un diccionario JSON:
    # st.write("Datos en formato JSON:")
    # st.json(st.session_state.datos_fila_seleccionada_callback.to_dict())
else:
    st.info("Haz clic en una fila de la tabla para ver sus detalles aquí.")

st.caption("La selección es procesada por una función callback que actualiza el estado de la sesión.")