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
                    t.id_turma,
                    m.NOME AS nome_materia,
                    m.tipo,
                    ds.DIA_SEMANA || ' - ' ||
                        TO_CHAR(tr.HORA_INICIO, 'HH24:MI') || ' a ' ||
                        TO_CHAR(tr.HORA_FIM, 'HH24:MI') AS TURNO_materia,
                    p.NOME AS NOME_PROFESSOR
                FROM
                    turmas t
                LEFT JOIN
                    turnos tr
                ON t.ID_turno = tr.id_turno
                LEFT JOIN
                    materias m 
                ON m.ID_MATERIA = t.ID_materia
                LEFT JOIN
                    DIAS_SEMANA ds 
                ON ds.ID_SEMANA = t.ID_SEMANA
                LEFT JOIN
                    PROFESSORES p
                ON	p.ID_PROFESSOR = t.ID_PROFESSOR
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





