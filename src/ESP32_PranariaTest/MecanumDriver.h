// 4輪オムニと中身は一緒
#pragma once
#include <Arduino.h>
#include "AnalogMotorDriver.h"
#include "Accelarator.h"

class Mecanum{
private:
  AnalogMotor motors[4];
  
  enum MOTOR{
    FRONTLEFT,BACKLEFT,BACKRIGHT,FRONTRIGHT
  };

  struct ConfigData_leg{
    bool reversed[4] = {false,false,false,false};
    int max_speed[4] = {};
  } config;

  Accelarator<int> acceler;

public:
  Mecanum():acceler(5){}

  void begin(const uint8_t pin_FL[], const uint8_t pin_BL[], const uint8_t pin_BR[], const uint8_t pin_FR[]){
    this->motors[FRONTLEFT].attach(pin_FL, this->config.max_speed[FRONTLEFT]);
    this->motors[BACKLEFT].attach(pin_BL, this->config.max_speed[BACKLEFT]);
    this->motors[BACKRIGHT].attach(pin_BR, this->config.max_speed[BACKRIGHT]);
    this->motors[FRONTRIGHT].attach(pin_FR, this->config.max_speed[FRONTRIGHT]);
  }

  void update(float direction, int speed_line, int speed_turn){
    this->motors[FRONTLEFT].set_speed(
      this->acceler.apply(
        this->motors[FRONTLEFT].get_speed(),
        (speed_line *cos(0.25*PI +direction) +speed_turn) * (this->config.reversed[FRONTLEFT] ? -1:1)
      )
    );
    this->motors[BACKLEFT].set_speed(
      this->acceler.apply(this->motors[BACKLEFT].get_speed(),
        (speed_line *sin(0.25*PI +direction) +speed_turn) * (this->config.reversed[BACKLEFT] ? -1:1)
      )
    );
    this->motors[BACKRIGHT].set_speed(
      this->acceler.apply(this->motors[BACKRIGHT].get_speed(),
        (speed_line *cos(0.25*PI +direction) -speed_turn) * (this->config.reversed[BACKRIGHT] ? -1:1)
      )
    );
    this->motors[FRONTRIGHT].set_speed(
      this->acceler.apply(this->motors[FRONTRIGHT].get_speed(),
        (speed_line *sin(0.25*PI +direction) -speed_turn) * (this->config.reversed[FRONTRIGHT] ?-1:1)
      )
    );

  }
  
  void move(){
    for(AnalogMotor motor : this->motors){
      motor.move();
    }
  }

};