from agt_server.agents.base_agents.lsvm_agent import MyLSVMAgent
from agt_server.local_games.lsvm_arena import LSVMArena
from agt_server.agents.test_agents.lsvm.min_bidder.my_agent import MinBidAgent
from agt_server.agents.test_agents.lsvm.jump_bidder.jump_bidder import JumpBidder
from agt_server.agents.test_agents.lsvm.truthful_bidder.my_agent import TruthfulBidder
import time
import random
from .path_utils import path_from_local_root


NAME = "TA - RANDOM"
class MyAgent(MyLSVMAgent):
    def setup(self):
        self.filename = path_from_local_root("test.txt")
        self.file = open(self.filename, 'r+')

    def get_bids(self):
        min_bids = self.get_min_bids()
        valuations = self.get_valuations() 
        bids = {}
        weight = int(self.file.read(1))
        self.file.seek(0)
        for good in valuations: 
            if valuations[good] > min_bids[good]:
                bids[good] = min_bids[good] + (weight * (valuations[good] - min_bids[good]))
        return bids
    
    def update(self):
        weight = random.random()
        self.file.write(str(weight))
        self.file.truncate()
        self.file.seek(0)

################### SUBMISSION #####################
my_agent_submission = MyAgent(NAME)
####################################################

if __name__ == "__main__":
    ### DO NOT TOUCH THIS #####
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
