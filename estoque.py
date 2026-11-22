import persistencia
import utils


# devolve o saldo, se nao achar devolve 0
def saldo_do_item(dados, codigo):
    return dados["estoque"].get(codigo, 0)


def erro_de_saldo(dados, codigo, qtd):
    # qtd vem com sinal: negativo e saida (RN02)
    saldo = saldo_do_item(dados, codigo)
    if round(saldo + qtd, 4) < 0:
        unidade = dados["itens"][codigo]["unidade"]
        return ("saldo insuficiente (saldo atual: "
                + utils.formatar_numero(saldo) + " " + unidade + ")")
    return ""


# atualiza o saldo e anota no kardex
def registrar_movimento(dados, codigo, tipo, qtd, documento, data):
    erro = erro_de_saldo(dados, codigo, qtd)
    if erro != "":
        return erro
    novo_saldo = round(saldo_do_item(dados, codigo) + qtd, 4)
    dados["estoque"][codigo] = novo_saldo
    movimento = {
        "data": data,
        "item": codigo,
        "tipo": tipo,
        "qtd": qtd,
        "saldo": novo_saldo,
        "documento": documento,
    }
    dados["movimentos"].append(movimento)
    return ""


# entrada, saida ou ajuste de estoque
def movimentar(dados):
    utils.titulo("MOVIMENTACAO DE ESTOQUE")
    codigo = utils.ler_texto("Codigo do item: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    tipo = utils.ler_opcao("Tipo [E]ntrada [S]aida [A]juste: ",
                           ["E", "S", "A"])

    # o ajuste pode ser positivo ou negativo
    if tipo == "A":
        qtd = utils.ler_decimal(
            "Quantidade do ajuste (negativa para diminuir): ")
        if qtd == 0:
            print("ERRO: o ajuste nao pode ser zero.")
            return
        nome_tipo = "AJUSTE"
    else:
        qtd = utils.ler_decimal("Quantidade: ", positivo=True)
        if tipo == "S":
            # saida vira numero negativo
            qtd = -qtd
            nome_tipo = "SAIDA"
        else:
            nome_tipo = "ENTRADA"

    erro = erro_de_saldo(dados, codigo, qtd)
    if erro != "":
        print("ERRO: " + erro + ". Operacao cancelada.")
        return

    data = utils.ler_data("Data (dd/mm/aaaa, Enter = hoje): ")
    documento = utils.ler_texto("Documento/motivo: ")
    registrar_movimento(dados, codigo, nome_tipo, qtd, documento, data)
    persistencia.salvar_tudo(dados)
    print("Movimentacao registrada. Novo saldo: "
          + utils.formatar_numero(saldo_do_item(dados, codigo))
          + " " + dados["itens"][codigo]["unidade"])
    avisar_estoque_baixo(dados, codigo)


# avisa se o saldo esta abaixo do estoque de seguranca
def avisar_estoque_baixo(dados, codigo):
    item = dados["itens"][codigo]
    saldo = saldo_do_item(dados, codigo)
    if saldo < item["estoque_seguranca"]:
        print("ALERTA: saldo (" + utils.formatar_numero(saldo) + " "
              + item["unidade"] + ") abaixo do estoque de seguranca ("
              + utils.formatar_numero(item["estoque_seguranca"]) + " "
              + item["unidade"] + ").")


# mostra o saldo de um item
def consultar_saldo(dados):
    utils.titulo("CONSULTA DE SALDO")
    codigo = utils.ler_texto("Codigo do item: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    item = dados["itens"][codigo]
    print(codigo + " " + item["descricao"])
    print("Saldo atual: " + utils.formatar_numero(saldo_do_item(dados, codigo))
          + " " + item["unidade"])
    print("Estoque de seguranca: "
          + utils.formatar_numero(item["estoque_seguranca"]))
    avisar_estoque_baixo(dados, codigo)


# mostra o historico de movimentos de um item
def mostrar_kardex(dados):
    utils.titulo("KARDEX")
    codigo = utils.ler_texto("Codigo do item: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    item = dados["itens"][codigo]
    print("KARDEX - " + codigo + " " + item["descricao"]
          + " (" + item["unidade"] + ")")
    print("Data        Tipo     Qtde   Saldo  Documento")
    achou = False
    for mov in dados["movimentos"]:
        # pula os movimentos de outros itens
        if mov["item"] != codigo:
            continue
        achou = True
        qtd = utils.formatar_numero(mov["qtd"])
        if mov["qtd"] > 0:
            qtd = "+" + qtd
        print("{:<12}{:<9}{:>5}{:>8}  {}".format(
            mov["data"], mov["tipo"], qtd,
            utils.formatar_numero(mov["saldo"]), mov["documento"]))
    if not achou:
        print("Nenhuma movimentacao para esse item.")
    avisar_estoque_baixo(dados, codigo)


# lista o saldo de todos os itens
def posicao_geral(dados):
    utils.titulo("POSICAO DE ESTOQUE")
    print("Codigo  Descricao                       Saldo  Est.Seg  Situacao")
    utils.linha(68)
    for codigo in sorted(dados["itens"]):
        item = dados["itens"][codigo]
        saldo = saldo_do_item(dados, codigo)
        situacao = "OK"
        if saldo < item["estoque_seguranca"]:
            situacao = "ABAIXO DO ESTOQUE DE SEGURANCA"
        print("{:<8}{:<32}{:>6}{:>9}  {}".format(
            codigo, item["descricao"], utils.formatar_numero(saldo),
            utils.formatar_numero(item["estoque_seguranca"]), situacao))
