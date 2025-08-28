import random
import math

def calculate_strength(x):
    return math.log2(x + 1) + (x / 10)

def calculate_utility(max_val, min_val):
    random_factor = random.randint(0, 1)
    random_modifier = random.randint(1, 10) / 10
    return round(calculate_strength(max_val) - calculate_strength(min_val) + ((-1) ** random_factor) * random_modifier, 2)

# Task --> 1
class ChessGame:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        
    def minimax_with_pruning(self, depth, current_player_is_max, max_player_strength, min_player_strength, alpha, beta):
        if depth == 0:
            return calculate_utility(max_player_strength, min_player_strength)
            
        if current_player_is_max:
            max_eval = float('-inf')
            for i in range(2):  
                eval_value = self.minimax_with_pruning(depth - 1, False, 
                                                      max_player_strength, min_player_strength, 
                                                      alpha, beta)
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break 
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(2):  
                eval_value = self.minimax_with_pruning(depth - 1, True, 
                                                      max_player_strength, min_player_strength, 
                                                      alpha, beta)
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break 
            return min_eval
    
    def simulate_match(self, p1_name, p2_name, p1_strength, p2_strength, starting_player, game_number):
        game_parity = game_number % 2
        p1_is_maximizing = (starting_player == 0 and game_parity == 0) or (starting_player == 1 and game_parity == 1)
        
        if p1_is_maximizing:
            max_player, min_player = p1_name, p2_name
            max_strength, min_strength = p1_strength, p2_strength
        else:
            max_player, min_player = p2_name, p1_name
            max_strength, min_strength = p2_strength, p1_strength
        
        utility = self.minimax_with_pruning(self.max_depth, True, max_strength, min_strength, float('-inf'), float('inf'))
        
        if utility > 0:
            return utility, max_player, "Max"
        elif utility < 0:
            return utility, min_player, "Min"
        else:
            return utility, "Draw", ""

tournament = ChessGame()

starting_player = int(input("Enter starting player for game 1 (0 for Carlsen, 1 for Caruana): "))
carlsen_strength = float(input("Enter base strength for Carlsen: "))
caruana_strength = float(input("Enter base strength for Caruana: "))
print()

carlsen_wins = caruana_wins = draws = 0

for game_num in range(4):
    utility, winner, role = tournament.simulate_match(
        "Magnus Carlsen", "Fabiano Caruana",
        carlsen_strength, caruana_strength,
        starting_player, game_num
    )
    
    if winner == "Draw":
        print(f"Game {game_num+1} Result: Draw (Utility value: {utility})")
        draws += 1
    else:
        print(f"Game {game_num+1} Winner: {winner} ({role}) (Utility value: {utility})")
        if winner == "Magnus Carlsen":
            carlsen_wins += 1
        else:
            caruana_wins += 1

print("\nTournament Results:")
print(f"Magnus Carlsen Wins: {carlsen_wins}")
print(f"Fabiano Caruana Wins: {caruana_wins}")
print(f"Draws: {draws}")

if carlsen_wins > caruana_wins:
    print("Overall Winner: Magnus Carlsen")
elif caruana_wins > carlsen_wins:
    print("Overall Winner: Fabiano Caruana")
else:
    print("Overall Result: Draw")

# Task --> 2
# class DeathNoteGame:
#     def __init__(self, max_depth=3):
#         self.max_depth = max_depth
    
#     def standard_minimax(self, depth, is_max_player, max_strength, min_strength, alpha, beta):
#         if depth == 0:
#             return calculate_utility(max_strength, min_strength)
            
#         if is_max_player:
#             best_val = float('-inf')
#             for i in range(2):
#                 eval_val = self.standard_minimax(depth-1, False, max_strength, min_strength, alpha, beta)
#                 best_val = max(best_val, eval_val)
#                 alpha = max(alpha, eval_val)
#                 if beta <= alpha:
#                     break
#             return best_val
#         else:
#             best_val = float('inf')
#             for i in range(2):
#                 eval_val = self.standard_minimax(depth-1, True, max_strength, min_strength, alpha, beta)
#                 best_val = min(best_val, eval_val)
#                 beta = min(beta, eval_val)
#                 if beta <= alpha:
#                     break
#             return best_val
    
#     def mind_control_minimax(self, depth, is_max_player, max_strength, min_strength, alpha, beta):
#         if depth == 0:
#             return calculate_utility(max_strength, min_strength)
            
#         best_val = float('-inf')
#         for i in range(2):
#             eval_val = self.mind_control_minimax(depth-1, True, max_strength, min_strength, alpha, beta)
#             best_val = max(best_val, eval_val)
#             alpha = max(alpha, eval_val)
#             if beta <= alpha and is_max_player: 
#                 break
#         return best_val
        
#     def analyze_mind_control_strategy(self, max_player, min_player, max_strength, min_strength, mind_control_cost):
#         normal_utility = self.standard_minimax(
#             self.max_depth, True, max_strength, min_strength, float('-inf'), float('inf')
#         )
        
#         mind_control_utility = self.mind_control_minimax(
#             self.max_depth, True, max_strength, min_strength, float('-inf'), float('inf')
#         )
        
#         final_mind_control_utility = mind_control_utility - mind_control_cost
        
#         print(f"Minimax value without Mind Control: {normal_utility:.2f}")
#         print(f"Minimax value with Mind Control: {mind_control_utility:.2f}")
#         print(f"Minimax value with Mind Control after incurring the cost: {final_mind_control_utility:.2f}")
        
#         if normal_utility > 0:
#             if final_mind_control_utility > 0:
#                 print(f"{max_player} should NOT use Mind Control as the position is already winning.")
#             else:
#                 print(f"{max_player} should NOT use Mind Control as it backfires.")
#         else:
#             if final_mind_control_utility > 0:
#                 print(f"{max_player} should use Mind Control.")
#             else:
#                 print(f"{max_player} should NOT use Mind Control as the position is losing either way.")

# game = DeathNoteGame()

# starting_player = int(input("Enter who goes first (0 for Light, 1 for L): "))
# mind_control_cost = float(input("Enter the cost of using Mind Control: "))
# light_strength = float(input("Enter base strength for Light: "))
# l_strength = float(input("Enter base strength for L: "))

# if starting_player == 0:
#     max_player, min_player = "Light", "L"
#     max_strength, min_strength = light_strength, l_strength
# else:
#     max_player, min_player = "L", "Light"
#     max_strength, min_strength = l_strength, light_strength

# game.analyze_mind_control_strategy(max_player, min_player, max_strength, min_strength, mind_control_cost)


