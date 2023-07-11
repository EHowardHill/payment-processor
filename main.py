import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class FullscreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Payment Window")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        label = QLabel(self)
        label.setText("Please insert your payment card.")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move((self.width() - label.width()) // 2, (self.height() - label.height()) // 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullscreenWindow()
    sys.exit(app.exec_())
