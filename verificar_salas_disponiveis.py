import pandas as pd


def verificar_salas_disponiveis(conn):
    sql_salas_disponiveis = """
                           SELECT 
                            S.ID_SALA,
                            T2.ID_TURNO,
                            SEM.ID_SEMANA,
                            S.NOME_SALA,
                            SEM.DIA_SEMANA || ' - ' ||
                                TO_CHAR(T2.HORA_INICIO, 'HH24:MI') || ' a ' ||
                                TO_CHAR(T2.HORA_FIM, 'HH24:MI') AS TURNO
                        FROM SALAS S
                        CROSS JOIN TURNOS T2
                        CROSS JOIN DIAS_SEMANA SEM
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM TURMAS T
                            WHERE T.ID_SALA = S.ID_SALA
                              AND T.ID_TURNO = T2.ID_TURNO
                              AND T.ID_SEMANA = SEM.ID_SEMANA
                        )
                        ORDER BY S.ID_SALA, SEM.ID_SEMANA, T2.ID_TURNO
                            """

    df_salas_disponiveis = pd.read_sql(sql_salas_disponiveis, conn)
    df_salas_disponiveis['Escolha'] = range(1, len(df_salas_disponiveis) + 1)
    return df_salas_disponiveis