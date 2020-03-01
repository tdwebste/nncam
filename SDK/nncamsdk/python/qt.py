import sys, toupcam
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox

class MainWin(QWidget):
    eventImage = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hcam = None
        self.buf = None      # video buffer
        self.w = 0           # video width
        self.h = 0           # video height
        self.setFixedSize(640, 480)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.initUI()
        self.initCamera()

    def initUI(self):
        self.cb = QCheckBox('Auto Exposure', self)
        self.cb.stateChanged.connect(self.changeAutoExposure)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.move(0, 30)
        self.label.resize(self.geometry().width(), self.geometry().height())

# the vast majority of callbacks come from toupcam.dll/so/dylib internal threads, so we use qt signal to post this event to the UI thread  
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == toupcam.TOUPCAM_EVENT_IMAGE:
            ctx.eventImage.emit()

# run in the UI thread
    @pyqtSlot()
    def eventImageCallback(self):
        if self.hcam is not None:
            try:
                self.hcam.PullImageV2(self.buf, 24, None)
            except toupcam.HRESULTException:
                QMessageBox.warning(self, '', 'pull image failed', QMessageBox.Ok)
            else:
                img = QImage(self.buf, self.w, self.h, (self.w * 24 + 31) // 32 * 4, QImage.Format_RGB888)
                if sys.platform == 'win32':
                    newimg = img.rgbSwapped()
                else:
                    newimg = img
                self.label.setPixmap(QPixmap.fromImage(newimg))

    def initCamera(self):
        a = toupcam.ToupCam.EnumV2()
        if len(a) <= 0:
            self.setWindowTitle('No camera found')
            self.cb.setEnabled(False)
        else:
            self.setWindowTitle(a[0].displayname)
            self.eventImage.connect(self.eventImageCallback)
            try:
                self.hcam = toupcam.ToupCam.Open(a[0].id)
            except toupcam.HRESULTException:
                QMessageBox.warning(self, '', 'failed to open camera', QMessageBox.Ok)
            else:
                self.w, self.h = self.hcam.get_Size()
                bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
                self.buf = bytes(bufsize)
                self.cb.setChecked(self.hcam.get_AutoExpoEnable())            
                try:
                    self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                except toupcam.HRESULTException:
                    QMessageBox.warning(self, '', 'failed to start camera', QMessageBox.Ok)

    def changeAutoExposure(self, state):
        if self.hcam is not None:
            self.hcam.put_AutoExpoEnable(state == Qt.Checked)

    def closeEvent(self, event):
        if self.hcam is not None:
            self.hcam.Close()
            self.hcam = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())