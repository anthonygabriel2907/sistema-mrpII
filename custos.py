import utils


# tempo do roteiro vezes o custo-hora do centro
def custo_mao_de_obra(dados, codigo):
    roteiro = dados["roteiros"].get(codigo)
    if roteiro is None:
        return 0
    centro = dados["centros"].get(roteiro["centro"])
    if centro is None:
        return 0
    return roteiro["tempo"] * centro["custo_hora"]


def custo_unitario(dados, codigo):
    # recursivo: custo do item = componentes (cada um calculado do mesmo
    # jeito) + mao de obra do roteiro
    item = dados["itens"][codigo]
    if item["tipo"] == "MP":
        return item["custo"]
    total = 0
    for comp in dados["estrutura"].get(codigo, []):
        total += comp["qtd"] * custo_unitario(dados, comp["componente"])
    total += custo_mao_de_obra(dados, codigo)
    return total


# mostra o detalhamento do custo de um item
def mostrar_custo(dados):
    utils.titulo("CUSTO PADRAO DE UM ITEM")
    codigo = utils.ler_texto("Codigo do item fabricado: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    if dados["itens"][codigo]["tipo"] == "MP":
        print("ERRO: materia-prima nao tem custo padrao, use o custo "
              "unitario do cadastro.")
        return
    if codigo not in dados["estrutura"]:
        print("ERRO: o item nao tem estrutura cadastrada.")
        return

    print("CUSTO PADRAO - " + codigo + " "
          + dados["itens"][codigo]["descricao"])
    print("{:<8}{:<28}{:>7}{:>12}{:>12}".format(
        "Item", "Descricao", "Qtde", "Custo un.", "Total"))
    for comp in dados["estrutura"][codigo]:
        cod_filho = comp["componente"]
        custo = custo_unitario(dados, cod_filho)
        total = custo * comp["qtd"]
        print("{:<8}{:<28}{:>7}{:>12}{:>12}".format(
            cod_filho, dados["itens"][cod_filho]["descricao"],
            utils.formatar_numero(comp["qtd"]),
            utils.formatar_dinheiro(custo), utils.formatar_dinheiro(total)))

    roteiro = dados["roteiros"].get(codigo)
    if roteiro is not None and roteiro["centro"] in dados["centros"]:
        custo_hora = dados["centros"][roteiro["centro"]]["custo_hora"]
        print("{:<36}{:>7}{:>12}{:>12}".format(
            "Mao de obra " + roteiro["centro"],
            utils.formatar_horas(roteiro["tempo"]) + " h",
            utils.formatar_dinheiro(custo_hora),
            utils.formatar_dinheiro(custo_mao_de_obra(dados, codigo))))
    else:
        print("AVISO: item sem roteiro, mao de obra considerada zero.")

    print("-" * 71)
    print("CUSTO PADRAO TOTAL R$ "
          + utils.formatar_dinheiro(custo_unitario(dados, codigo)))


# lista o custo de todos os itens fabricados
def listar_custos(dados):
    utils.titulo("CUSTO PADRAO DOS ITENS FABRICADOS")
    print("{:<8}{:<32}{:>14}".format("Item", "Descricao", "Custo (R$)"))
    achou = False
    for codigo in sorted(dados["itens"]):
        item = dados["itens"][codigo]
        if item["tipo"] == "MP":
            continue
        achou = True
        print("{:<8}{:<32}{:>14}".format(
            codigo, item["descricao"],
            utils.formatar_dinheiro(custo_unitario(dados, codigo))))
    if not achou:
        print("Nenhum item fabricado cadastrado.")
