import socket
import sys

# Configurações de conexão
HOST = '127.0.0.1'  # Endereço do servidor (localhost para testes)
PORT = 9000         # Deve ser a mesma porta configurada no servidor

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
            # Recebe uma linha digitada pelo usuário
            mensagem = input("> ").strip()

            if not mensagem:
                continue

            # Envia para o servidor
            cliente.sendall(mensagem.encode('utf-8'))

            # Verifica se o comando é SAIR para fechar o loop do cliente
            if mensagem.upper() == 'SAIR':
                print("Encerrando conexão...")
                break

            # Aguarda a resposta do servidor e a exibe no terminal
            resposta = cliente.recv(1024).decode('utf-8')
            if not resposta:
                print("Servidor encerrou a conexão inesperadamente.")
                break

            print(resposta)

        except KeyboardInterrupt:
            # Permite encerrar com Ctrl+C enviando o comando SAIR por segurança
            print("\nEncerrando...")
            cliente.sendall("SAIR".encode('utf-8'))
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()