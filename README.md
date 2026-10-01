# ChurnWise - AI Customer Churn Prediction System

A production-ready full-stack web application that predicts customer churn probability using machine learning and provides actionable retention insights.

## 🎯 Features

- **AI-Powered Predictions**: Real-time customer churn prediction using trained ML models
- **Professional Dashboard**: Analytics and metrics for churn analysis
- **Prediction History**: Track all predictions with filtering and search
- **Modern UI**: Glassmorphism design with responsive layout (mobile, tablet, desktop)
- **Real ML Model**: Trained Random Forest model with scikit-learn (not hardcoded)
- **Database Storage**: SQLite for persistent prediction history
- **RESTful API**: Flask backend with comprehensive error handling
- **Evaluation Metrics**: Model comparison (Accuracy, Precision, Recall, F1, ROC-AUC)

## 🏗️ Technology Stack

### Frontend
- React.js with Vite
- JavaScript/JSX
- HTML5 & CSS3
- Tailwind CSS
- Recharts for data visualization

### Backend
- Python 3.8+
- Flask & Flask-CORS
- SQLite3

### Machine Learning
- Pandas & NumPy
- Scikit-learn (Random Forest, Logistic Regression)
- Joblib (model persistence)

## 📁 Project Structure

```
ChurnWise/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── PredictionForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── Charts.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Predict.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── History.jsx
│   │   │   └── About.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model/
│   │   ├── train_model.py
│   │   ├── churn_model.pkl
│   │   └── scaler.pkl
│   └── database/
│       └── churnwise.db
│
├── dataset/
│   └── customer_churn.csv
│
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- Git

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the ML model (one-time setup)
python model/train_model.py

# Start Flask server
python app.py
```

Backend runs on: `http://localhost:5000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: `http://localhost:5173`

### 4. Access the Application
Open your browser and navigate to: `http://localhost:5173`

## 🤖 Machine Learning Model

### Training Process

```bash
cd backend
python model/train_model.py
```

### Model Details

- **Dataset**: Customer churn data with 20 features
- **Models Trained**:
  - Random Forest Classifier
  - Logistic Regression
  
- **Evaluation Metrics**:
  - Accuracy: Percentage of correct predictions
  - Precision: True positives / (True positives + False positives)
  - Recall: True positives / (True positives + False negatives)
  - F1-Score: Harmonic mean of precision and recall
  - ROC-AUC: Area under ROC curve (0.5 to 1.0)

- **Selected Model**: Random Forest (best overall performance)
- **Model Files**:
  - `backend/model/churn_model.pkl`: Trained model
  - `backend/model/scaler.pkl`: Feature scaler for preprocessing

### Dataset Features

1. Gender (Male/Female)
2. Senior Citizen (0/1)
3. Partner (Yes/No)
4. Dependents (Yes/No)
5. Tenure (months)
6. Phone Service (Yes/No)
7. Internet Service (DSL/Fiber optic/No)
8. Contract (Month-to-month/One year/Two year)
9. Payment Method
10. Monthly Charges ($)
11. Total Charges ($)
12. Tech Support (Yes/No)
13. Online Security (Yes/No)
14. Online Backup (Yes/No)
15. Device Protection (Yes/No)
16. Streaming TV (Yes/No)
17. Streaming Movies (Yes/No)

## 📡 API Documentation

### Prediction Endpoint

**POST** `/api/predict`

**Request:**
```json
{
  "gender": "Male",
  "senior_citizen": 0,
  "partner": "Yes",
  "dependents": "No",
  "tenure": 12,
  "phone_service": "Yes",
  "internet_service": "Fiber optic",
  "contract": "Month-to-month",
  "payment_method": "Electronic check",
  "monthly_charges": 79.5,
  "total_charges": 954,
  "tech_support": "No",
  "online_security": "No",
  "online_backup": "Yes",
  "device_protection": "No",
  "streaming_tv": "Yes",
  "streaming_movies": "Yes"
}
```

**Response:**
```json
{
  "prediction": "CHURN",
  "probability": 0.784,
  "risk_level": "HIGH",
  "factors": ["Month-to-month contract", "High monthly charges", "Short tenure"],
  "recommendations": ["Offer contract upgrade", "Provide loyalty discount"]
}
```

### Dashboard Endpoint

**GET** `/api/dashboard`

**Response:**
```json
{
  "total_predictions": 150,
  "churn_count": 45,
  "non_churn_count": 105,
  "churn_percentage": 30.0,
  "recent_predictions": [...]
}
```

