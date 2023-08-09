from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# API Key and URL
api_key = "YOUR_APP_ID"  # Replace with your actual API key
base_url = "https://openexchangerates.org/api/latest.json"

@app.route("/", methods=["GET", "POST"])
def currency_converter():
    if request.method == "POST":
        # Get form data using request.form.get
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")
        amount = request.form.get("amount")

        if from_currency and to_currency and amount:
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            amount = float(amount)

            params = {"app_id": api_key}
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                exchange_rates = data["rates"]

                if from_currency in exchange_rates and to_currency in exchange_rates:
                    original_amount = amount / exchange_rates[from_currency]
                    converted_amount = original_amount * exchange_rates[to_currency]
                    result = f"{amount:.2f} {from_currency} is equal to {converted_amount:.2f} {to_currency}"
                else:
                    result = "Invalid currency codes"
            else:
                result = "API request failed"
        else:
            result = "Please fill in all fields"

        return render_template("index.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
