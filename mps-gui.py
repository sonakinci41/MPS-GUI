#!/usr/bin/python3
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QStackedWidget)
from PyQt5.QtGui import QIcon
from pencereler import desitlepencere, paketgenelpencere, paketbilgipencere, kursilpencere
import os, sys, surec

class MerkezPencere(QMainWindow):
    def __init__(self, ebeveyn=None):
        super(MerkezPencere, self).__init__(ebeveyn)
        self.setMinimumSize(800,500)
        self.icon_adresi = "/usr/share/icons/Numix-Circle-Light/scalable/apps/"
        merkez_widget = QWidget()
        self.setCentralWidget(merkez_widget)
        merkez_kutu = QVBoxLayout()
        merkez_kutu.setContentsMargins(0,0,0,0)
        merkez_widget.setLayout(merkez_kutu)
        self.asamalar = QStackedWidget()
        merkez_kutu.addWidget(self.asamalar)

        self.desitlepencere = desitlepencere.DEsitlePencere()
        self.asamalar.addWidget(self.desitlepencere)
        self.paketgenelpencere = paketgenelpencere.PaketGenelPencere(self)
        self.asamalar.addWidget(self.paketgenelpencere)
        self.paketbilgipencere = paketbilgipencere.PaketBilgiPencere(self)
        self.asamalar.addWidget(self.paketbilgipencere)
        self.kursilpencere = kursilpencere.KurSilPencere(self)
        self.asamalar.addWidget(self.kursilpencere)

        self.asamalar.setCurrentIndex(0)
        self.depo_esitle()

    def icon_getir(self,icon_adi):
        if os.path.exists(self.icon_adresi+icon_adi+".svg"):
            icon = QIcon(self.icon_adresi+icon_adi+".svg")
        elif os.path.exists(self.icon_adresi+"package-manager-icon.svg"):
            icon = QIcon(self.icon_adresi+"package-manager-icon.svg")
        else:
            icon = QIcon.fromTheme(icon_adi, QIcon.fromTheme("package-manager-icon"))
        return icon

    def paket_kur_sil(self,paket_adi,islem):
        self.kursilpencere.sorgu_surec_baslat(paket_adi,islem)
        self.asamalar.setCurrentIndex(3)

    def paket_secildi(self,paket_adi):
        self.paketbilgipencere.surec_baslat(paket_adi)
        self.asamalar.setCurrentIndex(2)

    def tum_paketler_kontrol(self):
        self.tum_paketler = []
        self.komut = "mps paketler"
        self.islem = "tum_paketler_kontrol"
        self.surec_baslat()

    def kurulu_paketler_tespit(self):
        self.kurulu_paketler = []
        self.komut = "mps liste --normal"
        self.islem = "kurulu_paketler_tespit"
        self.surec_baslat()

    def grup_paketler_tespit(self,sayac):
        self.grup = self.gruplar[sayac]
        self.komut = "mps paketler {} --normal".format(self.grup)
        self.islem = "grup_paketler_tespit"
        self.surec_baslat()

    def gruplar_tespit(self):
        self.gruplar = []
        self.komut = "mps gruplar --normal"
        self.islem = "gruplar_tespit"
        self.surec_baslat()

    def depo_esitle(self):
        self.komut = "mps -GG && mps guncelle --normal"
        self.islem = "depo_esitle"
        self.surec_baslat()

    def surec_baslat(self):
        terminal_thread = surec.SurecThread(self)
        terminal_thread.update.connect(self.surec_guncelle)
        terminal_thread.finished.connect(self.surec_bitti)
        terminal_thread.start()

    def surec_bitti(self):
        if self.islem == "depo_esitle":
            self.desitlepencere.donut_label.setText("Depolar Güncelledi")
            self.kurulu_paketler_tespit()
        elif self.islem == "kurulu_paketler_tespit":
            self.desitlepencere.donut_label.setText("Kurulu Paketler Tespit Edildi")
            self.gruplar_tespit()
        elif self.islem == "gruplar_tespit":
            self.desitlepencere.donut_label.setText("Gruplar Tespit Edildi")
            self.grup_paketler = {}
            self.grup_sayac = 0
            self.grup_paketler_tespit(self.grup_sayac)
        elif self.islem == "grup_paketler_tespit":
            self.grup_sayac += 1
            if self.grup_sayac == len(self.gruplar):
                self.desitlepencere.donut_label.setText("Tüm Paketler Tespit Edildi")
                self.tum_paketler_kontrol()
            else:
                self.grup_paketler_tespit(self.grup_sayac)
        elif self.islem == "tum_paketler_kontrol":
            self.desitlepencere.donut_label.setText("Tüm Paketler Kontrol Edildi")
            self.asamalar.setCurrentIndex(1)
            self.paketgenelpencere.grup_liste_guncelle()
            self.paketgenelpencere.paket_liste_guncelle()

    def surec_guncelle(self,cikti):
        if self.islem == "depo_esitle":
            self.desitlepencere.donut_label.setText(cikti[7:-7])
        elif self.islem == "kurulu_paketler_tespit":
            self.kurulu_paketler.append(cikti)
            self.desitlepencere.donut_label.setText("Kurlu Paketler Tespit Ediliyor : "+cikti)
        elif self.islem == "gruplar_tespit":
            self.gruplar = cikti.split()
        elif self.islem == "grup_paketler_tespit":
            self.grup_paketler[self.grup] = cikti.split()
            self.desitlepencere.donut_label.setText(self.grup+" Altındaki Paketler Tespit Ediliyor")
        elif self.islem == "tum_paketler_kontrol":
            self.tum_paketler.append(cikti)
            

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    uygulama.setOrganizationName('Paketci')
    uygulama.setApplicationName('Paketci')
    merkezPencere = MerkezPencere()
    merkezPencere.show()
    sys.exit(uygulama.exec_())
