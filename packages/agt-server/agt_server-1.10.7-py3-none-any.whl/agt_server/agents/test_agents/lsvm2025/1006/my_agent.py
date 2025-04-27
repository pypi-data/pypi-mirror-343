from agt_server.agents.base_agents.lsvm_agent import MyLSVMAgent
from agt_server.local_games.lsvm_arena import LSVMArena
from agt_server.agents.test_agents.lsvm.min_bidder.my_agent import MinBidAgent
from agt_server.agents.test_agents.lsvm.jump_bidder.jump_bidder import JumpBidder
from agt_server.agents.test_agents.lsvm.truthful_bidder.my_agent import TruthfulBidder
import time


NAME = "TA - SECRET"
class MyAgent(MyLSVMAgent):
    def setup(self):
        self.lastNumbRounds = 650
        self.curRoundNumb = 0
        self.notBidding = set() 
    
    def get_space_valuation(self, aloc):
        val = 0
        for i in range(6):
            for j in range(3):
                temp = self.get_space_score(aloc, i, j)
                val += pow(temp, 1.5)
        return val
    
    def get_real_val(self, aloc, roundsRemaining):
        rx = roundsRemaining / self.lastNumbRounds
        spaceVal = self.get_space_valuation(aloc)
        val = self.calc_total_utility(aloc)

        delta = 1 - rx
        return val + delta * spaceVal

    def get_space_score(self, aloc, x, y):
        val = 0
        for a in aloc:
            loc = self.get_location(a, 6)
            if loc[0] == x:
                if loc[1] == y + 1 or loc[1] == y - 1:
                    val += 1
            elif loc[1] == y:
                if loc[0] == x + 1 or loc[0] == x - 1:
                    val += 1
        return val
    
    def get_location(self, s, numC):
        val = ord(s[0]) - ord('A')
        return [val % numC, val // numC]
    
    def bid_func(self, roundsRemaining, s):
        minBids = self.get_min_bids()
        fval = 0.8
        val = 0
        if self.get_current_round() == 0: 
            if self.get_valuation(s) * fval > minBids[s]: 
                val = self.get_valuation(s) * fval
            else:
                val = minBids[s]
        elif s not in self.notBidding:
            currAloc = self.get_tentative_allocation() 
            currAloc = set(currAloc)
            if s in currAloc:
                currAloc.remove(s)
            curVal = self.get_real_val(currAloc, roundsRemaining)
            currAloc.add(s)
            if self.get_real_val(currAloc, roundsRemaining) > curVal + minBids[s]:
                if minBids[s] + (self.get_real_val(currAloc, roundsRemaining) - curVal - minBids[s] * fval) > minBids[s]:
                    val = minBids[s] + (self.get_real_val(currAloc, roundsRemaining) - curVal - minBids[s] * fval)
                else:
                    val = minBids[s]
            else:
                self.notBidding.add(s)
        return val

    def national_bidder(self, roundsRemaining, minBids):
        ret = {}
        for s in minBids.keys():
            val = self.bid_func(roundsRemaining, s)
            if val > 0:
                ret[s] = val
        return ret
    
    def get_bids(self):
        minBids = self.get_min_bids()
        roundsRemaining = self.lastNumbRounds - self.curRoundNumb
        roundsRemaining = max(roundsRemaining, 1)
        ret = {}
        if self.is_national_bidder():  # Assuming this method is defined elsewhere
            ret = self.national_bidder(roundsRemaining, minBids)
        else:
            ret = self.national_bidder(roundsRemaining, minBids)
        return ret
    
    def update(self):
        self.curRoundNumb += 1

################### SUBMISSION #####################
my_agent_submission = MyAgent(NAME)
####################################################

if __name__ == "__main__":
    #### DO NOT TOUCH THIS #####
    agent = MyAgent(NAME)
    arena = LSVMArena(
        num_cycles_per_player = 3,
        timeout=1,
        # local_save_path="saved_games",
        players=[
            agent,
            MyAgent("CP - MyAgent"),
            MyAgent("CP2 - MyAgent"),
            MyAgent("CP3 - MyAgent"),
            MinBidAgent("Min Bidder"), 
            JumpBidder("Jump Bidder"), 
            TruthfulBidder("Truthful Bidder"), 
        ]
    )
    
    start = time.time()
    arena.run()
    end = time.time()
