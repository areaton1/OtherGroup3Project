from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'cve-dashboard-secret-key-2025')
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'm7wltxurw8d2n21q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'),
    'user': os.getenv('DB_USER', 'it2jpmptcbrfz9gq'),
    'password': os.getenv('DB_PASSWORD', 'e5voj8n91k1ni3m6'),
    'database': os.getenv('DB_NAME', 'ond7op6xmute4kcm'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'cursorclass': pymysql.cursors.DictCursor
}

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

def get_db_connection():
    """Create database connection"""
    return pymysql.connect(**DB_CONFIG)

# ============== ROUTES ==============

@app.route('/')
def index():
    """Landing page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect('/dashboard.html')
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/alerts.html')
def alerts_page():
    """Alerts list page"""
    if 'user_id' not in session:
        return redirect('/')
    return render_template('alerts.html')

@app.route('/saved.html')
def saved_page():
    """Saved vulnerabilities page"""
    if 'user_id' not in session:
        return redirect('/')
    return render_template('saved.html')

# ============== API ENDPOINTS ==============

@app.route('/api/signup', methods=['POST'])
def signup():
    """Register new user"""
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 400
        
        # Insert new user (plain text password, no hashing)
        cursor.execute(
            "INSERT INTO users (email, pw_hash, role, verified, created_at) VALUES (%s, %s, 'ANALYST', 1, NOW())",
            (email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        # Set session
        session['user_id'] = user_id
        session['email'] = email
        
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'email': email})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check credentials (plain text password)
        cursor.execute("SELECT id, email, pw_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user or user['pw_hash'] != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Set session
        session['user_id'] = user['id']
        session['email'] = user['email']
        
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'email': user['email']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'email': session.get('email')
        })
    return jsonify({'logged_in': False})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total alerts
        cursor.execute("SELECT COUNT(*) as count FROM alerts")
        total = cursor.fetchone()['count']
        
        # KEV count
        cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE kev_flag = 1")
        kev_count = cursor.fetchone()['count']
        
        # Bio-relevant (HIGH or MEDIUM)
        cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE bio_relevance IN ('HIGH', 'MEDIUM')")
        bio_count = cursor.fetchone()['count']
        
        # This month
        cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE YEAR(published_at) = YEAR(NOW()) AND MONTH(published_at) = MONTH(NOW())")
        month_count = cursor.fetchone()['count']
        
        # Bio-relevance breakdown
        cursor.execute("SELECT bio_relevance, COUNT(*) as count FROM alerts WHERE bio_relevance IS NOT NULL GROUP BY bio_relevance")
        bio_breakdown = {row['bio_relevance']: row['count'] for row in cursor.fetchall()}
        
        # Top vendors (top 5)
        cursor.execute("SELECT vendor, COUNT(*) as count FROM alerts WHERE vendor IS NOT NULL AND vendor != '' GROUP BY vendor ORDER BY count DESC LIMIT 5")
        top_vendors = cursor.fetchall()
        
        # Top products (top 5)
        cursor.execute("SELECT product, COUNT(*) as count FROM alerts WHERE product IS NOT NULL AND product != '' GROUP BY product ORDER BY count DESC LIMIT 5")
        top_products = cursor.fetchall()
        
        # Publication timeline (last 6 months)
        cursor.execute("""
            SELECT DATE_FORMAT(published_at, '%Y-%m') as month, COUNT(*) as count 
            FROM alerts 
            WHERE published_at >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY month 
            ORDER BY month DESC
        """)
        timeline = cursor.fetchall()
        
        # Recent critical alerts (top 10)
        cursor.execute("""
            SELECT cve_id, title, vendor, product, published_at 
            FROM alerts 
            WHERE severity = 'CRITICAL' 
            ORDER BY published_at DESC 
            LIMIT 10
        """)
        recent_alerts = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total': total,
            'kev_count': kev_count,
            'bio_count': bio_count,
            'month_count': month_count,
            'bio_breakdown': bio_breakdown,
            'top_vendors': top_vendors,
            'top_products': top_products,
            'timeline': timeline,
            'recent_alerts': recent_alerts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get alerts with filters"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get filter parameters
        vendor = request.args.get('vendor', '')
        product = request.args.get('product', '')
        bio_relevance = request.args.get('bio_relevance', '')
        kev_only = request.args.get('kev_only', '') == 'true'
        search = request.args.get('search', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []
        
        if vendor:
            query += " AND vendor = %s"
            params.append(vendor)
        
        if product:
            query += " AND product = %s"
            params.append(product)
        
        if bio_relevance:
            query += " AND bio_relevance = %s"
            params.append(bio_relevance)
        
        if kev_only:
            query += " AND kev_flag = 1"
        
        if search:
            query += " AND (cve_id LIKE %s OR title LIKE %s OR summary LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        if date_from:
            query += " AND published_at >= %s"
            params.append(date_from)
        
        if date_to:
            query += " AND published_at <= %s"
            params.append(date_to)
        
        # Count total
        count_query = query.replace("SELECT *", "SELECT COUNT(*) as total")
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Get paginated results
        query += " ORDER BY published_at DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        
        cursor.execute(query, params)
        alerts = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'alerts': alerts,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filter-options', methods=['GET'])
def get_filter_options():
    """Get unique values for filters"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get unique vendors
        cursor.execute("SELECT DISTINCT vendor FROM alerts WHERE vendor IS NOT NULL AND vendor != '' ORDER BY vendor")
        vendors = [row['vendor'] for row in cursor.fetchall()]
        
        # Get unique products
        cursor.execute("SELECT DISTINCT product FROM alerts WHERE product IS NOT NULL AND product != '' ORDER BY product")
        products = [row['product'] for row in cursor.fetchall()]
        
        # Bio-relevance options
        bio_options = ['HIGH', 'MEDIUM', 'LOW', 'NONE']
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'vendors': vendors,
            'products': products,
            'bio_relevance': bio_options
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-vulnerability', methods=['POST'])
def save_vulnerability():
    """Save a vulnerability"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    cve_id = data.get('cve_id')
    notes = data.get('notes', '')
    
    if not cve_id:
        return jsonify({'error': 'CVE ID required'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get alert details
        cursor.execute("SELECT * FROM alerts WHERE cve_id = %s", (cve_id,))
        alert = cursor.fetchone()
        
        if not alert:
            return jsonify({'error': 'CVE not found'}), 404
        
        # Check if already saved
        cursor.execute(
            "SELECT id FROM vulnerabilities WHERE cve_id = %s AND user_id = %s",
            (cve_id, session['user_id'])
        )
        
        if cursor.fetchone():
            return jsonify({'error': 'Already saved'}), 400
        
        # Insert into vulnerabilities
        cursor.execute("""
            INSERT INTO vulnerabilities 
            (cve_id, vendor_project, product, vulnerability_name, date_added, short_description, required_action, due_date, notes, user_id, analyzed_at)
            VALUES (%s, %s, %s, %s, NOW(), %s, %s, NULL, %s, %s, NULL)
        """, (
            cve_id,
            alert.get('vendor', ''),
            alert.get('product', ''),
            alert.get('title', ''),
            alert.get('summary', ''),
            alert.get('bio_impact', ''),
            notes,
            session['user_id']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/saved-vulnerabilities', methods=['GET'])
def get_saved_vulnerabilities():
    """Get user's saved vulnerabilities"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.*, a.severity, a.bio_relevance 
            FROM vulnerabilities v
            LEFT JOIN alerts a ON v.cve_id = a.cve_id
            WHERE v.user_id = %s
            ORDER BY v.date_added DESC
        """, (session['user_id'],))
        
        saved = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({'saved': saved})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-saved', methods=['POST'])
def delete_saved():
    """Delete saved vulnerability"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    vuln_id = data.get('id')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM vulnerabilities WHERE id = %s AND user_id = %s",
            (vuln_id, session['user_id'])
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Gemini AI chatbot"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not GEMINI_API_KEY:
        return jsonify({'error': 'Gemini API key not configured'}), 500
    
    data = request.json
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    try:
        # Search database for relevant CVEs
        conn = get_db_connection()
        cursor = conn.cursor()
        
        search_param = f"%{message}%"
        cursor.execute("""
            SELECT cve_id, title, summary, vendor, product, severity, bio_relevance 
            FROM alerts 
            WHERE cve_id LIKE %s OR title LIKE %s OR summary LIKE %s OR vendor LIKE %s
            LIMIT 5
        """, (search_param, search_param, search_param, search_param))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Build context for Gemini
        context = "You are a cybersecurity AI assistant specializing in CVE/CISA vulnerability analysis.\n\n"
        
        if results:
            context += "Relevant CVEs from the database:\n"
            for row in results:
                context += f"- {row['cve_id']}: {row['title']} (Vendor: {row['vendor']}, Severity: {row['severity']})\n"
            context += "\n"
        
        context += f"User question: {message}\n\nProvide a helpful, concise response."
        
        # Call Gemini API
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{
                    "parts": [{"text": context}]
                }]
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Gemini API error'}), 500
        
        result = response.json()
        ai_response = result['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({
            'response': ai_response,
            'related_cves': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