### History Endpoint

**GET** `/api/history?page=1&limit=20`

**Response:**
```json
{
  "predictions": [...],
  "total": 150,
  "page": 1,
  "limit": 20
}
```

## 💾 Database Schema

### Predictions Table

```sql
CREATE TABLE predictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id TEXT UNIQUE,
  gender TEXT,
  senior_citizen INTEGER,
  partner TEXT,
  dependents TEXT,
  tenure INTEGER,
  phone_service TEXT,
  internet_service TEXT,
  contract TEXT,
  payment_method TEXT,
  monthly_charges REAL,
  total_charges REAL,
  tech_support TEXT,
  online_security TEXT,
  online_backup TEXT,
  device_protection TEXT,
  streaming_tv TEXT,
  streaming_movies TEXT,
  probability REAL,
  prediction TEXT,
  risk_level TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🎨 UI/UX Features

- **Responsive Design**: Works on 320px - 1440px+ screens
- **Dark Theme**: Navy background with blue/purple gradients
- **Glassmorphism**: Frosted glass effect cards
- **Animations**: Smooth transitions and hover effects
- **Mobile Menu**: Hamburger navigation for small screens
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages

## 🔒 Security Features

- Input validation on frontend and backend
- Parameterized SQL queries (no SQL injection)
- CORS configuration
- Environment-based configuration
- No hardcoded secrets
- Proper HTTP status codes

## 📊 Dashboard Analytics

The dashboard provides:
- Total predictions count
- Churn vs non-churn breakdown
- Churn rate percentage
- Churn distribution by contract type
- Churn by internet service type
- Tenure vs churn analysis
- Monthly charges vs churn correlation
- Prediction history timeline

## 🧪 Testing the Application

### Test Prediction (High Risk)
```
Gender: Male
Senior Citizen: No
Partner: No
Dependents: No
Tenure: 2 (low)
Phone Service: Yes
Internet Service: Fiber optic
Contract: Month-to-month
Payment Method: Electronic check
Monthly Charges: 100
Total Charges: 200
Tech Support: No
Online Security: No
Online Backup: No
Device Protection: No
Streaming TV: Yes
Streaming Movies: Yes
```

### Test Prediction (Low Risk)
```
Gender: Female
Senior Citizen: No
Partner: Yes
Dependents: Yes
Tenure: 48 (high)
Phone Service: Yes
Internet Service: DSL
Contract: Two year
Payment Method: Bank transfer
Monthly Charges: 50
Total Charges: 2400
Tech Support: Yes
Online Security: Yes
Online Backup: Yes
Device Protection: Yes
Streaming TV: No
Streaming Movies: No
```

## 🐛 Troubleshooting

### Port already in use
```bash
# Backend (change port in app.py)
# Frontend (Vite uses 5173 by default)
```

### Model file not found
```bash
cd backend
python model/train_model.py
```

### Database errors
```bash
# Delete the database and let it auto-create
rm backend/database/churnwise.db
```

### CORS errors
- Ensure backend is running on port 5000
- Check CORS configuration in `app.py`

## 📈 Model Performance

After training, check `backend/model/train_model.py` output for:
- Model accuracy scores
- Precision, recall, F1-scores
- ROC-AUC values
- Feature importance (Random Forest)

## 🚀 Deployment Considerations

For production deployment:
1. Use environment variables for database path
2. Implement API rate limiting
3. Add authentication/authorization
4. Use HTTPS
5. Implement input sanitization
6. Add logging and monitoring
7. Use production-grade database (PostgreSQL)
8. Deploy frontend to CDN (Vercel, Netlify)
9. Deploy backend to cloud platform (Heroku, AWS, GCP)

## 📝 Future Improvements

- User authentication and profiles
- Bulk prediction import (CSV)
- Advanced analytics and reports
- Model retraining pipeline
- API key management
- Prediction export (PDF, Excel)
- Real-time notifications
- A/B testing for retention strategies
- Mobile app (React Native)

## 📄 License

MIT License - feel free to use for educational and commercial purposes.

## 👨‍💻 Author

Built as a comprehensive full-stack demonstration project showcasing:
- Full-stack development (React + Flask)
- Machine learning integration
- Database design
- REST API development
- Responsive UI/UX design
- Best practices in error handling and validation

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation
3. Check browser console for frontend errors
4. Check terminal for backend errors

---

**Happy Predicting! 🎯**
