#include <Arduino.h>

int pinServer = 7; 
float baudrate = 9600;
int msg;


void setup() {
  pinMode(pinServer, INPUT);
  Serial.begin(baudrate);
}

float timeSkipper(float skipTime = 1, float baudrate = 9600, float t_0 = 0) {
  double clock = 1 / (21*pow(10,6)); // f = 21MHz, T = 1 / f
  double T = 1 / baudrate; // tempo entre clocks
  int n_clocks = floor(T / clock) + 1;
  for (int i = 0; i < int(n_clocks * skipTime); i++){
    asm("NOP"); // Espera 
  }
}

void loop() {
  if (digitalRead(pinServer)== 0){
    int q_1s = 0;
    timeSkipper(1.5);
    for (int i = 0; i < 8; i ++){
      int bitAtual = digitalRead(pinServer); // lê o bit atual
      timeSkipper(); // Deve ser chamado após a leitura de 1 bit
      if (bitAtual == 1){
        q_1s++; // Conta número de bits
      }
      msg |= (bitAtual << i); // Adiciona o bit atual na mensagem
    }
    int bitParidade = digitalRead(pinServer); // lê o bit de paridade
    int bitParidade_msg = (q_1s % 2) // Cálculo do bit de paridade da mensagem 
    if (bitParidade == bitParidade_msg) {
      Serial.print("Dados Recebidos: ");
      Serial.println(msg, HEX);
      Serial.println("Bit de paridade está correto!");
    } else{
      Serial.println("ERRO, bit de paridade está incorreto");
    }
    delay(1000);
  }
}
