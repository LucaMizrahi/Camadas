import numpy as np
from math import ceil
import time
from datetime import datetime 

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
    head = bytes([h0, h1, h2, h3, h4, h5, h6, h7, 0, 0])
    return head

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
    
    with open(f'Projeto4/logs/{arquivo}', 'a') as f:
        conteudo = f'{datetime.now()} /{operacao}/Tipo:{tipo}/Tamanho:{tamanho}/Num_pacote:{pacote_enviado}/TotalPacotes:{total_pacotes} \n'
        f.write(conteudo)

