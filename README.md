TRACK_ID=PS03

# Retail Copilot - Sales and Inventory Management System

## Overview
Retail Copilot is an AI-powered sales and inventory management system designed for small retail operations. It helps store managers make data-driven decisions by providing intelligent insights, inventory alerts, and natural language question-answering capabilities.

## Features
- **AI-Powered Copilot**: Ask questions in plain language about inventory, sales, and get data-driven answers
- **Intelligent Alerts**: Automated alerts for stock-outs, low stock, overstock, slow-moving items, and sales anomalies
- **Real-time Analytics**: Track sales performance, inventory levels, and trends across multiple stores
- **Modern UI/UX**: Clean, responsive interface with intuitive navigation
- **Data-Driven Decisions**: Every recommendation backed by actual numbers and data

## Technology Stack
- **Backend**: Django 5.1.7 (Python)
- **AI/ML**: Google Gemini API for natural language processing
- **Database**: SQLite (included) - MySQL support available
- **Frontend**: Django Templates with modern CSS
- **Data Analysis**: Pandas, NumPy

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Gemini API Key (set as `GEMINI_API_KEY` environment variable)

### Installation Steps

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variable:**
```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Initialize database and generate sample data:**
```bash
python setup.py
```

Or run these commands individually:
```bash
python manage.py migrate
python manage.py generate_sample_data
python manage.py generate_alerts
```

4. **Run the application:**
```bash
python app.py
```

The application will start on `http://localhost:8000`

## Usage

### Dashboard
- View key metrics: stores, products, stock levels, recent sales
- Check stock-outs and low stock items at a glance
- Access quick actions for common queries

### AI Copilot
- Ask questions like:
  - "What products are running out of stock?"
  - "Which products are overstocked?"
  - "How did Wireless Headphones perform this month?"
  - "What are my slow-moving items?"
  - "What needs attention today?"
- Filter questions by specific store
- Get answers with supporting data and actionable recommendations

### Inventory Alerts
- View real-time alerts for items needing attention
- Alerts include:
  - Stock outs (critical)
  - Low stock (high priority)
  - Overstock (medium priority)
  - Slow-moving items (medium priority)
  - Sales spikes/drops (high/medium priority)
- Generate new alerts based on current data
- Track alert severity and recommended actions

### Data Generated
The system generates comprehensive sample data including:
- **3 Stores**: Downtown Store, Mall Branch, Suburban Outlet
- **29 Products**: Across 5 categories (Electronics, Clothing, Groceries, Home & Garden, Sports)
- **87 Stock entries**: Product combinations across all stores
- **896 Sales transactions**: Simulated over 90 days with realistic patterns

## Project Structure
```
D:\Project\
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── manage.py                       # Django management script
├── db.sqlite3                      # SQLite database (auto-generated)
├── retail_copilot/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inventory/                      # Main application
│   ├── models.py                   # Database models
│   ├── views.py                    # View functions
│   ├── admin.py                    # Admin interface
│   ├── genai_service.py            # AI integration
│   ├── templates/                  # HTML templates
│   │   └── inventory/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── alerts.html
│   │       └── product_analysis.html
│   └── management/commands/        # Custom management commands
│       ├── generate_sample_data.py
│       └── generate_alerts.py
```

## API Endpoints

### POST /api/copilot/
Ask the AI copilot a question.
```json
{
  "question": "What products are running out of stock?",
  "store_id": null
}
```

### POST /api/generate-alerts/
Generate new inventory alerts based on current data.

### GET /api/stores/
Get list of all stores.

### GET /api/products/
Get list of all products.

## Environment Variables
- `GEMINI_API_KEY`: Required for AI functionality (Gemini API key)

## Demo Video
[Link to demo video - to be added]

## Hackathon Compliance
- ✅ Single command startup: `python app.py`
- ✅ Runs on port 8000
- ✅ Uses Gemini API only (as specified)
- ✅ No external vector databases or hosted services
- ✅ Includes sample data and documents
- ✅ Clean, modular code structure
- ✅ Grounds AI answers in actual data
- ✅ Escalates when data is insufficient

## Key Design Decisions
1. **Data-First Approach**: AI answers are always grounded in actual inventory and sales data
2. **Graceful Degradation**: System functions without API key (limited AI features)
3. **Modular Architecture**: Clear separation between AI logic and deterministic business rules
4. **User-Friendly Interface**: Modern UI with intuitive navigation and clear visual hierarchy
5. **Actionable Insights**: Every alert and recommendation includes specific actions to take

## Future Enhancements
- Integration with real POS systems
- Multi-user support with authentication
- Advanced forecasting and predictive analytics
- Mobile application
- Real-time notifications
- Export reports to PDF/Excel

## License
This project was created for the NexusTiq24 Hackathon.

## Contact
For questions or issues, please refer to the hackathon organizers.