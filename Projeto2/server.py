#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


comandos_dic = {
    b'\x00\x00\x00\x00': "Comando 1",
    b'\x00\x00\xAA\x00': "Comando 2",
    b'\xAA\x00\x00': "Comando 3",
    b'\x00\xAA\x00': "Comando 4",
    b'\x00\x00\xAA': "Comando 5",
    b'\x00\xAA': "Comando 6",
    b'\xAA\x00': "Comando 7",
    b'x\00': "Comando 8",
    b'\xFF': "Comando 9",
}

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
                 
        # Definindo o timeout em 5 segundos
        timeout = 5

        # Esperando byte de sacrifício
        rxBuffer, nRx = com1.getData(1)
        print(rxBuffer)
        com1.rx.clearBuffer() # Limpa o buffer de recebimento para receber os comandos
        time.sleep(0.1)

        # Recebendo o número de comandos
        rxBuffer, nRx = com1.getData(1)
        numero_comandos = int.from_bytes(rxBuffer, byteorder='little')
        print("O número de comandos é: {}" .format(numero_comandos))
        time.sleep(0.1)

        #Contador para contar o número de comandos recebidos
        c = 0

        verifica_timeout = float(time.time()) # Variável para verificar se o timeout foi atingido
        print("Verifica timeout: {}" .format(verifica_timeout))
        deu_timeout = float(time.time() - verifica_timeout) 
        print("Deu timeout: {}" .format(deu_timeout))

        # Função que atualiza o tempo para verificar timeout
        def atualiza_timeout(tempo):
            tempo_atual = float(time.time())
            tempo_referencia = float(tempo_atual - tempo)
            return tempo_referencia
        
        #Loop para receber os comandos do client
        while (c < numero_comandos) and (deu_timeout < timeout):
            print("Recebendo o tamanho do comando")
            rxBuffer, nRx = com1.getData(1)
            time.sleep(0.1)
            tamanho_esperado = int.from_bytes(rxBuffer, byteorder='little')
            time.sleep(0.5)
            print("O tamanho esperado do comando é: {}" .format(tamanho_esperado))
            time.sleep(0.1)
            rxBuffer, nRx = com1.getData(tamanho_esperado)
            print('Comando recebido: {}' .format(rxBuffer))
            time.sleep(0.1)
            c += 1
            deu_timeout = atualiza_timeout(verifica_timeout)
            verifica_timeout = float(time.time())
        
        # Verifica se o timeout foi atingido
        if deu_timeout >= timeout:
            print("Timeout atingido")
            com1.disable()
            
        else:
            print('----------------------------------------')
            print('O número de comandos recebidos foi: {}' .format(c))
            print('----------------------------------------')

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
