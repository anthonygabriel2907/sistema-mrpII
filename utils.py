import math
from datetime import date, datetime

# tipos de item: produto acabado, semiacabado e materia-prima
TIPOS = ["PA", "SA", "MP"]
# quantas semanas o planejamento tem
SEMANAS = 8


# imprime uma linha repetindo um caractere
def linha(tamanho=50, caractere="-"):
    print(caractere * tamanho)


# titulo entre duas linhas de =
def titulo(texto):
    print()
    linha(50, "=")
    print(texto)
    linha(50, "=")


# data de hoje no formato dd/mm/aaaa
def hoje():
    return date.today().strftime("%d/%m/%Y")


def formatar_numero(valor):
    # mostra sem casa decimal quando for inteiro (10 em vez de 10.0)
    if valor == int(valor):
        return str(int(valor))
    return str(round(valor, 2)).replace(".", ",")


# dinheiro com 2 casas e virgula
def formatar_dinheiro(valor):
    return "{:.2f}".format(valor).replace(".", ",")


# horas com 1 casa e virgula
def formatar_horas(valor):
    return "{:.1f}".format(valor).replace(".", ",")


# vira S1, S2, S3...
def semana_texto(numero):
    return "S" + str(numero)


def codigo_valido(codigo):
    # formato Tipo-Numero, exemplo PA-001
    partes = codigo.split("-")
    if len(partes) != 2:
        return False
    if partes[0] not in TIPOS:
        return False
    numero = partes[1]
    return numero.isascii() and numero.isdigit() and len(numero) == 3


# nao deixa o campo ficar vazio
def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("ERRO: o campo nao pode ficar vazio.")


# le um inteiro e confere o minimo e o maximo
def ler_inteiro(mensagem, minimo=None, maximo=None, padrao=None):
    while True:
        texto = input(mensagem).strip()
        if texto == "" and padrao is not None:
            return padrao
        try:
            valor = int(texto)
        except ValueError:
            print("ERRO: digite um numero inteiro.")
            continue
        if minimo is not None and valor < minimo:
            print("ERRO: o valor minimo e " + str(minimo) + ".")
            continue
        if maximo is not None and valor > maximo:
            print("ERRO: o valor maximo e " + str(maximo) + ".")
            continue
        return valor


# igual ao inteiro, mas aceita virgula
def ler_decimal(mensagem, minimo=None, positivo=False, padrao=None):
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        if texto == "" and padrao is not None:
            return padrao
        try:
            valor = float(texto)
        except ValueError:
            print("ERRO: digite um numero valido.")
            continue
        # nao deixa passar nan nem infinito
        if not math.isfinite(valor):
            print("ERRO: numero invalido.")
            continue
        if positivo and valor <= 0:
            print("ERRO: o valor deve ser maior que zero.")
            continue
        if minimo is not None and valor < minimo:
            print("ERRO: o valor minimo e " + formatar_numero(minimo) + ".")
            continue
        return valor


# repete ate digitar uma das opcoes
def ler_opcao(mensagem, validas):
    while True:
        texto = input(mensagem).strip().upper()
        if texto in validas:
            return texto
        print("ERRO: opcao invalida. Escolha entre: " + ", ".join(validas))


# se der enter usa a data de hoje
def ler_data(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            return hoje()
        try:
            data = datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            print("ERRO: data invalida. Use dd/mm/aaaa.")
            continue
        return data.strftime("%d/%m/%Y")
