import threading
import time
import random

class CoordenadorCentralizado:
    def __init__(self):
        self.lock_coordenador = threading.Lock()
        self.id_coordenador = -1
        self.condicao = threading.Condition(self.lock_coordenador)

    def entrar_secao_critica(self, id_processo):
        with self.lock_coordenador:
            while self.id_coordenador != -1:
                print(f"Processo {id_processo} está esperando a seção crítica.")
                self.condicao.wait()
            self.id_coordenador = id_processo
            print(f"Processo {id_processo} entrou na seção crítica.")

    def sair_secao_critica(self, id_processo):
        with self.lock_coordenador:
            if self.id_coordenador == id_processo:
                self.id_coordenador = -1
                print(f"Processo {id_processo} saiu da seção crítica.")
                self.condicao.notify_all()
            else:
                print(f"Processo {id_processo} não pode sair da seção crítica pois não é o coordenador.")

class AlgoritmoEleicao:
    def __init__(self, num_processos):
        self.processos = [True] * num_processos
        self.lock_eleicao = threading.Lock()

    def iniciar_eleicao(self, id_processo):
        with self.lock_eleicao:
            print(f"Processo {id_processo} iniciou a eleição.")
            for i in range(id_processo + 1, len(self.processos)):
                if self.processos[i]:
                    print(f"Processo {id_processo} enviou uma mensagem de eleição para o processo {i}.")
                    time.sleep(random.random() * 0.5)  
            print(f"Processo {id_processo} é o novo coordenador.")
            with coordenador.lock_coordenador:
                coordenador.id_coordenador = id_processo

    def lidar_com_falha(self, id_processo_falho):
        print(f"Processo {id_processo_falho} falhou. Iniciando uma nova eleição.")
        self.processos[id_processo_falho] = False
        for i in range(id_processo_falho + 1, len(self.processos)):
            if self.processos[i]:
                print(f"Processo {id_processo_falho} enviou uma mensagem de falha para o processo {i}.")
                self.iniciar_eleicao(i)
                return

def thread_processo(id_processo, coordenador, algoritmo_eleicao):
    while True:
        coordenador.entrar_secao_critica(id_processo)
        time.sleep(random.random() * 0.5) 
        coordenador.sair_secao_critica(id_processo)
        time.sleep(random.random() * 0.5)  
        if random.random() < 0.05:  
            algoritmo_eleicao.lidar_com_falha(id_processo)
            break

def main():
    num_processos = 7
    global coordenador
    coordenador = CoordenadorCentralizado()
    algoritmo_eleicao = AlgoritmoEleicao(num_processos)

    threads = []
    for i in range(num_processos):
        t = threading.Thread(target=thread_processo, args=(i, coordenador, algoritmo_eleicao))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
if __name__ == "__main__":
    main()
    print("As threads acabaram")

