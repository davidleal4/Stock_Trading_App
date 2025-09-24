# Stock Trading Application

A production-ready full-stack web application for stock trading with ML-powered predictions, real-time data streaming, and an AI assistant.

## 🚀 Features

- **Real-time Stock Data**: Minute-by-minute data ingestion and live streaming
- **ML/AI Models**: LightGBM, XGBoost, CatBoost, LSTM, and Transformer models
- **Interactive Charts**: Plotly-powered candlestick charts with technical indicators
- **AI Assistant**: Local LLM-powered chatbot for trading guidance and analysis
- **Trading Integration**: Fidelity API connector with sandbox and live trading
- **Responsive UI**: Next.js with Tailwind CSS and Framer Motion animations
- **Time-series Database**: TimescaleDB for efficient time-series data storage
- **Real-time Updates**: WebSocket streaming for live data updates

## 🛠 Tech Stack

### Frontend
- **Next.js 14** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Plotly.js** for interactive charts
- **Zustand** for state management

### Backend
- **FastAPI** with Python 3.11
- **AsyncPG** for database operations
- **WebSockets** for real-time communication
- **Redis** for caching and job queues
- **Celery** for background tasks

### Database
- **TimescaleDB** (PostgreSQL extension) for time-series data
- **Redis** for caching and session storage

### ML/AI
- **scikit-learn**, **LightGBM**, **XGBoost**, **CatBoost**
- **PyTorch** for deep learning (LSTM, Transformers)
- **SHAP** for model explainability
- **Optuna** for hyperparameter optimization

### Infrastructure
- **Docker** and **docker-compose**
- **GitHub Actions** for CI/CD
- **Kubernetes** manifests for production deployment

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   ML Service    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐             │
         │              │     Redis       │             │
         └──────────────┤   (Cache/Jobs)  ├─────────────┘
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │   TimescaleDB   │
                        │ (Time-series)   │
                        └─────────────────┘
```

## 🚦 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Stock_Trading_App
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start with Docker Compose
```bash
docker-compose up --build
```

This will start:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- TimescaleDB: localhost:5432
- Redis: localhost:6379

### 3. Access the Application
- **Web App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📊 Default Stock Symbols

The application comes pre-configured with the top 10 US companies:
- AAPL (Apple)
- MSFT (Microsoft) 
- NVDA (NVIDIA)
- GOOG (Alphabet)
- AMZN (Amazon)
- META (Meta)
- TSLA (Tesla)
- BRK.B (Berkshire Hathaway)
- JPM (JPMorgan Chase)
- V (Visa)

## 🤖 AI Assistant Capabilities

The built-in AI assistant can:
- Explain stock data and market trends
- Run model training and backtests
- Execute trading actions (with user confirmation)
- Provide market insights and recommendations
- Guide users through complex workflows

## 🔧 Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### ML Service Development
```bash
cd ml
pip install -r requirements.txt
python main.py
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Run All Tests
```bash
docker-compose -f docker-compose.test.yml up --build
```

## 🔒 Security Features

- HTTPS enforced in production
- CORS protection
- Input validation and sanitization
- 2FA for trading operations
- Audit logging for all actions
- Environment-based secrets management
- GDPR compliance features

## 📈 Trading Integration

### Fidelity API Setup
1. Obtain API credentials from Fidelity
2. Set `FIDELITY_API_KEY` and `FIDELITY_API_SECRET` in `.env`
3. Set `FIDELITY_SANDBOX=true` for testing
4. Configure 2FA for live trading

### Trading Workflow
1. User selects stock and order parameters
2. AI assistant provides risk analysis
3. User confirms with 2FA
4. Order is placed and tracked
5. All actions are logged for audit

## 🚀 Production Deployment

### Using Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Using Kubernetes
```bash
kubectl apply -f infra/k8s/
```

### Environment Variables
Set the following in production:
- `ENVIRONMENT=production`
- `DEBUG=false`
- Strong `SECRET_KEY`
- Production database URLs
- API keys for data sources
- SSL certificates

## 📝 API Documentation

The FastAPI backend provides interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints
- `GET /api/stocks/{symbol}/data` - Historical stock data
- `POST /api/models/train` - Train ML model
- `GET /api/models/{id}/predictions` - Model predictions
- `POST /api/trading/orders` - Place trading order
- `POST /api/agent/chat` - Chat with AI assistant

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with modern web technologies
- Inspired by professional trading platforms
- Designed for educational and research purposes
