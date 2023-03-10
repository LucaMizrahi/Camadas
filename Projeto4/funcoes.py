import numpy as np
from math import ceil
import time
from datetime import datetime

# End of Package    
EOP = b'\xAA\xBB\xCC\xDD' 


def atualiza_tempo(tempo_referencia):
    tempo_atual = time.time()
    ref = tempo_atual - tempo_referencia
    return ref

def verifica_eop(head, pacote): # Função para verificar se o payload está correto
    tamanho = head[2] # Tamanho = 3º byte do head = 0
    eop = pacote[12+tamanho:]
    if eop == b'\x01\x02\x03':
        print('Payload recebido com sucesso, esperando próximo pacote')
        return True
    else:
        print('Payload não recebido corretamente')
        return False

def verifica_handshake(head, is_server): # Função para verificar se o handshake está correto
    handshake = head[:2] #Pega os dois primeiros bytes do head
    delta_tempo = 0

    combinado = bytes([9, 1])
    if not is_server:
        combinado = bytes([8, 0])
    while delta_tempo <= 5:
        tempo_atual = time.time()
        if handshake == combinado: 
            print('Handshake realizado com sucesso')
            return True
        delta_tempo = atualiza_tempo(tempo_atual)
    return False


def verifica_ordem(recebido, numero_pacote_atual): # Função usada pelo server para verificar se o pacote está na ordem correta
    head = recebido[:10]
    numero_pacote = head[4] # 5º byte do head = número do pacote
    if numero_pacote == numero_pacote_atual:
        print('Pacote recebido na ordem correta')
        return True
    else:
        print('Pacote recebido fora de ordem')
        return False

def monta_payload(info):
    tamanho = len(info)
    pacotes = ceil(tamanho/50) # 50 é o tamanho máximo do payload
    payloads = []
    for i in range(pacotes):
        if i == pacotes-1:
            payload = info[i*50:tamanho]
            print(f'tamanho do último payload:{len(payload)}')
        else:
            payload = info[i*50:(i+1)*50]
            print(f'tamanho dos payloads intermediários:{len(payload)}')
        payloads.append(payload)
    return payloads

def junta_payloads(lista_payloads, tamanho_info, numero_pacotes): # Função para juntar os payloads em um único array e verificar se o número está correto
    info_total = b''
    for payload in lista_payloads:
        info_total += payload
    
    if numero_pacotes == tamanho_info:
        return True
    else:
        return False

def trata_head(head):
    tamanho_payload = head[2]
    numero_pacote = head[3]
    numero_total_pacotes = head[4]

    return tamanho_payload, numero_pacote, numero_total_pacotes

def monta_head(h0, h1, h2, h3, h4, h5, h6, h7):
    '''
Parametros:
    h0(byte): Tipo de mensagem (dados, comando etc.).
    h1(byte): Se for tipo1: número do servidor. Qualquer outro tipo: livre
    h2(byte): Livre.
    h3(bytes): Número total de pacotes do arquivo.
    h4(byte): Número do pacote
    h5(byte): Se a mensagem for do tipo HandShake, representa o id do arquivo,
    se for do tipo de dados: representa o tamanho do payload.
    h6(byte): pacote solicitado para recomeço quando a erro no envio.
    h7(byte): último pacote recebido com sucesso. (1 se foi sucesso e 0 se não)
    h8(byte): CRC. (Em branco)
    h9(byte): CRC. (Em branco)
'''
    header = bytes([h0, h1, h2, h3, h4, h5, h6, h7, 0, 0])
    return header

def log_write(arquivo:str, operacao:str, tipo:int, tamanho:int, pacote_enviado:int=None, total_pacotes:int=None):
    '''
    Função para escrever os logs em um arquivo txt.

    Parâmetros:
        arquivo: Nome do arquivo em que o log será escrito.
        op : String indicando a operação que está sendo feita (Envio, recebimento ou reenvio)
        tipo : Número do tipo do pacote.
        tamanho_bytes : Número do tamanho do payload da mensagem.
        pacote_enviado : Número do pacote (é incrementado durante a transmissão).
        total_pacotes : Número total de pacotes que serão enviados na transmissão que está sendo realizada.
    '''
    if not total_pacotes:
        total_pacotes = ''
    if not pacote_enviado:
        pacote_enviado = ''
    
    with open(f'logs/{arquivo}.txt', 'a') as f:
        conteudo = f'{datetime.now()} /{operacao}/Tipo:{tipo}/Tamanho:{tamanho}/Nºpacote:{pacote_enviado}/TotalPacotes:{total_pacotes} \n'
        f.write(conteudo)

