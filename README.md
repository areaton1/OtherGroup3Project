# CVE Dashboard - CISA/CVE Vulnerability Intelligence Platform

Real-time vulnerability monitoring with AI-driven insights powered by Gemini.

## Features

- 🔐 **User Authentication** - Simple login/signup system
- 📊 **Dashboard** - Visual statistics from your CVE database
- 🔍 **Smart Filters** - Search by vendor, product, bio-relevance, date, and KEV status
- 💾 **Save Vulnerabilities** - Bookmark important CVEs for later
- 🤖 **AI Chatbot** - Ask Gemini questions about cybersecurity and CVEs
- 📱 **Responsive Design** - Works on desktop and mobile

## Tech Stack

- **Backend**: Flask (Python 3.11+)
- **Frontend**: Vanilla HTML/CSS/JavaScript + Bootstrap 5
- **Database**: MySQL (AWS RDS)
- **AI**: Google Gemini API

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with the following:

```env
# Database Configuration (already configured for your AWS RDS)
DB_HOST=m7wltxurw8d2n21q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com
DB_USER=it2jpmptcbrfz9gq
DB_PASSWORD=e5voj8n91k1ni3m6
DB_NAME=ond7op6xmute4kcm
DB_PORT=3306

# Flask Configuration
SECRET_KEY=cve-dashboard-secret-key-2025

# Gemini API Key (get from https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Create Default Admin User

Connect to your MySQL database and run:

```sql
INSERT INTO users (username, email, pw_hash, role, verified, created_at)
VALUES ('admin', 'admin@cisa.gov', 'admin123', 'ADMIN', 1, NOW());
```

### 4. Run the Application

```bash
python app.py
```

The app will start at: **http://localhost:5000**

## Default Login Credentials

- **Username/Email**: `admin@cisa.gov`
- **Password**: `admin123`

## Project Structure

```
OtherGroup3Project/
├── app.py                  # Flask backend (all routes & API)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML pages
│   ├── index.html         # Login/signup page
│   ├── dashboard.html     # Main dashboard
│   ├── alerts.html        # CVE list with filters
│   └── saved.html         # Saved vulnerabilities
└── static/
    ├── css/
    │   └── main.css       # Custom styles
    └── js/
        ├── auth.js        # Login/signup logic
        ├── dashboard.js   # Dashboard functionality
        ├── alerts.js      # Alerts page with filters
        ├── saved.js       # Saved vulnerabilities
        └── chatbot.js     # Gemini AI chatbot
```

## Database Tables Used

- `users` - User accounts
- `alerts` - Main CVE data (1000+ entries)
- `vulnerabilities` - User-saved CVEs
- `sources` - Data source tracking (NVD, CISA_KEV)

## API Endpoints

### Authentication
- `POST /api/login` - Login user
- `POST /api/signup` - Create new account
- `POST /api/logout` - Logout
- `GET /api/check-session` - Check if logged in

### Data
- `GET /api/stats` - Dashboard statistics
- `GET /api/alerts` - Get alerts with filters
- `GET /api/filter-options` - Get filter dropdown values
- `GET /api/saved-vulnerabilities` - Get user's saved CVEs

### Actions
- `POST /api/save-vulnerability` - Save a CVE
- `POST /api/delete-saved` - Delete saved CVE
- `POST /api/chatbot` - Chat with Gemini AI

## Filters Available

- **Vendor** - Filter by vendor (Microsoft, Apple, Google, etc.)
- **Product** - Filter by product
- **Bio-Relevance** - HIGH/MEDIUM/LOW/NONE
- **Date Range** - Published date filtering
- **Search** - CVE ID or keyword search
- **KEV Only** - Show only CISA Known Exploited Vulnerabilities

## Features Not Included

❌ No build process (no npm, no webpack)
❌ No password hashing (plain text for simplicity)
❌ No complex frameworks (just Flask + vanilla JS)
❌ No charts (numbers only for reliability)

## Troubleshooting

### Database Connection Error
- Check that your MySQL credentials in `.env` are correct
- Ensure your IP is whitelisted in AWS RDS security group

### Gemini API Not Working
- Get an API key from: https://aistudio.google.com/app/apikey
- Add it to your `.env` file as `GEMINI_API_KEY`

### Port 5000 Already in Use
- Change the port in `app.py` (last line): `app.run(port=5001)`

## Deployment

### Heroku/Render/Railway

1. Set environment variables in the platform dashboard
2. Use `gunicorn` as the web server:
   ```bash
   gunicorn app:app
   ```

3. No build step needed - just deploy!

## Team Setup

Each teammate should:

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Create their own `.env` file (use same database credentials)
4. Run `python app.py`

No node_modules, no build tools, no version conflicts!

## License

MIT License - Use freely for educational purposes.

