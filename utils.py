import os


def read_int(msg, exept_msg="Inválido"):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print(f"{exept_msg}\n")


def read_option(msg, max_opt, exept_msg="Opção inválida."):
    while True:
        opt = read_int(msg, "Digite números")
        if 0 < opt <= max_opt:
            return opt
        print(f"\033[31m{exept_msg}\033[m\n")


def is_directory(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)


def is_empty_directory(path: str) -> bool:
    try:
        file  = os.listdir(path)
        return len(file) == 0
    except FileNotFoundError:
        return True


def is_document_added(nome: str) -> bool:
    try:
        with open("./base_de_documentos.txt", 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        linhas = []

    return nome in linhas


def write_document_name(document_title: str):
    with open("./base_de_documentos.txt", 'a', encoding='utf-8') as f:
        f.write(f"{document_title}\n")