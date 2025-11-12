import conexao as cx
import validar_login as vl
import verificar_materias_alunos as vm
import verificar_materias_professores as vp
import verificar_salas_disponiveis as vsd
import cadastrar_salas as cs
import cadastrar_professor as cp


if __name__ == '__main__':
    conexao = cx.conectar_banco()

    # login = input('Login: ')
    # senha = input('Senha: ')

    # login = 'yuris' #usuario e senha aluno
    # senha = '123'
    login = 'Paulo' #usuario e senha professor
    senha = '123'

    tipo_usuario,id_usuario = vl.validar_login(login, senha, conexao)
    if tipo_usuario:
        print(f"Seja bem vindo {tipo_usuario} !")
    else:
        print("Login ou senha incorretos.")

    if tipo_usuario == 'Aluno':
        id_aluno, semestre_atual, limite_ch = vm.verificar_aluno(id_usuario,conexao)
        while True:
            print('Escolha uma opção:')
            print('1 - Realizar matricula')
            print('2 - Conferir carga horária atual')
            print('3 - Ver grade de matérias atual ')
            print('4 - Sair')

            opcao = input('Opção: ')

            if opcao == '1':
                df_materias = vm.verificar_materias_disponiveis(id_aluno, semestre_atual, limite_ch, conexao)

                if df_materias is not None and not df_materias.empty:
                    print("Matérias disponíveis para matrícula: \n")
                    print(df_materias[['Escolha','NOME','CH']].to_string(index=False))
                else:
                    print("Nenhuma matéria disponível para matrícula.")
                    break

                escolha = input("Digite o número da matéria que deseja matricular (ou 'sair' para voltar): ")

                if escolha.lower() == 'sair':
                    continue
                if not escolha.isdigit():
                    print("Entrada inválida. Por favor, digite apenas números válidos. \n\n")
                    continue

                indices_selecionados = [int(i.strip()) for i in escolha.split(',')]
                materias_selecionadas = df_materias[df_materias['Escolha'].isin(indices_selecionados)]

                print('Você selecionou as seguintes matérias para matrícula:\n\n\n ',materias_selecionadas[['NOME','CH']].to_string(index=False))
                confirmar = input("Confirma a matrícula nessas matérias? (s/n): ")

                if confirmar.lower() == 's':
                    ch_materia = materias_selecionadas['CH'].sum()

                    for _, row in materias_selecionadas.iterrows():
                        vm.realizar_matricula(id_aluno, row['ID_MATERIA'],ch_materia,conexao)

                    print("Matrícula realizada com sucesso!")
                elif confirmar.lower() == 'n':
                    print("Matrícula cancelada.")
                else:
                    print("Opção inválida. Matrícula cancelada.")

            elif opcao == '2':
                ch_atual = vm.verificar_carga_horaria(id_aluno, conexao)
                print(f"Sua carga horária atual é: {ch_atual} horas")
            elif opcao == '3':
                print('Funçionalidade de ver grade de matérias ainda não implementada.')
            elif opcao == '4':
                print("Saindo...")
                break

            else:
                print("Opção inválida. Tente novamente.")

    elif tipo_usuario == 'Professor':
        while True:
            print('Escolha uma opção:')
            print('1 - Solicitar criação de matéria')
            print('2 - Conferir carga horária atual')
            print('3 - Sair')

            opcao = input('Opção: ')

            if opcao.lower() == 'sair':
                continue

            if not opcao.isdigit():
                print("Entrada inválida. Por favor, digite apenas números válidos. \n\n")
                continue

            if opcao == '1':

                df_materias_sem_professores = vp.mostrar_materias_sem_professores(conexao)
                if df_materias_sem_professores is not None and not df_materias_sem_professores.empty:
                    print("Matérias sem professores atribuídos: \n")
                    print(df_materias_sem_professores[['Escolha','NOME']].to_string(index=False))
                    escolha = input("\n\nDigite o número da matéria que deseja solicitar (ou 'sair' para voltar): ")

                    if escolha.lower() == 'sair':
                        continue

                    if not escolha.isdigit():
                        print("Entrada inválida. Por favor, digite apenas números válidos. \n\n")
                        continue

                    indice_selecionado = int(escolha)
                    materia_selecionada = df_materias_sem_professores[df_materias_sem_professores['Escolha'] == indice_selecionado]

                    if not materia_selecionada.empty:
                        confirmar = input(f"Confirma a solicitação para lecionar a matéria '{materia_selecionada.iloc[0]['NOME']}'? (s/n): ")

                        if confirmar.lower() == 's':
                            print('Salas disponíveis para alocação:')
                            df_salas_disponiveis = vsd.verificar_salas_disponiveis(conexao)
                            print(df_salas_disponiveis[['Escolha','NOME_SALA','TURNO']].to_string(index=False))
                            escolha_sala = input("Digite o número da sala que deseja alocar (ou 'sair' para voltar): ")

                            if escolha_sala.lower() == 'sair':
                                continue

                            if not escolha_sala.isdigit():
                                print("Entrada inválida. Por favor, digite apenas números válidos. \n\n")
                                continue

                            indice_sala_selecionada = int(escolha_sala)

                            sala_selecionada = df_salas_disponiveis[df_salas_disponiveis['Escolha'] == indice_sala_selecionada]

                            if not sala_selecionada.empty:
                                id_professor = cp.selecionar_id_professor(id_usuario, conexao)
                                print(id_professor)
                                id_materia = int(materia_selecionada.iloc[0]['ID_MATERIA'])
                                print(id_materia)
                                erro = cp.cadastrar_materia_professor(
                                    int(materia_selecionada.iloc[0]['ID_MATERIA']),
                                    id_professor,
                                    conexao
                                )

                                if erro:
                                    print("Erro ao cadastrar matéria para professor:", erro)
                                    continue
                                print(sala_selecionada.columns)
                                id_sala = int(sala_selecionada.iloc[0]['ID_SALA'])
                                # id_semana = int(sala_selecionada.iloc[0]['ID_SEMANA'])
                                id_turno = int(sala_selecionada.iloc[0]['ID_TURNO'])
                                vagas = 40

                                print("id_sala:", id_sala)
                                # print("id_semana:", id_semana)
                                print("id_turno:", id_turno)
                                print("vagas:", vagas)

                                erro = cs.cadastrar_sala_materia(
                                    int(materia_selecionada.iloc[0]['ID_MATERIA']),
                                    id_usuario,
                                    int(id_sala),
                                    int(sala_selecionada.iloc[0]['ID_SEMANA']),
                                    int(sala_selecionada.iloc[0]['ID_TURNO']),
                                    vagas,
                                    conexao
                                )

                                if erro:
                                    print("Erro ao cadastrar sala para matéria:", erro)
                                    continue

                                print("Solicitação realizada com sucesso!")
                            else:
                                print("Sala selecionada inválida.")

                        elif confirmar.lower() == 'n':
                            print("Solicitação cancelada.")
                        else:
                            print("Opção inválida. Solicitação cancelada.")
                    else:
                        print("Matéria selecionada inválida.")
                else:
                    print("Todas as matérias já possuem professores atribuídos.")

            elif opcao == '2':
                print('Funçionalidade de conferir carga horária atual ainda não implementada.')
            elif opcao == '3':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")
