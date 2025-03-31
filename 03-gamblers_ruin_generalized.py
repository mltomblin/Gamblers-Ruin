import random
from typing import Union, Tuple, List

def simulate_gamblers_ruin(
    i: int,           # Initial money (integer dollars)
    n: int,           # Goal amount (integer dollars)
    j: int,           # Bet size (integer dollars)
    p: float,         # Win probability (must be float between 0 and 1)
    q: Union[int, float] = 1  # Payout multiplier (can be int or float)
) -> Tuple[bool, int, List[int]]:
    """
    Simulates the Gambler's Ruin problem with generalized parameters
    
    Parameters:
    i (int): Initial amount of money in whole dollars
    n (int): Goal amount to reach in whole dollars
    j (int): Size of each bet in whole dollars
    p (float): Probability of winning each game (between 0 and 1)
    q (int or float): Payout multiplier (e.g., 1 means you win what you bet, 2 means double)
    
    Returns:
    tuple: (bool, int, list) - (Whether the gambler won, Number of games, History of money)
    """
    current_money = i  # Start with initial amount
    num_games = 0
    money_history = [current_money]
    
    while current_money > 0 and current_money < n:
        # Make sure bet isn't larger than current money
        bet = min(j, current_money)
        
        # Play one game
        num_games += 1
        if random.random() < p:
            # Win: add winnings (bet * payout multiplier)
            # Convert to int to ensure whole dollar amounts
            current_money += int(bet * q)
        else:
            # Lose: subtract bet amount
            current_money -= bet
        
        money_history.append(current_money)
    
    return current_money >= n, num_games, money_history

def calculate_win_probability(i, n, j, p, q, num_simulations=1000):
    """
    Calculate probability of winning by running multiple simulations
    
    Parameters:
    i (int): Initial amount of money
    n (int): Goal amount
    j (int): Bet size
    p (float): Win probability per game
    q (float): Payout multiplier
    num_simulations (int): Number of simulations to run
    
    Returns:
    tuple: (win_probability, ruin_probability, avg_games)
    """
    wins = 0
    total_games = 0
    
    for _ in range(num_simulations):
        won, games, _ = simulate_gamblers_ruin(i, n, j, p, q)
        wins += 1 if won else 0
        total_games += games
    
    win_probability = wins / num_simulations
    ruin_probability = 1 - win_probability
    avg_games = total_games / num_simulations
    
    return win_probability, ruin_probability, avg_games

def main():
    # Example parameters
    i = 100    # Initial amount ($100)
    n = 200    # Goal amount ($200)
    j = 10     # Bet size ($10)
    p = 0.5    # Probability of winning (50%)
    q = 1      # Payout multiplier (fair odds)
    
    # Run single simulation
    won, games, history = simulate_gamblers_ruin(i, n, j, p, q)
    
    # Print single simulation results
    if won:
        print(f"Example simulation: Gambler won after {games} games!")
    else:
        print(f"Example simulation: Gambler went broke after {games} games.")
    print(f"Money history: {history}")

    # Calculate probabilities from multiple simulations
    win_prob, ruin_prob, avg_games = calculate_win_probability(i, n, j, p, q)
    print(f"\nProbability Analysis (based on multiple simulations):")
    print(f"Probability of winning: {win_prob:.1%}")
    print(f"Probability of ruin: {ruin_prob:.1%}")
    print(f"Average number of games: {avg_games:.1f}")

    # Show theoretical calculations
    expected_value_per_game = (p * q - (1 - p)) * j
    print(f"\nTheoretical analysis:")
    print(f"Expected value per game: ${expected_value_per_game:.2f}")
    if expected_value_per_game > 0:
        print("The game is in the gambler's favor")
    elif expected_value_per_game < 0:
        print("The game is in the house's favor")
    else:
        print("This is a fair game")

if __name__ == "__main__":
    main() 