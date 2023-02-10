import sys,os,requests,ezgmail,urllib,threading, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PIL import Image
from api import API_KEY

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Window1.ui", self)
        self.show()
    

        #roverDets:

        self.spirit = self.findChild(QRadioButton,'radioButton')
        self.curiosity = self.findChild(QRadioButton,'radioButton_2')
        self.opportunity = self.findChild(QRadioButton,'radioButton_3')

        #cameraDets:

        self.FHAZ = self.findChild(QRadioButton,'radioButton_4')
        self.RHAZ = self.findChild(QRadioButton,'radioButton_5')
        self.PANCAM = self.findChild(QRadioButton,'radioButton_6')

        #calendar:

        self.calendar = self.findChild(QCalendarWidget,'calendarWidget')
        self.calendar.clicked.connect(self.date) 


        #pageChangers:

        self.fetch=self.findChild(QPushButton,'pushButton')
        self.back=self.findChild(QPushButton,'pushButton_2')
        self.mailPage=self.findChild(QPushButton,'pushButton_5')
        self.home=self.findChild(QPushButton,'pushButton_8')
        self.fetch.clicked.connect(self.changePage)
        self.back.clicked.connect(self.prevPage)
        self.home.clicked.connect(self.homePage)
        self.fetch.clicked.connect(self.fetchPage)
        
        #imageToggleButtons:

        self.nextBut=self.findChild(QPushButton,'pushButton_3')
        self.prevBut=self.findChild(QPushButton,'pushButton_4')
        self.prevBut.clicked.connect(self.previous)
        self.nextBut.clicked.connect(self.next)
        
        #sendingEmail:

        self.mailBut=self.findChild(QPushButton,'pushButton_6')
        self.mailBut.clicked.connect(self.sendMail)
        self.subject=self.findChild(QLineEdit,'lineEdit')
        self.body=self.findChild(QLineEdit,'lineEdit_2')
        self.recipients=self.findChild(QLineEdit,'lineEdit_3')

        

        #PAGES:
        self.stackedWidget = self.findChild(QStackedWidget,'stackedWidget')
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)

        self.frame=self.findChild(QFrame,'frame_7')
        
        self.mailPage.clicked.connect(self.mailpage)
        

    def roverDet(self):    
        if (self.radioButton_2.isChecked()):
            return("curiosity")

        elif (self.radioButton.isChecked()):
            return("spirit")

        elif (self.radioButton_3.isChecked()):
            return("opportunity")

    def cameraDet(self):
        if(self.radioButton_4.isChecked()):
            return("FHAZ")
        elif(self.radioButton_5.isChecked()):
            return("RHAZ")
        elif(self.radioButton_6.isChecked()):
            return("PANCAM")
    
    def date(self):
        selectedDate = self.calendar.selectedDate()
        pyDate = selectedDate.toPyDate()
        print(pyDate.strftime("%Y-%m-%d"))
        return (pyDate.strftime("%Y-%m-%d"))

    def homePage(self):
        self.stackedWidget.setCurrentIndex(0)

    def changePage(self):
        self.stackedWidget.setCurrentIndex(1)
        self.num=0
        self.image_list=[]
        try:
            data = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{self.roverDet()}/photos?camera={self.cameraDet()}&earth_date={self.date()}&api_key={API_KEY}")
            rover_data = data.json()
            self.no_photos = len(rover_data['photos'])
            print(self.no_photos)
            for pic in rover_data['photos']:
                    self.num=self.num+1
                    urllib.request.urlretrieve(f"{pic['img_src']}",f"image{self.num}.jpg")
                    self.image_list.append(f"image{self.num}.jpg")
        except:
            print("no photos")


    def fetchPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def images(self): #*
        
        self.label = QtWidgets.QLabel(self.frame)
        self.pixmap=QPixmap(f"image1.jpg")
        self.pixmap =self.pixmap.scaled(self.frame.width(),self.frame.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.show()
    
    def next(self):
        self.num=self.num+1
        if(self.num) > self.no_photos:
            self.num = 1
        print(self.num)
        self.label = QtWidgets.QLabel(self.frame)
        self.pixmap=QPixmap(f"image{self.num}.jpg")
        self.pixmap =self.pixmap.scaled(self.frame.width(),self.frame.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.show()


    def previous(self):
        self.num=self.num-1
        if self.num<=0:
            self.num=self.no_photos
        print(self.num)
        self.label = QtWidgets.QLabel(self.frame)
        self.pixmap=QPixmap(f"image{self.num}.jpg")
        self.pixmap =self.pixmap.scaled(self.frame.width(),self.frame.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.show()
    
    def prevPage(self):
        current_index = self.stackedWidget.currentIndex()
        x=current_index
        self.stackedWidget.setCurrentIndex(x-1)


    def mailpage(self):
        self.stackedWidget.setCurrentIndex(2)

    def sendMail(self):
        self.sub = self.subject.text()
        self.bod = self.body.text()
        self.recip=self.recipients.text()

        self.subject = f"{self.sub}"
        self.body = f"{self.bod}"
        self.recipients=f'{self.recip}'
        sending=self.recipients.split(',')
        for i in sending:
            ezgmail.send(str(i) ,self.subject,self.body,attachments=self.image_list,cc="")
        print('done')
    
    def sendMailThread(self):
        thread=  threading.Thread(target=self.sendMail)
        thread.start()
    def fetchPageThread(self):
        thread= threading.Thread(target=self.fetchPage)
        thread.start()
    
    
if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    window = AppWindow()
    sys.exit(qt_app.exec_())
