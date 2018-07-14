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
        self.geri_dugme.setIcon(QIcon.fromTheme("edit-undo"))
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
        self.kaynak_2_label = QLabel()
        form_kutu.addRow(QLabel("<b>Kaynak-2\t: </b>"),self.kaynak_2_label)

    def geri_fonk(self):
        self.ebeveyn.asamalar.setCurrentIndex(1)

    def paket_kur_sil_fonk(self):
        self.ebeveyn.paket_kur_sil(self.paket_adi,self.kur_sil_dugme.text())


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
            self.kur_sil_dugme.setIcon(QIcon.fromTheme("user-trash"))
            self.kur_sil_dugme.setIconSize(QSize(48,48))
            self.kur_sil_dugme.setStyleSheet("background-color:#c6262e;border:None;color:#ffffff;font-weight:bold")
        else:
            self.kur_sil_dugme.setText("Kur")
            self.kur_sil_dugme.setIcon(QIcon.fromTheme("download"))
            self.kur_sil_dugme.setIconSize(QSize(48,48))
            self.kur_sil_dugme.setStyleSheet("background-color:#68b723;border:None;color:#ffffff;font-weight:bold")
