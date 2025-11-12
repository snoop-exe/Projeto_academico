import pandas as pd


def verificar_aluno(codigo_aluno,conn):
    sql_semestre = """
            SELECT 
                id_aluno,
                semestre_atual,
                limite_ch
            FROM alunos
            WHERE id_usuario = :id_usuario
        """
    df_aluno = pd.read_sql(sql_semestre, conn, params={"id_usuario": codigo_aluno})

    if df_aluno.empty:
        return None

    id_aluno = int(df_aluno.at[0, "ID_ALUNO"])
    semestre_atual = int(df_aluno.at[0, "SEMESTRE_ATUAL"])
    limite_ch = int(df_aluno.at[0, "LIMITE_CH"])

    return id_aluno,semestre_atual,limite_ch


def verificar_materias_disponiveis(id_aluno,semestre_atual,limite_ch,conn):
    # Pegando semestre e limite de CH do aluno

    sql_materias = """
                SELECT
                    m.id_materia,
                    m.nome,
                    m.ch
                FROM
                    materias m
                WHERE
                    m.semestre <= :semestre_atual
                    AND m.ch <= :limite_ch
                    AND m.id_materia NOT IN (
                SELECT
                    ma.id_materia
                FROM
                    matriculas ma
                WHERE
                    ma.id_aluno = :id_aluno
                        )
                AND NOT EXISTS (
                SELECT
                    1
                FROM
                    materias_pre_requisitos pr
                LEFT JOIN matriculas ma2 
                                ON
                    pr.id_pre_requisito = ma2.id_materia
                    AND ma2.id_aluno = :id_aluno
                    AND ma2.status = 'Aprovado'
                WHERE
                    pr.id_materia = m.id_materia
                    AND ma2.id_materia IS NULL
                        )
                AND 
                        m.ID_MATERIA IN(( SELECT
                id_materia
                FROM
                turmas
                WHERE 
                    VAGAS_TOTAL >= VAGAS_OCUPADAS + 1 ))
    """
    df_materias = pd.read_sql(sql_materias, conn, params={
        "semestre_atual": semestre_atual,
        "limite_ch": limite_ch,
        "id_aluno": id_aluno
    })
    df_materias['Escolha'] = range(1, len(df_materias) + 1)
    return df_materias


def verificar_carga_horaria(codigo_aluno, conn):
    sql_ch = """
        SELECT 
            SUM(m.ch) AS carga_horaria_atual
        FROM matriculas ma
        JOIN materias m ON ma.id_materia = m.id_materia
        WHERE 
            ma.id_aluno = :id_aluno
            AND ma.status IN ('Matriculado')
    """
    df_ch = pd.read_sql(sql_ch, conn, params={"id_aluno": codigo_aluno})

    if df_ch.empty or pd.isna(df_ch.at[0, "CARGA_HORARIA_ATUAL"]):
        return 0

    carga_horaria_atual = int(df_ch.at[0, "CARGA_HORARIA_ATUAL"])
    return carga_horaria_atual


def cadastro_horas(id_aluno, conn):
    cursor = conn.cursor()
    sql_hrs = """select limite_ch from alunos where id_aluno = :id_aluno"""
    cursor.execute(sql_hrs, {"id_aluno": id_aluno})
    conn.commit()
    resultado = cursor.fetchone()[0] or 0
    return resultado


def realizar_matricula(id_aluno, id_materia, ch_materia,conn):
    cursor = conn.cursor()

    carga_horaria_atual = cadastro_horas(id_aluno, conn)

    if ch_materia > carga_horaria_atual:
        return "Limite de carga horária atingido. Não é possível realizar mais matrículas."

    sql_insert = """
        INSERT INTO matriculas (id_aluno, id_materia, status)
        VALUES (:id_aluno, :id_materia, 'Matriculado')
    """

    cursor.execute(sql_insert, {"id_aluno": id_aluno, "id_materia": id_materia})
    conn.commit()

    valor_horas = carga_horaria_atual - ch_materia

    sql_update = """
        UPDATE alunos
        SET limite_ch = :limite_ch
        WHERE id_aluno = :id_aluno
    """
    cursor.execute(sql_update, {"limite_ch": int(valor_horas), "id_aluno": int(id_aluno)})
