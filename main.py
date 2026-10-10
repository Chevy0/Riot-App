import random
from collections import deque

class Player:
    def __init__(self, player_id: int, mmr: int):
        self.player_id = player_id
        self.mmr = mmr
        self.wait_time = 0

class Matchmaker:
    def __init__(self, mmr_threshold=50):
        self.queue = deque()
        self.mmr_threshold = mmr_threshold

    def add_player(self, player: Player):
        self.queue.append(player)

    def find_matches(self):
        matches = []
        unmatched = deque()

        while self.queue:
            current_player = self.queue.popleft()
            matched = False

            # Check if any player currently in unmatched fits the MMR window
            for other_player in unmatched:
                if abs(current_player.mmr - other_player.mmr) <= self.mmr_threshold:
                    matches.append((current_player, other_player))
                    unmatched.remove(other_player)
                    matched = True
                    break
            
            if not matched:
                unmatched.append(current_player)

        self.queue = unmatched
        return matches

# Quick Simulation Test
if __name__ == "__main__":
    mm = Matchmaker(mmr_threshold=40)
    
    # Simulate players joining the queue with random MMRs (e.g., Diamond/Master tier)
    print("Simulating Riot Matchmaking Queue...")
    for i in range(10):
        mm.add_player(Player(player_id=i+1, mmr=random.randint(2000, 2300)))

    matches = mm.find_matches()
    print(f"\nSuccessfully formed {len(matches)} lobbies:")
    for idx, (p1, p2) in enumerate(matches, 1):
        print(f"Lobby {idx}: Player {p1.player_id} (MMR {p1.mmr}) vs Player {p2.player_id} (MMR {p2.mmr})")