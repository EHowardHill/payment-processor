import sys
import uuid
import keyboard
import stripe
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide2.QtGui import QFont, QMovie
from PySide2.QtCore import Qt, Signal, QObject, QTimer, QThread
from datetime import datetime
from time import sleep

stripe.api_key = 'YOUR_STRIPE_API_KEY'

class KeyboardListener(QObject):
    key_pressed = Signal(str)

    def __init__(self):
        super().__init__()

    def start_listening(self):
        keyboard.on_press(self.handle_key_event)

    def handle_key_event(self, event):
        key_value = event.name
        self.key_pressed.emit(key_value)

class CommandThread(QThread):
    output_changed = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.output_changed.emit(str(datetime.now()))
            sleep(0.2)

class FullscreenWindow(QMainWindow):

    state = 0
    quantity = 0
    card = []
    exp_month = []
    exp_year = []
    cvc = []

    def update_label(self, output):
        self.quant.setText(output)

    def clear(self):
        for i in reversed(range(self.vert.count())): 
            self.vert.itemAt(i).widget().deleteLater()

    def complete_transaction(self):
        transaction_id = str(uuid.uuid4())
        item_price = 1

        charge = stripe.Charge.create(
            amount=item_price,
            currency='usd',
            source={
                'object': 'card',
                'number': ''.join(str(self.card[:-4])),
                'exp_month': ''.join(str(self.card[-4:-2])),
                'exp_year': ''.join(str(self.card[-2:])) ,
                'cvc': self.cvc
            },
            description='Payment Example'
        )

        try:
            self.state = 3
            self.clear()

            self.vert.addStretch()
            self.label = QLabel()
            self.label.setText("Payment Successful")
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont("Arial", 20))
            self.label.adjustSize()
            self.label.setStyleSheet("color: black;")
            self.cont = QPushButton("Finish Dispensation", self)
            self.vert.addWidget(self.cont)
            self.vert.addStretch()

        except Exception as e:
            print("Error occurred during payment:", str(e))

    def state_fillup(self):
        self.state = 2
        self.clear()
        
        self.vert.addStretch()

        self.label = QLabel()
        self.label.setText("Quantity dispensed:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 20))
        self.label.adjustSize()
        self.label.setStyleSheet("color: black;")

        self.quant = QLabel()
        self.quant.setText(str(self.quantity))
        self.quant.setAlignment(Qt.AlignCenter)
        self.quant.setFont(QFont("Arial", 96))
        self.quant.adjustSize()
        self.quant.setStyleSheet("color: black;")

        self.vert.addWidget(self.label)
        self.vert.addWidget(self.quant)

        self.vert.addStretch()

        self.cont = QPushButton("Finish Dispensation", self)
        self.cont.clicked.connect(self.complete_transaction)
        self.vert.addWidget(self.cont)

        self.vert.addStretch()

        self.command_thread = CommandThread(self)
        self.command_thread.output_changed.connect(window.update_label)
        self.command_thread.start()

    def set_loading(self):
        if self.state == 0:
            self.clear()
            gif_path = "/home/ethan/Documents/GitHub/payment-processor/loading.gif"  # Replace with the actual path to your GIF
            movie = QMovie(gif_path)
            movie.setCacheMode(QMovie.CacheAll)
            movie.setSpeed(100)
            spinning = QLabel()
            spinning.setAlignment(Qt.AlignCenter)
            spinning.setMovie(movie)
            movie.start()
            self.vert.addWidget(spinning)
            self.state = 1
            QTimer.singleShot(3000, self.state_fillup)

    def handle_key_pressed(self, event):
        self.card.append(event)
        if self.state == 0:
            self.set_loading()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Payment Window")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        widget = QWidget(self)
        widget.setStyleSheet("background-color: white;")
        self.vert = QVBoxLayout(widget)

        self.label = QLabel()
        self.label.setText("Please insert your payment card.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 20))
        self.label.adjustSize()
        self.label.setStyleSheet("color: black;")
        self.vert.addWidget(self.label)

        self.keyboard_listener = KeyboardListener()
        self.keyboard_listener.key_pressed.connect(self.handle_key_pressed)
        self.keyboard_listener.start_listening()

        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullscreenWindow()
    sys.exit(app.exec_())
