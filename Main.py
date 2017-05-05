import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget,QPushButton,QLabel,QMainWindow, QStackedWidget, QLineEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIntValidator
from Transaction import Transaction
from TicketMachine import TicketMachine


class MainWindow(QMainWindow):
    transaction = Transaction()
    ticketMachine = TicketMachine()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setMinimumSize(1200, 800)
        self.setMaximumSize(1200, 800)
        self.center()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        firstWindow = TicketChoiceWindow(self.transaction)
        firstWindow.next.clicked.connect(self.PayIntoWidgetSet)
        self.central_widget.addWidget(firstWindow)

    def PayIntoWidgetSet(self):
        if self.transaction.valueOfTransaction != 0:
            payIntoWidget = PayIntoWindow(self.transaction)
            if self.transaction.paidInto >= self.transaction.valueOfTransaction:
               payIntoWidget.checkTransacionStatus()
            payIntoWidget.pay.clicked.connect(self.FinalWindowWidgetSet)
            payIntoWidget.returnTo.clicked.connect(self.TicketChoiceWidgetSetNoReset)
            self.central_widget.addWidget(payIntoWidget)
            self.central_widget.setCurrentWidget(payIntoWidget)

    def FinalWindowWidgetSet(self):
        if self.transaction.checkTransactionStatus() == True:
            self.ticketMachine.handleTransaction(self.transaction)
            finalWindnow = FinalWindow(self.transaction, self.ticketMachine)
            finalWindnow.reset.clicked.connect(self.TicketChoiceWidgetSet)
            self.central_widget.addWidget(finalWindnow)
            self.central_widget.setCurrentWidget(finalWindnow)

    def TicketChoiceWidgetSet(self):
        self.transaction.resetTransaction()
        ticketChoiceWidget = TicketChoiceWindow(self.transaction)
        ticketChoiceWidget.next.clicked.connect(self.PayIntoWidgetSet)
        self.central_widget.addWidget(ticketChoiceWidget)
        self.central_widget.setCurrentWidget(ticketChoiceWidget)

    def TicketChoiceWidgetSetNoReset(self):
        ticketChoiceWidget = TicketChoiceWindow(self.transaction)
        ticketChoiceWidget.next.clicked.connect(self.PayIntoWidgetSet)
        self.central_widget.addWidget(ticketChoiceWidget)
        self.central_widget.setCurrentWidget(ticketChoiceWidget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class TicketChoiceWindow(QWidget):

    def __init__(self, transact):
        super(TicketChoiceWindow, self).__init__()
        self.biletCounter = 0
        self.transaction = transact
        self.initUI()

    def initUI(self):
        font = QtGui.QFont("Times", 50, QtGui.QFont.Bold)
        font.setBold(True)
        font.setWeight(75)
        self.title = QLabel('Automat Biletowy',self)
        self.title.setFont(font)
        self.title.move(300, 100)

        font = QtGui.QFont("Times", 25, QtGui.QFont.Bold)
        self.downTitile = QLabel('Wybierz bilet: ', self)
        self.downTitile.setFont(font)
        self.downTitile.move(515, 225)

        self.next = QPushButton('Dalej', self)
        self.next.setFont(font)
        self.next.move(1000,700)

        font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.ticketCounter = QLabel(str(self.biletCounter) + '      ', self)
        self.ticketCounter.setFont(font)
        self.ticketCounter.move(600, 650)

        self.moneyCounter = QLabel(str(self.transaction.valueOfTransaction / 100) + '                  ', self)
        self.moneyCounter.setFont(font)
        self.moneyCounter.move(350, 650)

        self.shortTimeTicket = QLabel('Bilet 20 minutowy: ',self)
        self.shortTimeTicket.setFont(font)
        self.shortTimeTicket.move(250,350)

        self.mediumTimeTicket = QLabel('Bilet 40 minutowy: ', self)
        self.mediumTimeTicket.setFont(font)
        self.mediumTimeTicket.move(250, 400)

        self.longTimeTicket = QLabel('Bilet 60 minutowy: ', self)
        self.longTimeTicket.setFont(font)
        self.longTimeTicket.move(250, 450)

        self.studentTicket = QLabel('Ulgowy', self)
        self.studentTicket.setFont(font)
        self.studentTicket.move(500, 300)

        self.normalTicket = QLabel('Normalny', self)
        self.normalTicket.setFont(font)
        self.normalTicket.move(700, 300)


        self.studentShort = QPushButton(' 1.40 zł ', self)
        self.studentShort.setFont(font)
        self.studentShort.move(490, 350)
        self.studentShort.clicked.connect(lambda: self.addTicket(0))

        self.normalShort = QPushButton(' 2.80 zł ', self)
        self.normalShort.setFont(font)
        self.normalShort.move(690, 350)
        self.normalShort.clicked.connect(lambda: self.addTicket(3))

        self.studentMedium = QPushButton(' 1.90 zł ', self)
        self.studentMedium.setFont(font)
        self.studentMedium.move(490, 400)
        self.studentMedium.clicked.connect(lambda: self.addTicket(1))

        self.normalMedium = QPushButton(' 3.80 zł ', self)
        self.normalMedium.setFont(font)
        self.normalMedium.move(690, 400)
        self.normalMedium.clicked.connect(lambda: self.addTicket(4))

        self.studentLong = QPushButton(' 2.50 zł ', self)
        self.studentLong.setFont(font)
        self.studentLong.move(490, 450)
        self.studentLong.clicked.connect(lambda: self.addTicket(2))

        self.normalLong = QPushButton(' 5.00 zł ', self)
        self.normalLong.setFont(font)
        self.normalLong.move(690, 450)
        self.normalLong.clicked.connect(lambda: self.addTicket(5))

        self.ticket = QLabel('Wybrano biletow: ', self)
        self.ticket.setFont(font)
        self.ticket.move(600, 600)

        self.toPay = QLabel('Do zaplaty(zł): ', self)
        self.toPay.setFont(font)
        self.toPay.move(350, 600)

        self.resetTitle = QPushButton("Reset",self)
        self.resetTitle.setFont(font)
        self.resetTitle.move(50, 700)
        self.resetTitle.clicked.connect(lambda: self.reset())

        self.biletsNumber = QLineEdit(self)
        self.biletsNumber.setFont(font)
        self.validator = QIntValidator(0,1000)
        self.biletsNumber.setValidator(self.validator)
        self.biletsNumber.setText("1")
        self.biletsNumber.move(600,520)
        self.biletsNumber.setMinimumSize(100,35)
        self.biletsNumber.setMaximumSize(100,35)

        self.biletsNumberLabel = QLabel('Liczba biletow: ',self)
        self.biletsNumberLabel.setFont(font)
        self.biletsNumberLabel.move(400, 525)

    def addTicket(self, ticketType):
        for x in range(int(self.biletsNumber.text())):
            self.transaction.addTicket(ticketType)
        self.biletCounter= self.biletCounter + int(self.biletsNumber.text())
        self.ticketCounter.setText(str(self.biletCounter)+'      ')
        self.moneyCounter.setText(str(self.transaction.valueOfTransaction / 100)+ '            ')

    def reset(self):
        self.transaction.resetTransaction()
        self.biletCounter = 0
        self.ticketCounter.setText(str(self.biletCounter) + '      ')
        self.moneyCounter.setText(str(self.transaction.valueOfTransaction / 100) + '            ')


class PayIntoWindow(QWidget):
    def __init__(self,transact):
        super(PayIntoWindow, self).__init__()
        self.transaction = transact
        self.initUI()


    def initUI(self):

        font = QtGui.QFont("Times", 30, QtGui.QFont.Bold)
        self.paidInto = QLabel('Wpłać:', self)
        self.paidInto.setFont(font)
        self.paidInto.move(530, 150)

        font = QtGui.QFont("Times", 25, QtGui.QFont.Bold)
        self.pay = QPushButton(' Zaplac ', self)
        self.pay.setFont(font)
        self.pay.move(850, 600)
        self.pay.setEnabled(False)

        self.returnTo = QPushButton(' Powrot ', self)
        self.returnTo.setFont(font)
        self.returnTo.move(150, 600)

        font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.toPayTitle = QLabel('Do zapłaty(zł): ', self)
        self.toPayTitle.setFont(font)
        self.toPayTitle.move(50, 250)

        self.toPay = QLabel(str(self.transaction.valueOfTransaction / 100), self)
        self.toPay.setFont(font)
        self.toPay.move(50, 300)

        self.paidIntoTitle = QLabel('Wpłacono (zł): ', self)
        self.paidIntoTitle.setFont(font)
        self.paidIntoTitle.move(50, 350)

        self.paidInto = QLabel(str(self.transaction.paidInto / 100) + '              ', self)
        self.paidInto.setFont(font)
        self.paidInto.move(50, 400)

        self.oneGrosh = QPushButton(' 1 gr.', self)
        self.oneGrosh.setFont(font)
        self.oneGrosh.move(450, 250)
        self.oneGrosh.clicked.connect(lambda: self.payInto(1))

        self.twoGrosh = QPushButton(' 2 gr.', self)
        self.twoGrosh.setFont(font)
        self.twoGrosh.move(550, 250)
        self.twoGrosh.clicked.connect(lambda: self.payInto(2))

        self.fiveGrosh = QPushButton(' 5 gr.', self)
        self.fiveGrosh.setFont(font)
        self.fiveGrosh.move(650, 250)
        self.fiveGrosh.clicked.connect(lambda: self.payInto(5))

        self.tenGrosh = QPushButton('10 gr.', self)
        self.tenGrosh.setFont(font)
        self.tenGrosh.move(450, 300)
        self.tenGrosh.clicked.connect(lambda: self.payInto(10))

        self.twentyGrosh = QPushButton('20 gr.', self)
        self.twentyGrosh.setFont(font)
        self.twentyGrosh.move(550, 300)
        self.twentyGrosh.clicked.connect(lambda: self.payInto(20))

        self.fiftyGrosh = QPushButton('50 gr.', self)
        self.fiftyGrosh.setFont(font)
        self.fiftyGrosh.move(650, 300)
        self.fiftyGrosh.clicked.connect(lambda: self.payInto(50))

        self.oneZloty = QPushButton(' 1 zł.', self)
        self.oneZloty.setFont(font)
        self.oneZloty.move(450, 350)
        self.oneZloty.clicked.connect(lambda: self.payInto(100))

        self.twoZloty = QPushButton(' 2 zł.', self)
        self.twoZloty.setFont(font)
        self.twoZloty.move(550, 350)
        self.twoZloty.clicked.connect(lambda: self.payInto(200))

        self.fiveZloty = QPushButton(' 5 zł.', self)
        self.fiveZloty.setFont(font)
        self.fiveZloty.move(650, 350)
        self.fiveZloty.clicked.connect(lambda: self.payInto(500))

        self.coinNumber = QLineEdit(self)
        self.coinNumber.setFont(font)
        self.validator = QIntValidator(0, 1000)
        self.coinNumber.setValidator(self.validator)
        self.coinNumber.setText("1")
        self.coinNumber.move(625, 425)
        self.coinNumber.setMinimumSize(100, 35)
        self.coinNumber.setMaximumSize(100, 35)

        self.coinsNumberLabel = QLabel('Liczba pieniędzy: ', self)
        self.coinsNumberLabel.setFont(font)
        self.coinsNumberLabel.move(445, 430)


    def payInto(self,value):

       try:
            for x in range(int(self.coinNumber.text())):
                self.transaction.payInto(value)
            self.paidInto.setText(str(self.transaction.paidInto / 100))
            self.checkTransacionStatus()
       except :
           pass

    def checkTransacionStatus(self):
        if self.transaction.checkTransactionStatus() is True:
            self.oneGrosh.setEnabled(False)
            self.twoGrosh.setEnabled(False)
            self.fiveGrosh.setEnabled(False)
            self.fiveZloty.setEnabled(False)
            self.twoZloty.setEnabled(False)
            self.oneZloty.setEnabled(False)
            self.fiftyGrosh.setEnabled(False)
            self.twentyGrosh.setEnabled(False)
            self.tenGrosh.setEnabled(False)
            self.pay.setEnabled(True)

class FinalWindow(QWidget):
    def __init__(self,transact, machine):
        super(FinalWindow, self).__init__()
        self.transaction = transact
        self.ticketMachine = machine
        self.initUI()


    def initUI(self):
        font = QtGui.QFont("Times", 30, QtGui.QFont.Bold)
        self.summary = QLabel('Podsumowanie', self)
        self.summary.setFont(font)
        self.summary.move(450, 100)

        if(self.transaction.corectnessOfTransaction == True):
            font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
            self.corectness = QLabel('Platnosc przebiegla poprawnie.', self)
            self.corectness.setFont(font)
            self.corectness.move(450,180)

            self.differenceTitle = QLabel('Wydano: ', self)
            self.differenceTitle.setFont(font)
            self.differenceTitle.move(450, 230)

            self.change = QLabel(str(self.transaction.difference / 100) , self)
            self.change.setFont(font)
            self.change.move(700, 230)
        else:
            font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
            self.corectness = QLabel('Automat nie może wydać reszty. Zwrot gotówki.', self)
            self.corectness.setFont(font)
            self.corectness.move(350, 230)

        font = QtGui.QFont("Times", 25, QtGui.QFont.Bold)
        self.reset = QPushButton(' Dalej ', self)
        self.reset.setFont(font)
        self.reset.move(850 , 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())