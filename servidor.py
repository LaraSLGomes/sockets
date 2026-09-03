import socket
import threading

# Configurações do servidor
HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 9000       # Porta configurável, conforme sugerido no documento

COMANDOS_VALIDOS = ['SOM', 'SOMA', 'SUB', 'MUL', 'DIV']

def divisao_truncada(num1, num2):
    """Divisão inteira que trunca em direção a zero (em vez de floor)."""
    sinal = -1 if (num1 < 0) != (num2 < 0) else 1
    return sinal * (abs(num1) // abs(num2))

def lidar_com_cliente(conexao, endereco):
    print(f"[CONECTOU] {endereco[0]}:{endereco[1]}")

    while True:
        try:
            # Recebe a mensagem do cliente
            dados = conexao.recv(1024)
            if not dados:
                break  # Cliente desconectou abruptamente

            mensagem = dados.decode('utf-8').strip()

            # Se a mensagem for vazia (apenas enter), ignora
            if not mensagem:
                continue

            partes = mensagem.split()
            comando = partes[0].upper()

            # Condição de encerramento
            if comando == 'SAIR':
                break

            # 1º) Tratamento: Formato inválido (quantidade de argumentos)
            # Checado antes do comando ser desconhecido, para dar prioridade
            # a erros de formato quando ambos os problemas ocorrem juntos.
            if len(partes) != 3:
                resposta = "ERRO: formato invalido (use: OPERACAO NUM1 NUM2)"
                conexao.sendall(resposta.encode('utf-8'))
                continue

            # 2º) Tratamento: Comando desconhecido
            # Nota: O documento lista "SOM" como comando, mas "SOMA" no exemplo. Aceitaremos ambos.
            if comando not in COMANDOS_VALIDOS:
                resposta = "ERRO: comando desconhecido"
                conexao.sendall(resposta.encode('utf-8'))
                continue

            # 3º) Tratamento: operandos não são inteiros válidos
            try:
                num1 = int(partes[1])
                num2 = int(partes[2])
            except ValueError:
                resposta = "ERRO: formato invalido (use: OPERACAO NUM1 NUM2)"
                conexao.sendall(resposta.encode('utf-8'))
                continue

            # Processamento do cálculo
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
                    # Divisão inteira truncada em direção a zero
                    # (ex: -7 / 2 = -3, e não -4 como faria o floor //)
                    resultado = divisao_truncada(num1, num2)
                    resposta = f"RESULTADO {resultado}"

            # Retorna o resultado ao cliente
            conexao.sendall(resposta.encode('utf-8'))

        except ConnectionResetError:
            break
        except Exception as e:
            print(f"[ERRO] {e}")
            break

    print(f"[DESCONECTOU] {endereco[0]}:{endereco[1]}")
    conexao.close()

def iniciar_servidor():
    # Criação do socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escutando na porta {PORT}...")

    try:
        while True:
            conexao, endereco = servidor.accept()
            # Cria uma thread para cada cliente que conecta
            thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
            thread.start()
    except KeyboardInterrupt:
        print("\nEncerrando o servidor...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()