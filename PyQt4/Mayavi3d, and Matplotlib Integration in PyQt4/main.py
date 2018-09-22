import sys,os
os.environ['ETS_TOOLKIT'] = 'qt4'

from pyface.qt import QtGui, QtCore

# from PyQt4 import QtCore
# from PyQt4 import QtGui

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor
import numpy as np
from numpy import *
from scipy.special import sph_harm
from mayavi.mlab import *

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

global q

q = 100


class MplCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 1, height = 1):
        self.figure = Figure(figsize = (width, height))
        self.axes = self.figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.update_figure()


    def update_figure(self):


        X = np.linspace(0,1,100)
        Y = X.copy()
        X, Y = np.meshgrid(X, Y)
        alpha = np.radians(25)
        cX, cY = 0.5, 0.5
        sigX, sigY = 0.2, 0.3
        rX = np.cos(alpha) * (X-cX) - np.sin(alpha) * (Y-cY) + cX
        rY = np.sin(alpha) * (X-cX) + np.cos(alpha) * (Y-cY) + cY

        Z = (rX-cX)*np.exp(-((rX-cX)/sigX)**2) * np.exp(- ((rY-cY)/sigY)**2)

        #print q

        slic = np.s_[0:q,0:q]

        x = X[slic]
        y = Y[slic]
        z = Z[slic]

        #cpf = self.axes.contourf(x,y,z, 25, cmap=cm.seismic)
        #colours = ['w' if level<0 else 'k' for level in cpf.levels]

        cp = self.axes.contour(x, y, z, 25, colors=('r','b','g','m','c','y','k'))

        # data = np.clip(np.random.randn(250, 250), -2, 2)
        #
        # cax = self.axes.imshow(data, interpolation='nearest', cmap=cm.coolwarm)
        cbar = self.figure.colorbar(cp, ticks=[-2, -1, 0, 1, 2])
        #cbar.self.axes.set_yticklabels(['-2', '< -1', '0', '> 1', '2'])
        #self.axes.contour(X, Y, Z)
        self.axes.grid(True)

        self.axes.set(xlabel='X-axis', ylabel='Y-axis', title='Sectional Graph')

        self.draw()


class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):

        theta_1d = linspace(0,   pi,  91)
        phi_1d   = linspace(0, 2*pi, 181)

        theta_2d, phi_2d = meshgrid(theta_1d, phi_1d)
        xyz_2d = array([sin(theta_2d) * sin(phi_2d),
                        sin(theta_2d) * cos(phi_2d),
                        cos(theta_2d)])


        l=3
        m=0

        Y_lm = sph_harm(m,l, phi_2d, theta_2d)
        r = abs(Y_lm.real)*xyz_2d

        s = mesh(r[0], r[1], r[2], scalars=Y_lm.real, colormap="cool")
        s = outline()
        s = axes()
        s = orientation_axes()

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )



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

        spacer = QtGui.QWidget(self)
        spacer.setSizePolicy(1|2|4,1|4)

        self.toolbar = QtGui.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(spacer)
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


        self.twoDBtn = QtGui.QPushButton("Matplotlib")
        self.twoDBtn.setStyleSheet("QPushButton {background-color: #c609b7;border: none;color: white;width: 57px;padding: 15px 32px;text-align: center;text-decoration: none;font-size: 16px; margin: 4px 2px;}")
        self.twoDBtn.clicked.connect(self.show2D)


        self.threeDBtn = QtGui.QPushButton("Mayavi 3D")
        self.threeDBtn.setStyleSheet("QPushButton {background-color: #b20808;border: none;color: white;width: 57px;padding: 15px 32px;text-align: center;text-decoration: none;font-size: 16px; margin: 4px 2px;}")
        self.threeDBtn.clicked.connect(self.show3D)

        self.lbl1 = QtGui.QLabel("Admin")
        self.lbl1.setStyleSheet("QLabel { border: 0; background: transparent; font-size: 20px; }")

        self.vlbl = QtGui.QLabel("Welcome")

        self.vbox = QtGui.QVBoxLayout()

        self.vbox.addWidget(self.lbl1)
        self.vbox.addWidget(self.adminBtn)
        self.vbox.addWidget(self.twoDBtn)
        self.vbox.addWidget(self.threeDBtn)
        self.vbox.addWidget(self.vlbl,QtCore.Qt.AlignBottom)

        self.visualization = Visualization()

        self.ui = self.visualization.edit_traits(parent=self,kind='subpanel').control

        self.scrollArea.setWidget(self.ui)

        self.mainLayout = QtGui.QGridLayout()

        self.mainLayout.addLayout(self.vbox,0,0)
        self.mainLayout.addWidget(self.scrollArea,0,1)

        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(self.mainLayout)

        self.showFullScreen()



    def show2D(self):
        self.newwidget = QtGui.QWidget()
        self.glayout = QtGui.QGridLayout(self.newwidget)

        self.sl = QtGui.QSlider(QtCore.Qt.Vertical)
        self.sl.setMinimum(2)
        self.sl.setMaximum(100)
        self.sl.setValue(100)
        self.sl.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.sl.setTickInterval(5)
        self.sl.valueChanged.connect(self.valuechange)

        self.canvas = MplCanvas()

        self.glayout.addWidget(self.canvas,0,0)
        self.glayout.addWidget(self.sl,0,1)

        self.scrollArea.setWidget(self.newwidget)

    def show3D(self):
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits(parent=self,kind='subpanel').control
        self.scrollArea.setWidget(self.ui)

    def valuechange(self):
        global q
        q = self.sl.value()

        self.canvas = MplCanvas()
        self.glayout.addWidget(self.canvas,0,0)

        self.scrollArea.setWidget(self.newwidget)


def main():

    app = QtGui.QApplication.instance()
    ex = MyApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
