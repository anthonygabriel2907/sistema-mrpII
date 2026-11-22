import estoque
import persistencia
import utils


# cria uma OP ou OC com numero sequencial
def criar_ordem(dados, tipo, codigo, qtd, liberar, entregar):
    ordens = dados["ordens"]
    # OP e OC tem contadores separados
    if tipo == "OP":
        numero = ordens["proximo_op"]
        ordens["proximo_op"] = numero + 1
    else:
        numero = ordens["proximo_oc"]
        ordens["proximo_oc"] = numero + 1

    # dados da ordem
    ordem = {
        "numero": tipo + "-" + str(numero).zfill(4),
        "tipo": tipo,
        "item": codigo,
        "qtd": qtd,
        "liberar": liberar,
        "entregar": entregar,
        "status": "PLANEJADA",
    }
    # RN07: liberacao antes da semana 1 fica atrasada
    if liberar < 1:
        ordem["status"] = "ATRASADA"
    ordens["lista"].append(ordem)
    return ordem


# procura a ordem pelo numero, se nao achar devolve None
def buscar_ordem(dados, numero):
    for ordem in dados["ordens"]["lista"]:
        if ordem["numero"] == numero:
            return ordem
    return None


# mostra a lista de ordens
def listar_ordens(dados):
    data = dados["mrp"]["data"]
    if data == "":
        utils.titulo("ORDENS - o MRP ainda nao foi executado")
    else:
        utils.titulo("ORDENS - execucao do MRP em " + data)
    lista = dados["ordens"]["lista"]
    if len(lista) == 0:
        print("Nenhuma ordem cadastrada.")
        return
    print("{:<9}{:<5}{:<8}{:>7}  {:<9}{:<10}{}".format(
        "Ordem", "Tipo", "Item", "Qtde", "Liberar", "Entregar", "Status"))
    atrasadas = 0
    for ordem in lista:
        if ordem["status"] == "ATRASADA":
            atrasadas += 1
        print("{:<9}{:<5}{:<8}{:>7}  {:<9}{:<10}{}".format(
            ordem["numero"], ordem["tipo"], ordem["item"],
            utils.formatar_numero(ordem["qtd"]),
            utils.semana_texto(ordem["liberar"]),
            utils.semana_texto(ordem["entregar"]), ordem["status"]))
    if atrasadas > 0:
        texto = " mensagens"
        if atrasadas == 1:
            texto = " mensagem"
        print(str(atrasadas) + texto + " de excecao: ordens com "
              "liberacao antes da semana 1.")


# planejada ou atrasada vira firme
def firmar_ordem(dados):
    numero = utils.ler_texto("Numero da ordem: ").upper()
    ordem = buscar_ordem(dados, numero)
    if ordem is None:
        print("ERRO: ordem nao encontrada.")
        return
    if ordem["status"] != "PLANEJADA" and ordem["status"] != "ATRASADA":
        print("ERRO: so da para firmar ordem PLANEJADA ou ATRASADA "
              "(status atual: " + ordem["status"] + ").")
        return
    ordem["status"] = "FIRME"
    persistencia.salvar_tudo(dados)
    print("Ordem " + numero + " firmada.")


# firme vira liberada
def liberar_ordem(dados):
    numero = utils.ler_texto("Numero da ordem: ").upper()
    ordem = buscar_ordem(dados, numero)
    if ordem is None:
        print("ERRO: ordem nao encontrada.")
        return
    if ordem["status"] != "FIRME":
        print("ERRO: so da para liberar ordem FIRME "
              "(status atual: " + ordem["status"] + ").")
        return
    ordem["status"] = "LIBERADA"
    persistencia.salvar_tudo(dados)
    print("Ordem " + numero + " liberada.")


# da baixa nos componentes e da entrada no item produzido
def apontar(dados, ordem):
    codigo = ordem["item"]
    componentes = dados["estrutura"].get(codigo, [])
    if len(componentes) == 0:
        print("ERRO: o item " + codigo + " nao tem estrutura cadastrada.")
        return

    # primeiro confere se todos os componentes tem saldo
    faltas = []
    for comp in componentes:
        preciso = round(ordem["qtd"] * comp["qtd"], 4)
        saldo = estoque.saldo_do_item(dados, comp["componente"])
        if saldo < preciso:
            faltas.append("  " + comp["componente"] + ": precisa de "
                          + utils.formatar_numero(preciso) + " e tem "
                          + utils.formatar_numero(saldo))
    if len(faltas) > 0:
        print("ERRO: apontamento rejeitado, falta componente:")
        for texto in faltas:
            print(texto)
        return

    data = utils.hoje()
    for comp in componentes:
        preciso = round(ordem["qtd"] * comp["qtd"], 4)
        estoque.registrar_movimento(
            dados, comp["componente"], "SAIDA", -preciso,
            ordem["numero"] + " (" + codigo + ")", data)
    estoque.registrar_movimento(
        dados, codigo, "ENTRADA", ordem["qtd"],
        ordem["numero"] + " (producao)", data)
    ordem["status"] = "ENCERRADA"
    persistencia.salvar_tudo(dados)
    print("Producao apontada. Ordem " + ordem["numero"] + " encerrada.")
    print("Entrada de " + utils.formatar_numero(ordem["qtd"]) + " "
          + dados["itens"][codigo]["unidade"] + " de " + codigo
          + " no estoque.")


# so OP liberada pode ser apontada
def apontar_producao(dados):
    numero = utils.ler_texto("Numero da OP: ").upper()
    ordem = buscar_ordem(dados, numero)
    if ordem is None:
        print("ERRO: ordem nao encontrada.")
        return
    if ordem["tipo"] != "OP":
        print("ERRO: apontamento de producao so vale para OP.")
        return
    if ordem["status"] != "LIBERADA":
        print("ERRO: a OP precisa estar LIBERADA "
              "(status atual: " + ordem["status"] + ").")
        return
    apontar(dados, ordem)


# encerra uma ordem liberada
def encerrar_ordem(dados):
    numero = utils.ler_texto("Numero da ordem: ").upper()
    ordem = buscar_ordem(dados, numero)
    if ordem is None:
        print("ERRO: ordem nao encontrada.")
        return
    if ordem["status"] != "LIBERADA":
        print("ERRO: so da para encerrar ordem LIBERADA "
              "(status atual: " + ordem["status"] + ").")
        return
    if ordem["tipo"] == "OP":
        # OP encerra pelo apontamento de producao
        apontar(dados, ordem)
        return
    # OC encerrada = material chegou, entra no estoque
    estoque.registrar_movimento(
        dados, ordem["item"], "ENTRADA", ordem["qtd"],
        ordem["numero"] + " (recebimento)", utils.hoje())
    ordem["status"] = "ENCERRADA"
    persistencia.salvar_tudo(dados)
    print("Ordem " + numero + " encerrada. Material recebido no estoque.")
