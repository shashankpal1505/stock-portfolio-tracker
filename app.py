import logging
import tkinter as tk
from tkinter import messagebox
import yfinance as yf

logger = logging.getLogger("yfinance")
logger.disabled = True
logger.propagate = False


# --- 1. The Core Logic ---
def calculate_pl():
    # Grab the data the user typed into the text boxes
    symbol = symbol_entry.get().upper().strip()
    if symbol and not "." in symbol:
        symbol = f"{symbol}.NS"

    try:
        buy_price = float(buy_price_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror(
            "Input Error", "Please enter valid numbers for price and quantity."
        )
        return

    try:
        
        result_label.config(text="Fetching live data...", fg="blue")
        app.update()

        def calc(live_data):
            # Calculate Profit / Loss
            total_invested = buy_price * quantity
            latest_price = live_data["Close"].iloc[-1]
            current_value = latest_price * quantity
            profit_loss = current_value - total_invested
            pl_percentage = (profit_loss / current_value) * 100

            # Format the result text
            if profit_loss >= 0:
                color = "green"
                status = "PROFIT"
            else:
                color = "red"
                status = "LOSS"
            if current_value < total_invested:
                result_text = (
                f"Current Price: ₹{latest_price:.2f}\n"
                f"Total Invested: ₹{total_invested:.2f}\n"
                f"Current Value: ₹{current_value:.2f}\n"
                f"Target has to achieve: ₹{abs(profit_loss):.2f} ({pl_percentage:.2f}%)"
            )
                result_label.config(text=result_text, fg=color)
            else:
                result_text = (
                    f"Current Price: ₹{latest_price:.2f}\n"
                    f"Total Invested: ₹{total_invested:.2f}\n"
                    f"Current Value: ₹{current_value:.2f}\n"
                    f"Total {status}: ₹{abs(profit_loss):.2f} ({pl_percentage:.2f}%)"
                )
                result_label.config(text=result_text, fg=color)

        # Fetch the latest price using yfinance
        stock = yf.Ticker(symbol)
        live_data = stock.history(period="1d", interval="1m")

        if not live_data.empty:
            calc(live_data)
        else:
            live_data = stock.history(period="5d", interval="1m")
            if not live_data.empty:
                calc(live_data)
            else:
               
                messagebox.showerror(
                    "Stock Not Found",
                    f"Please check the symbol or stock may be delisted.\nCould not find data for {symbol}.",
                )
                result_label.config(text="Ready", fg="black")
                return

        

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        result_label.config(text="Ready", fg="black")


# --- 2. Building the Windows GUI ---
app = tk.Tk()
app.title("Live Stock P&L Calculator")
app.geometry("350x420")
app.configure(padx=20, pady=20)

# Symbol Input
tk.Label(app, text="Stock Symbol (e.g., RELIANCE):").pack(anchor="w")
symbol_entry = tk.Entry(app, font=("Arial", 12), width=30)
symbol_entry.pack(pady=5)

# Buy Price Input
tk.Label(app, text="Average Buy Price/ Target Price (₹):").pack(anchor="w")
buy_price_entry = tk.Entry(app, font=("Arial", 12), width=30)
buy_price_entry.pack(pady=5)

# Quantity Input
tk.Label(app, text="Quantity of Shares:").pack(anchor="w")
quantity_entry = tk.Entry(app, font=("Arial", 12), width=30)
quantity_entry.pack(pady=5)

# Calculate Button
calc_button = tk.Button(
    app,
    text="Calculate Live P&L",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    command=calculate_pl,
)
calc_button.pack(pady=20, fill="x")

# Result Display Area
result_label = tk.Label(
    app, text="Enter details and click Calculate", font=("Arial", 12), justify="left"
)
result_label.pack(pady=10)

# --- 3. Run the Application ---
app.mainloop()
