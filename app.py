import logging
import streamlit as strimlit  # Imported as 'strimlit' per your exact spelling
import yfinance as yf

# Suppress yfinance internal logger noise
logger = logging.getLogger("yfinance")
logger.disabled = True
logger.propagate = False

# --- 1. Page Configuration & Header ---
strimlit.set_page_config(page_title="Live Stock P&L Calculator", page_icon="📈")
strimlit.title("📈 Live Stock P&L Calculator")
strimlit.markdown("---")

# --- 2. Building the Web GUI Input Fields ---
symbol_input = strimlit.text_input("Stock Symbol (e.g., RELIANCE):", value="").strip()
buy_price_input = strimlit.text_input("Average Buy Price/ Target Price (₹):", value="")
quantity_input = strimlit.text_input("Quantity of Shares:", value="")

# --- 3. The Core Logic Execution ---
if strimlit.button("Calculate Live P&L", type="primary"):
    
    # Validation 1: Check if inputs are filled
    if not symbol_input or not buy_price_input or not quantity_input:
        strimlit.error("⚠️ Please fill in all fields before calculating.")
    else:
        # Format the symbol for Indian Markets if suffix is missing
        symbol = symbol_input.upper()
        if symbol and "." not in symbol:
            symbol = f"{symbol}.NS"

        # Validation 2: Ensure numbers are valid numerical values
        try:
            buy_price = float(buy_price_input)
            quantity = int(quantity_input)
        except ValueError:
            strimlit.error("❌ Input Error: Please enter valid numbers for price and quantity.")
            symbol = None  # Prevent further execution

        if symbol:
            with strimlit.spinner("Fetching live data from Yahoo Finance..."):
                try:
                    # Fetch the latest price using yfinance
                    stock = yf.Ticker(symbol)
                    live_data = stock.history(period="1d", interval="1m")

                    # Fallback lookup if 1d data interval is empty
                    if live_data.empty:
                        live_data = stock.history(period="5d", interval="1m")

                    if not live_data.empty:
                        # Calculate Profit / Loss
                        total_invested = buy_price * quantity
                        latest_price = live_data["Close"].iloc[-1]
                        current_value = latest_price * quantity
                        profit_loss = current_value - total_invested
                        pl_percentage = (profit_loss / current_value) * 100

                        # Format results into distinct metric strings
                        metrics_html = f"""
                        **Current Price:** ₹{latest_price:.2f}  
                        **Total Invested:** ₹{total_invested:.2f}  
                        **Current Value:** ₹{current_value:.2f}  
                        """
                        
                        # Display output with contextual color treatments
                        if current_value < total_invested:
                            strimlit.markdown(metrics_html)
                            strimlit.error(f"📉 **Target has to achieve:** ₹{abs(profit_loss):.2f} ({pl_percentage:.2f}%)")
                        else:
                            strimlit.markdown(metrics_html)
                            strimlit.success(f"📈 **Total PROFIT:** ₹{abs(profit_loss):.2f} ({pl_percentage:.2f}%)")

                    else:
                        strimlit.error(f"🔍 Stock Not Found: Please check the symbol or stock may be delisted. Could not find data for {symbol}.")

                except Exception as e:
                    strimlit.error(f"💥 An unexpected error occurred: {e}")
