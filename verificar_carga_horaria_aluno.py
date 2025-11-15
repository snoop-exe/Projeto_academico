

def cadastro_horas(id_aluno, conn):
    cursor = conn.cursor()
    sql_hrs = """select limite_ch from alunos where id_aluno = :id_aluno"""
    cursor.execute(sql_hrs, {"id_aluno": id_aluno})
    conn.commit()
    resultado = cursor.fetchone()[0] or 0
    return resultado