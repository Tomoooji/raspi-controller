#pragma once
#include <Arduino.h>

template <typename T = int>
class Accelarator{
private:
  const T _accel;
  const T _decel;
  T _target;
public:
  Accelarator(const T accel, const T decel):_accel(accel), _decel(decel){}
  Accelarator(const T accel):Accelarator(accel, accel){}
  T apply(T current, T target){
    if(target<current+this->_accel && target>current-this->_decel){
      return target;
    }
    else if(target>current){
      return current+this->_accel;
    }
    else{
      return current-this->_decel;
    }
  }
  T apply(T current){return this->apply(current, this->_target);}
  void set_target(T target){this->_target = target;}
};

