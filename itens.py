import persistencia
import utils


def cadastrar_item(dados):
    utils.titulo("CADASTRO DE ITEM")
    codigo = utils.ler_texto("Codigo (ex.: PA-001, SA-020, MP-201): ").upper()
    if not utils.codigo_valido(codigo):
        print("ERRO: codigo invalido. Use Tipo-Numero com 3 digitos.")
        return
    if codigo in dados["itens"]:
        print("ERRO: ja existe um item com o codigo " + codigo + ".")
        return

    tipo = codigo[:2]
    print("Tipo do item: " + tipo)
    descricao = utils.ler_texto("Descricao: ")
    unidade = utils.ler_texto("Unidade de medida (un, m, L, kg...): ")

    custo = 0.0
    if tipo == "MP":
        custo = utils.ler_decimal("Custo unitario (R$): ", minimo=0)
    else:
        print("O custo de item fabricado e calculado pela estrutura.")

    lead_time = utils.ler_inteiro("Lead time (semanas): ", minimo=0)
    seguranca = utils.ler_decimal("Estoque de seguranca: ", minimo=0)
    lote = utils.ler_decimal("Lote minimo: ", minimo=0)

    item = {
        "codigo": codigo,
        "descricao": descricao,
        "tipo": tipo,
        "unidade": unidade,
        "custo": custo,
        "lead_time": lead_time,
        "estoque_seguranca": seguranca,
        "lote_minimo": lote,
    }
    dados["itens"][codigo] = item
    dados["estoque"][codigo] = 0
    persistencia.salvar_tudo(dados)
    print("Item " + codigo + " cadastrado com sucesso.")


def listar_itens(dados):
    utils.titulo("LISTA DE ITENS")
    if len(dados["itens"]) == 0:
        print("Nenhum item cadastrado.")
        return
    print("Codigo  Descricao                       Tipo Un    "
          "Custo(R$)  LT  Est.Seg  Lote")
    utils.linha(78)
    for codigo in sorted(dados["itens"]):
        item = dados["itens"][codigo]
        if item["tipo"] == "MP":
            custo = utils.formatar_dinheiro(item["custo"])
        else:
            custo = "-"
        print("{:<8}{:<32}{:<5}{:<5}{:>9}{:>5}{:>9}{:>6}".format(
            codigo,
            item["descricao"],
            item["tipo"],
            item["unidade"],
            custo,
            item["lead_time"],
            utils.formatar_numero(item["estoque_seguranca"]),
            utils.formatar_numero(item["lote_minimo"])))


def alterar_item(dados):
    utils.titulo("ALTERAR ITEM")
    codigo = utils.ler_texto("Codigo do item: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    item = dados["itens"][codigo]
    print("Tecle Enter para manter o valor atual.")

    novo = input("Descricao [" + item["descricao"] + "]: ").strip()
    if novo != "":
        item["descricao"] = novo
    novo = input("Unidade [" + item["unidade"] + "]: ").strip()
    if novo != "":
        item["unidade"] = novo

    if item["tipo"] == "MP":
        texto = "Custo unitario [" + utils.formatar_dinheiro(item["custo"])
        item["custo"] = utils.ler_decimal(
            texto + "]: ", minimo=0, padrao=item["custo"])

    item["lead_time"] = utils.ler_inteiro(
        "Lead time [" + str(item["lead_time"]) + "]: ",
        minimo=0, padrao=item["lead_time"])
    item["estoque_seguranca"] = utils.ler_decimal(
        "Estoque de seguranca ["
        + utils.formatar_numero(item["estoque_seguranca"]) + "]: ",
        minimo=0, padrao=item["estoque_seguranca"])
    item["lote_minimo"] = utils.ler_decimal(
        "Lote minimo [" + utils.formatar_numero(item["lote_minimo"]) + "]: ",
        minimo=0, padrao=item["lote_minimo"])

    persistencia.salvar_tudo(dados)
    print("Item " + codigo + " alterado.")
