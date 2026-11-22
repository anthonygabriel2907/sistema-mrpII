import persistencia
import utils


# mostra o MPS das 8 semanas
def exibir_mps(dados):
    utils.titulo("PLANO MESTRE DE PRODUCAO (MPS)")
    if len(dados["mps"]) == 0:
        print("Nenhum MPS cadastrado.")
        return
    cabecalho = "{:<8}".format("Item")
    for semana in range(1, utils.SEMANAS + 1):
        cabecalho += "{:>6}".format("S" + str(semana))
    print(cabecalho)
    utils.linha(8 + 6 * utils.SEMANAS)
    for codigo in sorted(dados["mps"]):
        texto = "{:<8}".format(codigo)
        for demanda in dados["mps"][codigo]:
            texto += "{:>6}".format(utils.formatar_numero(demanda))
        print(texto + "   " + dados["itens"][codigo]["descricao"])


# digita a demanda das 8 semanas de um produto
def cadastrar_mps(dados):
    utils.titulo("CADASTRAR / ALTERAR MPS")
    codigo = utils.ler_texto("Codigo do produto acabado: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    # o MPS so tem produto acabado
    if dados["itens"][codigo]["tipo"] != "PA":
        print("ERRO: o MPS so aceita produtos acabados (PA).")
        return

    # se ainda nao tem MPS comeca tudo com zero
    atual = dados["mps"].get(codigo, [0] * utils.SEMANAS)
    novo = []
    print("Demanda por semana (Enter mantem o valor entre colchetes).")
    for i in range(utils.SEMANAS):
        valor = utils.ler_inteiro(
            "Semana " + str(i + 1) + " [" + str(atual[i]) + "]: ",
            minimo=0, padrao=atual[i])
        novo.append(valor)
    dados["mps"][codigo] = novo
    persistencia.salvar_tudo(dados)
    print("MPS de " + codigo + " salvo. Execute o MRP novamente.")


# muda a demanda de uma semana so
def alterar_semana(dados):
    utils.titulo("ALTERAR UMA SEMANA DO MPS")
    codigo = utils.ler_texto("Codigo do produto acabado: ").upper()
    if codigo not in dados["mps"]:
        print("ERRO: esse produto nao tem MPS cadastrado.")
        return
    semana = utils.ler_inteiro("Semana (1 a " + str(utils.SEMANAS) + "): ",
                               minimo=1, maximo=utils.SEMANAS)
    print("Demanda atual: " + str(dados["mps"][codigo][semana - 1]))
    # a semana 1 fica na posicao 0 da lista
    dados["mps"][codigo][semana - 1] = utils.ler_inteiro(
        "Nova demanda: ", minimo=0)
    persistencia.salvar_tudo(dados)
    print("MPS alterado. Execute o MRP novamente.")
