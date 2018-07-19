from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QListWidget, QListWidgetItem, QPushButton, qApp, QListView, QLineEdit)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import surec

class PaketGenelPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(PaketGenelPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        merkez_kutu = QVBoxLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)
 
        self.arama_le = QLineEdit()
        self.arama_le.textChanged.connect(self.yazi_degisti)
        merkez_kutu.addWidget(self.arama_le)
 
        liste_kutu = QHBoxLayout()
        merkez_kutu.addLayout(liste_kutu)

        self.grup_liste = QListWidget()
        self.grup_liste.itemSelectionChanged.connect(self.paket_liste_guncelle)
        self.grup_liste.setFixedWidth(250)
        liste_kutu.addWidget(self.grup_liste)

        self.paket_liste = QListWidget()
        #self.paket_liste.setViewMode(QListView.IconMode)
        self.paket_liste.setResizeMode(QListView.Adjust)
        #self.paket_liste.setMovement(QListView.Snap)
        liste_kutu.addWidget(self.paket_liste)

        self.arama_sonucu = []

    def yazi_degisti(self):
        self.arama_sonucu = []
        aranacak = self.arama_le.text()
        self.grup_liste.setCurrentRow(0)
        self.grup_liste.setDisabled(True)
        if len(aranacak) > 0:
            for paket in self.ebeveyn.paketler_sozluk.keys():
                if aranacak == self.arama_le.text():
                    if aranacak in paket:
                        self.arama_sonucu.append(paket)
                else:
                    break
        self.grup_liste.setDisabled(False)
        self.paket_liste_guncelle(aranacak)

    def paket_liste_guncelle(self,arama=None):
        self.paket_liste.clear()
        secili = self.grup_liste.currentItem().text()
        if secili == "Tümü":
            paketler = self.ebeveyn.tum_paketler
        elif secili == "Arama":
            self.arama_le.setFocus(True)
            paketler = self.arama_sonucu
        else:
            paketler = self.ebeveyn.gruplar_sozluk[secili]
        for paket in paketler:
            if secili == self.grup_liste.currentItem().text() and (arama == None or arama == self.arama_le.text()):
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
        self.grup_liste.addItem(QListWidgetItem(QIcon("./iconlar/ara.svg"),"Arama"))
        icon = self.ebeveyn.icon_getir("application-default-icon")
        self.grup_liste.addItem(QListWidgetItem(icon,"Tümü"))
        for grup in self.ebeveyn.gruplar_sozluk.keys():
            icon = self.ebeveyn.icon_getir("applications-other")
            icon = QIcon.fromTheme(grup, icon)
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
        yazi_kutu = QVBoxLayout()
        yazi_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(merkez_kutu)
        self.resim_dugme = QPushButton()
        self.resim_dugme.clicked.connect(self.secildi)
        self.resim_dugme.setFixedWidth(64)
        self.resim_dugme.setFixedHeight(64)
        self.resim_dugme.setIconSize(QSize(64,64))
        self.resim_dugme.setStyleSheet("border:None")
        merkez_kutu.addWidget(self.resim_dugme)
        merkez_kutu.addLayout(yazi_kutu)
        self.yazi_dugme = QLabel()
        self.yazi_dugme.setFixedHeight(18)
        self.yazi_dugme.setStyleSheet("border:None;text-align:left;font-weight:bold")
        yazi_kutu.addWidget(self.yazi_dugme)
        self.aciklama_dugme = QLabel()
        self.aciklama_dugme.setWordWrap(True)
        self.aciklama_dugme.setFixedHeight(40)
        #self.aciklama_dugme.setStyleSheet("border:None;text-align:left")
        yazi_kutu.addWidget(self.aciklama_dugme)
        self.kur_sil_dugme = QPushButton()
        self.kur_sil_dugme.clicked.connect(self.secildi)
        self.kur_sil_dugme.setFixedWidth(64)
        self.kur_sil_dugme.setFixedHeight(60)
        merkez_kutu.addWidget(self.kur_sil_dugme)

    def madde_duzenle(self,isim):
        icon = self.ebeveyn.ebeveyn.icon_getir(isim)
        self.resim_dugme.setIcon(icon)
        self.yazi_dugme.setText(isim)
        try:
            self.aciklama_dugme.setText(self.ebeveyn.ebeveyn.paketler_sozluk[isim]["Tanim"])
        except:
            self.ebeveyn.ebeveyn.tum_paketler.remove(isim)
            self.aciklama_dugme.setText("")
            pass
        self.paket_adi = isim
        if isim in self.ebeveyn.ebeveyn.kurulu_paketler:
            self.kur_sil_dugme.setIcon(QIcon("./iconlar/sil.svg"))
            self.kur_sil_dugme.setIconSize(QSize(24,24))
            self.kur_sil_dugme.setStyleSheet("background-color:#c6262e;border:None;color:#ffffff;font-weight:bold")
        else:
            self.kur_sil_dugme.setIcon(QIcon("./iconlar/kur.svg"))
            self.kur_sil_dugme.setIconSize(QSize(24,24))
            self.kur_sil_dugme.setStyleSheet("background-color:#68b723;border:None;color:#ffffff;font-weight:bold")

    def secildi(self):
        self.ebeveyn.ebeveyn.paket_secildi(self.paket_adi)
