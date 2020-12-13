from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector
import re


class Anasayfa(QWidget):

    def __init__(self):
        super(Anasayfa, self).__init__()
        self.setWindowTitle("Personel İşlem Uygulaması")
        self.layout = QGridLayout()

        self.layout.addWidget(QLabel("Adı, Soyadı:"), 0, 0)
        self.layout.addWidget(QLabel("T.C. Kimlik No:"), 1, 0)
        self.layout.addWidget(QLabel("Banka Hesap No:"), 2, 0)
        self.layout.addWidget(QLabel("Çalıştığı Departman:"), 3, 0)
        self.layout.addWidget(QLabel("Çalıştığı konum:"), 4, 0)
        self.layout.addWidget(QLabel("Doğum Tarihi:"), 5, 0)
        self.layout.addWidget(QLabel("Cinsiyeti:"), 6, 0)

        self.adi = QLineEdit()
        self.soyadi = QLineEdit()
        self.tc = QLineEdit()
        self.banka = QLineEdit()
        self.departman = QLineEdit()
        self.konum = QLineEdit()
        self.tarih = QDateEdit(calendarPopup=True)
        self.erkek = QRadioButton("Erkek")
        self.kadin = QRadioButton("Kadın")
        self.cinsiyet = QButtonGroup(self)
        self.cinsiyet.addButton(self.erkek)
        self.cinsiyet.addButton(self.kadin)
        ekle = QPushButton("Ekle")
        ekle.clicked.connect(self.pers_ekle)
        sil = QPushButton("Sil")
        sil.clicked.connect(self.pers_sil)

        self.layout.addWidget(self.adi, 0, 1)
        self.layout.addWidget(self.tc, 1, 1)
        self.layout.addWidget(self.banka, 2, 1)
        self.layout.addWidget(self.departman, 3, 1)
        self.layout.addWidget(self.konum, 4, 1)
        self.layout.addWidget(self.tarih, 5, 1)
        self.layout.addWidget(self.erkek, 6, 1)
        self.layout.addWidget(self.kadin, 6, 2)
        self.layout.addWidget(ekle, 7, 0, 1, 2)
        self.layout.addWidget(sil, 7, 3, 1, 2)

        self.liste_guncelle()

        self.setLayout(self.layout)
        self.show()

    def pers_ekle(self):
        adi = self.adi.text()
        tc = self.tc.text()
        banka = self.banka.text()
        departman = self.departman.text()
        konum = self.konum.text()
        tarih = self.tarih.date()
        t = tarih.toPyDate()
        cinsiyet = ""
        if self.erkek.isChecked() is True:
            cinsiyet = "Erkek"
        elif self.kadin.isChecked() is True:
            cinsiyet = "Kadın"
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="programlama2"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO perskayit (adi, tc, banka, departman, konum, tarih, cinsiyet) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (adi, tc, banka, departman, konum, t, cinsiyet)

        mycursor.execute(sql, val)
        mydb.commit()

        mydb.close()
        self.liste_guncelle()
        self.temizle()

    def liste_guncelle(self):
        self.pers_liste = QListWidget()
        self.layout.addWidget(self.pers_liste, 0, 3, 7, 2)

        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="programlama2"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT adi FROM perskayit")

        myresult = mycursor.fetchall()

        for x in myresult:
            x = str(x)
            x = re.sub("[,()']", '', x)
            self.pers_liste.addItem(str(x))

    def pers_sil(self):
        secili = pers_liste.currentItem()
        silinecek = secili.text()

        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="programlama2"
        )

        mycursor = mydb.cursor()

        sql = "DELETE FROM perskayit WHERE adi = %s"
        ad = (silinecek,)

        mycursor.execute(sql, ad)

        mydb.commit()

        self.liste_guncelle()

    def temizle(self):
        self.adi.setText("")
        self.tc.setText("")
        self.banka.setText("")
        self.departman.setText("")
        self.konum.setText("")
        self.tarih.clear()


app = QApplication([])
window = Anasayfa()
window.show()
app.exec_()
