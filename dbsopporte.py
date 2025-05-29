import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connection to {db_file} established.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def buscar_usuario(conn, correo,contraseña):
    """Search for a user in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo=? AND contraseña=?", (correo, contraseña))
    row = cursor.fetchone()
    if row:
        return row
    else:
        return None
    
def buscar_datos_usuario(conn, correo):
    """Search for a user in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo=?", (correo,))
    row = cursor.fetchone()
    if row:
        return row
    else:
        return None
    
    
def buscar_rol(conn, correo):
    """Search for a role associated with the user."""
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE correo=? ", (correo,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None
    
def buscar_pagina(conn, rol):
    """
    Busca una página en la base de datos asociada a un rol específico.
    Asume que la tabla se llama 'rol_paginas' y que la columna 'roles'
    contiene una cadena donde se puede buscar el rol.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos SQLite.
        rol (str): El rol a buscar.

    Returns:
        str or None: La columna 'pagina' del primer resultado que coincide, o None si no se encuentra.
    """
    
    cursor = conn.cursor()
    # Construimos el patrón LIKE con los comodines % en Python, no en la cadena de consulta SQL
    search_pattern = f"%{rol}%"
    
    try:
        cursor.execute("SELECT pagina,nombre,roles,icono FROM paginas WHERE roles LIKE ?", (search_pattern,))
        row = cursor.fetchall()
        if row:
            
            return row  # Retorna el valor de la columna 'pagina'
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error al buscar página en la base de datos: {e}")
        return None

def buscar_todos_los_usuarios(conn,nombre,apellido, correo,rol):
    """Search for all users in the database."""
    n=nombre
    a=apellido
    c=correo
    r=rol
    
    # Construir consulta

    query = '''
        SELECT *            FROM usuarios
        WHERE 1=1
    '''
    condiciones = []

    if c:
        condiciones.append(f"correo LIKE '%{c}%'")
    if r:
        condiciones.append(f"rol LIKE '%{r}%'")
    if n:
        condiciones.append(f"nombre LIKE '%{n}%'")
    if a:
        condiciones.append(f"apellido LIKE '%{a}%'")
    

    # Unir condiciones
    if condiciones:
        query += " AND " + " AND ".join(condiciones)

    else :
        query = '''
        SELECT * FROM usuarios
        '''

    
    c = conn.cursor()
    c.execute(query)

    valores = c.fetchall()
    conn.commit()
    conn.close()
    
    if valores:
        return valores
    else:
        return None
    
def buscar_todos_los_usuarios1(conn):
    c = conn.cursor()
    c.execute("""SELECT * FROM usuarios""")

    valores = c.fetchall()
    conn.commit()
    conn.close()
    
    if valores:
        return valores
    else:
        return None
    
def buscar_usuario_por_id(conn,id):
    c = conn.cursor()
   
    c.execute("SELECT * FROM usuarios WHERE ID = ?",(id,))
    valores = c.fetchone()
    conn.commit()
    conn.close()
    if valores:
        print(valores)
        return valores
    else:
        return None

def agregar_usuario(conn,usuario,contraseña,correo,rol,nombre,apellido):
    # Buscar usuario en la base de datos
    u=usuario
    cc=contraseña
    co=correo
    r=rol
    n=nombre
    a=apellido

    c = conn.cursor()
    c.execute("""INSERT INTO Usuarios (usuario,contraseña,correo,rol,nombre,apellido) VALUES (?,?,?,?,?,?)""",(u,cc,co,r,n,a))
    conn.commit()
    conn.close()

def editar_usuario(conn,id, usua, contraseña, correo, rol, nombre, apellido):
    c = conn.cursor()
    c.execute("""UPDATE usuarios SET usuario = ?, contraseña = ?, correo = ?, rol = ?, nombre= ?, apellido = ? WHERE ID = ?""",(usua,contraseña,correo,rol,nombre,apellido,id))
    conn.commit()
    conn.close()

