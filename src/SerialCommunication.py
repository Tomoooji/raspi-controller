import serial
import json
import os.path as path
import serial.tools.list_ports

class SerialCommunicater:
    def __init__(self,config_json, print_log = False):
        self.send_message = ""
        #self.recieve_message = ""
        self.print_log = print_log
        with open(path.join("config",config_json), "r") as config:
            self.serial_info = json.load(config)
        self.serial = serial.Serial()
        
        if "port" in self.serial_info:
            self.serial.port = self.serial_info["port"]
            # raspi用に/dev/ttyS0を足さないといけない? if /dev/ttyAMA0 in device
        else:
            device = [port.device for port in serial.tools.list_ports.comports() if port.serial_number == self.serial_info.get("seiralnumber","")]
            if len(device):
                self.serial.port = device[0]
            else:
                ...    
        
        self.serial.baudrate = self.serial_info["baudrate"]
        if "timeout" in self.serial_info:
            self.serial.timeout = self.serial_info["timeout"]
            
    def begin(self):
        try:
            self.serial.open()
        except serial.SerialException as e:
            print(f"error:{e}")
    
    def reseive(self):
        self.recieve_message = self.serial.readline().decode('utf-8').strip()
        if self.print_log: print(self.recieve_message)
    
    def send(self):
        self.serial.write(self.send_message.encode('utf-8'))
        if self.print_log: print(self.send_message)