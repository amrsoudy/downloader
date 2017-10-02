from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import sys
from os import  path
import  os
import urllib.request
import pafy
import humanize
print ('hiiiiiiiiiiiiii')

print ('hiiiiiiiiiiiiii')
FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"joodi.ui"))
class maindailog(QMainWindow,FORM_CLASS):
    def __init__(self,parent = None):
        super(maindailog,self).__init__(parent)
        self.setupUi(self)
        self.pushButton.setText("amr")
        self.handel_ui()
        self.handel_btn()

    def handel_browes(self):
        save_place = QFileDialog.getSaveFileName(self,caption = "Save as",directory = ".",filter="All Files (*.*)")
        self.textEdit_2.setText(save_place)
    def handel_progress(self,blocnum,blocsize,totalsize):
        read = blocnum * blocsize
        if totalsize > 0:
            percetage = read *100 /totalsize
            self.progressBar.setValue(percetage)
            QApplication.processEvents()# to solve the problem of not responding
    def download(self):
        url = self.textEdit.toPlainText()
        save_lacation = self.textEdit_2.toPlainText()
        try:
            urllib.request.urlretrieve(url,save_lacation,self.handel_progress)
        except Exception:
            QMessageBox.warning(self,"download Error","download faild finished ")
            return
        QMessageBox.information(self,"download completed","download finished ")
        self.progressBar.setValue(0)
        self.textEdit.setText("")
        self.textEdit_2.setText("")

    def handel_btn(self):
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2.clicked.connect(self.handel_browes)
        self.pushButton_6.clicked.connect(self.detyoutubeinfo)
        self.pushButton_3.clicked.connect(self.download_vidio)
        self.pushButton_7.clicked.connect(self.save_Browes)
        self.pushButton_5.clicked.connect(self.play_list)
        self.pushButton_4.clicked.connect(self.save_Browes)


    def handel_ui(self):
        self.setWindowTitle("pydownloader")

    def detyoutubeinfo(self):
        vidio_link = self.textEdit_3.toPlainText()
        v = pafy.new(vidio_link)
        # print(v.title)
        # print(v.viewcount)
        st =v.allstreams
        for s in st :
            size = humanize.naturalsize(s.get_filesize())
            data ="{} - {} - {} - {}".format(s.mediatype , s.extension, s.quality,size)
            self.comboBox.addItem(data)
    def save_Browes(self):
        win =QFileDialog.getExistingDirectory(self,'Select the directory')
        self.textEdit_4.setText(win)
        self.textEdit_6.setText( win )

    def download_vidio(self):
        video_link = self.textEdit_3.toPlainText()
        save_location = self.textEdit_4.toPlainText()
        quality = self.comboBox.currentIndex()
        v = pafy.new(video_link)
        st =v.allstreams
        down = st[quality].download(filepath = save_location)
        QMessageBox.information(self,"download completed","download finished ")

    def play_list(self):
        palylist_url = self.textEdit_5.toPlainText()
        save_location = self.textEdit_6.toPlainText()
        plylist = pafy.get_playlist(palylist_url)
        videos = plylist['items']
        os.chdir(save_location)
        if os.path.exists(plylist['title']):
            os.mkdir(str(plylist['title']))
        else:
            os.mkdir(str(plylist['title']))
            os.chdir(str(plylist['title']))

        for vidio in videos:
            p = vidio['pafy']
            best = p.getbest(preftype='mp4')
            best.download()


app = QApplication(sys.argv)
form = maindailog()
form.show()
app.exec_()
