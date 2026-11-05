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
}

void loop() {
  int16_t x, y, z;
  lireXYZ(x, y, z);
  Serial.print("X=");    Serial.print(x * 0.0039, 3);
  Serial.print("  Y=");  Serial.print(y * 0.0039, 3);
  Serial.print("  Z=");  Serial.println(z * 0.0039, 3);
  delay(500);
}