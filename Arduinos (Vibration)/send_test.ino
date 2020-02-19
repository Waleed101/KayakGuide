#include <SPI.h>
#include <NRFLite.h>

NRFLite _radio;
uint8_t _data;

void setup() {
  _radio.init(0, 9, 10);
}

void loop() {
  _data++;
  _radio.send(1, &_data, sizeof(_data));
  delay(1000);
}
