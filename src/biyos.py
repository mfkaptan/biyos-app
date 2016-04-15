import cookielib
import urllib
import urllib2
import sys
import biyosui
import base64 as b64
import re

from docx import Document, text, table
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT

from PyQt4 import QtGui
from bs4 import BeautifulSoup

# No, Blok, Daire
kiraci = [ [7710, "B", 6],
         ]


class BiyosApp(QtGui.QMainWindow, biyosui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BiyosApp, self).__init__(parent)
        self.setupUi(self)

        self.document = None
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
        hesap =  html.body.find('span', attrs={'style':'font-size:22px;'}).get_text()

        p1 = self.document.add_paragraph()
        p1.style.paragraph_format.keep_together = True
        p1.style.paragraph_format.keep_with_next = True
        p1.style.paragraph_format.widow_control = True
        self.document.add_heading(hesap, level=1)
        self.document.add_heading(blok + " Blok / No: " + str(daire), level=2)

        try:
            data = html.body.find('div', attrs={'class':'table-responsive'})
            geciken = html.body.find('div', attrs={'class':'detail-payment-item text-danger big-title'})
            bakiye = html.body.find('div', attrs={'class':'detail-payment-item text-warning big-title'})
            tablo = self.create_table(data, geciken, bakiye)
        except AttributeError:
            return

    def create_table(self, data, geciken, bakiye):
        p = self.document.add_paragraph()
        p.style.paragraph_format.keep_together = True

        if bakiye:
            table = data.find('table', attrs={'class':'table table-detail'})
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')

            tbl = self.document.add_table(rows=0, cols=3)
            tbl.autofit = True
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl.style.paragraph_format.keep_together = True
            tbl.style.paragraph_format.widow_control = True

            row_cells = tbl.add_row().cells
            row_cells[0].text = "Son Odeme Tarihi"
            row_cells[1].text = "Aciklama"
            row_cells[2].text = "Tutar"

            for r in rows:
                row_cells = tbl.add_row().cells
                cols = r.find_all('td')
                i = 0
                for c in cols:
                    if c.text:
                        row_cells[i].text = c.text
                        i += 1

            non_decimal = re.compile(r'[^\d.,]+')

            row_cells = tbl.add_row().cells
            row_cells[1].text =  "Toplam Borc"
            row_cells[2].text = non_decimal.sub('',bakiye.get_text())

        else:
            self.document.add_heading("Odenmemis borcunuz bulunmamaktadir.", level=3)
            self.document.add_heading("Gosterdiginiz hassasiyet icin tesekkur ederiz.", level=4)

    def print_all(self):
        self.tum_borclar.setText('Yazdiriliyor, lutfen bekleyin...')

        try:
            self.document = Document()

            bar = "".join(['_']*78)

            daire = 1
            blok = "A"
            for i in range(6149, 6197):
                p = self.document.add_paragraph()
                p.style.paragraph_format.keep_together = True
                p.style.paragraph_format.keep_with_next = True
                p.add_run(bar).bold = True

                self.print_single_account(i, blok, daire)

                daire += 1
                if daire == 25:
                    daire = 1
                    blok = "B"

                print blok, daire

            for k in kiraci:
                p = self.document.add_paragraph()
                p.style.paragraph_format.keep_together = True
                p.style.paragraph_format.keep_with_next = True
                p.add_run(bar).bold = True

                self.print_single_account(*k)

            self.document.save('Tum borclar.docx')

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
