import http.server
import json
import random
from typing import Union, Tuple, List
from urllib.parse import parse_qs, urlparse

def simulate_gamblers_ruin(i: int, n: int, j: int, p: float, q: Union[int, float] = 1) -> Tuple[bool, int, List[int]]:
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
    wins = 0
    total_games = 0
    sample_history = []
    
    for sim in range(num_simulations):
        won, games, history = simulate_gamblers_ruin(i, n, j, p, q)
        wins += 1 if won else 0
        total_games += games
        if sim == 0:  # Keep one sample history for visualization
            sample_history = history
    
    win_probability = wins / num_simulations
    ruin_probability = 1 - win_probability
    avg_games = total_games / num_simulations
    
    return win_probability, ruin_probability, avg_games, sample_history

class GamblerUI(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>Interactive Gambler's Ruin Simulator</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
                    .container { display: flex; gap: 20px; }
                    .controls { flex: 1; padding: 20px; border: 1px solid #ddd; }
                    .results { flex: 2; padding: 20px; border: 1px solid #ddd; }
                    .form-group { margin-bottom: 15px; }
                    label { display: block; margin-bottom: 5px; }
                    input[type="range"] { width: 100%; }
                    .value-display { display: inline-block; margin-left: 10px; }
                    #graph { width: 100%; height: 400px; }
                </style>
            </head>
            <body>
                <h1>Interactive Gambler's Ruin Simulator</h1>
                <div class="container">
                    <div class="controls">
                        <h2>Parameters</h2>
                        <div class="form-group">
                            <label for="initial_money">Initial Money: <span id="initial_money_value">100</span></label>
                            <input type="range" id="initial_money" min="10" max="500" value="100" step="10">
                        </div>
                        <div class="form-group">
                            <label for="goal">Goal Amount: <span id="goal_value">200</span></label>
                            <input type="range" id="goal" min="20" max="1000" value="200" step="10">
                        </div>
                        <div class="form-group">
                            <label for="bet_size">Bet Size: <span id="bet_size_value">10</span></label>
                            <input type="range" id="bet_size" min="1" max="50" value="10" step="1">
                        </div>
                        <div class="form-group">
                            <label for="win_probability">Win Probability: <span id="win_probability_value">0.5</span></label>
                            <input type="range" id="win_probability" min="0.1" max="0.9" value="0.5" step="0.1">
                        </div>
                        <button onclick="runSimulation()">Run Simulation</button>
                    </div>
                    <div class="results">
                        <h2>Results</h2>
                        <div id="graph"></div>
                        <div id="stats"></div>
                    </div>
                </div>

                <script>
                    // Update displayed values as sliders move
                    document.querySelectorAll('input[type="range"]').forEach(input => {
                        input.oninput = () => {
                            document.getElementById(input.id + '_value').textContent = input.value;
                        }
                    });

                    // Run simulation and update results
                    function runSimulation() {
                        const params = {
                            initial_money: document.getElementById('initial_money').value,
                            goal: document.getElementById('goal').value,
                            bet_size: document.getElementById('bet_size').value,
                            win_probability: document.getElementById('win_probability').value
                        };

                        fetch('/calculate_probability?' + new URLSearchParams(params))
                            .then(response => response.json())
                            .then(data => {
                                // Update stats
                                document.getElementById('stats').innerHTML = `
                                    <h3>Statistics</h3>
                                    <p>Win Probability: ${(data.win_probability * 100).toFixed(1)}%</p>
                                    <p>Ruin Probability: ${(data.ruin_probability * 100).toFixed(1)}%</p>
                                    <p>Average Games: ${data.average_games.toFixed(1)}</p>
                                `;

                                // Create graph
                                const trace = {
                                    y: data.parameters.money_history,
                                    type: 'line',
                                    name: 'Money'
                                };

                                const layout = {
                                    title: 'Sample Game Progression',
                                    yaxis: { title: 'Money ($)' },
                                    xaxis: { title: 'Game Number' }
                                };

                                Plotly.newPlot('graph', [trace], layout);
                            });
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
            
        elif parsed_path.path == '/calculate_probability':
            try:
                params = parse_qs(parsed_path.query)
                i = int(params.get('initial_money', ['100'])[0])
                n = int(params.get('goal', ['200'])[0])
                j = int(params.get('bet_size', ['10'])[0])
                p = float(params.get('win_probability', ['0.5'])[0])
                q = 1  # Fixed payout for simplicity
                
                win_prob, ruin_prob, avg_games, history = calculate_win_probability(i, n, j, p, q)
                
                response = {
                    'win_probability': win_prob,
                    'ruin_probability': ruin_prob,
                    'average_games': avg_games,
                    'parameters': {
                        'money_history': history
                    }
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except (ValueError, KeyError) as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, GamblerUI)
    print('Server running on port 8000...')
    httpd.serve_forever() 