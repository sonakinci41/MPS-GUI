from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import surec

class PaketBilgiPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(PaketBilgiPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        merkez_kutu = QGridLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)
        self.icon_label = QLabel()
        merkez_kutu.addWidget(self.icon_label,0,0,1,1)
        self.kur_sil_dugme = QPushButton()
        merkez_kutu.addWidget(self.kur_sil_dugme,0,1,1,1)
        self.kur_sil_dugme.setFixedHeight(64)
        self.geri_dugme = QPushButton("Geri")
        self.geri_dugme.clicked.connect(self.geri_fonk)
        merkez_kutu.addWidget(self.geri_dugme,0,2,1,1)
        self.geri_dugme.setFixedHeight(64)
        merkez_kutu.addWidget(QLabel("Adı      : "),1,0,1,1)
        self.adi_label = QLabel()
        merkez_kutu.addWidget(self.adi_label,1,1,1,2)
        merkez_kutu.addWidget(QLabel("Tanımı   : "),2,0,1,1)
        self.tanim_label = QLabel()
        merkez_kutu.addWidget(self.tanim_label,2,1,1,2)
        merkez_kutu.addWidget(QLabel("Url      : "),3,0,1,1)
        self.url_label = QLabel()
        merkez_kutu.addWidget(self.url_label,3,1,1,2)
        merkez_kutu.addWidget(QLabel("Paketçi  : "),4,0,1,1)
        self.paketci_label = QLabel()
        merkez_kutu.addWidget(self.paketci_label,4,1,1,2)
        merkez_kutu.addWidget(QLabel("Sürüm    : "),5,0,1,1)
        self.surum_label = QLabel()
        merkez_kutu.addWidget(self.surum_label,5,1,1,2)
        merkez_kutu.addWidget(QLabel("Devir    : "),6,0,1,1)
        self.devir_label = QLabel()
        merkez_kutu.addWidget(self.devir_label,6,1,1,2)
        merkez_kutu.addWidget(QLabel("Grup     : "),7,0,1,1)
        self.grup_label = QLabel()
        merkez_kutu.addWidget(self.grup_label,7,1,1,2)
        merkez_kutu.addWidget(QLabel("Gerekler : "),8,0,1,1)
        self.gerekler_label = QLabel()
        merkez_kutu.addWidget(self.gerekler_label,8,1,1,2)
        merkez_kutu.addWidget(QLabel("Kaynak-1 : "),9,0,1,1)
        self.kaynak_1_label = QLabel()
        merkez_kutu.addWidget(self.kaynak_1_label,9,1,1,2)
        merkez_kutu.addWidget(QLabel("Kaynak-2 : "),10,0,1,1)
        self.kaynak_2_label = QLabel()
        merkez_kutu.addWidget(self.kaynak_2_label,10,1,1,2)

    def geri_fonk(self):
        self.ebeveyn.asamalar.setCurrentIndex(1)


    def surec_baslat(self,paket):
        self.paket_adi = paket
        self.komut = "mps bilgi {} --normal".format(paket)
        terminal_thread = surec.SurecThread(self)
        terminal_thread.update.connect(self.surec_guncelle)
        terminal_thread.finished.connect(self.surec_bitti)
        terminal_thread.start()

    def surec_bitti(self):
        print("okey")

    def surec_guncelle(self,cikti):
        print(cikti)
        if cikti[7:10] == "ADI":
            self.adi_label.setText(cikti[20:-7])
        elif cikti[7:12] == "TANIM":
            self.tanim_label.setText(cikti[20:-7])
        elif cikti[7:10] == "URL":
            self.url_label.setText(cikti[20:-7])
        elif cikti[7:14] == "PAKETÇİ":
            self.paketci_label.setText(cikti[20:-7])
        elif cikti[7:12] == "SÜRÜM":
            self.surum_label.setText(cikti[20:-7])
        elif cikti[7:12] == "DEVİR":
            self.devir_label.setText(cikti[20:-7])
        elif cikti[7:11] == "GRUP":
            self.grup_label.setText(cikti[20:-7])
        elif cikti[0:11] == "# Gerekler:":
            self.gerekler_label.setText(cikti[11:])
        elif cikti[7:15] == "file:///":
            self.kaynak_1_label.setText(cikti[7:-7])
        elif cikti[7:15] == "https://":
            self.kaynak_2_label.setText(cikti[7:-7])

        icon = QIcon.fromTheme(self.paket_adi, QIcon.fromTheme("package-manager-icon"))
        self.icon_label.setPixmap(icon.pixmap(icon.actualSize(QSize(64,64))))
        if self.paket_adi in self.ebeveyn.kurulu_paketler:
            self.kur_sil_dugme.setText("Sil")
        else:
            self.kur_sil_dugme.setText("Kur")
