import socket

HOST = "127.0.0.1"
PORTA = 5050
TAMANHO_MAX = 65507
TEMPO_ESPERA = 3

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.settimeout(TEMPO_ESPERA)
    print(f"cliente UDP enviando para {HOST}:{PORTA}. digite sair para encerrar")
    while True:
        comando = input("> ").strip()
        if not comando:
            continue
        if comando.lower() == "sair":
            break
        cliente.sendto((comando + "\n").encode("utf-8"), (HOST, PORTA))
        try:
            resposta, _ = cliente.recvfrom(TAMANHO_MAX)
        except socket.timeout:
            print("sem resposta do servidor, confira se ele esta rodando")
            continue
        except ConnectionResetError:
            print(f"nao foi possivel falar com {HOST}:{PORTA}")
            continue
        print(resposta.decode("utf-8").strip())
    cliente.close()


if __name__ == "__main__":
    main()