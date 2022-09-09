import socket
import os
import sys

IP = sys.argv[1]
PORTA = int(sys.argv[2])
ADDR = (IP, PORTA)
FORMAT = "utf-8"
SIZE = 1024
BUFFER_SIZE = 4096

# Função principal
def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(ADDR)
    dado = cliente.recv(SIZE).decode(FORMAT)
    if dado == "DISCONNECTED":
        print("\n\t SERVIDOR DESCONECTADO")
    elif dado == "CONECTADO":
        print("\n\tBEM VINDO AO SERVIDOR DE ARQUIVOS")
    # Se o comando for ajuda
    comando = sys.argv[3]
    if comando == "help":
        cliente.send(comando.encode(FORMAT))
        dado = cliente.recv(SIZE).decode(FORMAT)
        print(dado)
    # Se o comando for para listar os arquivos do servidor
    elif comando == "list":
        cliente.send(comando.encode(FORMAT))
        dado = cliente.recv(SIZE).decode(FORMAT)
        print(dado)
    # Se o comando for para requisitar um arquivo do servidor
    elif comando == "file":
        nome_arquivo = sys.argv[4]
        cliente_data_path = sys.argv[5]
        envio = f"{comando} {nome_arquivo}"
        cliente.send(envio.encode(FORMAT))
        resposta_requisicao = cliente.recv(SIZE)
        if resposta_requisicao == "ANE":
            print("ARQUIVO NÃO ENCONTRADO!")
        else:
            with open(os.path.join(cliente_data_path, nome_arquivo), 'wb') as file:
                while True:
                    arquivo = cliente.recv(BUFFER_SIZE)
                    if not arquivo:
                        break
                    file.write(arquivo)
            print(f"{nome_arquivo} RECEBIDO!\n")
    else:
        print("ERRO: COMANDO INVÁLIDO.\n")
    cliente.close()
    print("DESCONECTADO DO SERVIDOR")

if __name__ == "__main__":
    main()