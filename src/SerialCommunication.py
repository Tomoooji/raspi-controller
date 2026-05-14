import os
import json
import struct
import serial
import serial.tools.list_ports

class SerialCommunicater:
    def __init__(self,config_json, print_log = False):
        self.print_log = print_log #"raspi-controller","src",
        
        with open(os.path.join(os.getcwd(),"raspi-controller","src","config", config_json), "r") as config:
            self.serial_info = json.load(config)
        self.serial = serial.Serial()
        
        if "port" in self.serial_info:
            self.serial.port = self.serial_info["port"]
        else:
            device = [port.device for port in serial.tools.list_ports.comports() if port.serial_number == self.serial_info.get("seiralnumber","")]
            if len(device):
                self.serial.port = device[0]
            else:
                ...
        self.serial.baudrate = self.serial_info["baudrate"]
        if "timeout" in self.serial_info:
            self.serial.timeout = self.serial_info["timeout"]
            
        #self.send_message = ""
        #self.receive_message = ""
        
        if "send_data" in self.serial_info:
            self.serial_info["send_format"] = "<"+"".join(self.serial_info["send_datatype"].values())
        
        if "receive_data" in self.serial_info:
            self.serial_info["receive_format"] = "<"+"".join(self.serial_info["receive_datatype"].values())
        
    def begin(self):
        try:
            self.serial.open()
        except serial.SerialException as e:
            print(f"error:{e}")
    
    #def receive(self):
        #self.receive_message = self.serial.readline().decode('utf-8').strip()
        #if self.print_log: print(self.receive_message)
    
    def receive_dict(self):
        if "receive_data" in self.serial_info:
            data_bytes = self.serial.read(struct.calcsize(self.serial_info["receive_format"]))
            print("receive",data_bytes)
            self.serial_info["receive_data"] = dict(zip(self.serial_info["receive_data"].keys(),
                struct.unpack(self.serial_info["receive_format"],data_bytes)
            ))
        else:
            return False

    def receive_dict_(self):
        if not "receive_data" in self.serial_info:return False
        if self.serial.in_waiting >= 14:
            if self.serial.read(2) == b'\xAA\xBB':
                data_bytes = self.serial.read(struct.calcsize(self.serial_info["receive_format"]))
                print("receive",data_bytes)
                self.serial_info["receive_data"] = dict(zip(self.serial_info["receive_data"].keys(),
                    struct.unpack(self.serial_info["receive_format"],data_bytes)
                ))
            else:
                self.serial.read(1)
    
    #def send(self, message = None):
        #if message: self.send_message = message
        #self.serial.write(self.send_message.encode('utf-8'))
        #if self.print_log: print(self.send_message)
    
    def send_dict(self):
        if "send_data" in self.serial_info:
            self.serial.write(data:=struct.pack(
                    self.serial_info["send_format"],
                    *list(map(int,self.serial_info["send_data"].values()))
            ))
            #print("send",data)
        else:
            return False
        
"""
import pygame,sys
def main():
    pygame.init()
    pygame.display.set_mode((200,200))
    ser = SerialCommunicater("ESP32.json",True)
    ser.begin()
    while ser.serial.is_open:
        #ser.send()
        #ser.receive()
        
        for event in pygame.event.get():
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_RETURN:
                    #ser.send("test")
                #if event.key == pygame.K_SPACE:
                    #ser.send("quit")
                    
            if event.type == pygame.QUIT:
                ser.serial.close()
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main()
"""