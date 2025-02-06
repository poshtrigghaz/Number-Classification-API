from flask import Flask, request, jsonify
from urllib.parse import quote
import requests
import math
import os


app = Flask(__name__)

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(d) for d in str(abs(int(n)))]  # Handle negative numbers
    length = len(digits)
    return sum(d**length for d in digits) == abs(int(n))

def get_digit_sum(n):
    return sum(int(d) for d in str(abs(int(n))))  # Handle negative numbers

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact available."

# API Endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Validate input
    try:
        number = float(number)  # Accept both integers and floating-point numbers
    except (ValueError, TypeError):
        return jsonify({"number": number, "error": True}), 400

    # Handle floating-point numbers
    if not number.is_integer():
        return jsonify({
            "number": number,
            "is_prime": False,  # Floating-point numbers cannot be prime
            "is_perfect": False,  # Floating-point numbers cannot be perfect
            "properties": ["non-integer"],  # Special property for floating-point numbers
            "digit_sum": None,  # Digit sum is not applicable for floating-point numbers
            "fun_fact": get_fun_fact(number)
        }), 200

    number = int(number)  # Convert to integer for further processing
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": get_digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    return jsonify(response), 200

# Handle CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))