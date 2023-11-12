from flask import Flask, render_template_string, request

def is_valid_2x2_matrix(matrix):
    """Validate if the provided matrix is 2x2."""
    return len(matrix) == 2 and all(len(row) == 2 for row in matrix)

def nash_equilibrium(playerA_matrix, playerB_matrix):
    """Find the Nash equilibria for general 2x2 games."""
    # Validate the input matrices
    if not (is_valid_2x2_matrix(playerA_matrix) and is_valid_2x2_matrix(playerB_matrix)):
        raise ValueError("Both matrices must be 2x2.")
    
    # Identify Pure Strategy Equilibria
    pure_strategies = []
    for i in range(2):
        for j in range(2):
            row_player_best = playerA_matrix[i][j] >= max(playerA_matrix[k][j] for k in range(2))
            col_player_best = playerB_matrix[i][j] >= max(playerB_matrix[i][k] for k in range(2))
            
            if row_player_best and col_player_best:
                pure_strategies.append((playerA_matrix[i][j], playerB_matrix[i][j]))
    
    if not pure_strategies:
        pure_strategies = "NONE"
    
    # Calculate Mixed Strategy Equilibria
    a, b = playerA_matrix[0]
    c, d = playerA_matrix[1]
    w, x = playerB_matrix[0]
    y, z = playerB_matrix[1]
    
    try:
        p = (z - x) / ((a - c) + (d - b))
        q = (d - b) / ((w - y) + (z - x))
    except ZeroDivisionError:
        p, q = None, None

    mixed_strategy = None
    if p is not None and q is not None and 0 <= p <= 1 and 0 <= q <= 1:
        mixed_strategy = [(p, 1-p), (q, 1-q)]
    else:
        mixed_strategy = "NONE"
    
    return {
        "Pure_strategies": pure_strategies,
        "Mixed_strategies": mixed_strategy
    }


# Initialize the Flask app
app = Flask(__name__)

# HTML template for the input form and display
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bimatrix Game Solver</title>
    <style>
        body {
            font-family: Palatino, monospace;
            background-color: #f4f4f4;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            color: #333;
        }
        .content {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .matrix-container {
            display: flex;
            justify-content: center;
            gap: 40px;
            align-items: center;
        }
        table {
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid Black;
            padding: 10px;
            text-align: center;
        }
        input[type="number"] {
            width: 80px;
            padding: 5px;
            border: 1px solid Black;
            border-radius: 4px;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            width: fit-content;
            border-radius: 4px;
            background: #e9f5db;
            border: 1px solid Black;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: 1px solid Black;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="content">
        <h2>Bimatrix Game Solver</h2>
        <form action="/" method="post">
            <div class="matrix-container">
                <div>
                    <h3>Player A:</h3>
                    <table>
                        <tr>
                            <td><input type="number" name="uA11" placeholder="uA1,1" value="{{ request.form['uA11'] }}" required></td>
                            <td><input type="number" name="uA12" placeholder="uA1,2" value="{{ request.form['uA12'] }}" required></td>
                        </tr>
                        <tr>
                            <td><input type="number" name="uA21" placeholder="uA2,1" value="{{ request.form['uA21'] }}" required></td>
                            <td><input type="number" name="uA22" placeholder="uA2,2" value="{{ request.form['uA22'] }}" required></td>
                        </tr>
                    </table>
                </div>
                <div>
                    <h3>Player B:</h3>
                    <table>
                        <tr>
                            <td><input type="number" name="uB11" placeholder="uB1,1" value="{{ request.form['uB11'] }}" required></td>
                            <td><input type="number" name="uB12" placeholder="uB1,2" value="{{ request.form['uB12'] }}" required></td>
                        </tr>
                        <tr>
                            <td><input type="number" name="uB21" placeholder="uB2,1" value="{{ request.form['uB21'] }}" required></td>
                            <td><input type="number" name="uB22" placeholder="uB2,2" value="{{ request.form['uB22'] }}" required></td>  
                        </tr>
                    </table>
                </div>
            </div>
            <br>
            <input type="submit" value="Solve">
        </form>

        {% if result %}
        <div class="result">
            <h3>Payoff Matrix:</h3>
            <table>
                <tr>
                    <td>({{ request.form['uA11'] }}, {{ request.form['uB11'] }})</td>
                    <td>({{ request.form['uA12'] }}, {{ request.form['uB12'] }})</td>
                </tr>
                <tr>
                    <td>({{ request.form['uA21'] }}, {{ request.form['uB21'] }})</td>
                    <td>({{ request.form['uA22'] }}, {{ request.form['uB22'] }})</td>
                </tr>
            </table>
            <br>
            <strong>Pure Strategies:</strong> {{ result['Pure_strategies'] }}<br>
            <strong>Mixed Strategies:</strong> {{ result['Mixed_strategies'] }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        playerA_matrix = [
            [float(request.form["uA11"]), float(request.form["uA12"])],
            [float(request.form["uA21"]), float(request.form["uA22"])]
        ]
        playerB_matrix = [
            [float(request.form["uB11"]), float(request.form["uB12"])],
            [float(request.form["uB21"]), float(request.form["uB22"])]
        ]
        
        result = nash_equilibrium(playerA_matrix, playerB_matrix)
    
    return render_template_string(template, result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
