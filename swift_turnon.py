# -*- coding: utf-8 -*
import ro_to_xf_to_ro as ro
import time
class turnsw():
    flag=False
    def turnon(self):
        print("我开开了")
    def turnoff(self):
        print("我又关上了")
    def swiftturn(self):

        if(self.flag):
            self.turnoff()
            self.flag=False
        else:
            self.turnon()
            self.flag=True
if (
        __name__ == "__main__"):
    tu=turnsw()
    tu.swiftturn()