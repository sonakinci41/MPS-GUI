from PyQt5.QtWidgets import (QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import surec

class KurSilPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(KurSilPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        merkez_kutu = QVBoxLayout()
        merkez_kutu.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setLayout(merkez_kutu)
        merkez_kutu.setContentsMargins(10,10,10,10)
        baslik_kutu = QHBoxLayout()
        baslik_kutu.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        merkez_kutu.addLayout(baslik_kutu)
        self.icon_label = QLabel()
        baslik_kutu.addWidget(self.icon_label)
        self.paket_adi_label = QLabel()
        baslik_kutu.addWidget(self.paket_adi_label)
        self.yapilan_islem = QLabel()
        merkez_kutu.addWidget(self.yapilan_islem)





    def sorgu_surec_baslat(self,paket,islem):
        self.paket_adi = paket
        icon = QIcon.fromTheme(self.paket_adi, QIcon.fromTheme("package-manager-icon"))
        self.icon_label.setPixmap(icon.pixmap(icon.actualSize(QSize(64,64))))
        self.paket_adi_label.setText(self.paket_adi)
        if islem == "Kur":
            self.yapilan_islem.setText("{} Paketinin Bağımlılıkları Sorgulanıyor".format(paket))
            self.komut = "mps -ykp {} --normal".format(paket)
            terminal_thread = surec.SurecThread(self)
            terminal_thread.update.connect(self.sorgu_surec_guncelle)
            terminal_thread.finished.connect(self.sorgu_surec_bitti)
            terminal_thread.start()
        elif islem == "Sil":
            self.komut = "mps bilgi {} --normal".format(paket)
            self.yapilan_islem.setText("{} Paketi İle Silinecekler Sorgulanıyor".format(paket))

    def sorgu_surec_bitti(self):
        print("bitti")

    def sorgu_surec_guncelle(self,cikti):
        self.bagimliliklar = cikti.replace(".","").split()







    def islem_surec_baslat(self,paket,islem):
        self.paket_adi = paket
        if islem == "Kur":
            self.komut = "mps kur {} --normal".format(paket)
        elif islem == "Sil":
            self.komut = "mps sil {} --normal".format(paket)
        terminal_thread = surec.SurecThread(self)
        terminal_thread.update.connect(self.islem_surec_guncelle)
        terminal_thread.finished.connect(self.islem_surec_bitti)
        terminal_thread.start()

    def islem_surec_bitti(self):
        print("okey")

    def islem_surec_guncelle(self,cikti):
        print(cikti)
