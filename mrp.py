import estoque
import ordens
import persistencia
import utils


def calcular_necessidade_bruta(dados, codigo):
    nb = [0] * utils.SEMANAS
    item = dados["itens"][codigo]

    # PA: a necessidade bruta vem direto do MPS
    if item["tipo"] == "PA":
        if codigo in dados["mps"]:
            nb = list(dados["mps"][codigo])
        return nb

    # SA e MP: soma das liberacoes das ordens dos pais x qtd por unidade (RN04)
    for pai in dados["estrutura"]:
        for comp in dados["estrutura"][pai]:
            if comp["componente"] != codigo:
                continue
            for ordem in dados["ordens"]["lista"]:
                if ordem["item"] != pai or ordem["status"] == "ENCERRADA":
                    continue
                # ordem atrasada consome o componente ja na semana 1
                semana = max(1, ordem["liberar"])
                if semana <= utils.SEMANAS:
                    nb[semana - 1] += ordem["qtd"] * comp["qtd"]
    return nb


def calcular_recebimentos(dados, codigo):
    # RN08: so ordens FIRMES ou LIBERADAS entram como recebimento programado
    rp = [0] * utils.SEMANAS
    for ordem in dados["ordens"]["lista"]:
        if ordem["item"] != codigo:
            continue
        if ordem["status"] != "FIRME" and ordem["status"] != "LIBERADA":
            continue
        if 1 <= ordem["entregar"] <= utils.SEMANAS:
            rp[ordem["entregar"] - 1] += ordem["qtd"]
    return rp


def calcular_item(dados, codigo, excecoes):
    item = dados["itens"][codigo]
    nb = calcular_necessidade_bruta(dados, codigo)
    rp = calcular_recebimentos(dados, codigo)
    saldo = estoque.saldo_do_item(dados, codigo)

    if item["tipo"] == "MP":
        tipo_ordem = "OC"
    else:
        tipo_ordem = "OP"

    ep = []
    nl = []
    rpl = []
    lp = [0] * utils.SEMANAS
    estoque_anterior = saldo

    for i in range(utils.SEMANAS):
        semana = i + 1
        # RN05
        necessidade = nb[i] + item["estoque_seguranca"] - (
            estoque_anterior + rp[i])
        if necessidade < 0:
            necessidade = 0

        # RN06
        recebimento = 0
        if necessidade > 0:
            recebimento = max(necessidade, item["lote_minimo"])

        estoque_atual = estoque_anterior + rp[i] + recebimento - nb[i]

        # RN07
        if recebimento > 0:
            liberar = semana - item["lead_time"]
            ordem = ordens.criar_ordem(
                dados, tipo_ordem, codigo, recebimento, liberar, semana)
            if liberar >= 1:
                lp[liberar - 1] += recebimento
            else:
                mensagem = ("ATENCAO: " + ordem["numero"] + " (" + codigo
                            + ") deveria ser liberada na semana "
                            + str(liberar) + ", antes da semana 1.")
                excecoes.append({"item": codigo, "mensagem": mensagem})

        nl.append(necessidade)
        rpl.append(recebimento)
        ep.append(estoque_atual)
        estoque_anterior = estoque_atual

    registro = {
        "estoque_inicial": saldo,
        "nb": nb,
        "rp": rp,
        "ep": ep,
        "nl": nl,
        "rpl": rpl,
        "lp": lp,
    }
    return registro


def executar_mrp(dados):
    utils.titulo("EXECUCAO DO MRP")
    # RN08: apaga as ordens planejadas para recalcular
    lista = []
    for ordem in dados["ordens"]["lista"]:
        if ordem["status"] != "PLANEJADA" and ordem["status"] != "ATRASADA":
            lista.append(ordem)
    dados["ordens"]["lista"] = lista

    registros = {}
    excecoes = []
    # RN04: primeiro os PA, depois os SA e por fim as MP
    for tipo in ["PA", "SA", "MP"]:
        for codigo in sorted(dados["itens"]):
            if dados["itens"][codigo]["tipo"] == tipo:
                registros[codigo] = calcular_item(dados, codigo, excecoes)

    dados["mrp"] = {
        "data": utils.hoje(),
        "registros": registros,
        "excecoes": excecoes,
    }
    persistencia.salvar_tudo(dados)

    total_op = 0
    total_oc = 0
    for ordem in dados["ordens"]["lista"]:
        if ordem["status"] == "PLANEJADA" or ordem["status"] == "ATRASADA":
            if ordem["tipo"] == "OP":
                total_op += 1
            else:
                total_oc += 1
    print("MRP executado em " + dados["mrp"]["data"] + ".")
    print("Ordens planejadas: " + str(total_op) + " OP e "
          + str(total_oc) + " OC.")
    if len(excecoes) > 0:
        if len(excecoes) == 1:
            print("1 mensagem de excecao:")
        else:
            print(str(len(excecoes)) + " mensagens de excecao:")
        for exc in excecoes:
            print("  " + exc["mensagem"])


def imprimir_linha(nome, valores):
    texto = "{:<22}".format(nome)
    for valor in valores:
        texto += "{:>6}".format(utils.formatar_numero(valor))
    print(texto)


def mostrar_registro(dados):
    utils.titulo("REGISTRO MRP DE UM ITEM")
    codigo = utils.ler_texto("Codigo do item: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    if codigo not in dados["mrp"]["registros"]:
        print("ERRO: nao ha registro MRP para esse item. Execute o MRP.")
        return

    item = dados["itens"][codigo]
    reg = dados["mrp"]["registros"][codigo]
    print("REGISTRO MRP - " + codigo + " " + item["descricao"])
    print("Lead time: " + str(item["lead_time"]) + " sem | Est. seguranca: "
          + utils.formatar_numero(item["estoque_seguranca"])
          + " | Lote min.: " + utils.formatar_numero(item["lote_minimo"])
          + " | Estoque: " + utils.formatar_numero(reg["estoque_inicial"]))
    print()
    imprimir_linha("Semana", list(range(1, utils.SEMANAS + 1)))
    imprimir_linha("Necessidade bruta", reg["nb"])
    imprimir_linha("Receb. programados", reg["rp"])
    imprimir_linha("Estoque projetado", reg["ep"])
    imprimir_linha("Necessidade liquida", reg["nl"])
    imprimir_linha("Receb. planejados", reg["rpl"])
    imprimir_linha("Liberacao planejada", reg["lp"])

    for exc in dados["mrp"]["excecoes"]:
        if exc["item"] == codigo:
            print()
            print(exc["mensagem"])
