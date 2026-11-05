#include <Arduino.h>
#include <SPI.h>

#define PIN_CS 5

SPISettings reglages(1000000, MSBFIRST, SPI_MODE3);

void ecrireRegistre(uint8_t adresse, uint8_t valeur) {
  SPI.beginTransaction(reglages);
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(adresse);
  SPI.transfer(valeur);
  digitalWrite(PIN_CS, HIGH);
  SPI.endTransaction();
}

uint8_t lireRegistre(uint8_t adresse) {
  SPI.beginTransaction(reglages);
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(0x80 | adresse);
  uint8_t valeur = SPI.transfer(0x00);
  digitalWrite(PIN_CS, HIGH);
  SPI.endTransaction();
  return valeur;
}

void lireXYZ(int16_t &x, int16_t &y, int16_t &z) {
  uint8_t b[6];
  SPI.beginTransaction(reglages);
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(0x80 | 0x40 | 0x32);
  for (int i = 0; i < 6; i++) b[i] = SPI.transfer(0x00);
  digitalWrite(PIN_CS, HIGH);
  SPI.endTransaction();
  x = (int16_t)(b[1] << 8 | b[0]);
  y = (int16_t)(b[3] << 8 | b[2]);
  z = (int16_t)(b[5] << 8 | b[4]);
}

const int N = 1000;
unsigned long t[N];

void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(PIN_CS, OUTPUT);
  digitalWrite(PIN_CS, HIGH);
  SPI.begin(18, 19, 23, PIN_CS); 

  Serial.print("DEVID=0x");     Serial.println(lireRegistre(0x00), HEX);
  ecrireRegistre(0x31, 0x08);
  ecrireRegistre(0x2D, 0x08);
  Serial.print("POWER_CTL=0x"); Serial.println(lireRegistre(0x2D), HEX);

  ecrireRegistre(0x2C, 0x0F); // Le BWRATE est de 3200Hz
}

void loop() {
  int16_t x, y, z;
  for (int i = 0; i < N; i++) {
    lireXYZ(x, y, z);
    t[i]= micros();
  }
  
  unsigned long somme = 0;
  unsigned long min = 1000000;
  unsigned long max = 0;
  for (int i = 1; i < N; i++) {
    unsigned long ecart = t[i] - t[i - 1];
    somme += ecart;
    if (ecart < min) min = ecart;
    if (ecart > max) max = ecart;
  }

  Serial.print("min="); Serial.print(min);
  Serial.print(" max="); Serial.print(max);
  Serial.print(" moy="); Serial.println(somme / (N - 1));

  delay(3000);
}