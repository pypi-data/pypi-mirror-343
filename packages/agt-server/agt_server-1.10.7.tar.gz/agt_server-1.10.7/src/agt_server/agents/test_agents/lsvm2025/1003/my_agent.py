from agt_server.agents.base_agents.lsvm_agent import MyLSVMAgent
from agt_server.local_games.lsvm_arena import LSVMArena
import time
class OverBidder(MyLSVMAgent):
    def setup(self):
        pass

    def get_bids(self):
        min_bids = self.get_min_bids()
        valuations = self.get_valuations() 
        bids = {}
        for good in valuations: 
            if valuations[good] > min_bids[good]:
                bids[good] = 20 * valuations[good]
        
        return bids
    
    def update(self):
        pass

################### SUBMISSION #####################
my_agent_submission = OverBidder("TA - Confidence")
####################################################

if __name__ == "__main__":
    #### DO NOT TOUCH THIS #####
    agent = OverBidder("Overbidder")
    arena = LSVMArena(
        num_cycles_per_player = 5,
        timeout=1,
        # local_save_path="saved_games",
        players=[
            agent,
            OverBidder("Agent_1"),
            OverBidder("Agent_2"),
            OverBidder("Agent_3"),
            OverBidder("Agent_4"), 
            OverBidder("Agent_5"), 
            OverBidder("Agent_6"), 
        ]
    )
    
    start = time.time()
    arena.run()
    end = time.time()
