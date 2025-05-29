import streamlit as st
import login as login
import dbsopporte as dbs
import pandas as pd
import time

archivo = __file__.split("\\")[-1]

login.generarLogin(archivo)


def agregar_nuevo():
    
    @st.dialog("Agregar Nuevo Usuario")
    def agrega():
        st.write("Ingrese los datos del nuevo usuario")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        correo = st.text_input("Correo")
        contraseña = st.text_input("Contraseña", type="password")
        confirmar_contraseña = st.text_input("Confirmar Contraseña", type="password")
        
        rol = st.selectbox('Rol', ['', 'Admin', 'Usuario', 'Soporte'])
        
        if st.button("Agregar"):
            if nombre == "" or apellido == "" or correo == "" or contraseña == "" or confirmar_contraseña == "" or rol == "":
                st.error("Por favor complete todos los campos")
            else:
                if contraseña == confirmar_contraseña:
                    usuario = f"{nombre[0]}{apellido}"
                    conn = dbs.create_connection("soportes.db")
                    # Es importante que esta función realmente devuelva None si no encuentra usuarios,
                    # o una lista vacía para que la lógica de `if usuarios == None` funcione.
                    # Asumo que dbs.buscar_todos_los_usuarios devuelve None si no hay.
                    usuarios_existentes = dbs.buscar_todos_los_usuarios(conn, "", "", correo, "")
                    
                    if usuarios_existentes is None or len(usuarios_existentes) == 0: # Mejorar la verificación de si el usuario ya existe
                        conn_add = dbs.create_connection("soportes.db") 
                        dbs.agregar_usuario(conn_add, usuario, contraseña, correo, rol, nombre, apellido)
                        st.success("Usuario agregado con éxito")
                        time.sleep(4)
                        st.rerun()
                    else:
                        st.error("El usuario ya existe con ese correo")
                else:
                    st.error("Las contraseñas no coinciden")
    agrega()

def edit(id):
    
    conn = dbs.create_connection("soportes.db")
    usuariof = dbs.buscar_usuario_por_id(conn,f"{id}") 
    
    @st.dialog("Editar Usuario")
    def edita():
        st.write("Revise los datos del usuario a editar")
        
        if usuariof:
            id= st.text_input("ID", value=usuariof[0],disabled=True)
            usua= st.text_input("Usuario", value=usuariof[1],disabled=True)
            contraseña = st.text_input("Contraseña", type="password",value=usuariof[2])
            confirmar_contraseña = st.text_input("Confirmar Contraseña", type="password",value=usuariof[2])
            correo = st.text_input("Correo", value=usuariof[3])
            rol = st.selectbox('Rol', ['', 'Admin', 'Usuario', 'Soporte'])
            nombre = st.text_input("Nombre", value=usuariof[5])
            apellido = st.text_input("Apellido", value=usuariof[6])

            boton= st.button("Guardar")
            if boton:
                if contraseña == "" or confirmar_contraseña == "" or correo == "" or rol == "" or nombre == "" or apellido == ""   :
                    st.error("Por favor complete todos los campos")
                else:
                    if contraseña == confirmar_contraseña:
                        conn = dbs.create_connection("soportes.db")
                        dbs.editar_usuario(conn,id, usua, contraseña, correo, rol, nombre, apellido)
                        st.success("Usuario editado con éxito")
                        time.sleep(4)
                        st.rerun()

                    else:
                        st.error("Las contraseñas no coinciden")
                        edita()
        else:
            st.error("No se encontró el usuario")
        
    edita()

def eliminar_usuario(id):
    conn = dbs.create_connection("soportes.db")
    usuariof = dbs.buscar_usuario_por_id(conn,f"{id}") 
    @st.dialog("Eliminar Usuario")
    def elimina():
        st.write("Desea eliminar usuario?")
    if usuariof:
        pass



