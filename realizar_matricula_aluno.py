from datetime import datetime


def realizar_matricula(id_aluno, id_turma,id_materia, ch_materia,carga_horaria_atual,conn):
    cursor = conn.cursor()
    ano = datetime.year

    if ch_materia > carga_horaria_atual:
        return "Limite de carga horária atingido. Não é possível realizar mais matrículas."

    sql_insert = """
        INSERT INTO matriculas (id_aluno, id_turma,ano,id_turma,id_materia, status)
        VALUES (:id_aluno,:id_turma,:ano :id_materia, 'Matriculado')
    """

    cursor.execute(sql_insert, {
                                    "id_aluno": id_aluno,
                                    "id_materia": id_materia,
                                    "id_turma": id_turma,
                                    "ano": ano
                                })
    conn.commit()

    valor_horas = carga_horaria_atual - ch_materia

    sql_update = """
        UPDATE alunos
        SET limite_ch = :limite_ch
        WHERE id_aluno = :id_aluno
    """
    cursor.execute(sql_update, {"limite_ch": int(valor_horas), "id_aluno": int(id_aluno)})