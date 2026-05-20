#include "SerialController.h"
#include "MecanumDriver.h"

//constexpr uint8_t FLpin[] = {27,14};
//constexpr uint8_t BLpin[] = {25,26};
//constexpr uint8_t BRpin[] = {32,33};
//constexpr uint8_t FRpin[] = {17,16};
//int leg_max[] = {170,170,170,170};
//Mecanum leg;

Controller_Serial ctr(Serial,115200);

void setup(){
  //*leg.get_config().max_speed = *leg_max;

  if(!ctr.begin()) return;
  //leg.begin(FLpin,BLpin,BRpin,FRpin);
}

void loop(){
  ctr.update();
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
