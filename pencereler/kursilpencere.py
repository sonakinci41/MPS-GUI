from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QLabel, QPushButton, QDialog, QTextEdit)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QMovie
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
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        merkez_kutu.addWidget(self.gif_label)
        animasyon = QMovie("iconlar/surec.gif")
        self.gif_label.setMovie(animasyon)
        animasyon.start()
        self.yapilan_islem = QLabel()
        merkez_kutu.addWidget(self.yapilan_islem)

    def sorgu_surec_baslat(self,paket,islem):
        self.paket_adi = paket
        self.islem = islem
        icon = QIcon.fromTheme(self.paket_adi, QIcon.fromTheme("package-manager-icon"))
        self.icon_label.setPixmap(icon.pixmap(icon.actualSize(QSize(64,64))))
        self.paket_adi_label.setText(self.paket_adi)
        self.yapilan_islem.setText("{} Paketinin Bağımlılıkları Sorgulanıyor".format(paket))
        self.komut = "mps -ykp {} --normal".format(paket)
        terminal_thread = surec.SurecThread(self)
        terminal_thread.update.connect(self.sorgu_surec_guncelle)
        terminal_thread.finished.connect(self.sorgu_surec_bitti)
        terminal_thread.start()


    def sorgu_surec_bitti(self):
        if self.islem == "Kur":
            surec_pencere = SurecBaslatOnay(self)
            surec_pencere.kutu_guncelle("{} paketi için aşağıdaki paketler kurulacak".format(self.paket_adi),"\n".join(self.bagimliliklar))
            surec_pencere.exec_()
        elif self.islem == "Sil":
            self.yapilan_islem.setText("{} Paketi İle Silinecekler Sorgulanıyor".format(self.paket_adi))
            surec_pencere = SurecBaslatOnay(self)
            surec_pencere.kutu_guncelle("{} paketiyle beraber aşağıdaki paketler silinecek".format(self.paket_adi),self.paket_adi)
            surec_pencere.exec_()


    def sorgu_surec_guncelle(self,cikti):
        self.bagimliliklar = cikti.replace(".","").split()

    def islem_surec_baslat(self):
        if self.islem == "Kur":
            self.komut = "mps kur {} --normal".format(self.paket_adi)
        elif self.islem == "Sil":
            self.yapilan_islem.setText("{} Paketi Siliniyor".format(self.paket_adi))
            self.komut = "mps sil {} evet --normal".format(self.paket_adi)
        terminal_thread = surec.SurecThread(self)
        terminal_thread.update.connect(self.islem_surec_guncelle)
        terminal_thread.finished.connect(self.islem_surec_bitti)
        terminal_thread.start()

    def islem_surec_bitti(self):
        if self.islem == "Kur":
            for bagimlilik in self.bagimliliklar:
                self.ebeveyn.kurulu_paketler.append(bagimlilik)
        elif self.islem == "Sil":
            self.ebeveyn.kurulu_paketler.remove(self.paket_adi)
        self.ebeveyn.asamalar.setCurrentIndex(1)
        self.ebeveyn.paketgenelpencere.paket_liste_guncelle()

    def islem_surec_guncelle(self,cikti):
        self.yapilan_islem.setText(cikti.replace(".", ""))


class SurecBaslatOnay(QDialog):
    def __init__(self, ebeveyn=None):
        super(SurecBaslatOnay, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        merkez_kutu = QGridLayout()
        self.setLayout(merkez_kutu)
        self.bilgi_label = QLabel()
        merkez_kutu.addWidget(self.bilgi_label,0,0,1,2)
        self.olay_te = QTextEdit()
        self.olay_te.setReadOnly(True)
        merkez_kutu.addWidget(self.olay_te,1,0,1,2)
        self.onay_dugme = QPushButton("Onayla")
        self.onay_dugme.clicked.connect(self.onay_fonk)
        self.geri_dugme = QPushButton("Vazgeç")
        self.geri_dugme.clicked.connect(self.geri_fonk)
        merkez_kutu.addWidget(self.geri_dugme,2,0,1,1)
        merkez_kutu.addWidget(self.onay_dugme,2,1,1,1)

    def onay_fonk(self):
        self.ebeveyn.islem_surec_baslat()
        QDialog.accept(self)

    def geri_fonk(self):
        self.ebeveyn.ebeveyn.asamalar.setCurrentIndex(1)
        QDialog.accept(self)

    def kutu_guncelle(self,ust,alt):
        self.bilgi_label.setText(ust)
        self.olay_te.setText(alt)
