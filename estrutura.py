import persistencia
import utils


def pode_ser_componente(tipo_pai, tipo_filho):
    # RN03: PA aceita SA e MP, SA aceita so MP, MP nao tem estrutura
    if tipo_pai == "PA":
        return tipo_filho == "SA" or tipo_filho == "MP"
    if tipo_pai == "SA":
        return tipo_filho == "MP"
    return False


# coloca um componente na estrutura de um item
def cadastrar_componente(dados):
    utils.titulo("CADASTRO DE ESTRUTURA (BOM)")
    pai = utils.ler_texto("Codigo do item pai: ").upper()
    if pai not in dados["itens"]:
        print("ERRO: item pai nao encontrado.")
        return
    tipo_pai = dados["itens"][pai]["tipo"]
    # materia-prima nao tem estrutura
    if tipo_pai == "MP":
        print("ERRO: materia-prima nao possui estrutura (RN03).")
        return

    filho = utils.ler_texto("Codigo do componente: ").upper()
    if filho not in dados["itens"]:
        print("ERRO: componente nao encontrado.")
        return
    tipo_filho = dados["itens"][filho]["tipo"]
    if not pode_ser_componente(tipo_pai, tipo_filho):
        print("ERRO: um " + tipo_pai + " nao pode ter " + tipo_filho
              + " como componente (RN03).")
        return

    qtd = utils.ler_decimal("Quantidade por unidade do pai: ", positivo=True)

    if pai not in dados["estrutura"]:
        dados["estrutura"][pai] = []
    # se o componente ja esta na lista, so troca a quantidade
    for comp in dados["estrutura"][pai]:
        if comp["componente"] == filho:
            comp["qtd"] = qtd
            persistencia.salvar_tudo(dados)
            print("Componente ja existia, quantidade atualizada.")
            return
    dados["estrutura"][pai].append({"componente": filho, "qtd": qtd})
    persistencia.salvar_tudo(dados)
    print("Componente " + filho + " adicionado em " + pai + ".")


# tira um componente da estrutura
def remover_componente(dados):
    utils.titulo("REMOVER COMPONENTE DA ESTRUTURA")
    pai = utils.ler_texto("Codigo do item pai: ").upper()
    if pai not in dados["estrutura"]:
        print("ERRO: esse item nao tem estrutura cadastrada.")
        return
    filho = utils.ler_texto("Codigo do componente: ").upper()
    # procura o componente na lista pra remover
    for comp in dados["estrutura"][pai]:
        if comp["componente"] == filho:
            dados["estrutura"][pai].remove(comp)
            if len(dados["estrutura"][pai]) == 0:
                del dados["estrutura"][pai]
            persistencia.salvar_tudo(dados)
            print("Componente removido.")
            return
    print("ERRO: componente nao encontrado nessa estrutura.")


def mostrar_arvore(dados, codigo, prefixo, nivel, niveis):
    # funcao recursiva: desce um nivel a cada chamada
    if nivel > 3:
        return
    filhos = dados["estrutura"].get(codigo, [])
    for i in range(len(filhos)):
        comp = filhos[i]
        cod_filho = comp["componente"]
        item = dados["itens"][cod_filho]
        # o ultimo filho usa um conector diferente
        if i == len(filhos) - 1:
            conector = "└── "
            novo_prefixo = prefixo + "    "
        else:
            conector = "├── "
            novo_prefixo = prefixo + "│   "

        texto = prefixo + conector + cod_filho + " " + item["descricao"] + " "
        # completa com pontos ate a coluna da quantidade
        pontos = "." * max(2, 52 - len(texto))
        print(texto + pontos + " " + utils.formatar_numero(comp["qtd"])
              + " " + item["unidade"])

        if nivel not in niveis:
            niveis[nivel] = []
        if cod_filho not in niveis[nivel]:
            niveis[nivel].append(cod_filho)
        mostrar_arvore(dados, cod_filho, novo_prefixo, nivel + 1, niveis)


# mostra a arvore da estrutura de um produto
def exibir_estrutura(dados):
    utils.titulo("ESTRUTURA DE PRODUTO (EXPLOSAO DA BOM)")
    codigo = utils.ler_texto("Codigo do produto: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    if codigo not in dados["estrutura"]:
        print("O item " + codigo + " nao possui estrutura cadastrada.")
        return

    print(codigo + " " + dados["itens"][codigo]["descricao"])
    # guarda os itens de cada nivel pro resumo do final
    niveis = {}
    mostrar_arvore(dados, codigo, "", 1, niveis)

    resumo = "Niveis: 0 = " + codigo
    for nivel in sorted(niveis):
        resumo += " | " + str(nivel) + " = " + ", ".join(niveis[nivel])
    print(resumo)
