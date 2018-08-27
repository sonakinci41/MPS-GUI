from PyQt5.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QDialog, QVBoxLayout, QLabel, QMessageBox, QListWidget, QListWidgetItem, QPushButton, qApp)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import surec

class GuncellePencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(GuncellePencere, self).__init__(ebeveyn)
        self.islem = "guncelle"
        self.ebeveyn = ebeveyn
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

    def guncelle_surec_baslat(self):
        if self.islem == "guncelle":
            self.donut_label.setText("Güncellenebilir paketler aranıyor...")
            self.komut = "mps yukselt dosya"
        elif self.islem == "paket_guncelle":
            self.donut_label.setText("Seçilen paketler güncelleniyor...")
            self.komut = "mps yukselt /tmp/mps.guncellenecekler evet"
        terminal_thread = surec.SurecThread(self)
        terminal_thread.update.connect(self.guncelle_surec_guncelle)
        terminal_thread.finished.connect(self.guncelle_surec_bitti)
        terminal_thread.start()

    def guncelle_surec_bitti(self):
        if self.islem == "guncelle":
            dosya = open("/tmp/mps.guncellenecekler","r")
            paketler = dosya.readlines()
            dosya.close()
            if len(paketler) != 0:
                surec_pencere = SurecBaslatOnay(self)
                surec_pencere.liste_guncelle(paketler)
                surec_pencere.exec_()
            else:
                QMessageBox.information(self,"Paket bulunamadı","Sisteminiz güncel durumda.\nGüncellemeye ihtiyaç duyan bir paket bulunamadı")
        elif self.islem == "paket_guncelle":
            self.donut_label.setText("Paketler başarıyla güncellendi.")
            self.ebeveyn.asamalar.setCurrentIndex(1)

    def guncelle_surec_guncelle(self,cikti):
        if self.islem == "guncelle":
            self.donut_label.setText("Paketler taranıyor %" + cikti.split("[")[0][:-2])
        else:
            self.donut_label.setText(cikti.replace(".", ""))



class SurecBaslatOnay(QDialog):
    def __init__(self, ebeveyn=None):
        super(SurecBaslatOnay, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        merkez_kutu = QGridLayout()
        self.setLayout(merkez_kutu)
        self.bilgi_label = QLabel()
        self.bilgi_label.setText("Lütfen güncellemek istediğiniz paketleri seçiniz.")
        merkez_kutu.addWidget(self.bilgi_label,0,0,1,2)
        self.liste = QListWidget()
        merkez_kutu.addWidget(self.liste,1,0,1,2)
        self.onay_dugme = QPushButton("Güncelle")
        self.onay_dugme.clicked.connect(self.onay_fonk)
        self.geri_dugme = QPushButton("Vazgeç")
        self.geri_dugme.clicked.connect(self.geri_fonk)
        merkez_kutu.addWidget(self.geri_dugme,2,0,1,1)
        merkez_kutu.addWidget(self.onay_dugme,2,1,1,1)

    def onay_fonk(self):
        #self.ebeveyn.islem_surec_baslat()
        dosya = open("/tmp/mps.guncellenecekler","w")
        for i in range(0,self.liste.count()):
            if self.liste.item(i).checkState():
                dosya.write(self.liste.item(i).text()+"\n")
        dosya.close()
        self.ebeveyn.islem = "paket_guncelle"
        self.ebeveyn.guncelle_surec_baslat()
        QDialog.accept(self)

    def geri_fonk(self):
        self.ebeveyn.ebeveyn.asamalar.setCurrentIndex(1)
        QDialog.accept(self)

    def liste_guncelle(self,paketler):
        for paket in paketler:
            lm = QListWidgetItem()
            lm.setText(paket[:-1])
            lm.setFlags(lm.flags() | Qt.ItemIsUserCheckable)
            lm.setCheckState(Qt.Checked)
            self.liste.addItem(lm)