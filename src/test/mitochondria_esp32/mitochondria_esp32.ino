#include "SimpleMecanumDriver.h"
#include <AccelMotorDriver.h>

namespace Pins {
constexpr uint8_t dc_omuni4_FL[] = { 19, 21 };
constexpr uint8_t dc_omuni4_FR[] = { 27, 26 };
constexpr uint8_t dc_omuni4_BR[] = { 33, 25 };
constexpr uint8_t dc_omuni4_BL[] = { 16, 17 };
constexpr uint8_t led_builtin = 2;
}  // namespace Pins

namespace Gains {
constexpr int omuni4_accel = 2;
constexpr float omuni4_speed_ratio[4] = { 1.0f, 1.0f, 1.0f, 1.0f };
}  // namespace Gains

SimpleOmuni4Driver<AccelMotor> Omuni4{
  AccelMotor(Pins::dc_omuni4_FL, Gains::omuni4_accel),
  AccelMotor(Pins::dc_omuni4_FR, Gains::omuni4_accel),
  AccelMotor(Pins::dc_omuni4_BL, Gains::omuni4_accel),
  AccelMotor(Pins::dc_omuni4_BR, Gains::omuni4_accel),
  Gains::omuni4_speed_ratio
};

struct Input {
  int32_t angle;
  int32_t magnitued;
  int32_t turn;
} __attribute__((__packed__));

Input data;

void setup() {
  Serial.begin(115200);
  pinMode(Pins::led_builtin, OUTPUT);
  Omuni4.begin();
}

void loop() {
  if(Serial.available() >= sizeof(Input)){
    Serial.readBytes(reinterpret_cast<uint8_t*>(&data), sizeof(Input));
    while(Serial.available()) Serial.read();
    digitalWrite(Pins::led_builtin, abs(data.turn) > 10);
    Omuni4.setVelocity(
      Vector2D<float>::fromPolar(data.magnitued, data.angle), data.turn
    );
    Serial.write(reinterpret_cast<uint8_t*>(&data), sizeof(Input));
    //Serial.print(data.angle);Serial.print(",");
    //Serial.print(data.magnitued);Serial.print(",");
    //Serial.print(data.turn);Serial.println();
  }else{
  data = Input(0,0,0);
  }
  Omuni4.update();
  delayMicroseconds(100);
}
