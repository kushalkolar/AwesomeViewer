from PyQt5 import QtWidgets, QtCore
from pyqtgraph import ImageView
from tifffile import TiffFile


class Viewer(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        path = QtWidgets.QFileDialog(self, 'Choose file', '/', "(*.tiff *.tif)")

        if not path[0]:
            return
        path = path[0]

        tif = TiffFile(path)

        iv = ImageView(parent=self)
        iv.setImage(tif.series[0].asarray())
        self.setCentralWidget(iv)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMaximum(len(tif.series))
        slider.setMinimum(0)
        slider.setSingleStep(1)
        slider.setPageStep(10)
        slider.show()

        slider.valueChanged.connect(
            lambda i: iv.setImage(
                tif.series[i],
                autoRange=False,
                autoLevels=False,
                autoHistogramRange=False
            )
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    viewer = Viewer()
    viewer.show()

    app.exec_()
