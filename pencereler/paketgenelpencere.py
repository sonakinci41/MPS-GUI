from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class PaketGenelPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(PaketGenelPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        merkez_kutu = QHBoxLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)

        self.grup_liste = QListWidget()
        self.grup_liste.setFixedWidth(250)
        merkez_kutu.addWidget(self.grup_liste)

        self.paket_liste = QListWidget()
        merkez_kutu.addWidget(self.paket_liste)

    def paket_liste_guncelle(self):
        secili = self.grup_liste.currentItem().text()
        if secili == "Tümü":
            for paket in self.ebeveyn.tum_paketler:
                icon = QIcon.fromTheme(paket, QIcon.fromTheme("package-manager-icon"))
                lm = QListWidgetItem(icon,paket)
                self.paket_liste.addItem(lm)                


    def grup_liste_guncelle(self):
        self.grup_liste.addItem(QListWidgetItem(QIcon.fromTheme("application-default-icon"),"Tümü"))
        for grup in self.ebeveyn.gruplar:
            icon = QIcon.fromTheme(grup, QIcon.fromTheme("applications-other"))
            lm = QListWidgetItem(icon,grup)
            self.grup_liste.addItem(lm)
        self.grup_liste.setCurrentRow(0)
