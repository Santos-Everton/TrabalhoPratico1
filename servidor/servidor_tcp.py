# Imports
import os
import socket
import threading
import sys

# Constantes
IP = "localhost"
PORTA = 4457 if sys.argv[1] == "" else int(sys.argv[1])
ADDR = (IP, PORTA)
SIZE = 1024
FORMAT = "utf-8"
DIRETORIO_SERVIDOR = "diretorio_servidor"
BUFFER_SIZE = 4096
TAMANHO_MAXIMO_CACHE = 64e+6

# Memória cache
cache = dict()

# função que trata de cada cliente
def cliente(con, addr, lock):
    print(f"NOVA CONEXÃO: {addr} CONECTADO.")
    con.send("CONECTADO".encode(FORMAT))
    while True:
        dado = con.recv(SIZE).decode(FORMAT)
        comando = dado.split(" ")[0]
        arquivos = os.listdir(DIRETORIO_SERVIDOR)
        #Se o comando for list
        if comando == "list":
            print(f"{addr} SOLICITOU A LISTA DE ARQUIVOS.")
            if len(arquivos) == 0:
                retorno = "O DIRETÓRIO DO SERVIDOR ESTÁ VAZIO!"
            else:
                retorno = "\n---ARQUIVOS NO SERVIDOR---\n"
                retorno += "\t"
                retorno += "\n\t".join(f for f in arquivos)
                retorno += "\n---ARQUIVOS NA CACHE DO SERVIDOR---:\n"
                retorno += "\t"
                retorno += "\n\t".join(k for k in cache.keys())
            con.send(retorno.encode(FORMAT))
            break
        # Se o comando for help
        elif comando == "help":
            print(f"{addr} SOLICITOU AJUDA.")
            retorno = "---AJUDA---\n"
            retorno += "IP_SERVIDOR PORTA_SERVIDOR list: PARA LISTAR OS ARQUIVOS DO SERVIDOR\n"
            retorno += "IP_SERVIDOR PORTA_SERVIDOR help: PARA LISTAR OS COMANDOS.\n"
            retorno += "IP_SERVIDOR PORTA_SERVIDOR file NOME_ARQUIVO DIRETÓRIO_DESTINO: PARA REQUISITAR UM ARQUIVO DO SERVIDOR.\n"
            con.send(retorno.encode(FORMAT))
            break
        # Se o comando for file
        elif comando == "file":
            nome_arquivo = dado.split(" ")[1]
            print(f"CLIENTE: {addr} ESTÁ REQUISITANDO O ARQUIVO: {nome_arquivo}\n")
            if nome_arquivo in arquivos or nome_arquivo in cache:
                con.send("OK".encode(FORMAT))
                # Se o arquivo estiver na cache
                if nome_arquivo in cache:
                    for dado in cache[nome_arquivo]:
                        con.send(dado)
                    print("ARQUIVO ENVIADO DA MEMÓRIA CACHE")
                    break
                # Se o arquivo estiver no disco
                else:
                    # Usando locking para garantir exclusão mútua
                    lock.acquire()
                    with open(os.path.join(DIRETORIO_SERVIDOR, nome_arquivo), 'rb') as file:
                        while True:
                            bytes_lidos = file.read(BUFFER_SIZE)
                            if not bytes_lidos:
                                break
                            con.send(bytes_lidos)
                    print("ARQUIVO ENVIADO\n")
                    with open(os.path.join(DIRETORIO_SERVIDOR, nome_arquivo), 'rb') as file:
                        dado = file.readlines()
                        tamanho_arquivo = tamanho(dado)
                        tamanho_atual_cache = tamanhoAtualCache(cache)
                        keys = []
                        if not tamanho_arquivo > TAMANHO_MAXIMO_CACHE:
                            while (tamanho_atual_cache+tamanho_arquivo) > TAMANHO_MAXIMO_CACHE:
                                for k in cache:
                                    keys.append(k)
                                tamanho_atual_cache -= tamanho(cache[keys[0]])
                                cache.pop(keys[0])
                                keys.pop(0)
                            cache.update({nome_arquivo: dado})
                            print("ADICIONANDO ARQUIVO NA CACHE")
                    lock.release()
                    break
            # Se arquivo não estiver no disco nem na cache: Arquivo Não Encontrado
            else:
                print(f"{nome_arquivo} NÃO EXISTE NO SERVIDOR.")
                con.send(("ANE").encode(FORMAT))
                break
    print(f"{addr} DESCONECTOU\n")
    con.close()

# Função para o tamanho atual da cache
def tamanhoAtualCache(cache: dict):
    size = 0
    for key in cache:
        size += tamanho(cache[key])
    return size

# Função para o tamanho do arquivo
def tamanho(dado):
    size = 0
    for linha in dado:
        size += linha.__sizeof__()
    return size

# Função principal
def main():
    print("INICIANDO SERVIDOR")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    lock = threading.Semaphore()
    print(f"SERVIDOR INICIADO EM: {IP}:{PORTA}.\n")
    while True:
        con, addr = server.accept()
        thread = threading.Thread(
            target=cliente, args=(con, addr, lock))
        thread.start()
        print(f"CONEXÕES ATIVAS: {threading.active_count() - 1}\n")

if __name__ == "__main__":
    main()