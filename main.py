import menu
import persistencia


# carrega os dados e abre o menu
def main():
    dados = persistencia.carregar_tudo()
    try:
        menu.menu_principal(dados)
    # ctrl+c ou fim da entrada fecha sem erro
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado.")


if __name__ == "__main__":
    main()
