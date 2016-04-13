import cookielib
import urllib
import urllib2
import sys
import biyosui
import base64 as b64

from docx import Document, text
from PyQt4 import QtGui
from bs4 import BeautifulSoup

# No, Blok, Daire
kiraci = [ [7710, "B", 6],
         ]


class BiyosApp(QtGui.QMainWindow, biyosui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BiyosApp, self).__init__(parent)
        self.setupUi(self)

        self.giris.setStyleSheet('QPushButton {background-color: #FF0000; color: white;}')
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

        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        # need this twice - once to set cookies, once to log in...
        self._login()
        self._login()
        self.giris.setStyleSheet('QPushButton {background-color: #00FF00; color: black;}')
        self.giris.setText(self.email + ' adresi ile giris yapildi!')

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
        url = 'https://app.biyos.net/hesaplar/' + str(no)
        try:
            resp = self.opener.open(url)
            return BeautifulSoup(resp.read(), "lxml")
        except Exception as e:
            raise e

    def print_single_account(self, no, blok, daire):
        html = self.getAccount(no)

        hesap = html.body.find('span', attrs={'style':'font-size:22px;'}).prettify('latin-1')
        ret = ""
        #ret = hesap + " - " + blok + " Blok / No: " + str(daire)

        try:
            tablo = html.body.find('div', attrs={'class':'table-responsive'}).prettify('latin-1')
            geciken = html.body.find('div', attrs={'class':'detail-payment-item text-danger big-title'}).prettify('latin-1')
            bakiye = html.body.find('div', attrs={'class':'detail-payment-item text-warning big-title'}).prettify('latin-1')
        except AttributeError:
            ret += "Odenmemis borcunuz bulunmamaktadir. Gosterdiginiz hassasiyet icin tesekkur ederiz."
        else:
            ret += "NO"
            #ret += tablo
            #ret += geciken
            #ret += bakiye

        return ret

    def print_all(self):
        self.tum_borclar.setText('Yazdiriliyor, lutfen bekleyin...')

        try:
            document = Document()
            document.add_heading('Tum Borclar', 0)

            text.paragraph.ParagraphFormat.keep_together = True

            bar = "".join(['_']*80)

            daire = 1
            blok = "A"
            for i in range(6149, 6197):
                p = document.add_paragraph()
                p.add_run(bar).bold = True
                p.add_run(self.print_single_account(i, blok, daire))
                p.add_run(bar).bold = True

                daire += 1
                if daire == 25:
                    daire = 1
                    blok = "B"

            for k in kiraci:
                p = document.add_paragraph()
                p.add_run(bar).bold = True
                p.add_run(self.print_single_account(*k))
                p.add_run(bar).bold = True

            document.save('Tum borclar.docx')

        except Exception as e:
            print e
            self.tum_borclar.setStyleSheet('QPushButton {background-color: #FF0000; color: white;}')
            self.tum_borclar.setText('Yazdirma basarisiz!')
        else:
            self.tum_borclar.setStyleSheet('QPushButton {background-color: #00FF00; color: black;}')
            self.tum_borclar.setText('Tum borclar.html dosyasina yazdirildi!')

def main():
    app = QtGui.QApplication(sys.argv)
    biyos = BiyosApp()
    biyos.show()
    app.exec_()

if __name__ == '__main__':
    main()
