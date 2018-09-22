import sys,os
from PyQt4 import QtCore
from PyQt4 import QtGui
import time
from datetime import datetime

import subprocess
import psutil
import urllib2
from wifi import Cell, Scheme

interface = "wlan0"

ROUNDED_STYLE_SHEET1 = """QPushButton {
    background-color: #4CAF50;
    border: none;
    color: white;
    width: 57px;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 4px 2px;

 }
"""
ROUNDED_STYLE_SHEET2 = """QPushButton {
     background-color: #f44336;
     border: none;
     color: white;
     width: 100px;
     padding: 15px 32px;
     text-align: center;
     text-decoration: none;
     font-size: 16px;
     margin: 4px 2px;
 }
"""
ROUNDED_STYLE_SHEET3 = """QPushButton {
     background-color: #008CBA;
     border: none;
     color: white;
     width: 57px;
     padding: 15px 32px;
     text-align: center;
     text-decoration: none;
     font-size: 16px;
     margin: 4px 2px;
 }
"""

ROUNDED_STYLE_SHEET4 = """QPushButton {
     background-color:  #111111;
     border: none;
     color: white;
     padding: 15px 32px;
     text-align: center;
     text-decoration: none;
     font-size: 16px;
     margin: 4px 2px;
 }
"""





class MyApp(QtGui.QMainWindow):

    def __init__(self):
        super(MyApp, self).__init__()

        self.initUI()

    def initUI(self):

        self.powerBtn = QtGui.QToolButton()
        self.powerBtn.setIcon(QtGui.QIcon("./img/power1.png"))
        self.powerBtn.setIconSize(QtCore.QSize(50,50))
        self.powerBtn.setCheckable(True)
        self.powerBtn.setToolTip("Exit")
        self.powerBtn.setStyleSheet("QToolButton { border: 0; background: transparent; width: 40px; height: 35px; }")



        self.powerBtn.toggled.connect(self.close)

        self.timelabel = QtGui.QLabel()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

        self.percentLbl = QtGui.QLabel()
        self.batteryIndicator = QtGui.QToolButton()

        self.timer2 = QtCore.QTimer(self)
        self.timer2.setInterval(200)
        self.timer2.timeout.connect(self.batteryStatus)
        self.timer2.start()

        self.wifi = QtGui.QToolButton()
        # self.wifi.setToolTip(x)

        self.timer3 = QtCore.QTimer(self)
        self.timer3.setInterval(1000)
        self.timer3.timeout.connect(self.wifiStatus)
        self.timer3.start()

        spacer = QtGui.QWidget(self)
        spacer.setSizePolicy(1|2|4,1|4)

        self.toolbar = QtGui.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(spacer)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.wifi)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.batteryIndicator)
        self.toolbar.addWidget(self.percentLbl)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.timelabel)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.powerBtn)
        self.toolbar.setMovable(False)

        self.adminBtn = QtGui.QToolButton()
        self.adminBtn.setText("Admin")
        self.adminBtn.setIcon(QtGui.QIcon("./img/admin.png"))
        self.adminBtn.setIconSize(QtCore.QSize(300,300))

        self.adminBtn.setStyleSheet("QToolButton { border: 0; background: transparent; width: 300px; height: 200px; }")

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        #self.scrollArea.setWidget(self.textEdit)
        self.scrollArea.setWidgetResizable(True)

        self.wifiBtn = QtGui.QPushButton("Show wifi networks")
        self.wifiBtn.setStyleSheet(ROUNDED_STYLE_SHEET3)
        self.wifiBtn.clicked.connect(self.showNetworks)


        self.lbl1 = QtGui.QLabel("User")
        self.lbl1.setStyleSheet("QLabel { border: 0; background: transparent; font-size: 20px; }")

        self.vlbl = QtGui.QLabel("Welcome")

        self.vbox = QtGui.QVBoxLayout()

        self.vbox.addWidget(self.lbl1)
        self.vbox.addWidget(self.adminBtn,)
        self.vbox.addWidget(self.wifiBtn)
        self.vbox.addWidget(self.vlbl,QtCore.Qt.AlignBottom)


        self.mainLayout = QtGui.QGridLayout()

        self.mainLayout.addLayout(self.vbox,0,0)
        self.mainLayout.addWidget(self.scrollArea,0,1)

        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(self.mainLayout)

        self.showFullScreen()




    def displayTime(self):

        cur_time = datetime.strftime(datetime.now(), "%I:%M:%S %p ")
        self.timelabel.setText(cur_time)


    def batteryStatus(self):
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = int(battery.percent)
        remaining = str((100 - percent)) + "%  remaining to charge"
        #print percent
        if percent == 100:
            self.percentLbl.setText("100 %")
        else:
            self.percentLbl.setText(str(percent) + "%")

        if plugged:
            self.batteryIndicator.setIcon(QtGui.QIcon("./img/charge.jpg"))
            self.batteryIndicator.setToolTip(remaining)
        else:
            remaining = str(percent) + "%  remaining"
            self.batteryIndicator.setToolTip(remaining)
            if percent >=90 :
                self.batteryIndicator.setIcon(QtGui.QIcon("./img/full.jpg"))

            elif percent >=75 and percent <=89:
                self.batteryIndicator.setIcon(QtGui.QIcon("./img/80.jpg"))

            elif percent >=50 and percent <=74:
                self.batteryIndicator.setIcon(QtGui.QIcon("./img/50.jpg"))

            elif percent >=20 and percent <=49:
                self.batteryIndicator.setIcon(QtGui.QIcon("./img/30.jpg"))

            elif percent >=5 and percent <=19:
                self.batteryIndicator.setIcon(QtGui.QIcon("./img/10.jpg"))

            else:
                self.batteryIndicator.setIcon(QtGui.QIcon("./img/empty.jpg"))


    def wifiStatus(self):


        internet_on()

        # print c

        if connected:
            range = str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3)
            # range = 70
            #print range
            if range >= 80:
                self.wifi.setIcon(QtGui.QIcon("./img/wifi.png"))

            elif range >=40 and  range < 80:
                self.wifi.setIcon(QtGui.QIcon("./img/mid2.png"))
            else:
                self.wifi.setIcon(QtGui.QIcon("./img/low.png"))
        else:
            self.wifi.setIcon(QtGui.QIcon())


    def showNetworks(self):

        if connected:
            self.newwidget = QtGui.QWidget()
            self.glayout = QtGui.QGridLayout(self.newwidget)

            l = []
            l = Cell.all('wlan0')
            x = str(l[0])
            y = x[10:-1]

            self.s = QtGui.QLabel()
            self.s.setText(y)
            self.s.setStyleSheet("QLabel {color:black; font-size: 20px;}")

            self.btn = QtGui.QPushButton( "Disconnect" )
            self.btn.setStyleSheet("QPushButton { background-color: #ff0011; border: none; color: white; width: 90px; padding: 8px 8px; text-align: center; text-decoration: none;font-size: 16px; margin: 4px 2px; }")
            self.btn.clicked.connect(self.disConnect)

            self.glayout.addWidget(self.s,0,0)
            self.glayout.addWidget(self.btn,0,1)

            self.glayout.setAlignment(QtCore.Qt.AlignCenter)
            self.scrollArea.setWidget(self.newwidget)

        else:
            self.newwidget = QtGui.QWidget()
            self.glayout = QtGui.QGridLayout(self.newwidget)
            l = []
            l = Cell.all('wlan0')
            for i,value in enumerate(l):
                self.s = "lbl" + str(i)
                #print self.s
                self.s = QtGui.QLabel()
                self.s.installEventFilter(self)


                x = str(l[i])

                y = x[10:-1]
                #print y
                self.s.setText(y)
                self.s.setStyleSheet("QLabel {color:black; font-size: 20px;}")
                self.glayout.addWidget(self.s,i,0)
                self.glayout.setRowMinimumHeight(i,40)

            self.refreshBtn = QtGui.QPushButton("Refresh")
            self.refreshBtn.setStyleSheet(ROUNDED_STYLE_SHEET3)
            self.refreshBtn.clicked.connect(self.showNetworks)
            self.glayout.addWidget(self.refreshBtn)
            self.glayout.setAlignment(QtCore.Qt.AlignCenter)
            self.scrollArea.setWidget(self.newwidget)


    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            # print "The sender is:", source.text()
            self.network = str(source.text())
            self.showDialog()

        return super(MyApp, self).eventFilter(source, event)

    def showDialog(self):

        self.text,ok = QtGui.QInputDialog.getText(self, 'Wifi Authentication','Enter Password:')

        self.tpass = str(self.text)

        if ok:
            self.connection()

    def connection(self):

        status = os.popen("ifconfig wlan0 up").read()

        winame = "wlan0"

        stream = os.popen("iwlist " + winame + " scan")

        if self.tpass == '':
            os.popen("iwconfig " + winame + " essid "+ self.network)
        else:
            connectstatus = os.popen("iwconfig " + winame + " essid " + self.network + " key s:" + self.tpass)

        os.popen("dhclient " + winame)
        ontest = os.popen("ping -c 1 google.com").read()

        if ontest == '':
            print "Connection failed. (Bad pass?)"

        print "Connected successfully!"

    def disConnect(self):
        os.popen("ifconfig wlan0 down")




def internet_on():
    global connected
    connected = False
    for timeout in [1,5,10,15]:
        try:
            response=urllib2.urlopen('http://google.com',timeout=timeout)
            connected = True
            return True
        except urllib2.URLError as err: pass
        connected = False
    return False



def get_name(cell):

    return matching_line(cell,"ESSID:")[1:-1]

def get_quality(cell):

    global quality
    quality = matching_line(cell,"Quality=").split()[0].split('/')
    #print str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"
    return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"



rules={"Name":get_name,"Quality":get_quality}

def matching_line(lines, keyword):
    """Returns the first matching line in a list of lines. See match()"""
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

def match(line,keyword):
    """If the first part of line (modulo blanks) matches keyword,
    returns the end of that line. Otherwise returns None"""
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return None

def parse_cell(cell):
    """Applies the rules to the bunch of text describing a cell and returns the
    corresponding dictionary"""
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell



def main():

    cells=[[]]
    parsed_cells=[]

    proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()


    for line in out.split("\n"):
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())

    cells=cells[1:]

    for cell in cells:
        parsed_cells.append(parse_cell(cell))

    app = QtGui.QApplication(sys.argv)

    global ex
    ex = MyApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
