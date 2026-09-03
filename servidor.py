import socket
import threading

HOST = '0.0.0.0'  
PORT = 9000       

COMANDOS_VALIDOS = ['SOM', 'SOMA', 'SUB', 'MUL', 'DIV']

def divisao_truncada(num1, num2):
    """Divisão inteira que trunca em direção a zero (em vez de floor)."""
    sinal = -1 if (num1 < 0) != (num2 < 0) else 1
    return sinal * (abs(num1) // abs(num2))

def lidar_com_cliente(conexao, endereco):
    print(f"[CONECTOU] {endereco[0]}:{endereco[1]}")

    while True:
        try:
            dados = conexao.recv(1024)
            if not dados:
                break 
            mensagem = dados.decode('utf-8').strip()

            if not mensagem:
                continue

            partes = mensagem.split()
            comando = partes[0].upper()

            if comando == 'SAIR':
                break

            if len(partes) != 3:
                resposta = "ERRO: formato invalido (use: OPERACAO NUM1 NUM2)"
                conexao.sendall(resposta.encode('utf-8'))
                continue

            if comando not in COMANDOS_VALIDOS:
                resposta = "ERRO: comando desconhecido"
                conexao.sendall(resposta.encode('utf-8'))
                continue

            try:
                num1 = int(partes[1])
                num2 = int(partes[2])
            except ValueError:
                resposta = "ERRO: formato invalido (use: OPERACAO NUM1 NUM2)"
                conexao.sendall(resposta.encode('utf-8'))
                continue

            if comando == 'SOM' or comando == 'SOMA':
                resultado = num1 + num2
                resposta = f"RESULTADO {resultado}"
            elif comando == 'SUB':
                resultado = num1 - num2
                resposta = f"RESULTADO {resultado}"
            elif comando == 'MUL':
                resultado = num1 * num2
                resposta = f"RESULTADO {resultado}"
            elif comando == 'DIV':
                if num2 == 0:
                    resposta = "ERRO: divisao por zero"
                else:
                    resultado = divisao_truncada(num1, num2)
                    resposta = f"RESULTADO {resultado}"

            conexao.sendall(resposta.encode('utf-8'))

        except ConnectionResetError:
            break
        except Exception as e:
            print(f"[ERRO] {e}")
            break

    print(f"[DESCONECTOU] {endereco[0]}:{endereco[1]}")
    conexao.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escutando na porta {PORT}...")

    try:
        while True:
            conexao, endereco = servidor.accept()
            thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
            thread.start()
    except KeyboardInterrupt:
        print("\nEncerrando o servidor...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()