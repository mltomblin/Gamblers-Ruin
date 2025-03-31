import random

def calculate_bet(current_money, goal, strategy="fixed", base_bet=10, max_bet=10000, losing_streak=0, win_probability=0.5):
    """
    Calculate bet amount based on different strategies
    
    Parameters:
    current_money (int): Current amount of money the gambler has
    goal (int): Target amount to reach
    strategy (str): Betting strategy to use ('fixed', 'percentage', 'martingale', 'inverse_p')
    base_bet (int): Base betting amount for fixed or initial bet
    losing_streak (int): Number of consecutive losses (for inverse_p strategy)
    win_probability (float): Probability of winning (for inverse_p strategy)
    
    Returns:
    int: Amount to bet
    """
    if strategy == "fixed":
        return min(base_bet, current_money, max_bet)
    
    #elif strategy == "percentage":
     #   return max(1, int(current_money * 0.1))
    
    elif strategy == "martingale":
        return min(base_bet, max_bet)
    
    elif strategy == "inverse_p":
        # Increase bet by factor of 1/p for each loss in the streak
        multiplier = (1 / win_probability) ** losing_streak
        return min(int(base_bet * multiplier), current_money, max_bet)
    
    return base_bet

def simulate_gamblers_ruin(initial_money, goal, strategy="fixed", base_bet=10, 
                          win_probability=0.5, max_loan=0, max_bet = 10000):
    """
    Simulates the Gambler's Ruin problem with variable betting and loan capability
    
    Parameters:
    initial_money (int): The amount of money the gambler starts with
    goal (int): The amount of money the gambler aims to reach
    strategy (str): Betting strategy to use ('fixed', 'percentage', 'martingale', 'inverse_p')
    base_bet (int): Base betting amount
    win_probability (float): The probability of winning each game (between 0 and 1)
    max_loan (int): Maximum loan amount available when broke (0 means no loans)
    max_bet (int): Maximum bet amount
    
    Returns:
    tuple: (bool, int, list, int) - (Whether gambler won, Number of games, History of money, Final debt)
    """
    current_money = initial_money
    num_games = 0
    money_history = [current_money]
    current_bet = min(base_bet, max_bet)
    debt = 0
    losing_streak = 0
    
    while (current_money > 0 or debt < max_loan) and current_money < goal:
        # Handle case where gambler is out of money but can take a loan
        if current_money <= 0 and max_loan > 0:
            loan_amount = min(base_bet, max_loan - debt)
            if loan_amount > 0:
                current_money += loan_amount
                debt += loan_amount
        
        # Calculate bet amount based on strategy
        if strategy == "martingale":
            bet_amount = min(current_bet, current_money)
        elif strategy == "inverse_p":
            bet_amount = calculate_bet(current_money, goal, strategy, base_bet, max_bet, 
                                    losing_streak, win_probability)
        else:
            bet_amount = calculate_bet(current_money, goal, strategy, base_bet, max_bet)
        
        # If can't place minimum bet, game over
        if bet_amount <= 0:
            break
            
        # Play one game
        num_games += 1
        if random.random() < win_probability:
            # Win
            current_money += bet_amount
            if strategy == "martingale":
                current_bet = min(base_bet, max_bet)  # Reset to base bet after win
            losing_streak = 0  # Reset losing streak
        else:
            # Lose
            current_money -= bet_amount
            if strategy == "martingale":
                current_bet = current_bet * 2  # Double bet after loss
            losing_streak += 1  # Increment losing streak
        
        money_history.append(current_money)
    
    return current_money >= goal, num_games, money_history, debt

