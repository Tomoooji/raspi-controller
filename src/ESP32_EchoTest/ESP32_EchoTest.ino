#define BAUDRATE 115200

constexpr int data_num = 20;
int inputData[data_num];

void setup(){
  Serial.begin(BAUDRATE);
}

void loop(){
  readInput();
  //writeArray();
}

void readInput(){
  while(Serial.available()){
    String pair = Serial.readStringUntil(',');
    //Serial.print(pair);
    int siteColon = pair.indexOf(':');
    //Serial.println(siteColon);
    if(siteColon>0){
      int index = pair.substring(0,siteColon).toInt();
      int value = pair.substring(siteColon+1).toInt();
      if(index>=0 && index<data_num){
        inputData[index] = value;
        writeArray();
        if(index == data_num-1){
          return;
        }
      }
    }
  }
}

void writeArray(){
  for(int i=0; i<data_num; i++){
    //Serial.print(",");
    Serial.print(i);
    Serial.print(":");
    Serial.print(inputData[i]);
  }
  Serial.println();
}
