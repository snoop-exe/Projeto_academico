import pandas as pd
from pandas.errors import DatabaseError


def mostrar_materias_sem_professores(conn):
    sql_materias_sem_professores = """
                                    SELECT
                                        ID_MATERIA,
                                        M.NOME,
                                        m.tipo as tipo
                                    FROM
                                        MATERIAS M
                                    WHERE 
                                        M.ID_MATERIA NOT IN((SELECT ID_MATERIA FROM MATERIAS_PROFESSORES))
    	                            """
    df_materias_sem_professores = pd.read_sql(sql_materias_sem_professores, conn)
    df_materias_sem_professores['Escolha'] = range(1, len(df_materias_sem_professores) + 1)
    return df_materias_sem_professores