def run_simulation_set(strategy, initial_money, goal, base_bet, win_probability, max_loan, max_bet, num_trials=1):
    """
    Run multiple trials of a simulation with given parameters
    
    Parameters:
    strategy (str): Betting strategy to use
    initial_money (int): Starting money
    goal (int): Target money
    base_bet (int): Base betting amount
    win_probability (float): Probability of winning each game
    max_loan (int): Maximum loan amount (0 for no loans)
    num_trials (int): Number of trials to run
    
    Returns:
    dict: Statistics about the trials
    """
    wins = 0
    total_games = 0
    total_debt = 0
    
    for _ in range(num_trials):
        won, games, history, debt = simulate_gamblers_ruin(
            initial_money, goal, 
            strategy=strategy, 
            base_bet=base_bet, 
            win_probability=win_probability,
            max_loan=max_loan,
            max_bet=10000
        )
        wins += 1 if won else 0
        total_games += games
        total_debt += debt
    
    return {
        'win_rate': wins / num_trials,
        'avg_games': total_games / num_trials,
        'avg_debt': total_debt / num_trials
    }

def main():
    # Example parameters
    initial_money = 100
    goal = 200
    base_bet = 10
    win_probability = 0.5
    max_loan = 50  # Amount available for loan scenarios
    num_trials = 100  # Run multiple trials for more reliable statistics
    
    # Try different strategies
    strategies = ["fixed", "martingale", "inverse_p"]
    
    print("\nComparing strategies with and without loans:")
    print("-" * 50)
    
    for strategy in strategies:
        print(f"\n{strategy.upper()} STRATEGY:")
        
        # Run without loans
        no_loan_results = run_simulation_set(
            strategy, initial_money, goal, base_bet, 
            win_probability, max_loan=0, max_bet=10000, num_trials=num_trials
        )

        # Run without loans and with binding max bet
        max_bet_results = run_simulation_set(
            strategy, initial_money, goal, base_bet, 
            win_probability, max_loan=0, max_bet=50, num_trials=num_trials
        )

        # Run with loans
        with_loan_results = run_simulation_set(
            strategy, initial_money, goal, base_bet, 
            win_probability, max_loan=max_loan, max_bet=10000, num_trials=num_trials
        )
        
        # Run with loans and with binding max bet
        max_bet_loan_results = run_simulation_set(
            strategy, initial_money, goal, base_bet, 
            win_probability, max_loan=max_loan, max_bet=50, num_trials=num_trials
        )

        # Print comparison
        print("\nWithout loans:")
        print(f"Win rate: {no_loan_results['win_rate']:.1%}")
        print(f"Average games played: {no_loan_results['avg_games']:.1f}")
        print(f"Average final debt: ${no_loan_results['avg_debt']:.2f}")

        print("\nWithout loans and with binding max bet:")
        print(f"Win rate: {max_bet_results['win_rate']:.1%}")
        print(f"Average games played: {max_bet_results['avg_games']:.1f}")
        print(f"Average final debt: ${max_bet_results['avg_debt']:.2f}")
        
        print("\nWith ${} loan available:".format(max_loan))
        print(f"Win rate: {with_loan_results['win_rate']:.1%}")
        print(f"Average games played: {with_loan_results['avg_games']:.1f}")
        print(f"Average final debt: ${with_loan_results['avg_debt']:.2f}")

        print("\nWith ${} loan available and binding max bet:".format(max_loan))
        print(f"Win rate: {max_bet_loan_results['win_rate']:.1%}")
        print(f"Average games played: {max_bet_loan_results['avg_games']:.1f}")
        print(f"Average final debt: ${max_bet_loan_results['avg_debt']:.2f}")
        
        # Calculate the difference
        win_rate_change = with_loan_results['win_rate'] - no_loan_results['win_rate']
        print(f"\nDifference in win rate (Loans): {win_rate_change:+.1%}")
        print(f"Difference in win rate (Max bet, no loans): {max_bet_results['win_rate'] - no_loan_results['win_rate']:+.1%}")
        print(f"Difference in win rate (Max bet, loans): {max_bet_loan_results['win_rate'] - with_loan_results['win_rate']:+.1%}")
if __name__ == "__main__":
    main() 