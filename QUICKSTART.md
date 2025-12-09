# Quick Start Guide

Get the CVE Dashboard running in 3 steps:

## Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment (1 minute)

Create a file named `.env` in the project root:

```bash
# Copy the template
cp env_template.txt .env
```

Edit `.env` and add your Gemini API key:
- Get one free at: https://aistudio.google.com/app/apikey
- Replace `your_gemini_api_key_here` with your actual key

## Step 3: Create Admin User (optional)

If you don't have an admin user yet, run this SQL:

```bash
mysql -h m7wltxurw8d2n21q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com \
  -u it2jpmptcbrfz9gq \
  -p ond7op6xmute4kcm < create_admin.sql
```

Password: `e5voj8n91k1ni3m6`

## Step 4: Run the App

```bash
python app.py
```

Open your browser to: **http://localhost:5000**

## Default Login

- Email: `admin@cisa.gov`
- Password: `admin123`

---

## Teammates Setup

Share these steps with your team:

1. `git clone [repository]`
2. `pip install -r requirements.txt`
3. Copy `env_template.txt` to `.env` and add Gemini key
4. `python app.py`

**That's it!** No npm, no build tools, no complexity.

---

## Troubleshooting

**Can't connect to database?**
- Check your internet connection
- The database is on AWS, make sure your IP isn't blocked

**Gemini not working?**
- You need to add a real API key to `.env`
- Get one at: https://aistudio.google.com/app/apikey

**Port 5000 in use?**
- Edit `app.py` line 334: change `port=5000` to `port=5001`

---

## What's Included

✅ Login/Signup system
✅ Dashboard with real CVE stats
✅ Searchable alerts table
✅ Smart filters (vendor, product, bio-relevance, KEV)
✅ Save/bookmark CVEs
✅ AI chatbot (Gemini)
✅ 100% reliable (no build tools, no frameworks)

## What's NOT Included

❌ No React/Vue/Angular complexity
❌ No npm/node_modules
❌ No password hashing (simple = reliable)
❌ No charts (numbers only, less likely to break)

