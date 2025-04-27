import numpy as np
from agt_server.agents.base_agents.lsvm_agent import MyLSVMAgent
from agt_server.local_games.lsvm_arena import LSVMArena
from agt_server.agents.test_agents.lsvm.min_bidder.my_agent import MinBidAgent
from agt_server.agents.test_agents.lsvm.jump_bidder.jump_bidder import JumpBidder
from agt_server.agents.test_agents.lsvm.truthful_bidder.my_agent import TruthfulBidder
import time
import os
import gzip
import json
from .path_utils import path_from_local_root
import random

NAME = "PW - Hot'n'Cold"

class MyAgent(MyLSVMAgent):
    def setup(self):
        """
        - Bid aggressively on items where we have a high true value relative to the distribution; otherwise bid passively
        - Identify whether an item on the grid has an aggressive bidder or not by bidding a medium-range jump bid; this will 
            beat out all passive bidders but not any aggressive bidders, so if we are not winning the item in round 1 then 
            there must be an aggressive bidder
        - When we reach close to our true item values in the items with the aggressive bidders, we then decide whether we 
            attempt to outbid them; if removing this item from that bidder's winnings (based on the current tentative 
            allocations) would reduce the aggressive bidders' value significantly, we know this would split a region of the 
            opponent's winning bundle into 2 smaller regions that aren't connected, so we start to bid more aggressively to 
            try and sabotage that opponent
        """
        # Define variables relating to information-gathering
        self.is_opponent_aggressive = dict()
        self.play_aggressive = dict()
        
        # Define thresholds for us to choose aggressive versus passive bidding
        self.distribution_threshold_national = 7
        self.distribution_threshold_regional = 9
        self.passive_bidding_factor = 1.1
        self.aggressive_bidding_factor_national = 4
        self.aggressive_bidding_factor_regional = 2.5
        self.aggressive_initial_jump_bid_factor = 0.95

        # Define thresholds to identify aggressive versus passive opponents
        self.initial_bid_national = 4
        self.initial_bid_regional = 4

        # Define thresholds to swap to aggressive bidding for spatial reasons
        self.self_swap_factor = 1.5
        self.opponent_swap_factor = 2
        self.min_items_in_bundle = 4

    def national_bidder_strategy(self):
        min_bids = self.get_min_bids()
        valuations = self.get_valuations(self.get_goods())
        goods = self.get_goods()
        tentative_allocation_goods = self.get_tentative_allocation()
        prior_bids = self.get_previous_bid_map()

        bids = dict()

        # Iterate through each item
        for good in goods:
            if self.get_current_round() == 0:
                # Bid the initial bid to get information, or aggressively if we have a high value
                if valuations[good] >= self.distribution_threshold_national:
                    self.play_aggressive[good] = True
                    bids[good] = self.aggressive_initial_jump_bid_factor * valuations[good]
                else:
                    self.play_aggressive[good] = False
                    bids[good] = min(self.initial_bid_national, valuations[good])

            else:
                if self.get_current_round() == 1:
                    # Gather information about aggressive vs passive for each item right after first round
                    if good not in tentative_allocation_goods:
                        self.is_opponent_aggressive[good] = True
                    else:
                        self.is_opponent_aggressive[good] = False
                        self.play_aggressive[good] = True

                # If we already own the good, hold our bid
                if good in tentative_allocation_goods and good in prior_bids:
                    bids[good] = prior_bids[good]
                
                else:
                    # Verify if we want to swap to an aggressive strategy to block off an opponent
                    prior_winners = self.get_previous_winners_map()
                    curr_item_prior_winner = prior_winners[good]
                    prior_winner_bundle = set()

                    for winners_good in prior_winners:
                        if prior_winners[winners_good] == curr_item_prior_winner:
                            prior_winner_bundle.add(winners_good)
                    
                    curr_winner_value = self.calc_total_valuation(prior_winner_bundle)
                    prior_winner_bundle.remove(good)
                    curr_winner_value_minus_curr_item = self.calc_total_valuation(prior_winner_bundle)

                    if len(prior_winner_bundle) > self.min_items_in_bundle \
                         and (curr_winner_value_minus_curr_item == 0 
                              or curr_winner_value / curr_winner_value_minus_curr_item >= self.opponent_swap_factor):
                        self.play_aggressive[good] = True

                    # Verify if we want to swap to an aggressive strategy to secure ourself a better partition
                    curr_self_value = self.calc_total_valuation(tentative_allocation_goods)
                    tentative_allocation_goods.add(good)
                    curr_self_value_with_curr_item = self.calc_total_valuation(tentative_allocation_goods)

                    if len(prior_winner_bundle) > self.min_items_in_bundle \
                        and (curr_self_value == 0 
                             or curr_self_value_with_curr_item / curr_self_value >= self.self_swap_factor):
                        self.play_aggressive[good] = True

                    # Normal round strategy
                    if self.play_aggressive[good]:
                        max_valuation = valuations[good] * self.aggressive_bidding_factor_national
                        if min_bids[good] <= max_valuation:
                            bids[good] = random.random() * (max_valuation - min_bids[good]) + min_bids[good]
                    else:
                        max_valuation = valuations[good] * self.passive_bidding_factor
                        if min_bids[good] <= max_valuation:
                            bids[good] = min_bids[good]

        return bids

    def regional_bidder_strategy(self):
        min_bids = self.get_min_bids()
        valuations = self.get_valuations(self.get_goods())
        nearby_goods = self.get_goods_in_proximity()
        tentative_allocation_goods = self.get_tentative_allocation()
        prior_bids = self.get_previous_bid_map()

        bids = dict()

        # Iterate through each item
        for good in nearby_goods:
            if self.get_current_round() == 0:
                # Bid the initial bid to get information, or aggressively if we have a high value
                if valuations[good] >= self.distribution_threshold_regional:
                    self.play_aggressive[good] = True
                    bids[good] = self.aggressive_initial_jump_bid_factor * valuations[good]
                else:
                    self.play_aggressive[good] = False
                    bids[good] = min(self.initial_bid_regional, valuations[good])
            
            else:
                if self.get_current_round() == 1:
                    # Gather information about aggressive vs passive for each item right after first round
                    if good not in tentative_allocation_goods:
                        self.is_opponent_aggressive[good] = True
                    else:
                        self.is_opponent_aggressive[good] = False
                        self.play_aggressive[good] = True

                # If we already own the good, hold our bid
                if good in tentative_allocation_goods and good in prior_bids:
                    bids[good] = prior_bids[good]
                
                else:
                    # Verify if we want to swap to an aggressive strategy to block off an opponent
                    prior_winners = self.get_previous_winners_map()
                    curr_item_prior_winner = prior_winners[good]
                    prior_winner_bundle = set()

                    for winners_good in prior_winners:
                        if prior_winners[winners_good] == curr_item_prior_winner:
                            prior_winner_bundle.add(winners_good)
                    
                    curr_winner_value = self.calc_total_valuation(prior_winner_bundle)
                    prior_winner_bundle.remove(good)
                    curr_winner_value_minus_curr_item = self.calc_total_valuation(prior_winner_bundle)

                    if len(prior_winner_bundle) > self.min_items_in_bundle \
                         and (curr_winner_value_minus_curr_item == 0 
                              or curr_winner_value / curr_winner_value_minus_curr_item >= self.opponent_swap_factor):
                        self.play_aggressive[good] = True

                    # Verify if we want to swap to an aggressive strategy to secure ourself a better partition
                    curr_self_value = self.calc_total_valuation(tentative_allocation_goods)
                    tentative_allocation_goods.add(good)
                    curr_self_value_with_curr_item = self.calc_total_valuation(tentative_allocation_goods)

                    if len(prior_winner_bundle) > self.min_items_in_bundle \
                        and (curr_self_value == 0 
                             or curr_self_value_with_curr_item / curr_self_value >= self.self_swap_factor):
                        self.play_aggressive[good] = True

                    # Normal round strategy
                    if self.play_aggressive[good]:
                        max_valuation = valuations[good] * self.aggressive_bidding_factor_regional
                        if min_bids[good] <= max_valuation:
                            bids[good] = random.random() * (max_valuation - min_bids[good]) + min_bids[good]
                    else:
                        max_valuation = valuations[good] * self.passive_bidding_factor
                        if min_bids[good] <= max_valuation:
                            bids[good] = min_bids[good]

        return bids

    def get_bids(self):
        if self.is_national_bidder():
            return self.national_bidder_strategy()
        else:
            return self.regional_bidder_strategy()

    def update(self):
        pass
        # self.current_round = self.get_current_round()
        # self.current_prices = self.get_current_prices_map()
        # self.winner_history = self.get_winner_history_map()
        # self.recent_util = self.get_previous_util()
        # if not self.is_national:
        #     self.nearby_goods = self.get_goods_in_proximity()
        # self.adjust_bidding_strategy()

    # def proximity(self, goods, regional_good):
    #     # Correct handling of the proximity method
    #     return np.where(goods == regional_good)[0]

