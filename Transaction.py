from Ticket import Ticket
from Money import Coin

class Transaction(object):
    listOftickets = list()
    listOfMoney = list()
    listOfMoneyPaidInto = list()
    valueOfTransaction = 0
    paidInto = 0
    difference = 0
    corectnessOfTransaction = False

    def addTicket(self,ticketType):
        self.listOftickets.append(Ticket(ticketType))
        self.updateValueOfTransaction()

    def updateValueOfTransaction(self):
        self.valueOfTransaction = 0;
        for x in self.listOftickets:
            self.valueOfTransaction = self.valueOfTransaction + x.value

    def payInto(self,money):
        self.listOfMoney.append(Coin(money))
        self.paidInto = self.paidInto + money

    def resetTransaction(self):
        self.valueOfTransaction = 0
        self.paidInto = 0
        del self.listOftickets[:]
        del self.listOfMoney[:]

    def checkTransactionStatus(self):
        if self.paidInto >= self.valueOfTransaction:
            return True
        else:
            return False

    def setCorrectness(self, correctness):
        self.corectnessOfTransaction = correctness

    def calcDifference(self):
        self.difference = self.paidInto - self.valueOfTransaction

    def resetMoneyList(self):
        del self.listOfMoney[:]