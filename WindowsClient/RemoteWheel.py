from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

serverPort = 6116

def getIpOfDesktopClient():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip=s.getsockname()[0]
    s.close()
    return ip

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if self.path.startswith("/s/"):
            sensorValues=self.path.replace("/s/","").split("/")
            print(sensorValues)
        elif self.path.startswith("/b/"):
            sensorValues=self.path.replace("/b/","").split("/")
            print(sensorValues)
        elif(self.path.startswith("/connect")):
            self.wfile.write(bytes("OK", "utf-8")) 
        else:
            print("Request Bug")
            self.wfile.write(bytes("Request Bug", "utf-8"))

if __name__ == "__main__":
    IP_OF_DESKTOP_CLIENT=getIpOfDesktopClient()
    webServer = HTTPServer((IP_OF_DESKTOP_CLIENT, serverPort), MyServer)
    print("IP Adress of Desktop Client: "+IP_OF_DESKTOP_CLIENT)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()