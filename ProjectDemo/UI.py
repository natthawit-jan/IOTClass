import warnings
import serial
import serial.tools.list_ports
import time
import tkinter as tk
import tkinter

# matching sketch at
# https://create.arduino.cc/editor/piti118/d62e2b1e-f304-48b8-99cd-0d57f0375e1c/preview

def connect_arduino(baudrate=9600): # a more civilized way to connect to arduino
    def is_arduino(p):

        # need more comprehensive test
        return p.manufacturer is not None and 'arduino' in p.manufacturer.lower()

    ports = serial.tools.list_ports.comports()
    arduino_ports = [p for p in ports if is_arduino(p)]


    def port2str(p):
        return "%s - %s (%s)" % (p.device, p.description, p.manufacturer)

    if not arduino_ports:
        portlist = "\n".join([port2str(p) for p in ports])
        raise IOError("No Arduino found\n" + portlist)

    if len(arduino_ports) > 1:
        portlist = "\n".join([port2str(p) for p in ports])
        warnings.warn('Multiple Arduinos found - using the first\n' + portlist)

    selected_port = arduino_ports[0]
    print("Using %s" % port2str(selected_port))
    print(selected_port.device)
    ser = serial.Serial(selected_port.device, baudrate)
    time.sleep(2)  # this is important it takes time to handshake
    return ser

class Serial:
    def __init__(self, ser):

        self.ser = ser





    def read(self):
        print(self.ser.readline())




    def send_rec(self, msg):
        # self.ser.write((msg + "\n").encode())
        # return self.ser.read_until(b"\n", 255)
        return self.ser.write((msg + "\n").encode())

    def scanTextBeforeSend(self, msg):
        self.send_rec(msg[0]);
        # self.read();
        print(msg[0])
        self.send_rec(msg[1]);
        # self.read();
        print(msg[1])
        # self.read()


    



class LoginPage:
    def __init__(self, parent, arduino):
        self.arduino = arduino
        self.parent = parent
        self.parent.title("Hey")
        self.parent.geometry("500x500")
        self.frame = tk.Frame(parent)


        id = tk.StringVar()
        self.user_and_pass = []

        Password = tk.StringVar()


        textID =  tk.Label(self.frame, text="Type your WIFI USERNAME").pack()
        text1= tk.Entry(self.frame, textvariable=id).pack()




        # switch.printBu(   "0"+self.id_password.get())).pack()



        textPass =  tk.Label(self.frame, text="Type your Password").pack()
        text2= tk.Entry(self.frame, show="*", textvariable=Password).pack()


        send_button = tk.Button(self.frame, text="Send", command=lambda:self.saveData(id.get(), Password.get())).pack()



        self.frame.pack()
    def saveData(self, msg1, msg2):
        self.user_and_pass.append("0"+msg1)
        self.user_and_pass.append("1"+msg2)
        print(self.user_and_pass)
        self.arduino.scanTextBeforeSend(self.user_and_pass)
        root2 = tkinter.Toplevel()
        myNextGUI  = MainGUI(root2, self.arduino)
        self.frame.destroy();




class MainGUI:
    def __init__(self, parent, arduino):
        self.arduino = arduino
        self.parent = parent
        self.parent.title("Main GUI page")
        self.parent.geometry("500x500")
        self.frame = tk.Frame(parent)

        textPass =  tk.Label(self.frame, text="This page is tended to show what it receives from the client").pack()



        self.frame.pack()




def main():

    print("we are ready")
    with connect_arduino() as ser:
        sr = Serial(ser)

        root = tk.Tk()

        welcompage = LoginPage(root,sr)
        root.mainloop()







if __name__ == '__main__':
    main()
