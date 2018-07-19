from PyQt5.QtWidgets import (QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton, QFormLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import surec

class PaketBilgiPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(PaketBilgiPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        merkez_kutu = QVBoxLayout()
        merkez_kutu.setContentsMargins(10,10,10,10)
        dugmeler_kutu = QHBoxLayout()
        merkez_kutu.addLayout(dugmeler_kutu)
        form_kutu = QFormLayout()
        merkez_kutu.addLayout(form_kutu)
        self.setLayout(merkez_kutu)
        self.icon_label = QLabel()
        dugmeler_kutu.addWidget(self.icon_label)
        self.kur_sil_dugme = QPushButton()
        self.kur_sil_dugme.clicked.connect(self.paket_kur_sil_fonk)
        dugmeler_kutu.addWidget(self.kur_sil_dugme)
        self.kur_sil_dugme.setFixedHeight(64)
        self.geri_dugme = QPushButton("Geri")
        self.geri_dugme.setStyleSheet("background-color:#3689e6;border:None;color:#ffffff;font-weight:bold")
        self.geri_dugme.setIcon(QIcon("./iconlar/geri.svg"))
        self.geri_dugme.setIconSize(QSize(48,48))
        self.geri_dugme.clicked.connect(self.geri_fonk)
        dugmeler_kutu.addWidget(self.geri_dugme)
        self.geri_dugme.setFixedHeight(64)
        self.adi_label = QLabel()
        form_kutu.addRow(QLabel("<b>Adı\t: </b>"),self.adi_label)
        self.tanim_label = QLabel()
        self.tanim_label.setWordWrap(True)
        form_kutu.addRow(QLabel("<b>Tanımı\t: </b>"),self.tanim_label)
        self.url_label = QLabel()
        form_kutu.addRow(QLabel("<b>Url\t: </b>"),self.url_label)
        self.paketci_label = QLabel()
        form_kutu.addRow(QLabel("<b>Paketçi\t: </b>"),self.paketci_label)
        self.surum_label = QLabel()
        form_kutu.addRow(QLabel("<b>Sürüm\t: </b>"),self.surum_label)
        self.devir_label = QLabel()
        form_kutu.addRow(QLabel("<b>Devir\t: </b>"),self.devir_label,)
        self.grup_label = QLabel()
        form_kutu.addRow(QLabel("<b>Grup\t: </b>"),self.grup_label)
        self.gerekler_label = QLabel()
        self.gerekler_label.setWordWrap(True)
        form_kutu.addRow(QLabel("<b>Gerekler\t: </b>"),self.gerekler_label)
        self.kaynak_1_label = QLabel()
        form_kutu.addRow(QLabel("<b>Kaynak-1\t: </b>"),self.kaynak_1_label)
 
    def geri_fonk(self):
        self.ebeveyn.asamalar.setCurrentIndex(1)

    def paket_kur_sil_fonk(self):
        self.ebeveyn.paket_kur_sil(self.paket_adi,self.kur_sil_dugme.text())


    def surec_baslat(self,paket):
        self.paket_adi = paket
        icon = self.ebeveyn.icon_getir(paket)
        self.icon_label.setPixmap(icon.pixmap(icon.actualSize(QSize(64,64))))
        if paket in self.ebeveyn.kurulu_paketler:
            self.kur_sil_dugme.setText("Sil")
            self.kur_sil_dugme.setIcon(QIcon("./iconlar/sil.svg"))
            self.kur_sil_dugme.setIconSize(QSize(48,48))
            self.kur_sil_dugme.setStyleSheet("background-color:#c6262e;border:None;color:#ffffff;font-weight:bold")
        else:
            self.kur_sil_dugme.setText("Kur")
            self.kur_sil_dugme.setIcon(QIcon("./iconlar/kur.svg"))
            self.kur_sil_dugme.setIconSize(QSize(48,48))
            self.kur_sil_dugme.setStyleSheet("background-color:#68b723;border:None;color:#ffffff;font-weight:bold")

        paket_bilgisi = self.ebeveyn.paketler_sozluk[paket]
        self.adi_label.setText(paket)
        self.tanim_label.setText(paket_bilgisi["Tanim"])
        self.url_label.setText(paket_bilgisi["URL"])
        self.paketci_label.setText(paket_bilgisi["Paketci"])
        self.surum_label.setText(paket_bilgisi["Surum"])
        self.devir_label.setText(paket_bilgisi["Devir"])
        self.grup_label.setText(paket_bilgisi["Grup"])
        self.gerekler_label.setText(paket_bilgisi["Gerekler"])
        self.kaynak_1_label.setText(paket_bilgisi["Kaynak"])
