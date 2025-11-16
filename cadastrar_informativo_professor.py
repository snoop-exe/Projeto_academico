

def cadastrar_horas_pendentes(faltantes,id_professor,id_materia,conn):
    try:
        if faltantes > 0:
            cursor = conn.cursor()
            sql = """INSERT INTO horas_pendentes_materias (id_professor, id_materia, horas_pendentes) 
                      VALUES (:id_professor, :id_materia, :horas_pendentes)"""
            cursor.execute(sql, {'id_professor': id_professor, 'id_materia': id_materia, 'horas_pendentes': faltantes})
            conn.commit()
            cursor.close()
            print(f"Cadastro de {faltantes} horas pendentes realizado com sucesso.")
    except Exception as e:
        return "Erro ao cadastrar horas pendentes: " + str(e)
