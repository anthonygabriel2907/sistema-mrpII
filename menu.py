import capacidade
import custos
import estoque
import estrutura
import graficos
import itens
import mps
import mrp
import ordens
import relatorios
import utils


def menu_cadastros(dados):
    while True:
        utils.titulo("CADASTROS")
        print("1. Cadastrar item")
        print("2. Listar itens")
        print("3. Alterar item")
        print("4. Cadastrar componente da estrutura (BOM)")
        print("5. Exibir estrutura de um produto (explosao da BOM)")
        print("6. Remover componente da estrutura")
        print("7. Cadastrar centro de trabalho")
        print("8. Listar centros de trabalho")
        print("9. Definir roteiro (item x centro)")
        print("10. Listar roteiros")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            itens.cadastrar_item(dados)
        elif opcao == "2":
            itens.listar_itens(dados)
        elif opcao == "3":
            itens.alterar_item(dados)
        elif opcao == "4":
            estrutura.cadastrar_componente(dados)
        elif opcao == "5":
            estrutura.exibir_estrutura(dados)
        elif opcao == "6":
            estrutura.remover_componente(dados)
        elif opcao == "7":
            capacidade.cadastrar_centro(dados)
        elif opcao == "8":
            capacidade.listar_centros(dados)
        elif opcao == "9":
            capacidade.definir_roteiro(dados)
        elif opcao == "10":
            capacidade.listar_roteiros(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_estoque(dados):
    while True:
        utils.titulo("ESTOQUE")
        print("1. Movimentar estoque (entrada, saida, ajuste)")
        print("2. Consultar saldo de um item")
        print("3. Kardex de um item")
        print("4. Posicao geral do estoque")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            estoque.movimentar(dados)
        elif opcao == "2":
            estoque.consultar_saldo(dados)
        elif opcao == "3":
            estoque.mostrar_kardex(dados)
        elif opcao == "4":
            estoque.posicao_geral(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_mps(dados):
    while True:
        utils.titulo("PLANO MESTRE DE PRODUCAO (MPS)")
        print("1. Exibir MPS")
        print("2. Cadastrar / alterar MPS de um produto")
        print("3. Alterar uma semana")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            mps.exibir_mps(dados)
        elif opcao == "2":
            mps.cadastrar_mps(dados)
        elif opcao == "3":
            mps.alterar_semana(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_mrp(dados):
    while True:
        utils.titulo("MRP")
        print("1. Executar MRP")
        print("2. Ver registro MRP de um item")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            mrp.executar_mrp(dados)
        elif opcao == "2":
            mrp.mostrar_registro(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_ordens(dados):
    while True:
        ordens.listar_ordens(dados)
        opcao = utils.ler_opcao(
            "[F] Firmar [L] Liberar [E] Encerrar [A] Apontar producao "
            "[V] Voltar: ", ["F", "L", "E", "A", "V"])
        if opcao == "F":
            ordens.firmar_ordem(dados)
        elif opcao == "L":
            ordens.liberar_ordem(dados)
        elif opcao == "E":
            ordens.encerrar_ordem(dados)
        elif opcao == "A":
            ordens.apontar_producao(dados)
        else:
            break


def menu_custos(dados):
    while True:
        utils.titulo("CUSTO PADRAO")
        print("1. Detalhar o custo de um item")
        print("2. Listar o custo de todos os itens fabricados")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            custos.mostrar_custo(dados)
        elif opcao == "2":
            custos.listar_custos(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_relatorios(dados):
    while True:
        utils.titulo("RELATORIOS (CSV)")
        print("1. Exportar posicao de estoque")
        print("2. Exportar lista de ordens")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            relatorios.exportar_estoque(dados)
        elif opcao == "2":
            relatorios.exportar_ordens(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_graficos(dados):
    while True:
        utils.titulo("GRAFICOS DE GESTAO")
        print("1. Posicao de estoque (saldo x estoque de seguranca)")
        print("2. Estoque projetado de um item")
        print("3. Ordens (OP e OC) por semana de entrega")
        print("4. Carga x capacidade de um centro")
        print("0. Voltar")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            graficos.grafico_estoque(dados)
        elif opcao == "2":
            graficos.grafico_projetado(dados)
        elif opcao == "3":
            graficos.grafico_ordens(dados)
        elif opcao == "4":
            graficos.grafico_carga(dados)
        elif opcao == "0":
            break
        else:
            print("ERRO: opcao invalida.")


def menu_principal(dados):
    while True:
        utils.titulo("MRP II - PEDAL FORTE BICICLETAS")
        print("1. Cadastros (itens, estrutura, centros, roteiros)")
        print("2. Estoque (movimentar, saldo, kardex)")
        print("3. Plano Mestre de Producao (MPS)")
        print("4. Executar MRP")
        print("5. Ordens de producao e de compra")
        print("6. Carga x capacidade (CRP)")
        print("7. Custo padrao dos produtos")
        print("8. Relatorios (exportar CSV)")
        print("9. Graficos de gestao")
        print("0. Sair")
        utils.linha()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            menu_cadastros(dados)
        elif opcao == "2":
            menu_estoque(dados)
        elif opcao == "3":
            menu_mps(dados)
        elif opcao == "4":
            menu_mrp(dados)
        elif opcao == "5":
            menu_ordens(dados)
        elif opcao == "6":
            utils.titulo("CARGA x CAPACIDADE (CRP)")
            capacidade.exibir_crp(dados)
        elif opcao == "7":
            menu_custos(dados)
        elif opcao == "8":
            menu_relatorios(dados)
        elif opcao == "9":
            menu_graficos(dados)
        elif opcao == "0":
            print("Ate logo!")
            break
        else:
            print("ERRO: opcao invalida.")
