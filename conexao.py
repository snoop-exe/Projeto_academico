import oracledb


def conectar_banco():

    dsn = "localhost:1521/xepdb1"
    conexao = oracledb.connect(
        user="trabalho",
        password="uniube",
        dsn=dsn
    )
    return conexao
