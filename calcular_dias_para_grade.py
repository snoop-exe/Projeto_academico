

def calcular_dias_e_unibe(ch):
    uniube_mais = 32 #valor fixo para considerar o horario do unibube mais
    horas_semanais = (ch-uniube_mais) / 16
    max_horas_presenciais = 2.667 #equivalente a 10 horas mensais

    duracao_aula = 1.33  # Cada aula = 1h20 = 1,33h
    semanas = 16  # Semestre de 16 semanas
    aulas_semana = 2  # Professor dará 2 aulas por semana

    if horas_semanais <= max_horas_presenciais:
        dias_obrigatorios = 1 if horas_semanais <= 2 else 2
        faltantes = 0
    else:
        dias_obrigatorios = 2
        horas_dadas = aulas_semana * duracao_aula * semanas

        # Horas restantes
        faltantes = (ch-uniube_mais) - horas_dadas

    return dias_obrigatorios,faltantes




