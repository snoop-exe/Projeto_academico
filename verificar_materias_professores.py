import pandas as pd


def mostrar_materias_sem_professores(lista_especialidades, conn):

    # Gerar binds dinâmicos 100% seguros
    parametros = {f"esp{i}": esp for i, esp in enumerate(lista_especialidades)}
    placeholders = ", ".join([f":esp{i}" for i in range(len(lista_especialidades))])

    sql_materias_sem_professores = f"""
        SELECT
            ID_MATERIA,
            M.NOME,
            m.ch as CARGA_HORARIA,
            M.TIPO AS tipo
        FROM
            MATERIAS M
        WHERE 
            M.ID_MATERIA NOT IN (SELECT ID_MATERIA FROM MATERIAS_PROFESSORES)
        AND
            M.TIPO IN ({placeholders})
    """

    df_materias_sem_professores = pd.read_sql(sql_materias_sem_professores, conn, params=parametros)

    df_materias_sem_professores["Escolha"] = range(1, len(df_materias_sem_professores) + 1)

    return df_materias_sem_professores
