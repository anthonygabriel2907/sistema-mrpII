import persistencia
import utils


def centro_valido(codigo):
    # formato CT-01
    partes = codigo.split("-")
    if len(partes) != 2 or partes[0] != "CT":
        return False
    return partes[1].isascii() and partes[1].isdigit() and len(partes[1]) == 2


def cadastrar_centro(dados):
    utils.titulo("CADASTRO DE CENTRO DE TRABALHO")
    codigo = utils.ler_texto("Codigo (ex.: CT-01): ").upper()
    if not centro_valido(codigo):
        print("ERRO: codigo invalido. Use CT-NN (ex.: CT-01).")
        return
    if codigo in dados["centros"]:
        print("ERRO: esse centro ja esta cadastrado.")
        return
    nome = utils.ler_texto("Nome: ")
    capacidade = utils.ler_decimal("Capacidade (horas/semana): ",
                                   positivo=True)
    custo_hora = utils.ler_decimal("Custo-hora (R$): ", minimo=0)
    dados["centros"][codigo] = {
        "nome": nome,
        "capacidade": capacidade,
        "custo_hora": custo_hora,
    }
    persistencia.salvar_tudo(dados)
    print("Centro " + codigo + " cadastrado.")


def listar_centros(dados):
    utils.titulo("CENTROS DE TRABALHO")
    if len(dados["centros"]) == 0:
        print("Nenhum centro cadastrado.")
        return
    print("{:<8}{:<25}{:>12}{:>14}".format(
        "Codigo", "Nome", "Cap.(h/sem)", "Custo-hora"))
    for codigo in sorted(dados["centros"]):
        centro = dados["centros"][codigo]
        print("{:<8}{:<25}{:>12}{:>14}".format(
            codigo, centro["nome"],
            utils.formatar_horas(centro["capacidade"]),
            utils.formatar_dinheiro(centro["custo_hora"])))


def definir_roteiro(dados):
    utils.titulo("ROTEIRO DE OPERACAO")
    codigo = utils.ler_texto("Codigo do item fabricado: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    if dados["itens"][codigo]["tipo"] == "MP":
        print("ERRO: materia-prima e comprada, nao tem roteiro.")
        return
    centro = utils.ler_texto("Codigo do centro de trabalho: ").upper()
    if centro not in dados["centros"]:
        print("ERRO: centro nao encontrado.")
        return
    tempo = utils.ler_decimal("Tempo por unidade (horas): ", positivo=True)
    dados["roteiros"][codigo] = {"centro": centro, "tempo": tempo}
    persistencia.salvar_tudo(dados)
    print("Roteiro de " + codigo + " salvo.")


def listar_roteiros(dados):
    utils.titulo("ROTEIROS")
    if len(dados["roteiros"]) == 0:
        print("Nenhum roteiro cadastrado.")
        return
    print("{:<8}{:<32}{:<8}{:>12}".format(
        "Item", "Descricao", "Centro", "Tempo (h/un)"))
    for codigo in sorted(dados["roteiros"]):
        rot = dados["roteiros"][codigo]
        print("{:<8}{:<32}{:<8}{:>12}".format(
            codigo, dados["itens"][codigo]["descricao"], rot["centro"],
            utils.formatar_horas(rot["tempo"])))


def calcular_carga(dados, centro):
    # RN09: carga = qtd da OP x tempo unitario, na semana de liberacao
    carga = [0.0] * utils.SEMANAS
    for ordem in dados["ordens"]["lista"]:
        if ordem["tipo"] != "OP" or ordem["status"] == "ENCERRADA":
            continue
        roteiro = dados["roteiros"].get(ordem["item"])
        if roteiro is None or roteiro["centro"] != centro:
            continue
        semana = max(1, ordem["liberar"])
        if semana <= utils.SEMANAS:
            carga[semana - 1] += ordem["qtd"] * roteiro["tempo"]
    return carga


def texto_semanas(lista):
    if len(lista) == 1:
        return "na semana " + str(lista[0])
    nomes = []
    for semana in lista:
        nomes.append(str(semana))
    return "nas semanas " + ", ".join(nomes[:-1]) + " e " + nomes[-1]


def exibir_crp(dados):
    if len(dados["centros"]) == 0:
        print("Nenhum centro de trabalho cadastrado.")
        return
    for codigo in sorted(dados["centros"]):
        centro = dados["centros"][codigo]
        carga = calcular_carga(dados, codigo)
        print()
        print("CARGA x CAPACIDADE - " + codigo + " " + centro["nome"]
              + " (" + utils.formatar_horas(centro["capacidade"])
              + " h/semana)")
        print("Sem Carga(h) Uso(%)")
        sobrecarga = []
        for i in range(utils.SEMANAS):
            percentual = carga[i] / centro["capacidade"] * 100
            barra = "#" * int(round(percentual / 10))
            aviso = ""
            if round(carga[i], 4) > centro["capacidade"]:
                aviso = " SOBRECARGA"
                sobrecarga.append(i + 1)
            print("{:<5}{:>6}{:>7} {}{}".format(
                i + 1, utils.formatar_horas(carga[i]), int(round(percentual)),
                barra, aviso).rstrip())
        if len(sobrecarga) > 0:
            print("Sugestao: antecipar OPs ou programar hora extra "
                  + texto_semanas(sobrecarga) + ".")
        else:
            print("Sem sobrecarga nas 8 semanas.")
