import random
import matplotlib.pyplot as plt

def simulate_gamblers_ruin(initial_money, goal, bet_amount, win_probability):
    """
    Simulates the Gambler's Ruin problem
    
    Parameters:
    initial_money (int): The amount of money the gambler starts with
    goal (int): The amount of money the gambler aims to reach
    bet_amount (int): The amount of money wagered in each game
    win_probability (float): The probability of winning each game (between 0 and 1)
    
    Returns:
    tuple: (bool, int, list) - (Whether the gambler won, Number of games, History of money)
    """
    current_money = initial_money
    num_games = 0
    money_history = [current_money]
    
    while current_money > 0 and current_money < goal:
        # Play one game
        num_games += 1
        if random.random() < win_probability:
            # Win
            current_money += bet_amount
        else:
            # Lose
            current_money -= bet_amount
        
        money_history.append(current_money)
    
    return current_money >= goal, num_games, money_history

def calculate_probabilities(initial_money, goal, bet_amount, win_probability, num_simulations=1000):
    """
    Calculate winning and ruin probabilities through simulation
    
    Returns:
    tuple: (win_probability, ruin_probability, avg_games, game_counts)
    """
    wins = 0
    total_games = 0
    game_counts = []  # Track number of games for each simulation
    
    for _ in range(num_simulations):
        won, games, _ = simulate_gamblers_ruin(initial_money, goal, bet_amount, win_probability)
        wins += 1 if won else 0
        total_games += games
        game_counts.append(games)
    
    win_probability = wins / num_simulations
    ruin_probability = 1 - win_probability
    avg_games = total_games / num_simulations
    
    return win_probability, ruin_probability, avg_games, game_counts

def plot_distribution(game_counts):
    """
    Create a histogram of the number of games played
    """
    plt.figure(figsize=(10, 6))
    plt.hist(game_counts, bins=50, edgecolor='black')
    plt.title('Distribution of Number of Games Until Win/Ruin')
    plt.xlabel('Number of Games')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    # Example parameters
    initial_money = 100  # Starting with $100
    goal = 200          # Trying to reach $200
    bet_amount = 10     # Betting $10 each game
    win_probability = 0.4  # 50% chance of winning each game
    
    # Run one example simulation
    won, games, history = simulate_gamblers_ruin(initial_money, goal, bet_amount, win_probability)
    
    # Print example simulation results
    if won:
        print(f"Example simulation: Gambler won after {games} games!")
    else:
        print(f"Example simulation: Gambler went broke after {games} games.")
    print(f"Money history: {history}")

    # Calculate probabilities from multiple simulations
    win_prob, ruin_prob, avg_games, game_counts = calculate_probabilities(
        initial_money, goal, bet_amount, win_probability
    )
    
    print(f"\nProbability Analysis (based on 1000 simulations):")
    print(f"Probability of winning: {win_prob:.1%}")
    print(f"Probability of ruin: {ruin_prob:.1%}")
    print(f"Average number of games: {avg_games:.1f}")

    # Show theoretical calculations
    expected_value_per_game = (win_probability - (1 - win_probability)) * bet_amount
    print(f"\nTheoretical analysis:")
    print(f"Expected value per game: ${expected_value_per_game:.2f}")
    if expected_value_per_game > 0:
        print("The game is in the gambler's favor")
    elif expected_value_per_game < 0:
        print("The game is in the house's favor")
    else:
        print("This is a fair game")

    # Plot the distribution of game counts
    plot_distribution(game_counts)

if __name__ == "__main__":
    main() 