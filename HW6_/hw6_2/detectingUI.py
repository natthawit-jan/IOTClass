import warnings
import serial
import serial.tools.list_ports
import time
import collections
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
style.use("ggplot")

# from matplotlib import pyplot as plt
import threading

import tkinter as tk
from matplotlib.figure import Figure



def connect_arduino(baudrate=9600):
    def is_arduino(p):
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
    ser = serial.Serial(selected_port.device, baudrate)
    time.sleep(2)  # this is important it takes time to handshake
    return ser


class DataStream:
    def __init__(self, ser):
        self.ser = ser
        ndata = 2000
        self.r = collections.deque([], ndata)
        self.g = collections.deque([], ndata)
        self.b = collections.deque([], ndata)
        self.lock = threading.Lock()
        self.shouldStop = True
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True  # Daemonize thread
        self.shouldStop = False
        self.thread.start()

    def run(self):
        while not self.shouldStop:
            self.get_data()

    def stop(self):
        self.shouldStop = True
        if self.thread is not None:
            self.thread.join()
            self.thred = None

    def get_data(self):
        try:
            data = self.ser.read_until(b"\n", 255).decode().strip()
        except UnicodeDecodeError as e:
            warnings.warn('invalid data got non unicode. This may happen at the start.')
            return

        print(data)
        splitted = data.split(' ')

        if len(splitted) == 3:
            r, g, b  = splitted
            intr, intg, intb = 0., 0., 0.
            try:
                fr, fg, fb = float(r), float(g), float(b)
                # print(fr)
                self.r.append(fr)
                self.g.append(fg)
                self.b.append(fb)
            except ValueError as e:
                pass

    def getR(self):
        return -1 if not self.r else self.r[-1]
    #
    def getG(self):
        return -1 if not self.g else self.g[-1]
    #
    def getB(self):
        return -1 if not self.b else self.b[-1]




class LabelValue(tk.Frame):
    def __init__(self, master,vname,vtext,*arg, **kwargs):
        super().__init__(master, *arg, **kwargs)


        # self.streamer = streamer


        #
        # self.detect = tk.Button(text="Detect Colour", command=lambda:
        # self.streamer.get_data()).pack()

        self.label = tk.Label(text=vname)
        self.label.pack()
        self.value = tk.Label(textvariable=vtext)
        self.value.pack()



        # self.label = tk.Label(text=vname)
        # self.label.pack(side=tk.LEFT)
        # self.value = tk.Label(textvariable=vtext)
        # self.value.pack(side=tk.LEFT)


class SummaryInfo(tk.Frame):
    def __init__(self, master, streamer, *arg, **kwargs):
        super().__init__(master, *arg, **kwargs)
        self.streamer = streamer
        self.r = tk.DoubleVar()
        self.g = tk.DoubleVar()
        self.b = tk.DoubleVar()


        self.detect = tk.Button(self, text="Detect Colour", command=lambda:
        self.update()).pack(side=tk.TOP)

        self.R_label = LabelValue(self, 'R: ', self.r)
        self.R_label.pack()

        self.G_label = LabelValue(self, 'G: ', self.g)
        self.G_label.pack()

        self.B_label = LabelValue(self, 'B: ', self.b)

        self.B_label.pack()
        self.text_colourResult =  tk.Label(self, text="Result colour: ?")
        self.text_colourResult.pack()


    def colourDetermine(self):
        ls = [self.r.get(), self.g.get(), self.b.get()]
        max_ = ls.index(max(ls))
        print (max_)
        if max_ == 0:
            return "red"
        elif max_ == 1:
            return "green"

        else:
            return "blue"






    def update(self):
        # print (self.streamer.getR())
        self.r.set(self.streamer.getR())
        self.g.set(self.streamer.getG())
        self.b.set(self.streamer.getB())
        self.text_colourResult.configure(text="Result colour: " + self.colourDetermine())








def main():
    with connect_arduino(250000) as ser:
        streamer = DataStream(ser)

        root = tk.Tk()
        root.geometry('200x200')
        getSteam = SummaryInfo(root, streamer)
        # getSteam.start()
        getSteam.pack()


        streamer.start()
        # sinfo.start()
        root.mainloop()


if __name__ == '__main__':
    main()
