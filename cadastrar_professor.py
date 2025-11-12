from pandas.errors import DatabaseError

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
    try:
        cursor = conn.cursor()
        sql_insert = """
            INSERT INTO materias_professores (id_materia, id_professor)
            VALUES (:id_materia, :id_professor)
        """
        cursor.execute(sql_insert, {
            "id_materia": id_materia,
            "id_professor": id_professor
        })
        conn.commit()
        conn.close()

    except Exception as e:
        print("Erro ao cadastrar matéria para professor:", e)
    except DatabaseError as e:
        print("Erro de banco de dados ao cadastrar matéria para professor:", e)
