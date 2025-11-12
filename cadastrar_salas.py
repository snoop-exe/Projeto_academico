from pandas.errors import DatabaseError


def cadastrar_sala_materia(id_materia,id_professor,id_sala,id_semana,id_turno,vagas_total, conn):
    try:
        cursor = conn.cursor()

        sql_insert = """ 
         INTO TURMAS (ID_MATERIA, ID_PROFESSOR, ID_SALA, ID_SEMANA, ID_TURNO, VAGAS_TOTAL,STATUS) values 
         ( :ID_MATERIA, :ID_PROFESSOR, :ID_SALA, :ID_SEMANA, :ID_TURNO, :VAGAS_TOTAL, 'ABERTA') )
        """

        cursor.execute(sql_insert, {
            "id_materia": id_materia,
            "id_professor": id_professor,
            "id_sala": id_sala,
            "id_semana": id_semana,
            "id_turno": id_turno,
            "vagas_total": vagas_total
        })

        conn.commit()
    except Exception as e:
        print("Erro ao cadastrar sala para matéria:", e)
    except DatabaseError as e:
        print("Erro de banco de dados ao cadastrar sala para matéria:", e)