################### SUBMISSION #####################
my_agent_submission = MyAgent(NAME)
####################################################

# Additional functions and main definition as previously defined.

def process_saved_game(filepath): 
    """ 
    Here is some example code to load in a saved game in the format of a json.gz and to work with it
    """
    
    # NOTE: Data is a dictionary mapping 
    with gzip.open(filepath, 'rt', encoding='UTF-8') as f:
        game_data = json.load(f)
        for agent, agent_data in game_data.items(): 
            if agent_data['valuations'] is not None: 
                # agent is the name of the agent whose data is being processed 
                agent = agent 
                
                # bid_history is the bidding history of the agent as a list of maps from good to bid
                bid_history = agent_data['bid_history']
                
                # price_history is the price history of the agent as a list of maps from good to price
                price_history = agent_data['price_history']
                
                # util_history is the history of the agent's previous utilities 
                util_history = agent_data['util_history']
                
                # winner_history is the history of the previous tentative winners of all goods as a list of maps from good to winner
                winner_history = agent_data['winner_history']
                
                # elo is the agent's elo as a string
                elo = agent_data['elo']
                
                # is_national_bidder is a boolean indicating whether or not the agent is a national bidder in this game 
                is_national_bidder = agent_data['is_national_bidder']
                
                # valuations is the valuations the agent received for each good as a map from good to valuation
                valuations = agent_data['valuations']
                
                # regional_good is the regional good assigned to the agent 
                # This is None in the case that the bidder is a national bidder 
                regional_good = agent_data['regional_good']
            
            # TODO: If you are planning on learning from previously saved games enter your code below. 

if __name__ == "__main__":

    ### DO NOT TOUCH THIS #####
    agent = MyAgent(NAME)
    arena = LSVMArena(
        num_cycles_per_player = 3,
        timeout=1,
        local_save_path="saved_games",
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
