from flask import Flask, request, render_template_string

app = Flask(__name__)

BITS_IN_A_BYTE = 8
TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Bit Calculator</title></head>
<body>
    <h2>Bit Calculator</h2>
    <form method="get">
        Amount: <input type="text" name="input_amount" value="{{ input_amount }}">
        <select name="input_units">
            {% for unit in units %}
                <option value="{{ unit }}" {% if unit == input_units %}selected{% endif %}>{{ unit }}</option>
            {% endfor %}
        </select>
        <input type="submit" value="Convert">
    </form>
    <h3>Results:</h3>
    <ul>
        {% for unit, value in output.items() %}
            <li>{{ value }} {{ unit }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

units = ["bits", "bytes", "kilobits", "kilobytes", "megabits", "megabytes", "gigabits", "gigabytes", "terabits", "terabytes", "petabits", "petabytes"]

def get_notation(notation_type):
    if notation_type == "ieee":
        return {"message": "(IEEE notation: kilobyte = 1000 bytes)", "kilo": 1000}
    return {"message": "(Legacy notation: kilobyte = 1024 bytes)", "kilo": 1024}

@app.route('/')
def index():
    input_units = request.args.get("input_units", "megabits")
    input_amount = request.args.get("input_amount", "1")
    notation_type = request.args.get("notation", "legacy").lower()
    
    try:
        input_amount = float(input_amount)
    except ValueError:
        input_amount = 1
    
    notation = get_notation(notation_type)
    kilo = notation["kilo"]
    
    output = {}
    
    conversions = {
        "bits": lambda x: x,
        "bytes": lambda x: x * BITS_IN_A_BYTE,
        "kilobits": lambda x: x * kilo,
        "kilobytes": lambda x: x * BITS_IN_A_BYTE * kilo,
        "megabits": lambda x: x * kilo * kilo,
        "megabytes": lambda x: x * kilo * kilo * BITS_IN_A_BYTE,
        "gigabits": lambda x: x * kilo ** 3,
        "gigabytes": lambda x: x * kilo ** 3 * BITS_IN_A_BYTE,
        "terabits": lambda x: x * kilo ** 4,
        "terabytes": lambda x: x * kilo ** 4 * BITS_IN_A_BYTE,
        "petabits": lambda x: x * kilo ** 5,
        "petabytes": lambda x: x * kilo ** 5 * BITS_IN_A_BYTE
    }
    
    bits_value = conversions.get(input_units, lambda x: x)(input_amount)
    for unit, func in conversions.items():
        output[unit] = func(bits_value) / (conversions["bits"](1))
    
    return render_template_string(TEMPLATE, input_amount=input_amount, input_units=input_units, output=output, units=units)

if __name__ == '__main__':
    app.run(debug=True)
