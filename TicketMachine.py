from Money import Coin


class TicketMachine(object):
    dictOfavailableMoney = {500 : 10, 200 :10, 100 : 10, 50 : 10, 20 : 10, 10 : 10, 5 : 10, 2 :10, 1:10 }
    listOfPaidOutMoney = list()


    def handleTransaction(self, transaction):
        transaction.calcDifference()
        self.updatingAvailableMoney(transaction)
        transaction.resetMoneyList()
        tempDiff = transaction.difference
        self.giveTheChange(transaction,tempDiff)


    def updatingAvailableMoney(self,transaction):
        transaction.listOfMoneyPaidInto = [i for i in transaction.listOfMoney]
        for x in transaction.listOfMoney:
            self.dictOfavailableMoney[x.coinValue] = self.dictOfavailableMoney.get(x.coinValue) + 1


    def cancleTransaction(self, transaction):
        for x in self.listOfPaidOutMoney:
            self.dictOfavailableMoney[x.coinValue] = self.dictOfavailableMoney.get(x.coinValue) + 1
        del self.listOfPaidOutMoney[:]
        transaction.resetMoneyList()



    def giveTheChange(self, transaction, diff):

        for x in range(6):
            count = 0;
            tempDiff = diff
            for k,v in self.dictOfavailableMoney.items():
                if count >= x :
                    while tempDiff >= k and v > 0 and tempDiff > 0:
                        tempDiff = tempDiff - int(k)
                        print(tempDiff)
                        self.listOfPaidOutMoney.append(Coin(int(k)))
                        self.dictOfavailableMoney[k] = self.dictOfavailableMoney.get(k) - 1
                        transaction.payInto(int(k))
                count+=1

            if tempDiff == 0:
                break;
            else:
                self.cancleTransaction(transaction)


        if tempDiff == 0:
            transaction.setCorrectness(True)
        else:
            self.cancleTransaction(transaction)
            for x in transaction.listOfMoneyPaidInto:
                self.dictOfavailableMoney[x.coinValue] = self.dictOfavailableMoney.get(x.coinValue) - 1
            transaction.setCorrectness(False)
