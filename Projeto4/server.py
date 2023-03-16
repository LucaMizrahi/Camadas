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
from funcoes import *
from timer_error import Timer1Error, Timer2Error


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def resposta_server(tipo, numero_pacote, total_pacotes, com1):
    head = monta_head(tipo, 0, 0, total_pacotes, numero_pacote, 0, numero_pacote, (numero_pacote - 1))
    pacote = head + EOP
    com1.sendData(pacote)
    time.sleep(0.1)
    log_write(ARQUIVO, 'envio', tipo, 14)


'''
Parametros: (head)
    h0(byte): Tipo de mensagem (dados, comando etc.).
    h1(byte): Se for tipo1: número do servidor. Qualquer outro tipo: livre
    h2(byte): Livre.
    h3(bytes): Número total de pacotes do arquivo.
    h4(byte): Número do pacote
    h5(byte): Se a mensagem for do tipo HandShake, representa o id do arquivo,
    se for do tipo de dados: representa o tamanho do payload.
    h6(byte): pacote solicitado para recomeço quando a erro no envio.
    h7(byte): último pacote recebido com sucesso.
    h8(byte): CRC. (Em branco)
    h9(byte): CRC. (Em branco)
'''

# Chamado do cliente para o servidor 
TIPO1 = 1
# Resposta do servidor para o cliente
TIPO2 = 2
# Mensagem contendo o tipo de dados
TIPO3 = 3
# Mensagem enviada ao servidor relatando que a mensagem do tipo 3 foi recebida e averiguada
TIPO4 = 4
# Mensagem de time out, toda vez que o limite de espera exceder, esta mensagem será enviada (tanto cliewnte quanto servidor)
TIPO5 = 5
# Mensagem de erro, servidor envia para o cliente quando ocorre algum erro na mensagem tipo 3 - orienta cliente a enviar novamente
TIPO6 = 6

# End of Package (4 bytes)
EOP = '\xAA\xBB\xCC\xDD' 

ARQUIVO = 'server1.txt'
SERVER_ID = 1

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        print('Abriu a comunicação')
        
        # Esperando byte de sacrifício
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer() # Limpa o buffer de recebimento para receber os comandos
        time.sleep(0.1)
        print('byte de sacrifício recebido')	

        ocioso = True
        while ocioso:
            # Recebendo Handshake
            HEAD_client_handshake, _ = com1.getData(10, timer1, timer2)
            end_of_package, _ = com1.getData(4, timer1, timer2)
            log_write(ARQUIVO, 'recebimento', 1, 14)
            total_pacotes = HEAD_client_handshake[3]
            id_client = HEAD_client_handshake[5]
            time.sleep(0.1)
            # Checagem de handshake
            if HEAD_client_handshake[0] == b'\x01' and end_of_package == EOP:
                print('Handshake recebido')
                if HEAD_client_handshake[1] == SERVER_ID:
                    ocioso = False
                    print('Handshake correto, e é para mim.') 
                    time.sleep(1)

                    # Enviando resposta do handshake                  
                    HEAD_server_handshake = monta_head(TIPO2, 0, 0, 0, 0, 0, 0, 0)
                    server_handshake = HEAD_server_handshake + EOP
                    com1.sendData(server_handshake)
                    log_write(ARQUIVO, 'envio', 2, 14)
                    print('Resposta do Handshake enviada')
                    contador = 1
                    time.sleep(0.1)
                else:
                    ocioso = True
                    print('Handshake não é para mim')
            else:
                ocioso = True
                print('Handshake incorreto')

        # Começando a trasmissão dos dados
        img_recebida = b''
        reenvio = False
    
        while contador <= total_pacotes:
            try:
                timer1 = time.time()
                if not reenvio:
                    timer2 = time.time()

                # Pegando o primeiro pacote com dados do cliente
                HEAD_client, _ = com1.getData(10, timer1, timer2)
                tamanho_msg = HEAD_client[5]
                numero_pacote = HEAD_client[4]
                payload, _ = com1.getData(tamanho_msg, timer1, timer2)
                eop = com1.getData(4, timer1, timer2)
                log_write(ARQUIVO, 'recebimento', 3, 14+tamanho_msg, numero_pacote, total_pacotes)
                time.sleep(0.1)
            
                if HEAD_client[0] == b'\x03':
                    if eop == EOP and numero_pacote == contador:
                        img_recebida += payload
                        reenvio = False
                        contador += 1
                        resposta_server(TIPO4, contador, total_pacotes, com1)
                        print('Pacote {} recebido com sucesso'.format(contador))
                    else:
                        if numero_pacote != contador:
                            print('Número do pacote está incorreto, reenviando pacote')
                        if com1.rx.getBufferLen() > 0:
                            print('Tamanho do payload está incorreto')
                        
                        com1.rx.clearBuffer()
                        resposta_server(TIPO6, contador, total_pacotes, com1)

            except Timer1Error:
                print('O tempo do timer 1 foi excedido')
                resposta_server(TIPO4, contador, total_pacotes, com1)
                reenvio = True
            except Timer2Error:
                print('O tempo do timer 2 foi excedido')
                resposta_server(TIPO5, contador, total_pacotes, com1)
                break
        
        if (contador - 1) == total_pacotes:
            img_recebida_nome = 'Projeto4/img/img_recebida.png'
            print("Salvando imagem recebida")
            with open(img_recebida_nome, 'wb') as img_file:
                img_file.write(img_recebida)
            print("Imagem salva com sucesso")
            img_file.close()
                
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
