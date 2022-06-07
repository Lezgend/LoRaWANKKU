"""
Warayut Poomiwatracanont
Date : 29/5/2022
Run on ESP32 with MAXIIOT DL7612-AS923-TH
"""
from machine import UART
import time, sys

class LoRaWAN:
    def __init__(self, uart_id, dclass, ismband):
        self.uart_id = uart_id
        self.dclass = dclass
        self.ismband = ismband
       
        # if UART1 can not work properly, please use UART2
        self.uart = UART(uart_id, baudrate=115200, bits=8, parity=None, stop=1, timeout=1000)

        if dclass is "A" or "a":
            self.dclass = "AT+CLASS=A"
        elif dclass is "B" or "b":
            self.dclass = "AT+CLASS=B"
        elif dclass is "C" or "c":
            self.dclass = "AT+CLASS=C"
        else:
            self.dclass = "AT+CLASS=C"

        if ismband is 6:
            self.ismband = "AT+ISMBAND=6"
        elif ismband is 2:
            self.ismband = "AT+ISMBAND=2"
        else:
            self.ismband = "AT+ISMBAND=6"

    def sendATcommand(self, ATcommand):
        rstr = ""
        print("Command: {0}\r\n".format(ATcommand))
        self.uart.write("{0}\r\n".format(ATcommand))
        time.sleep(1)
        rstr = self.uart.read().decode("utf-8")
        print(rstr)
        return rstr

    def restart(self):
        # Restart MAXIIOT DL7612-AS923-TH
        self.sendATcommand("AT+NRB")
        time.sleep(5)
        print("You're module restarted.")

        # Check LoRaWAN Network Server Connection (AT+CGATT)
        rstr = ""
        print("Check LoRaWAN Network Server Connection (If 1 mean module has connected)")
        while rstr != "+CGATT:1":
            rstr = self.sendATcommand("AT+CGATT")
            time.sleep(20.0)
            print(rstr)
            if rstr.startswith("+CGATT:1"):
                print("++++OTAA OK+++++")
                print("Join Success")
                break
            elif rstr.startswith("+CGATT:2"):
                print("Please check your device!")
                break
            else:
                break
            
    def checkConnect(self):
        # Check the Module Connection (AT)
        print("Check the Module Connection")
        self.sendATcommand("AT")

        # Check LoRaWAN Network Server Connection (AT+CGATT)
        print("Check LoRaWAN Network Server Connection (If 1 mean module has connected)")
        self.sendATcommand("AT+CGATT")

    def showInfo(self):
        # Show the module infomationtion (AT+INFO)
        print("Show the module infomationtion")
        self.sendATcommand("AT+INFO")

    def showConfig(self):
        # Show the module configuration (AT+NCONFIG)
        self.sendATcommand("AT+NCONFIG")

    def showChannel(self):
        # Show the module channel frequency (AT+CHSET)
        self.sendATcommand("AT+CHSET")

    def configClass(self):
        
        # Check the connection (AT)
        self.sendATcommand("AT")

        # Open debug mode
        print("Starting Config Module!")
        self.sendATcommand("AT+DEBUG=1")

        # Choose authentication with OTAA(1)
        # or could use authentication with ABP(0)
        self.sendATcommand("AT+ACTIVATE=1")

        # Choose sensor node Class
        self.sendATcommand("{0}".format(self.dclass))

        # Choose ISMBAND AS1 or AS2
        self.sendATcommand("{0}".format(self.ismband))

        # Save the config
        self.sendATcommand("AT+SAVE")
        print("Config Module Successfully!")

    # Show DEVEUI and APPKEY for binding in Chirpstack
    def showKey(self):
        self.uart.write("AT+DEVEUI\r\n")
        time.sleep(0.5)
        DEVEUI = self.uart.read().decode("utf-8").strip("+DevEUI:")
        print("DevEUI :",DEVEUI)
        time.sleep(0.05)

        self.uart.write("AT+APPKEY\r\n")
        time.sleep(0.5)
        APPKEY = self.uart.read().decode("utf-8").strip("+APPKEY:")
        print("AppKey :",APPKEY)
        time.sleep(0.05)

        return DEVEUI,APPKEY

    def sendHello(self):
        # Send 5 characters from string "HELLO"
        try:
            while True:
                print("Test sending HELLO")
                self.sendATcommand("AT+NCMGS=5,HELLO")
                
                print("Test sending hex")
                self.sendATcommand("AT+NMGS=5,AA112233BB")
                
                print("uses CTRL-C to stop sending")
        except KeyboardInterrupt:
            print("Interrupted!")
            pass

    def doChoice(self):
        list = ["Restart Module", "Check Connection", "Show Module Infomation",
                "Show Module Configuration", "Show Module Channel Frequency",
                "Auto Config Module", "Show DevEUI and AppKey", "Send HELLO", "Quit"]
        #print(list)

        # Do Choice List
        for i, x in enumerate(list):
            print("{0}. {1}\n".format(i, repr(x).replace("'","")))
        
        i = int(input("Please select your choice: "))
        try:
            # Check if input is integer
            choice = int(i)
        # if not a integer
        except ValueError:
            print("You did not enter a valid integer")
            print("************************************\n")
            try:
                self.doChoice()
            except Exception:
                sys.exit(0)
        # Select the Choice
        if choice in range(len(list)):
            print("Roger That!\n")
            if choice == 0:
                self.restart()
            elif choice == 1:
                self.checkConnect()
            elif choice == 2:
                self.showInfo()
            elif choice == 3:
                self.showConfig()
            elif choice == 4:
                self.showChannel()
            elif choice == 5:
                self.configClass()
            elif choice == 6:
                self.showKey()
            elif choice == 7:
                self.sendHello()
            elif choice == 8:
                sys.exit(0)
        # if input out of range
        else:
            print("The value is out of range")
            print("************************************\n")
            try:
                self.doChoice()
            except Exception as err:
                raise SystemExit(err)
            
if __name__ == "__main__":

    _uart = int(input("Which UART ID do you using: "))
    _dclass = input("Which class do you prefer? A, B, C: ")                
    _ismband = int(input("Which ISMBAND you want to use AS1(6) and AS2(2): "))

                
    LoRa = LoRaWAN(uart_id=_uart, dclass=_dclass, ismband=_ismband)
    
    try:
        while True:
            LoRa.doChoice() 
            print("uses CTRL-C to stop sending\n")
    except KeyboardInterrupt:
        print("Interrupted!")
        pass
    
    #LoRa.checkConnect()
    #LoRa.restart()
    #LoRa.showChannel()
    #LoRa.configClass()
    #LoRa.showConfig()
    #LoRa.showKey()