if 'usuario' in st.session_state:
    # Asegúrate de que df esté definido antes de que el callback pueda intentar usarlo.
    # Si la aplicación se carga por primera vez y `usuarios` es None, df no existirá.
    # Esto puede causar un NameError si se intenta seleccionar una fila antes de que se carguen los datos.
    # Una buena práctica es inicializar df o manejar el caso donde no hay datos.

    conn = dbs.create_connection("soportes.db")
    usuarios = dbs.buscar_todos_los_usuarios1(conn) # Asumo que esta función devuelve una lista de tuplas o None

    df = pd.DataFrame() # Inicializa df como un DataFrame vacío por defecto
    if usuarios:
        df = pd.DataFrame(usuarios, columns=["Id", "Usuario", "Contraseña", "Rol", "Correo", "Nombre", "Apellido"])
    else:
        st.warning("No se encontraron usuarios en la base de datos.")


    DATAFRAME_WIDGET_KEY = "df_con_callback"

    def procesar_seleccion_df():
        """
        Esta función es el 'callable'. Se ejecuta cuando la selección en el DataFrame cambia.
        Actualiza st.session_state con los detalles de la fila seleccionada.
        """
        if DATAFRAME_WIDGET_KEY in st.session_state:
            estado_seleccion = st.session_state[DATAFRAME_WIDGET_KEY].selection

            if estado_seleccion.rows: # .rows contiene los índices de las filas seleccionadas
                indice_fila = estado_seleccion.rows[0]
                # Asegúrate de que 'df' esté accesible y no esté vacío al llamar a iloc
                if not df.empty:
                    fila_datos = df.iloc[indice_fila] # Obtiene la Serie de Pandas para la fila
                    st.session_state.datos_fila_seleccionada_callback = fila_datos
                    st.session_state.indice_fila_seleccionada_callback = indice_fila
                else:
                    st.session_state.datos_fila_seleccionada_callback = None
                    st.session_state.indice_fila_seleccionada_callback = None
            else:
                # Si no hay filas seleccionadas, limpiamos el estado
                st.session_state.datos_fila_seleccionada_callback = None
                st.session_state.indice_fila_seleccionada_callback = None

    if 'datos_fila_seleccionada_callback' not in st.session_state:
        st.session_state.datos_fila_seleccionada_callback = None
    if 'indice_fila_seleccionada_callback' not in st.session_state:
        st.session_state.indice_fila_seleccionada_callback = None

    # --- Interfaz de Usuario de Streamlit ---
    
    st.header('Página :orange[Admin. Usuarios]')
    st.subheader('Bienvenido, {}'.format(st.session_state['nombre'])) # Asumo que st.session_state['nombre'] está definido

    agregar = st.button('Agregar nuevo usuario', type='primary')
    
    if agregar:
        agregar_nuevo() # Llama a la función agregar_nuevo que contiene el st.dialog


    # El formulario de búsqueda que tenías antes
    with st.form(key='formulario_busqueda_principal'):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            nombre_busqueda = st.text_input('Nombre de usuario', key='nombre_busqueda')
        
        with col2:
            apellido_busqueda = st.text_input('Apellido de usuario', key='apellido_busqueda')

        with col3:
            correo_busqueda = st.text_input('Correo electrónico', key='correo_busqueda')
        
        with col4:
            rol_busqueda = st.selectbox('Rol', ['', 'Admin', 'Usuario', 'Soporte'], key='rol_busqueda')
        
        with col5:
            st.write("") # Espacio para alinear el botón
            boton_buscar = st.form_submit_button('Buscar')

        if boton_buscar:
            if nombre_busqueda != "" or apellido_busqueda != "" or correo_busqueda != "" or rol_busqueda != "":
                conn_search = dbs.create_connection("soportes.db")
                usuarios_filtrados = dbs.buscar_todos_los_usuarios(conn_search, nombre_busqueda, apellido_busqueda, correo_busqueda, rol_busqueda)
                
                if usuarios_filtrados:
                    # Actualizar el DataFrame principal que se muestra
                    df = pd.DataFrame(usuarios_filtrados, columns=["Id", "Usuario", "Contraseña", "Correo", "Rol", "Nombre", "Apellido"])
                else:
                    df = pd.DataFrame() # Vaciar el DataFrame si no hay resultados
                    st.warning('No se encontraron usuarios con los criterios de búsqueda.')
            else:
                st.warning('Por favor, complete al menos un campo para buscar.')

    # Mostrar el DataFrame principal con todos los usuarios o los resultados de la búsqueda
    if not df.empty:
        st.subheader("Tabla de Usuarios:")
        st.dataframe(
            df,
            key=DATAFRAME_WIDGET_KEY,
            on_select=procesar_seleccion_df,
            selection_mode="single-row",
            hide_index=True,
            column_config={
                "Id":"id",
                "Usuario":"Usuario",
                "Contraseña":"Contraseña",
                # CORRECCIÓN AQUÍ: pasar 'options' como argumento con nombre
                "Rol":"Rol",
                "Correo":"Correo",
                "Nombre":"Nombre",
                "Apellido":"Apellido"
            },
        )
    else:
        st.info("No hay usuarios para mostrar o la búsqueda no arrojó resultados.")

    st.subheader("Seleccione Opcion para Usuario Seleccionado:")
    if st.session_state.datos_fila_seleccionada_callback is not None:
        
        st.write(f"Usuario Seleccionado:")
        # Asegúrate de que los datos_fila_seleccionada_callback no estén vacíos antes de intentar transponer
        if not st.session_state.datos_fila_seleccionada_callback.empty:
            st.dataframe(st.session_state.datos_fila_seleccionada_callback.to_frame().T, hide_index=True)
            st.write(f"Seleccione una Accion:")

            editar= st.button("Editar", type='primary')
            eliminar= st.button("Eliminar")
            
            if editar:
                
                edit(st.session_state.datos_fila_seleccionada_callback[0])
            
            if eliminar:
                eliminar_usuario(st.session_state.datos_fila_seleccionada_callback[0])

        else:
            st.info("Haz clic en una fila de la tabla para ver sus detalles aquí.")
    else:
        st.info("Haz clic en una fila de la tabla para ver sus detalles aquí.")

   