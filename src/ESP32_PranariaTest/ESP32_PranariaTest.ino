#include "SerialController.h"
#include "MecanumDriver.h"

//constexpr uint8_t FLpin[2] = {1,2};
//constexpr uint8_t BLpin[2] = {1,2};
//constexpr uint8_t BRpin[2] = {1,2};
//constexpr uint8_t FRpin[2] = {1,2};
//Mecanum leg;

Controller_Serial ctr(Serial,115200);

void setup(){
  if(!ctr.begin()) return;
  //leg.begin(FLpin,BLpin,BRpin,FRpin);
}

void loop(){
  ctr.update()
  /*if(ctr.update()){
    leg.update(
        radians(ctr.get_input().angle),
        ctr.get_input().dist,
        ctr.get_input().turn
    );
  }
  else{
    leg.update(0, 0, 0);
  }
  leg.move();*/
}
