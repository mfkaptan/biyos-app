import cookielib
import urllib
import urllib2
import sys
import biyosui
import base64 as b64

from docx import Document
from PyQt4 import QtGui
from bs4 import BeautifulSoup

# No, Blok, Daire
kiraci = [ [7710, "B", 6],
         ]


class BiyosApp(QtGui.QMainWindow, biyosui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BiyosApp, self).__init__(parent)
        self.setupUi(self)

        self.giris.setStyleSheet('QPushButton {background-color: #FF0000; color: white ;}')
        self.giris.clicked.connect(self.login)
        self.tum_borclar.clicked.connect(self.print_all)

    def login(self):
        with open('../log.in', 'r') as f:
            self.email = b64.decodestring(f.readline().strip())
            self.password = b64.decodestring(f.readline().strip())


        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )

        # need this twice - once to set cookies, once to log in...
        self._login()
        self._login()
        self.giris.setStyleSheet('QPushButton {background-color: #00FF00; color:green ;}')
        self.giris.setText('Giris Yapildi!')

    def _login(self):
        """
        Handle login. This should populate our cookie jar.
        """
        login_data = urllib.urlencode({
            'email' : self.email,
            'password' : self.password,
        })

        response = self.opener.open("https://app.biyos.net/login.php", login_data)

    def getAccount(self, no):
        url = 'http://app.biyos.net/hesaplar/' + str(no)
        resp = self.opener.open(url)
        return BeautifulSoup(resp.read(), "lxml")

    def print_single_account(self, no, blok, daire):
        ret = ""

        html = self.getAccount(no)
        hesap = html.body.find('span', attrs={'style':'font-size:22px;'}).prettify('latin-1')

        ret += hesap + " - " + blok + " Blok / No: " + str(daire) + "\n<br><br>"

        try:
            tablo = html.body.find('div', attrs={'class':'table-responsive'}).prettify('latin-1')
            geciken = html.body.find('div', attrs={'class':'detail-payment-item text-danger big-title'}).prettify('latin-1')
            bakiye = html.body.find('div', attrs={'class':'detail-payment-item text-warning big-title'}).prettify('latin-1')
        except AttributeError:
            ret += "<br>Odenmemis borcunuz bulunmamaktadir. Gosterdiginiz hassasiyet icin tesekkur ederiz.<br>"
        else:
            ret += tablo + "<br>"
            ret += geciken + "<br>"
            ret += bakiye

        return ret

    def print_all(self):
        self.tum_borclar.setText('Yazdiriliyor, lutfen bekleyin...')

        bar = "<br>" + "".join(['_']*80) + "<br>"
        # Open a file
        fo = open("Tum Borclar.html", "wb")
        fo.write("<html>")
        fo.write('<meta charset="ISO-8859-1">')

        daire = 1
        blok = "A"
        for i in range(6149, 6197):
            fo.write(bar)
            fo.write(self.print_single_account(i, blok, daire))
            fo.write(bar)
            daire += 1
            if daire == 25:
                daire = 1
                blok = "B"

        for k in kiraci:
            fo.write(bar)
            fo.write(self.print_single_account(*k))
            fo.write(bar)

        fo.write("<html>")
        # Close file
        fo.close()
        self.tum_borclar.setText('Tum borclar.html dosyasina yazdirildi!')

def main():
    app = QtGui.QApplication(sys.argv)
    biyos = BiyosApp()
    biyos.show()
    app.exec_()

if __name__ == '__main__':
    main()
