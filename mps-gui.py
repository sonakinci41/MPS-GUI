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
        self.asamalar.setCurrentIndex(3)
        self.kursilpencere.sorgu_surec_baslat(paket_adi,islem)

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

    def depo_esitle(self):
        self.komut = "mps -GG && mps guncelle --normal"
        self.islem = "depo_esitle"
        self.surec_baslat()

    def son_kontroller(self):
        self.paketler_sozluk = {}
        self.gruplar_sozluk = {}
        for i in os.listdir("/root/talimatname/genel"):
            dizin = "/root/talimatname/genel/"+i
            for a in os.listdir(dizin):
                self.bilgi_getir(dizin,a)
            for i in os.listdir("/root/talimatname/temel/"):
                dizin = "/root/talimatname/temel"
                self.bilgi_getir(dizin,i)

    def bilgi_getir(self,dizin,isim):
        if os.path.exists(dizin+"/"+isim+"/"+"talimat"):
            f = open(dizin+"/"+isim+"/"+"talimat","r")
            okunan = f.readlines()
            f.close()
            varmi =  self.paketler_sozluk.get(isim,"bunelan")
            if varmi == "bunelan":
                self.paketler_sozluk[isim] = {"Tanim":"","URL":"","Paketci":"","Gerekler":"","Grup":"","Surum":"","Devir":"","Kaynak":""}
                for satir in okunan:
                    if "# Tanım: " in satir:
                        self.paketler_sozluk[isim]["Tanim"] = satir.split("# Tanım: ")[1][:-1]
                    elif "# URL: " in satir:
                        self.paketler_sozluk[isim]["URL"] = satir.split("# URL: ")[1][:-1]
                    elif "# Paketçi: " in satir:
                        self.paketler_sozluk[isim]["Paketci"] = satir.split("# Paketçi: ")[1][:-1]
                    elif "# Gerekler: " in satir:
                        self.paketler_sozluk[isim]["Gerekler"] = satir.split("# Gerekler: ")[1][:-1]
                    elif "# Grup: " in satir:
                        gruplar = satir.split("# Grup: ")[1][:-1]
                        self.paketler_sozluk[isim]["Grup"] = gruplar
                        for grup in gruplar.split():
                            varmi =  self.gruplar_sozluk.get(grup,"bunelan")
                            if varmi == "bunelan":
                                self.gruplar_sozluk[grup]=[isim]
                            else:
                                varmi.append(isim)
                    elif "surum=" in satir:
                        self.paketler_sozluk[isim]["Surum"] = satir.split("surum=")[1][:-1]
                    elif "devir=" in satir:
                        self.paketler_sozluk[isim]["Devir"] = satir.split("devir=")[1][:-1]
                    elif "kaynak=" in satir:
                        self.paketler_sozluk[isim]["Kaynak"] = satir.split("kaynak=")[1][:-1]

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
            self.tum_paketler_kontrol()
        elif self.islem == "tum_paketler_kontrol":
            self.desitlepencere.donut_label.setText("MPS-GUI Paket Veri Tabanı Eşitleniyor")
            self.son_kontroller()
            self.paketgenelpencere.grup_liste_guncelle()
            self.paketgenelpencere.paket_liste_guncelle()
            self.asamalar.setCurrentIndex(1)

    def surec_guncelle(self,cikti):
        if self.islem == "depo_esitle":
            self.desitlepencere.donut_label.setText(cikti[7:-7])
        elif self.islem == "kurulu_paketler_tespit":
            self.kurulu_paketler.append(cikti)
            self.desitlepencere.donut_label.setText("Kurlu Paketler Tespit Ediliyor : "+cikti)
        elif self.islem == "tum_paketler_kontrol":
            self.tum_paketler.append(cikti)
            

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    uygulama.setOrganizationName('Paketci')
    uygulama.setApplicationName('Paketci')
    merkezPencere = MerkezPencere()
    merkezPencere.show()
    sys.exit(uygulama.exec_())
