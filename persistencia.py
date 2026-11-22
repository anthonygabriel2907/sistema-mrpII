import csv
import json
import os

# pastas do projeto
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA_BASE, "data")
PASTA_SAIDA = os.path.join(PASTA_BASE, "saida")

# colunas do movimentos.csv
CAMPOS_MOVIMENTO = ["data", "item", "tipo", "qtd", "saldo", "documento"]


# le um json da pasta data, se nao existir usa o padrao
def ler_json(nome, padrao):
    caminho = os.path.join(PASTA_DADOS, nome)
    if not os.path.exists(caminho):
        return padrao
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (OSError, ValueError):
        print("ERRO: nao foi possivel ler o arquivo " + caminho)
        raise SystemExit(1)


# grava num arquivo temporario antes, pra nao perder os dados se der erro
def gravar_json(nome, conteudo):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho = os.path.join(PASTA_DADOS, nome)
    temporario = caminho + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(conteudo, arquivo, indent=2, ensure_ascii=False)
    os.replace(temporario, caminho)


# le o kardex do csv
def ler_movimentos():
    caminho = os.path.join(PASTA_DADOS, "movimentos.csv")
    movimentos = []
    if not os.path.exists(caminho):
        return movimentos
    try:
        with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
            for linha in csv.DictReader(arquivo):
                linha["qtd"] = float(linha["qtd"])
                linha["saldo"] = float(linha["saldo"])
                movimentos.append(linha)
    except (OSError, ValueError, KeyError):
        print("ERRO: nao foi possivel ler o arquivo " + caminho)
        raise SystemExit(1)
    return movimentos


# regrava o csv inteiro
def gravar_movimentos(movimentos):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho = os.path.join(PASTA_DADOS, "movimentos.csv")
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_MOVIMENTO)
        escritor.writeheader()
        for mov in movimentos:
            escritor.writerow(mov)


# le todos os arquivos e junta num dicionario so
def carregar_tudo():
    dados = {}
    dados["itens"] = ler_json("itens.json", {})
    dados["estrutura"] = ler_json("estrutura.json", {})
    dados["estoque"] = ler_json("estoque.json", {})
    dados["movimentos"] = ler_movimentos()
    dados["centros"] = ler_json("centros.json", {})
    dados["roteiros"] = ler_json("roteiros.json", {})
    dados["mps"] = ler_json("mps.json", {})
    dados["ordens"] = ler_json(
        "ordens.json", {"proximo_op": 1, "proximo_oc": 1, "lista": []})
    dados["mrp"] = ler_json(
        "mrp.json", {"data": "", "registros": {}, "excecoes": []})
    return dados


# grava todos os arquivos de novo
def salvar_tudo(dados):
    gravar_json("itens.json", dados["itens"])
    gravar_json("estrutura.json", dados["estrutura"])
    gravar_json("estoque.json", dados["estoque"])
    gravar_movimentos(dados["movimentos"])
    gravar_json("centros.json", dados["centros"])
    gravar_json("roteiros.json", dados["roteiros"])
    gravar_json("mps.json", dados["mps"])
    gravar_json("ordens.json", dados["ordens"])
    gravar_json("mrp.json", dados["mrp"])
