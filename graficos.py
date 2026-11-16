import os

import capacidade
import estoque
import persistencia
import utils

try:
    import matplotlib.pyplot as plt
    TEM_MATPLOTLIB = True
except ImportError:
    TEM_MATPLOTLIB = False


def matplotlib_ok():
    if not TEM_MATPLOTLIB:
        print("ERRO: biblioteca matplotlib nao instalada. "
              "Rode: pip install matplotlib")
    return TEM_MATPLOTLIB


def salvar_e_mostrar(nome_arquivo):
    os.makedirs(persistencia.PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(persistencia.PASTA_SAIDA, nome_arquivo)
    plt.tight_layout()
    plt.savefig(caminho)
    print("Grafico salvo em: " + caminho)
    plt.show()
    plt.close()


def grafico_estoque(dados):
    if not matplotlib_ok():
        return
    if len(dados["itens"]) == 0:
        print("Nenhum item cadastrado.")
        return
    codigos = sorted(dados["itens"])
    saldos = []
    seguranca = []
    for codigo in codigos:
        saldos.append(estoque.saldo_do_item(dados, codigo))
        seguranca.append(dados["itens"][codigo]["estoque_seguranca"])

    posicoes = list(range(len(codigos)))
    esquerda = []
    direita = []
    for p in posicoes:
        esquerda.append(p - 0.2)
        direita.append(p + 0.2)

    plt.figure(figsize=(10, 5))
    plt.bar(esquerda, saldos, 0.4, label="Saldo atual")
    plt.bar(direita, seguranca, 0.4, label="Estoque de seguranca",
            color="orange")
    plt.xticks(posicoes, codigos, rotation=90)
    plt.xlabel("Item")
    plt.ylabel("Quantidade")
    plt.title("Posicao de estoque: saldo atual x estoque de seguranca")
    plt.legend()
    salvar_e_mostrar("grafico_posicao_estoque.png")


def grafico_projetado(dados):
    if not matplotlib_ok():
        return
    codigo = utils.ler_texto("Codigo do item: ").upper()
    if codigo not in dados["itens"]:
        print("ERRO: item nao encontrado.")
        return
    registro = dados["mrp"]["registros"].get(codigo)
    if registro is None:
        print("ERRO: nao ha registro MRP para esse item. Execute o MRP.")
        return

    semanas = list(range(1, utils.SEMANAS + 1))
    seguranca = dados["itens"][codigo]["estoque_seguranca"]
    plt.figure(figsize=(8, 5))
    plt.plot(semanas, registro["ep"], marker="o", label="Estoque projetado")
    plt.axhline(seguranca, color="red", linestyle="--",
                label="Estoque de seguranca")
    plt.xlabel("Semana")
    plt.ylabel("Quantidade")
    plt.title("Estoque projetado - " + codigo + " "
              + dados["itens"][codigo]["descricao"])
    plt.legend()
    salvar_e_mostrar("grafico_estoque_projetado_" + codigo + ".png")


def grafico_ordens(dados):
    if not matplotlib_ok():
        return
    qtd_op = [0] * utils.SEMANAS
    qtd_oc = [0] * utils.SEMANAS
    for ordem in dados["ordens"]["lista"]:
        if ordem["status"] == "ENCERRADA":
            continue
        if 1 <= ordem["entregar"] <= utils.SEMANAS:
            if ordem["tipo"] == "OP":
                qtd_op[ordem["entregar"] - 1] += 1
            else:
                qtd_oc[ordem["entregar"] - 1] += 1
    if sum(qtd_op) + sum(qtd_oc) == 0:
        print("Nao ha ordens abertas. Execute o MRP primeiro.")
        return

    semanas = list(range(1, utils.SEMANAS + 1))
    plt.figure(figsize=(8, 5))
    plt.bar(semanas, qtd_op, label="OP (producao)")
    plt.bar(semanas, qtd_oc, bottom=qtd_op, label="OC (compra)")
    plt.xlabel("Semana de entrega")
    plt.ylabel("Numero de ordens")
    plt.title("Ordens de producao e de compra por semana de entrega")
    plt.legend()
    salvar_e_mostrar("grafico_ordens_por_semana.png")


def grafico_carga(dados):
    if not matplotlib_ok():
        return
    centro = utils.ler_texto("Codigo do centro de trabalho: ").upper()
    if centro not in dados["centros"]:
        print("ERRO: centro nao encontrado.")
        return
    capacidade_horas = dados["centros"][centro]["capacidade"]
    carga = capacidade.calcular_carga(dados, centro)

    cores = []
    for valor in carga:
        if round(valor, 4) > capacidade_horas:
            cores.append("red")
        else:
            cores.append("steelblue")

    semanas = list(range(1, utils.SEMANAS + 1))
    plt.figure(figsize=(8, 5))
    plt.bar(semanas, carga, color=cores)
    plt.axhline(capacidade_horas, color="black", linestyle="--",
                label="Capacidade (" + utils.formatar_horas(capacidade_horas)
                + " h)")
    plt.xlabel("Semana")
    plt.ylabel("Carga (horas)")
    plt.title("Carga x capacidade - " + centro + " "
              + dados["centros"][centro]["nome"]
              + " (vermelho = sobrecarga)")
    plt.legend()
    salvar_e_mostrar("grafico_carga_" + centro + ".png")
