from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, qApp, QListView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

class PaketGenelPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(PaketGenelPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        merkez_kutu = QHBoxLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)

        self.grup_liste = QListWidget()
        self.grup_liste.currentItemChanged.connect(self.paket_liste_guncelle)
        self.grup_liste.setFixedWidth(250)
        merkez_kutu.addWidget(self.grup_liste)

        self.paket_liste = QListWidget()
        #self.paket_liste.setViewMode(QListView.IconMode)
        self.paket_liste.setResizeMode(QListView.Adjust)
        #self.paket_liste.setMovement(QListView.Snap)
        merkez_kutu.addWidget(self.paket_liste)

    def paket_liste_guncelle(self):
        self.paket_liste.clear()
        secili = self.grup_liste.currentItem().text()
        if secili == "Tümü":
            paketler = self.ebeveyn.tum_paketler
        else:
            paketler = self.ebeveyn.grup_paketler[secili]
        for paket in paketler:
            if secili == self.grup_liste.currentItem().text():
                ozel_madde = OzelMadde(self)
                ozel_madde.madde_duzenle(paket)
                ozel_madde_item = QListWidgetItem(self.paket_liste)
                ozel_madde_item.setSizeHint(ozel_madde.sizeHint())
                self.paket_liste.setItemWidget(ozel_madde_item,ozel_madde)
                qApp.processEvents()
            else:
                break

    def grup_liste_guncelle(self):
        self.grup_liste.clear()
        self.grup_liste.addItem(QListWidgetItem(QIcon.fromTheme("application-default-icon"),"Tümü"))
        for grup in self.ebeveyn.gruplar:
            icon = QIcon.fromTheme(grup, QIcon.fromTheme("applications-other"))
            lm = QListWidgetItem(icon,grup)
            self.grup_liste.addItem(lm)
        self.grup_liste.setCurrentRow(0)

class OzelMadde(QWidget):
    def __init__(self, ebeveyn=None):
        super(OzelMadde, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.setFixedHeight(64)
        merkez_kutu = QHBoxLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)
        self.resim_dugme = QPushButton()
        self.resim_dugme.clicked.connect(self.secildi)
        self.resim_dugme.setFixedWidth(64)
        self.resim_dugme.setFixedHeight(64)
        self.resim_dugme.setIconSize(QSize(64,64))
        self.resim_dugme.setStyleSheet("border:None")
        merkez_kutu.addWidget(self.resim_dugme)
        self.yazi_dugme = QPushButton()
        self.yazi_dugme.clicked.connect(self.secildi)
        self.yazi_dugme.setFixedHeight(64)
        self.yazi_dugme.setStyleSheet("border:None")
        merkez_kutu.addWidget(self.yazi_dugme)
        self.kur_sil_dugme = QPushButton()
        self.kur_sil_dugme.clicked.connect(self.secildi)
        self.kur_sil_dugme.setFixedWidth(64)
        self.kur_sil_dugme.setFixedHeight(60)
        merkez_kutu.addWidget(self.kur_sil_dugme)

    def madde_duzenle(self,isim):
        icon = QIcon.fromTheme(isim, QIcon.fromTheme("package-manager-icon"))
        self.resim_dugme.setIcon(icon)
        self.yazi_dugme.setText(isim)
        self.paket_adi = isim
        if isim in self.ebeveyn.ebeveyn.kurulu_paketler:
            self.kur_sil_dugme.setText("Sil")
            self.kur_sil_dugme.setStyleSheet("background-color:#c6262e;border:None;color:#ffffff")
        else:
            self.kur_sil_dugme.setText("Kur")
            self.kur_sil_dugme.setStyleSheet("background-color:#68b723;border:None;color:#ffffff")

    def secildi(self):
        self.ebeveyn.ebeveyn.paket_secildi(self.paket_adi)
