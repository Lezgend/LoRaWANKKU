import urequests, ujson
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

# Get JWT Token.
def get_jwt_token(username, password):
        
    post_data = ujson.dumps({"email": username, "password": password})
    print(post_data)

    url = "http://ex-lorawan.kku.ac.th:8080/api/internal/login"
    headers = {'content-type' : 'application/json'}
    
    send = urequests.post(url, headers = headers, data=post_data).json()
    #print(send['jwt'])
    print(send)

if __name__ == "__main__":
    do_connect()
    get_jwt_token("USERNAME", "PASSWORD")
