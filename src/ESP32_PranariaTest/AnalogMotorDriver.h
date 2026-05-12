#pragma once

inline int sign(auto x){
  return (x>0) - (x<0);
}

class AnalogMotor_Base{
 protected:
  const uint8_t* _pins = nullptr;
  int max;
  int _speed=0;
 public:
  AnalogMotor_Base(const int max=255):max(max){}
  virtual void attach(const uint8_t pins[], const int max=0)=0;
  virtual void move() = 0;
  void set_speed(int speed){
    this->_speed = constrain(abs(speed), 0, this->max) * sign(speed);
  }
  void move(int speed){
    this->set_speed(speed);
    this->move();
  }
  const int get_speed(){
    return this->_speed;
  }
  const uint8_t get_pin(uint8_t idx){
    return this->_pins[idx];
  }
};

#if defined(ARDUINO_ARCH_AVR)

class AnalogMotor_Arduino: public AnalogMotor_Base{
  public:
  using AnalogMotor_Base::AnalogMotor_Base;
  void attach(const uint8_t pins[], const int max_speed=0)override{
    this->_pins = pins;
    if(max_speed>0)this->max=max_speed;
    pinMode(this->_pins[0], OUTPUT);
    pinMode(this->_pins[1], OUTPUT);
  }
  void move()override{
    analogWrite(this->_pins[0], this->_speed>0?  this->_speed: 0);
    analogWrite(this->_pins[1], this->_speed<0? -this->_speed: 0);
  }
};
using AnalogMotor = AnalogMotor_Arduino;

class AnalogMotor_3pin_Arduino: public AnalogMotor_Base{
  public:
  using AnalogMotor_Base::AnalogMotor_Base;
  void attach(const uint8_t pins[],const int max_speed=0)override{
    this->_pins = pins;
    if(max_speed>0)this->max=max_speed;
    pinMode(this->_pins[0], OUTPUT);
    pinMode(this->_pins[1], OUTPUT);
    pinMode(this->_pins[2], OUTPUT);
  }
  void move()override{
    digitalWrite(this->_pins[0], this->_speed>0);
    digitalWrite(this->_pins[1], this->_speed<0);
    analogWrite(this->_pins[2], abs(this->_speed));
  }
};
using AnalogMotor_3pin = AnalogMotor_3pin_Arduino;

#elif defined(ESP32)

class AnalogMotor_ESP32:public AnalogMotor_Base{
  public:
  using AnalogMotor_Base::AnalogMotor_Base;
  void attach(const uint8_t pins[],const int max_speed=0)override{
    this->_pins = pins;
    if(max_speed>0)this->max=max_speed;
    ledcAttach(this->_pins[0], 12800, 8);
    ledcAttach(this->_pins[1], 12800, 8);
  }
  void move()override{
    ledcWrite(this->_pins[0], this->_speed>0?  this->_speed: 0);
    ledcWrite(this->_pins[1], this->_speed<0? -this->_speed: 0);
  }
};
using AnalogMotor = AnalogMotor_ESP32;

class AnalogMotor_3pin_ESP32: public AnalogMotor_Base{
  public:
  using AnalogMotor_Base::AnalogMotor_Base;
  void attach(const uint8_t pins[],const int max_speed=0)override{
    this->_pins = pins;
    if(max_speed>0)this->max=max_speed;
    pinMode(this->_pins[0], OUTPUT);
    pinMode(this->_pins[1], OUTPUT);
    ledcAttach(this->_pins[2], 12800, 8);
  }
  void move()override{
    digitalWrite(this->_pins[0], this->_speed>0);
    digitalWrite(this->_pins[1], this->_speed<0);
    ledcWrite(this->_pins[2], abs(this->_speed));
  }
};
using AnalogMotor_3pin = AnalogMotor_3pin_ESP32;

#endif
