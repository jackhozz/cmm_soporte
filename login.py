def main()
    # Importamos las librerías necesarias
    import streamlit as st  
    import pandas as pd  
    from streamlit_cookies_controller import CookieController 
    import dbsopporte as dbs  
    import sqlite3


    # Creamos una instancia de CookieController
    controller = CookieController()

    # Validación simple de usuario y clave con un archivo csv

    def validarUsuario(usuario,clave):    
        """Permite la validación de usuario y clave

        Args:
            usuario (str): usuario a validar
            clave (str): clave del usuario

        Returns:
            bool: True usuario valido, False usuario invalido
        """   

        conn=dbs.create_connection("soportes.db")
        us=dbs.buscar_usuario(conn,usuario,clave) # Buscamos el usuario en la base de datos
        
        if us: # Si el usuario existe
            if us[2]==clave:
                st.session_state['usuario'] = usuario
                st.session_state['nombre'] = f"{us[5]} {us[6]}" # Guardamos el usuario y la clave en el session state
                # Verificamos si la clave es correcta
                return True # Retornamos True si el usuario y la clave son correctos
            else:
                return False # Retornamos False si la clave es incorrecta
        else:
            return False # Retornamos False si el usuario no existe
        
        # # Leemos el archivo csv con los usuarios y claves
        # dfusuarios = pd.read_csv('usuarios.csv')
        # # Filtramos el dataframe para buscar el usuario y la clave
        # if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['clave']==clave)])>0:
        #     # Si el usuario y la clave existen, retornamos True
        #     return True
        # else:
        #     # Si el usuario o la clave no existen, retornamos False
        #     return False

    # Generación de menú según el usuario y el rol se maneja desde el código
    def generarMenu(usuario,clave):
        st.write("Hola **:blue-background[{}]**".format(usuario)) # Mostramos el nombre del usuario con formato
        """Genera el menú dependiendo del usuario y el rol

        Args:
            usuario (str): usuario utilizado para generar el menú
        """        
        with st.sidebar: # Creamos una barra lateral para el menú
            conn=dbs.create_connection("soportes.db")
            rol=dbs.buscar_rol(conn,usuario,clave)
            # Cargamos el rol
            rol= dfUsuario['rol'].values[0]
            #Mostramos el nombre del usuario
            st.write(f"Hola **:blue-background[{nombre}]** ") # Mostramos el nombre del usuario con formato
            st.caption(f"Rol: {rol}") # Mostramos el rol del usuario
            # Mostramos los enlaces de páginas
            st.page_link("inicio.py", label="Inicio", icon=":material/home:") # Enlace a la página de inicio
            st.subheader("Tableros") # Subtítulo para los tableros
            # Mostramos los enlaces a las páginas según el rol del usuario
            if rol in ['ventas','admin','comercial']:
                st.page_link("pages/paginaVentas.py", label="Ventas", icon=":material/sell:") # Enlace a la página de ventas        
            if rol in ['compras','admin','comercial']:
                st.page_link("pages/paginaCompras.py", label="Compras", icon=":material/shopping_cart:") # Enlace a la página de compras
            if rol in ['personal','admin','compras']:
                st.page_link("pages/paginaPersonal.py", label="Personal", icon=":material/group:") # Enlace a la página de personal   
            if rol in ['contabilidad','admin']:
                st.page_link("pages/paginaContabilidad.py", label="Contabilidad", icon=":material/payments:") # Enlace a la página de contabilidad    
            # Botón para cerrar la sesión
            btnSalir=st.button("Salir") # Creamos un botón para salir
            if btnSalir: # Si se presiona el botón
                st.session_state.clear() # Limpiamos las variables de sesión
                # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
                st.rerun() # Reiniciamos la aplicación

    def validarPagina(pagina,usuario):
        """Valida si el usuario tiene permiso para acceder a la página

        Args:
            pagina (str): página a validar
            usuario (str): usuario a validar

        Returns:
            bool: True si tiene permiso, False si no tiene permiso
        """
        # print(st.session_state)
        # Cargamos la información de usuarios y roles
        conn=dbs.create_connection("soportes.db")
        usuario= dbs.buscar_datos_usuario(conn,usuario) # Buscamos los datos del usuario
        rol = dbs.buscar_rol(conn,usuario[3]) # Buscamos el rol del usuario
        paginas= dbs.buscar_pagina(conn,rol) # Buscamos las páginas del rol del usuario
        
    
        # Validamos si el rol del usuario tiene acceso a la página
        if len(paginas)>0:
            if  rol in rol == "Admin" or st.secrets["tipoPermiso"]=="rol":
                return True # El usuario tiene permiso
            else:
                return False # El usuario no tiene permiso
        else:
            return False # La página no existe en el archivo de permisos


    # Validación de acceso a la página según los roles del usuario
    def generarMenuRoles(usuario):
        """
        Genera el menú lateral de Streamlit dependiendo del usuario y su rol,
        obteniendo los datos de una base de datos SQLite.

        Args:
            usuario (str): Correo electrónico del usuario utilizado para generar el menú.
        """
        conn = None # Inicializamos la conexión fuera del bloque try
        try:
            # Conectamos a la base de datos SQLite
            conn = dbs.create_connection("soportes.db")
            if conn is None:
                st.error("No se pudo conectar a la base de datos.")
                return

            # Obtenemos los datos completos del usuario (nombre, apellido, etc.)
            datos_usuario = dbs.buscar_datos_usuario(conn, usuario)
            if datos_usuario is None:
                st.error("Usuario no encontrado en la base de datos.")
                return

            # Asumiendo que datos_usuario es una tupla y contiene el nombre en el índice 4 y apellido en el 5
            # (Ajusta estos índices si la estructura de tu tabla 'usuarios' es diferente)
            nombre_usuario = datos_usuario[5] if len(datos_usuario) > 4 else "Usuario"
            apellido_usuario = datos_usuario[6] if len(datos_usuario) > 5 else ""
            nombre_completo = f"{nombre_usuario} {apellido_usuario}".strip()

            # Obtenemos el rol del usuario
            rol = dbs.buscar_rol(conn, usuario)
            if rol is None:
                st.error("Rol del usuario no encontrado.")
                return

            # Cargamos todas las páginas relevantes de la tabla 'rol_paginas'
            # Asumimos que dbs.buscar_pagina(conn, usuario) devuelve una LISTA de tuplas/registros
            # donde cada tupla representa una página y contiene (id, pagina, nombre, icono, roles)
            try:
                # Aquí la función dbs.buscar_pagina debería obtener todas las páginas disponibles
                # o las páginas relevantes para el usuario, dependiendo de su implementación.
                # Si dbs.buscar_pagina ya filtra por usuario, no sería necesario un filtro adicional.
                # Si dbs.buscar_pagina obtiene TODAS las páginas, entonces necesitaremos filtrar después.
                
                paginas_raw = dbs.buscar_pagina(conn, datos_usuario[4]) # Asumiendo que el índice 3 es el correo del usuario
                if paginas_raw is None: # Si la función devuelve None en caso de error o no encontrar nada
                    paginas_raw = [] # Aseguramos que sea una lista vacía para evitar errores de iteración
            except sqlite3.Error as e:
                st.error(f"Error al cargar las páginas desde la base de datos: {e}")
                return
            
            paginas = [{"pagina": p[0], "nombre": p[1], "roles":p[2],"icono": p[3]} for p in paginas_raw]

            

            with st.sidebar: # Menú lateral
                # Mostramos el nombre del usuario y su rol
                st.write(f"Hola **:blue-background[{nombre_completo}]** ")
                st.caption(f"Rol: {rol}")
                
                st.subheader("Opciones")
                
                # Verificamos si se deben ocultar o deshabilitar las opciones del menú
                # Usamos .get() para acceder de forma segura a los secretos
                ocultar_opciones = st.secrets.get("ocultarOpciones", "False") # Valor por defecto 'False'
                
                if ocultar_opciones == "True":
                    
                    # Si el rol no es 'admin', filtramos las páginas para mostrar solo las permitidas
                    paginas_filtradas = []
                    for pagina_data in paginas:
                        
                        # Asegúrate de que 'roles' en tu tabla 'rol_paginas' sea una cadena que contenga los roles permitidos (ej: 'admin,editor')
                        if rol == 'Admin' or rol in str(pagina_data['roles']):
                            paginas_filtradas.append(pagina_data)
                    
                    # Ocultamos las páginas que no tiene permiso (mostrando solo las filtradas)
                    for row in paginas_filtradas:
                        icono = row['icono']
                        st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:")
                        
                else: # Si no se ocultan las opciones, se deshabilitan las no permitidas
                    # Deshabilitamos las páginas que no tiene permiso
                    for row in paginas:
                        deshabilitarOpcion = True # Valor por defecto para deshabilitar las opciones
                        
                        # Verificamos si el rol del usuario está en la cadena de roles de la página
                        # o si el usuario es 'admin'.
                        # Asegúrate de que row["roles"] sea una cadena de texto.
                        if rol in str(row["roles"]) or rol == "Admin":
                            deshabilitarOpcion = False # Habilitamos la página si el usuario tiene permiso
                        
                        icono = row['icono']
                        # Mostramos el enlace de la página, deshabilitado o no según el permiso.
                        st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:", disabled=deshabilitarOpcion)
                
                # Botón para cerrar la sesión
                btnSalir = st.button("Salir")
                if btnSalir:
                    
                    st.session_state.clear() # Limpia todas las variables de sesión
                    # Si 'usuario' se guarda en st.session_state, lo eliminamos explícitamente
                    if 'usuario' in st.session_state:
                        del st.session_state['usuario']
                
                    st.rerun() # Reinicia la aplicación

        except sqlite3.Error as e:
            st.error(f"Error de base de datos: {e}")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {e}")
        finally:
            if conn:
                conn.close() # Aseguramos el cierre de la conexión a la base de datos


    # Generación de la ventana de login y carga de menú
    def generarLogin(archivo):
        """Genera la ventana de login o muestra el menú si el login es valido
        """    
        
        # Obtenemos el usuario de la cookie
        usuario = controller.get('usuario')    
        # Validamos si el usuario ya fue ingresado
        if usuario:
            # Si ya hay usuario en el cookie, lo asignamos al session state
            st.session_state['usuario'] = usuario
                            
        # Validamos si el usuario ya fue ingresado    
        if 'usuario' in st.session_state: # Verificamos si la variable usuario esta en el session state
            
            # Si ya hay usuario cargamos el menu
            if st.secrets["tipoPermiso"]=="rol":
                generarMenuRoles(usuario) # Generamos el menú para la página
            else:
                # print(st.session_state)
                generarMenu(st.session_state['usuario']) # Generamos el menú del usuario       
            if validarPagina(archivo,usuario)==False: # Si el usuario existe, verificamos la página        
            
                st.error(f"No tiene permisos para acceder a esta página {archivo}",icon=":material/gpp_maybe:")
                st.stop() # Detenemos la ejecución de la página
        else: # Si no hay usuario
            # Cargamos el formulario de login       
            with st.form('frmLogin'): # Creamos un formulario de login
                parUsuario = st.text_input('Correo') # Creamos un campo de texto para usuario
                parPassword = st.text_input('Contraseña',type='password') # Creamos un campo para la clave de tipo password
                btnLogin=st.form_submit_button('Ingresar',type='primary',) # Botón Ingresar
                if btnLogin: # Verificamos si se presiono el boton ingresar
                    print(st.session_state)
                    if validarUsuario(parUsuario,parPassword): # Verificamos si el usuario y la clave existen
                        
                        # Asignamos la variable de usuario
                        # Set a cookie
                        controller.set('usuario', f"{parUsuario}")
                        # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                        st.rerun() # Reiniciamos la aplicación
                    else:
                        # Si el usuario es invalido, mostramos el mensaje de error
                        st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:") # Mostramos un mensaje de error                    

if __name__ == "__main__" :
    main()
