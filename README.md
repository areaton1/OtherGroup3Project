# CVE Dashboard - CISA/CVE Vulnerability Intelligence Platform

Real-time vulnerability monitoring with AI-driven insights powered by Gemini.

**🚀 Everything is pre-configured and ready to run!**

---

## Quick Start (3 Steps)

### 1. Clone the Repository

```bash
git clone https://github.com/areaton1/OtherGroup3Project.git
cd OtherGroup3Project
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

That's it! Takes about 30 seconds.

### 3. Run the Application

```bash
python3 app.py
```

Open your browser to: **http://localhost:5001**

---

## Login

Use one of these existing accounts:

**Account 1:**
- Email: `areaton1@crimson.ua.edu`
- Password: (check with team)

**Account 2:**
- Email: `johndoe@gmail.com`
- Password: (check with team)

**Or create a new account** using the Sign Up tab!

---

## Features

✅ **User Authentication** - Simple login/signup system  
✅ **Dashboard** - Real CVE statistics from 1470+ alerts  
✅ **Smart Filters** - Search by vendor, product, bio-relevance, date, KEV status  
✅ **Save CVEs** - Bookmark important vulnerabilities  
✅ **AI Chatbot** - Ask Gemini questions about cybersecurity (💡 button)  
✅ **No Build Tools** - Pure HTML/CSS/JavaScript for maximum reliability  

---

## Tech Stack

- **Backend:** Flask (Python 3.9+)
- **Frontend:** Vanilla JavaScript + Bootstrap 5
- **Database:** MySQL (AWS RDS) - already configured
- **AI:** Google Gemini API - already configured

---

## Project Structure

```
OtherGroup3Project/
├── app.py                  # Flask backend (all routes)
├── requirements.txt        # Python dependencies
├── .env                    # Configuration (database + API keys)
├── templates/              # HTML pages
│   ├── index.html         # Login/signup
│   ├── dashboard.html     # Main dashboard
│   ├── alerts.html        # CVE list with filters
│   └── saved.html         # Saved vulnerabilities
└── static/
    ├── css/main.css       # Styles
    └── js/                # JavaScript
        ├── auth.js        # Authentication
        ├── dashboard.js   # Dashboard logic
        ├── alerts.js      # Alerts page
        ├── saved.js       # Saved items
        └── chatbot.js     # AI chatbot
```

---

## What's Included

### Database
- **1,470 CVE alerts** ready to display
- AWS RDS MySQL database (fully configured)
- 3 existing user accounts

### Pages
1. **Login/Signup** - User authentication
2. **Dashboard** - Statistics overview
3. **Alerts** - Searchable CVE table with filters
4. **My Saved** - Bookmarked vulnerabilities

### Filters Available
- Vendor (Microsoft, Apple, Google, etc.)
- Product (Windows, Multiple Products, etc.)
- Bio-Relevance (HIGH/MEDIUM/LOW/NONE)
- Date Range
- Search (CVE ID or keywords)
- KEV Only (CISA Known Exploited Vulnerabilities)

---

## Configuration

All configuration is in `.env` file (already included):

```env
# Database (AWS RDS)
DB_HOST=m7wltxurw8d2n21q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com
DB_USER=it2jpmptcbrfz9gq
DB_PASSWORD=e5voj8n91k1ni3m6
DB_NAME=ond7op6xmute4kcm
DB_PORT=3306

# Flask
SECRET_KEY=cve-dashboard-secret-key-2025

# Gemini AI
GEMINI_API_KEY=AIzaSyCRIPjp3dwmWR9VSvx4S2-JDFQY-3bpoeo
```

**Everything is pre-configured. No changes needed!**

---

## Troubleshooting

### Database Connection Error?

Test the connection:
```bash
python3 test_connection.py
```

Should show:
```
✅ Connection successful!
✅ Found 1470 alerts in database
✅ Found 3 users in database
```

### Port 5001 Already in Use?

Stop other processes or change the port in `app.py` (last line):
```python
app.run(host='0.0.0.0', port=5002, debug=True)
```

### Missing Dependencies?

Make sure you installed:
```bash
pip3 install -r requirements.txt
```

---

## Development

### Adding New Features

1. Backend: Add route to `app.py`
2. Frontend: Edit HTML in `templates/` or JS in `static/js/`
3. No build step - just refresh browser!

### Database Queries

All queries use plain SQL with PyMySQL. No ORM complexity.

---

## Why This Tech Stack?

**Simple = Reliable**

- ✅ No TypeScript compilation
- ✅ No React/Vue/Angular complexity
- ✅ No npm/node_modules (500MB nightmare)
- ✅ No build tools (Vite/Webpack failures)
- ✅ No version conflicts
- ✅ Works every time

**Previous project (Project Tutwiler) failed because:**
- Complex build process
- Multiple processes (ports 3000 + 5173)
- TypeScript + React + Vite
- Teammates couldn't `git pull` and run

**This project:**
- Single command: `python3 app.py`
- Works immediately
- No configuration needed
- No build failures

---

## Team Collaboration

### Pull Latest Changes
```bash
git pull origin main
```

### Push Your Changes
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### Create a New Branch
```bash
git checkout -b feature-name
# Make changes
git push origin feature-name
```

---

## API Endpoints

### Authentication
- `POST /api/login` - Login user
- `POST /api/signup` - Create account
- `POST /api/logout` - Logout
- `GET /api/check-session` - Check if logged in

### Data
- `GET /api/stats` - Dashboard statistics
- `GET /api/alerts?filters` - Get alerts (with filters)
- `GET /api/filter-options` - Get dropdown values
- `GET /api/saved-vulnerabilities` - User's saved CVEs

### Actions
- `POST /api/save-vulnerability` - Bookmark a CVE
- `POST /api/delete-saved` - Remove saved CVE
- `POST /api/chatbot` - AI chat with Gemini

---

## Production Deployment

### Heroku
```bash
# Use gunicorn instead of Flask dev server
gunicorn app:app
```

### Railway
```bash
# Same as Heroku
gunicorn app:app
```

### Render
```bash
gunicorn app:app
```

Set environment variables in platform dashboard (copy from `.env` file).

---

## Security Notes

⚠️ **This is designed for educational/internal use**

Current setup:
- Plain text passwords (no hashing)
- Shared database credentials
- API keys in repository
- No HTTPS enforcement

**For public deployment, you should:**
- Add password hashing (bcrypt)
- Use environment variables (not committed)
- Add rate limiting
- Enable HTTPS/TLS
- Add CSRF protection

---

## Need Help?

1. **Check** `QUICKSTART.md` for fast setup guide
2. **Read** `PROJECT_SUMMARY.md` for architecture details
3. **Run** `python3 test_connection.py` to test database
4. **Ask** your teammates or instructor

---

## Success Metrics

✅ **Clone and run in under 2 minutes**  
✅ **No build errors**  
✅ **Works on every teammate's machine**  
✅ **1470+ real CVEs displayed**  
✅ **AI chatbot functional**  
✅ **All filters working**  

---

**That's it! Just `pip3 install -r requirements.txt` and `python3 app.py` to start.** 🚀

No configuration. No build process. No complexity. It just works.
