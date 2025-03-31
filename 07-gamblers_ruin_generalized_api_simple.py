import http.server
import json
import random
from typing import Union, Tuple, List
from urllib.parse import parse_qs, urlparse

def simulate_gamblers_ruin(
    i: int,
    n: int,
    j: int,
    p: float,
    q: Union[int, float] = 1
) -> Tuple[bool, int, List[int]]:
    """
    Original simulation function
    """
    current_money = i
    num_games = 0
    money_history = [current_money]
    
    while current_money > 0 and current_money < n:
        bet = min(j, current_money)
        num_games += 1
        if random.random() < p:
            current_money += int(bet * q)
        else:
            current_money -= bet
        money_history.append(current_money)
    
    return current_money >= n, num_games, money_history

def calculate_win_probability(i, n, j, p, q, num_simulations=1000):
    """
    Original probability calculation function
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

class GamblerAPI(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Serve the form page for root URL
        if parsed_path.path == '/' or parsed_path.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Create HTML form
            html = """
            <html>
            <head>
                <title>Gambler's Ruin Calculator</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .form-group { margin-bottom: 15px; }
                    label { display: inline-block; width: 150px; }
                    input { padding: 5px; width: 100px; }
                    button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                    #result { margin-top: 20px; padding: 10px; border: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <h1>Gambler's Ruin Probability Calculator</h1>
                <form action="/calculate_probability" method="get">
                    <div class="form-group">
                        <label for="initial_money">Initial Money ($):</label>
                        <input type="number" id="initial_money" name="initial_money" value="100">
                    </div>
                    <div class="form-group">
                        <label for="goal">Goal Amount ($):</label>
                        <input type="number" id="goal" name="goal" value="200">
                    </div>
                    <div class="form-group">
                        <label for="bet_size">Bet Size ($):</label>
                        <input type="number" id="bet_size" name="bet_size" value="10">
                    </div>
                    <div class="form-group">
                        <label for="win_probability">Win Probability:</label>
                        <input type="number" id="win_probability" name="win_probability" value="0.5" step="0.1" min="0" max="1">
                    </div>
                    <div class="form-group">
                        <label for="payout">Payout Multiplier:</label>
                        <input type="number" id="payout" name="payout" value="1" step="0.1">
                    </div>
                    <div class="form-group">
                        <label for="num_simulations">Number of Simulations:</label>
                        <input type="number" id="num_simulations" name="num_simulations" value="1000">
                    </div>
                    <button type="submit">Calculate Probabilities</button>
                </form>
                <div id="result"></div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
            
        elif parsed_path.path == '/calculate_probability':
            params = parse_qs(parsed_path.query)
            
            try:
                # Extract parameters with default values
                i = int(params.get('initial_money', ['100'])[0])
                n = int(params.get('goal', ['200'])[0])
                j = int(params.get('bet_size', ['10'])[0])
                p = float(params.get('win_probability', ['0.5'])[0])
                q = float(params.get('payout', ['1'])[0])
                num_simulations = int(params.get('num_simulations', ['1000'])[0])
                
                # Validate parameters
                if not 0 < p < 1:
                    raise ValueError('Win probability must be between 0 and 1')
                if i <= 0 or n <= i or j <= 0:
                    raise ValueError('Invalid money parameters')
                
                # Calculate probabilities
                win_prob, ruin_prob, avg_games = calculate_win_probability(
                    i, n, j, p, q, num_simulations
                )
                
                # Create HTML response
                response_html = f"""
                <html>
                <head>
                    <title>Results - Gambler's Ruin Calculator</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                        .result {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                        .back-button {{ margin-top: 20px; }}
                    </style>
                </head>
                <body>
                    <h1>Calculation Results</h1>
                    <div class="result">
                        <h2>Probabilities:</h2>
                        <p>Win Probability: {win_prob:.1%}</p>
                        <p>Ruin Probability: {ruin_prob:.1%}</p>
                        <p>Average Number of Games: {avg_games:.1f}</p>
                        
                        <h2>Parameters Used:</h2>
                        <p>Initial Money: ${i}</p>
                        <p>Goal: ${n}</p>
                        <p>Bet Size: ${j}</p>
                        <p>Win Probability: {p}</p>
                        <p>Payout Multiplier: {q}</p>
                        <p>Simulations Run: {num_simulations}</p>
                    </div>
                    <div class="back-button">
                        <a href="/">← Back to Calculator</a>
                    </div>
                </body>
                </html>
                """
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response_html.encode())
                
            except (ValueError, KeyError) as e:
                # Handle errors
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            # Handle invalid endpoints
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())

if __name__ == '__main__':
    # Start the server
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, GamblerAPI)
    print('Server running on port 8000...')
    httpd.serve_forever() 