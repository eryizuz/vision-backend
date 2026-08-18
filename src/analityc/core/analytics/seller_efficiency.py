import time

class SellerEfficiency:
    def __init__(self):
        self.interaction_start_times = {} # {seller_id: start_time}
        self.total_interaction_duration = {} # {seller_id: total_seconds}

    def calculate(self, interactions):
        """
        interactions: List of tuples (id1, id2)
        Assuming Seller is ID 0
        """
        seller_id = 0
        is_interacting = False
        
        # Check if seller is in any interaction
        for id1, id2 in interactions:
            if seller_id in (id1, id2):
                is_interacting = True
                break
        
        current_time = time.time()
        
        if is_interacting:
            if seller_id not in self.interaction_start_times:
                self.interaction_start_times[seller_id] = current_time
        else:
            if seller_id in self.interaction_start_times:
                duration = current_time - self.interaction_start_times.pop(seller_id)
                self.total_interaction_duration[seller_id] = self.total_interaction_duration.get(seller_id, 0) + duration
                
        return {
            "is_currently_interacting": is_interacting,
            "total_interaction_seconds": round(self.total_interaction_duration.get(seller_id, 0), 2)
        }
