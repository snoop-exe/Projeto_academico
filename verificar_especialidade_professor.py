
def verificar_especialidades(id_professor, conn):
    cursor = conn.cursor()

    sql_especialidades = """ 
                        SELECT
                            e.NOME
                        FROM
                            PROFESSORES_ESPECIALIDADES pe 
                        LEFT JOIN ESPECIALIDADES e 
                        ON pe.ID_ESPECIALIDADE = e.ID_ESPECIALIDADE
                        WHERE
                            pe.ID_PROFESSOR = :id_professor
                            """

    cursor.execute(sql_especialidades, {"id_professor": id_professor})
    resultado = cursor.fetchall()

    lista_especialidades = [linha[0] for linha in resultado]
    return lista_especialidades
