

def selecionar_id_professor(id_usuario,conn):
    cursor = conn.cursor()
    sql_pes = """
                     SELECT 
                         ID_PROFESSOR 
                     FROM
                        professores
                     WHERE 
                       ID_USUARIO = :id_usuario
                     """
    cursor.execute(sql_pes, {"id_usuario": id_usuario})
    id_professor = cursor.fetchone()[0]
    return id_professor


def cadastrar_materia_professor(id_materia, id_professor, conn):
    cursor = conn.cursor()
    sql_materia_professor = """ 
                            select
                                *
                            from
                                materias_professores t
                            where 
                                t.id_materia = :id_materia
                            and
                                t.id_professor = :id_professor
                            """
    cursor.execute(sql_materia_professor,{'id_materia':id_materia,'id_professor':id_professor})
    resultado = cursor.fetchall()
    if resultado:
        return True
    try:

        sql_insert = """
            INSERT INTO materias_professores (id_materia, id_professor)
            VALUES (:id_materia, :id_professor)
        """
        cursor.execute(sql_insert, {
            "id_materia": id_materia,
            "id_professor": id_professor
        })
        conn.commit()
        return True
    except Exception as e:
        return False, 'Erro ao cadastrar matéria para professor: ' + str(e)

