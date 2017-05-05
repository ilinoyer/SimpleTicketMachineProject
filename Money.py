class Coin(object):

    acceptableCoinValues = [1,2,5,10,20,50,100,200,500]
    coinValue = 0

    def __init__(self, coinValue):
        try:
            self.coinValidator(coinValue)
        except ValueError:
            exit(1)

        self.coinValue = coinValue

    def coinValidator(self, coinValue):
        for x in self.acceptableCoinValues:
            if coinValue == x:
                break
        else:
            raise ValueError


