from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store for user portfolios (in production, use a database)
portfolios = {}

# ML model cache
ml_models = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        
        # Get different time periods based on query param
        period = request.args.get('period', '1y')
        hist = ticker.history(period=period)
        
        if hist.empty:
            return jsonify({"error": "Stock not found"}), 404
        
        # Get current info
        info = ticker.info
        
        # Prepare data for frontend
        stock_data = {
            "symbol": symbol.upper(),
            "name": info.get("longName", symbol.upper()),
            "currentPrice": info.get("currentPrice", hist['Close'].iloc[-1]),
            "change": hist['Close'].iloc[-1] - hist['Close'].iloc[-2],
            "changePercent": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100,
            "volume": int(hist['Volume'].iloc[-1]),
            "marketCap": info.get("marketCap", 0),
            "pe": info.get("trailingPE", 0),
            "historicalData": []
        }
        
        # Format historical data for charts
        for date, row in hist.iterrows():
            stock_data["historicalData"].append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2), 
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume'])
            })
        
        return jsonify(stock_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chart/<symbol>', methods=['GET'])
def get_chart_data(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        period = request.args.get('period', '1y')
        chart_type = request.args.get('type', 'candlestick')
        
        hist = ticker.history(period=period)
        
        if chart_type == 'candlestick':
            fig = go.Figure(data=go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=symbol.upper()
            ))
        else:
            fig = go.Figure(data=go.Scatter(
                x=hist.index,
                y=hist['Close'],
                mode='lines',
                name=symbol.upper(),
                line=dict(color='#3B82F6', width=2)
            ))
        
        fig.update_layout(
            title=f"{symbol.upper()} Stock Chart",
            yaxis_title="Price ($)",
            xaxis_title="Date",
            template="plotly_white",
            height=400
        )
        
        return jsonify({"chart": fig.to_json()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict/<symbol>', methods=['GET'])
def predict_stock(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period='2y')
        
        if len(hist) < 30:
            return jsonify({"error": "Insufficient data for prediction"}), 400
        
        # Prepare features for ML model
        hist['MA_5'] = hist['Close'].rolling(window=5).mean()
        hist['MA_20'] = hist['Close'].rolling(window=20).mean()
        hist['RSI'] = calculate_rsi(hist['Close'], 14)
        hist['Volume_MA'] = hist['Volume'].rolling(window=10).mean()
        hist['Price_Change'] = hist['Close'].pct_change()
        
        # Drop NaN values
        hist = hist.dropna()
        
        # Features and target
        features = ['Open', 'High', 'Low', 'Volume', 'MA_5', 'MA_20', 'RSI', 'Volume_MA', 'Price_Change']
        X = hist[features].values
        y = hist['Close'].shift(-1).dropna().values  # Predict next day's close
        X = X[:-1]  # Remove last row to match y length
        
        # Train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make prediction for next day
        last_features = X[-1].reshape(1, -1)
        prediction = model.predict(last_features)[0]
        
        current_price = hist['Close'].iloc[-1]
        predicted_change = prediction - current_price
        predicted_change_percent = (predicted_change / current_price) * 100
        
        return jsonify({
            "symbol": symbol.upper(),
            "currentPrice": round(current_price, 2),
            "predictedPrice": round(prediction, 2),
            "predictedChange": round(predicted_change, 2),
            "predictedChangePercent": round(predicted_change_percent, 2),
            "confidence": round(model.score(X_test, y_test), 3),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def calculate_rsi(prices, window):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@app.route('/api/portfolio', methods=['GET', 'POST'])
def portfolio():
    user_id = request.args.get('user_id', 'default')
    
    if request.method == 'GET':
        return jsonify(portfolios.get(user_id, {"cash": 10000, "stocks": {}}))
    
    elif request.method == 'POST':
        data = request.json
        action = data.get('action')  # 'buy' or 'sell'
        symbol = data.get('symbol', '').upper()
        quantity = int(data.get('quantity', 0))
        
        if user_id not in portfolios:
            portfolios[user_id] = {"cash": 10000, "stocks": {}}
        
        portfolio = portfolios[user_id]
        
        # Get current stock price
        ticker = yf.Ticker(symbol)
        current_price = ticker.history(period='1d')['Close'].iloc[-1]
        
        if action == 'buy':
            total_cost = current_price * quantity
            if portfolio['cash'] >= total_cost:
                portfolio['cash'] -= total_cost
                if symbol in portfolio['stocks']:
                    portfolio['stocks'][symbol]['quantity'] += quantity
                    # Update average price
                    old_total = portfolio['stocks'][symbol]['avgPrice'] * (portfolio['stocks'][symbol]['quantity'] - quantity)
                    new_total = old_total + total_cost
                    portfolio['stocks'][symbol]['avgPrice'] = new_total / portfolio['stocks'][symbol]['quantity']
                else:
                    portfolio['stocks'][symbol] = {
                        'quantity': quantity,
                        'avgPrice': current_price
                    }
                return jsonify({"success": True, "portfolio": portfolio})
            else:
                return jsonify({"error": "Insufficient funds"}), 400
        
        elif action == 'sell':
            if symbol in portfolio['stocks'] and portfolio['stocks'][symbol]['quantity'] >= quantity:
                portfolio['cash'] += current_price * quantity
                portfolio['stocks'][symbol]['quantity'] -= quantity
                if portfolio['stocks'][symbol]['quantity'] == 0:
                    del portfolio['stocks'][symbol]
                return jsonify({"success": True, "portfolio": portfolio})
            else:
                return jsonify({"error": "Insufficient stocks"}), 400
    
    return jsonify({"error": "Invalid request"}), 400

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        message = data.get('message', '')
        
        # Simple rule-based chatbot (in production, use OpenAI API)
        response = ""
        
        if any(word in message.lower() for word in ['price', 'stock', 'quote']):
            response = "I can help you get stock prices! Just ask me about any stock symbol like 'What's the price of AAPL?'"
        elif any(word in message.lower() for word in ['buy', 'sell', 'trade']):
            response = "To buy or sell stocks, use the trading interface. I can help you analyze which stocks might be good investments!"
        elif any(word in message.lower() for word in ['predict', 'forecast']):
            response = "I can help you with ML predictions! Try asking about price predictions for specific stocks."
        elif 'hello' in message.lower() or 'hi' in message.lower():
            response = "Hello! I'm your AI trading assistant. I can help you with stock prices, predictions, and trading advice. What can I help you with today?"
        else:
            response = "I'm here to help with stock trading and analysis! You can ask me about stock prices, predictions, or trading strategies."
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/trending', methods=['GET'])
def get_trending_stocks():
    # Popular stocks to track
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
    trending = []
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                
                trending.append({
                    "symbol": symbol,
                    "price": round(current, 2),
                    "change": round(change, 2)
                })
        except:
            continue
    
    return jsonify(trending)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)