from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class DEsitlePencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(DEsitlePencere, self).__init__(ebeveyn)
        merkez_kutu = QVBoxLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)
        self.gif_label = QLabel()
        merkez_kutu.addWidget(self.gif_label)
        animasyon = QMovie("iconlar/milis_.gif")
        self.gif_label.setMovie(animasyon)
        self.gif_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        animasyon.start()
        self.donut_label = QLabel()
        merkez_kutu.addWidget(self.donut_label)
        self.donut_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
