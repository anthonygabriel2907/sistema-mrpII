import menu
import persistencia


def main():
    dados = persistencia.carregar_tudo()
    try:
        menu.menu_principal(dados)
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado.")


if __name__ == "__main__":
    main()
