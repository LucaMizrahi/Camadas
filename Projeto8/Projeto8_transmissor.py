import soundfile as sf
from funcoes_LPF import filtro
from suaBibSignal import *

signal_plot = signalMeu()

# leitura do arquivo de áudio
signal_original = sf.read('soms/among.wav')[0]
taxa_de_amostragem = 48000
signal = signal_original[:, 0]
signal_original_1canal = signal
tempo_antes_filtro = np.linspace(0, 3, len(signal))

# filtragem do sinal modulado
signal = filtro(signal, taxa_de_amostragem, 4000)
tempo_pos_filtro = np.linspace(0, 3, len(signal))


# criação da onda portadora
frequencia_portadora = 14000  # em Hz
tempo = np.linspace(0, 3, len(signal))
portadora = np.sin(2*np.pi*frequencia_portadora*tempo)

# sinal modulado em AM
indice_modulacao = 0
sinal_modulado = (indice_modulacao+signal) * portadora
# reprodução do sinal filtrado
sd.play(sinal_modulado, taxa_de_amostragem)
sd.wait()
sf.write('soms/teste.wav', sinal_modulado, taxa_de_amostragem)

# Sinal de áudio original normalizado – domínio do tempo
plt.figure()
plt.plot(tempo_antes_filtro, signal_original_1canal)
plt.title('Sinal de áudio original normalizado – domínio do tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

#  Sinal de áudio filtrado – domínio do tempo
plt.figure()
plt.plot(tempo_pos_filtro, signal)
plt.title('Sinal de áudio filtrado – domínio do tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

# Sinal de áudio filtrado – domínio da frequência (Fourier)
plt.title('Sinal de áudio filtrado – domínio da frequência (Fourier)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

# Sinal de áudio modulado em AM – domínio do tempo
plt.figure()
plt.plot(tempo, sinal_modulado)
plt.title('Sinal de áudio modulado em AM – domínio do tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

# Sinal de áudio modulado em AM – domínio da frequência (Fourier)
signal_plot.plotFFT(sinal_modulado, taxa_de_amostragem)
plt.title('Sinal de áudio modulado em AM – domínio da frequência (Fourier)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()
