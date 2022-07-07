from ctypes import alignment
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import platform
import tkinter as tk
from tkinter import messagebox
import threading
import os

if platform.system()=="Linux":
    import gamepad_linux as vgl
    gamepadKeys={
        "1":vgl.uinput.BTN_TL,
        "2":vgl.uinput.BTN_DPAD_UP,
        "3":vgl.uinput.BTN_X,
        "4":vgl.uinput.BTN_A,
        "5":vgl.uinput.BTN_TR,
        "6":vgl.uinput.BTN_DPAD_DOWN,
        "7":vgl.uinput.BTN_Y,
        "8":vgl.uinput.BTN_B,
        "9":vgl.uinput.BTN_THUMBL,
        "0":vgl.uinput.BTN_THUMBR,
    }
    gamepad=vgl.XboxController()
else:
    import vgamepad as vg
    gamepadKeys={
        "1":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        "2":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        "3":vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        "4":vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        "5":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        "6":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        "7":vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        "8":vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        "9":vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        "0":vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    }
    gamepad = vg.VX360Gamepad()




serverPort = 6116

def getIpOfDesktopClient():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip=s.getsockname()[0]
    s.close()
    return ip

if platform.system()=="Linux":
    class GamepadControllerServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            if self.path.startswith("/s/"):
                sensorValues=self.path.replace("/s/","").split("/")

                gamepad.emit(vgl.uinput.ABS_X, int(max(min(float(sensorValues[1])/10*128+128,256),0)))

            elif self.path.startswith("/m/"):
                sensorValues=self.path.replace("/m/","").split("/")
                if(sensorValues[0]=="2"):
                    gamepad.emit(vgl.uinput.ABS_Z,int(sensorValues[1]))
                    gamepad.emit(vgl.uinput.ABS_RZ,0)
                else:
                    gamepad.emit(vgl.uinput.ABS_RZ,int(sensorValues[1]))
                    gamepad.emit(vgl.uinput.ABS_Z,0)

            elif self.path.startswith("/b/"):
                sensorValues=self.path.replace("/b/","").split("/")
                gamepad.emit(gamepadKeys[sensorValues[1]], int(sensorValues[0]))


            elif(self.path.startswith("/connect")):
                self.wfile.write(bytes("OK", "utf-8"))
                try:
                    messagebox.showinfo("Connect", "New Device Connected")
                except NotImplementedError:
                    pass
            else:
                print("Request Bug")
                self.wfile.write(bytes("Request Bug", "utf-8"))
        def log_message(self, format, *args):
            return

else:
    t1=0.0
    class GamepadControllerServer(BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            if self.path.startswith("/s/"):
                global t1
                sensorValues=self.path.replace("/s/","").split("/")
                t2=float(sensorValues[1])
                filteredValue=abs(t2-t1)
                if(filteredValue>2):
                    if(t1-t2<0):
                        t1+=2
                    else:
                        t1-=2
                else:
                    t1=t2


                if (t1>8.5):
                    gamepad.left_joystick_float(x_value_float=1.0, y_value_float=0.0)
                elif(t1<-8.5):
                    gamepad.left_joystick_float(x_value_float=-1.0, y_value_float=0.0)
                else:
                    gamepad.left_joystick_float(x_value_float=t1/10, y_value_float=0.0)



            elif self.path.startswith("/m/"):
                sensorValues=self.path.replace("/m/","").split("/")
                if(sensorValues[0]=="2"):
                    gamepad.left_trigger_float(value_float=int(sensorValues[1])/10)
                    gamepad.right_trigger_float(value_float=0)
                else:
                    gamepad.right_trigger_float(value_float=int(sensorValues[1])/10)
                    gamepad.left_trigger_float(value_float=0)

            elif self.path.startswith("/b/"):
                sensorValues=self.path.replace("/b/","").split("/")

                if(sensorValues[0]=="1"):
                    gamepad.press_button(button=gamepadKeys[sensorValues[1]])
                else:
                    gamepad.release_button(button=gamepadKeys[sensorValues[1]])


            elif(self.path.startswith("/connect")):
                self.wfile.write(bytes("OK", "utf-8"))
                try:
                    messagebox.showinfo("Connect", "New Device Connected")
                except NotImplementedError:
                    pass
            else:
                print("Request Bug")
                self.wfile.write(bytes("Request Bug", "utf-8"))
            gamepad.update()
        def log_message(self, format, *args):
            return


def closeServer():
    webServer.server_close()
    root.destroy()
    os._exit(0)

def runGui(thread_name,IP):
    global root
    root=tk.Tk()
    root.resizable(False,False)
    root.geometry("390x100")
    root.title("Remote Wheel")
    tk.Label(root,text="IP of Desktop Client: "+IP,font=("Serif", 15),justify=tk.CENTER).place(x=10, y=10, width=380)
    tk.Button(root,text="Close Application",font=("Serif", 10),command=closeServer).place(x=20,y=53, width=360)

    root.protocol("WM_DELETE_WINDOW", closeServer)
    root.mainloop()

if __name__ == "__main__":
    IP_OF_DESKTOP_CLIENT=getIpOfDesktopClient()

    guiApp = threading.Thread(target=runGui, args=("guiApp", IP_OF_DESKTOP_CLIENT))
    guiApp.start()

    global webServer

    webServer = HTTPServer((IP_OF_DESKTOP_CLIENT, serverPort), GamepadControllerServer)
    webServer.serve_forever()

    guiApp.join()
    webServer.server_close()
