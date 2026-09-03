import socket
import sys

HOST = '127.0.0.1' 
PORT = 9000         

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")
        print("Digite o comando no formato: OPERACAO NUM1 NUM2 (ou SAIR para encerrar)")
    except Exception as e:
        print(f"Não foi possível conectar ao servidor: {e}")
        sys.exit()

    while True:
        try:
            mensagem = input("> ").strip()

            if not mensagem:
                continue

            cliente.sendall(mensagem.encode('utf-8'))

            if mensagem.upper() == 'SAIR':
                print("Encerrando conexão...")
                break

            resposta = cliente.recv(1024).decode('utf-8')
            if not resposta:
                print("Servidor encerrou a conexão inesperadamente.")
                break

            print(resposta)

        except KeyboardInterrupt:
            print("\nEncerrando...")
            cliente.sendall("SAIR".encode('utf-8'))
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()