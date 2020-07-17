from PyQt5 import QtWidgets, QtCore
from pyqtgraph import ImageView
from tifffile import TiffFile


class Viewer(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose file', '/', "(*.tiff *.tif)")

        if not path[0]:
            return
        path = path[0]

        self.tif = TiffFile(path)

        self.widget = QtWidgets.QWidget(parent=self)
        self.vlayout = QtWidgets.QVBoxLayout(self.widget)

        iv = ImageView(parent=self)
        iv.setImage(self.tif.asarray(key=0))
        self.vlayout.addWidget(iv)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, parent=self)
        self.slider.setMaximum(len(self.tif.series) - 1)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(10)

        self.spinbox = QtWidgets.QSpinBox(parent=self)
        self.spinbox.setMaximum(len(self.tif.series) - 1)
        self.spinbox.setMinimum(0)
        self.spinbox.valueChanged.connect(self.slider.setValue)

        self.vlayout.addWidget(self.spinbox)
        self.vlayout.addWidget(self.slider)

        self.slider.valueChanged.connect(
            lambda i: iv.setImage(
                self.tif.asarray(key=i),
                autoRange=False,
                autoLevels=False,
                autoHistogramRange=False
            )
        )

        self.slider.valueChanged.connect(self.spinbox.setValue)

        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    viewer = Viewer()
    viewer.show()

    viewer.resize(1000, 900)

    app.exec_()
