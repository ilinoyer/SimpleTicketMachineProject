class Ticket(object):
    valuesOfTicket = [140, 190,250,280,380,500]
    value = 0

    def __init__(self,x):
         self.value = self.valuesOfTicket[x]


