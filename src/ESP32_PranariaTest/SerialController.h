#pragma once
#include <Arduino.h>

#pragma pack(push,1)
struct ReceiveData{
    uint32_t angle;//degree
    uint32_t dist;
    int32_t turn;
};
#pragma pack(pop)

class Controller_Serial{
private:
  HardwareSerial& Ser;
  struct ConfigData_serial{
    int baudrate;
  } config;
  ReceiveData input;

public:
  Controller_Serial(HardwareSerial& serial, int baudrate):SER(serial),config{baudrate},input{}{}
  bool begin(){
    this->SER.begin(this->config.baodrate);
  }
  bool begin(const uint8_t Rx, const uint8_t Tx){
    this->SER.begin(this->config.baodrate, SERIAL_8N1, Rx, Yx); //8ビット、パリティなし、ストップビット1（8N1）
  }
  bool update(){
    if(this->SER.available()){
      this->SER.readBytes((uint8_t*)&this->input, sizeof(receive_data));
      this->SER.write((uint8_t*)&this->input, sizeof(receive_data)) //feedback echo
      return true;
    }
    else{
      return false;
    }
  }
  const ReceiveData& get_input(){return this->input;}
  ConfigData_serial& get_config(){return this->config;}
};