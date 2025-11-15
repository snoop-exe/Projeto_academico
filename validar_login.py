


def validar_login(login, senha,conn):
    conn = conn
    cursor = conn.cursor()

    sql = f"""
        SELECT tipo_usuario,id_usuario FROM usuarios
        WHERE username = '{login}' AND senha = '{senha}'
    """

    cursor.execute(sql)
    resultado = cursor.fetchall()

    if not resultado:
        return None,None

    tipo_usuario, id_usuario = resultado[0]
    return tipo_usuario,id_usuario
