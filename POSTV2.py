"""
Warayut Poomiwatracanont
Date : 7/6ุุ/2022
Run on ESP32 with MAXIIOT DL7612-AS923-TH
"""
import urequests, ujson
import sys
# Let ESP32 connect to the internet for download some library.
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('dragino-1ee88c', 'dragino+dragino')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# When you've connected to internet, then install micropython libraries named urequests and ujson.
#>>>import upip
#>>>upip.install('urequests')
#>>>upip.install('ujson')

class DOWNLINK():
    def __init__(self, username, password, DevEUI, data):
        self.username = username
        self.password = password
        self.DevEUI = DevEUI
        
        if data is "":
            self.data = "AQID"
        else:
            self.data = data
        
    # Get JWT Token.
    def get_jwt_token(self):    
        headers = {'Content-Type':'application/json'}
        post_data = ujson.dumps({"email": self.username, "password": self.password})
        url = "http://ex-lorawan.kku.ac.th:8080/api/internal/login"
    
        send = urequests.post(url, headers=headers, data = post_data).json()
        print("\n",send['jwt'])

    # POST Downlink
    def post_downlink(self):
        
        _jwt = str(input("Enter JWT Token: "))

        data = {"deviceQueueItem": {"data": "AQID", "fPort": 2}}
        
        data["deviceQueueItem"]["data"] = self.data
        #data["deviceQueueItem"]["fPort"] = 2

        post_data = ujson.dumps(data)
        url = "http://ex-lorawan.kku.ac.th:8080/api/devices/{0}/queue".format(self.DevEUI)
        headers = {'Content-Type':'application/json', 'Grpc-Metadata-Authorization' : ''}
        
        headers["Grpc-Metadata-Authorization"] = 'Bearer ' + _jwt

        send = urequests.post(url, headers=headers, data = post_data).json()
        print("\n",send)

    def doChoice(self):
        list = ["Get JWT TOKEN", "Send DOWNLINK", "Quit"]
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
                self.get_jwt_token()
            elif choice == 1:
                self.post_downlink()
            elif choice == 2:
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

    do_connect()

    _username = str(input("Enter ChirpStack Username: "))
    _password = str(input("Enter ChirpStack Password: "))
    _DevEUI = str(input("Enter your DevEUI for DOWNLINK: "))
    _data = str(input("What data you wanna send(BASE64 TO HEX): "))
    print("\n")
    
    # USE https://cryptii.com/pipes/base64-to-hex FOR CHECK THE FORMAT
    
    DL = DOWNLINK(username=_username, password=_password, DevEUI=_DevEUI, data=_data)
    
    try:
        while True:
            DL.doChoice()
            print("\nuses CTRL-C to stop sending\n")
    except KeyboardInterrupt:
        print("Interrupted!")
        pass
