#pragma once
#include <Arduino.h>

#pragma pack(push,1)
struct ReceiveData{
    uint8_t header1 = 0xAA;
    uint8_t header2 = 0xBB;
    uint32_t angle;//degree
    uint32_t dist;
    uint32_t turn;
};
#pragma pack(pop)

class Controller_Serial{
private:
  HardwareSerial& SER;
  struct ConfigData_serial{
    int baudrate;
  } config;
  ReceiveData input;

public:
  Controller_Serial(HardwareSerial& serial, int baudrate):SER(serial),config{baudrate},input{}{}
  bool begin(){
    this->SER.begin(this->config.baudrate);
  }
  bool begin(const uint8_t Rx, const uint8_t Tx){
    this->SER.begin(this->config.baudrate, SERIAL_8N1, Rx, Tx); //8ビット、パリティなし、ストップビット1（8N1）
  }
  bool update(){
    if(this->SER.available()){
      this->SER.readBytes((uint8_t*)&this->input, sizeof(ReceiveData));
      this->SER.write((uint8_t*)&this->input, sizeof(ReceiveData)); //feedback echo
      return true;
    }
    else{
      return false;
    }
  }
  const ReceiveData& get_input(){return this->input;}
  ConfigData_serial& get_config(){return this->config;}
};