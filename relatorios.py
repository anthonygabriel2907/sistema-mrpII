import csv
import os

import estoque
import persistencia
import utils


def exportar_estoque(dados):
    os.makedirs(persistencia.PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(persistencia.PASTA_SAIDA, "posicao_estoque.csv")
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["codigo", "descricao", "tipo", "unidade", "saldo",
                           "estoque_seguranca", "situacao"])
        for codigo in sorted(dados["itens"]):
            item = dados["itens"][codigo]
            saldo = estoque.saldo_do_item(dados, codigo)
            situacao = "OK"
            if saldo < item["estoque_seguranca"]:
                situacao = "ABAIXO DO ESTOQUE DE SEGURANCA"
            escritor.writerow([
                codigo, item["descricao"], item["tipo"], item["unidade"],
                utils.formatar_numero(saldo),
                utils.formatar_numero(item["estoque_seguranca"]), situacao])
    print("Posicao de estoque exportada em: " + caminho)


def exportar_ordens(dados):
    os.makedirs(persistencia.PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(persistencia.PASTA_SAIDA, "lista_ordens.csv")
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["ordem", "tipo", "item", "descricao", "quantidade",
                           "semana_liberacao", "semana_entrega", "status"])
        for ordem in dados["ordens"]["lista"]:
            descricao = dados["itens"][ordem["item"]]["descricao"]
            escritor.writerow([
                ordem["numero"], ordem["tipo"], ordem["item"], descricao,
                utils.formatar_numero(ordem["qtd"]), ordem["liberar"],
                ordem["entregar"], ordem["status"]])
    print("Lista de ordens exportada em: " + caminho)
