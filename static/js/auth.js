// Authentication JavaScript

// Login form handler
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;
  const errorDiv = document.getElementById('loginError');

  errorDiv.classList.add('d-none');

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      errorDiv.textContent = data.error || 'Login failed';
      errorDiv.classList.remove('d-none');
      return;
    }

    // Success - add swoop transition then redirect
    const swoop = document.createElement('div');
    swoop.className = 'swoop-transition';
    document.body.appendChild(swoop);
    
    setTimeout(() => {
      window.location.href = '/dashboard.html';
    }, 400);
  } catch (error) {
    errorDiv.textContent = 'Connection error. Please try again.';
    errorDiv.classList.remove('d-none');
  }
});

// Signup form handler
document.getElementById('signupForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.getElementById('signupEmail').value;
  const password = document.getElementById('signupPassword').value;
  const errorDiv = document.getElementById('signupError');

  errorDiv.classList.add('d-none');

  try {
    const response = await fetch('/api/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      errorDiv.textContent = data.error || 'Signup failed';
      errorDiv.classList.remove('d-none');
      return;
    }

    // Success - add swoop transition then redirect
    const swoop = document.createElement('div');
    swoop.className = 'swoop-transition';
    document.body.appendChild(swoop);
    
    setTimeout(() => {
      window.location.href = '/dashboard.html';
    }, 400);
  } catch (error) {
    errorDiv.textContent = 'Connection error. Please try again.';
    errorDiv.classList.remove('d-none');
  }
});

// Check if already logged in on page load
checkSession();

async function checkSession() {
  try {
    const response = await fetch('/api/check-session');
    const data = await response.json();

    if (data.logged_in) {
      window.location.href = '/dashboard.html';
    }
  } catch (error) {
    console.error('Session check failed:', error);
  }
}

