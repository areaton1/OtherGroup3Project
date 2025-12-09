// Dashboard JavaScript

let currentUser = null;

// Check session on page load
checkSession();

async function checkSession() {
  try {
    const response = await fetch('/api/check-session');
    const data = await response.json();

    if (!data.logged_in) {
      window.location.href = '/';
      return;
    }

    currentUser = data;
    document.getElementById('navUsername').textContent = data.email;
    loadDashboardData();
  } catch (error) {
    console.error('Session check failed:', error);
    window.location.href = '/';
  }
}

// Logout handler
document.getElementById('logoutBtn').addEventListener('click', async () => {
  try {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/';
  } catch (error) {
    console.error('Logout failed:', error);
  }
});

// Load dashboard statistics
async function loadDashboardData() {
  try {
    const response = await fetch('/api/stats');
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to load stats');
    }

    // Update stat cards
    document.getElementById('statTotal').textContent = data.total.toLocaleString();
    document.getElementById('statKEV').textContent = data.kev_count.toLocaleString();
    document.getElementById('statBio').textContent = data.bio_count.toLocaleString();
    document.getElementById('statMonth').textContent = data.month_count.toLocaleString();

    // Update bio-relevance breakdown
    document.getElementById('bioHigh').textContent = (data.bio_breakdown.HIGH || 0).toLocaleString();
    document.getElementById('bioMedium').textContent = (data.bio_breakdown.MEDIUM || 0).toLocaleString();
    document.getElementById('bioLow').textContent = (data.bio_breakdown.LOW || 0).toLocaleString();

    // Render top vendors
    renderTopVendors(data.top_vendors);

    // Render top products
    renderTopProducts(data.top_products);

    // Render publication timeline
    renderTimeline(data.timeline);

    // Render priority alerts
    renderPriorityAlerts(data.recent_alerts);
  } catch (error) {
    console.error('Failed to load dashboard data:', error);
  }
}

function renderTopVendors(vendors) {
  const container = document.getElementById('topVendorsList');

  if (!vendors || vendors.length === 0) {
    container.innerHTML = '<div class="text-center text-muted py-3">No data available</div>';
    return;
  }

  container.innerHTML = vendors
    .map(
      (v) => `
    <div class="list-group-item d-flex justify-content-between align-items-center border-0 px-0">
      <div class="fw-semibold">${escapeHtml(v.vendor)}</div>
      <span class="badge bg-secondary rounded-pill">${v.count} alerts</span>
    </div>
  `
    )
    .join('');
}

function renderTopProducts(products) {
  const container = document.getElementById('topProductsList');

  if (!products || products.length === 0) {
    container.innerHTML = '<div class="text-center text-muted py-3">No data available</div>';
    return;
  }

  container.innerHTML = products
    .map(
      (p) => `
    <div class="list-group-item d-flex justify-content-between align-items-center border-0 px-0">
      <div class="fw-semibold">${escapeHtml(p.product)}</div>
      <span class="badge bg-secondary rounded-pill">${p.count}</span>
    </div>
  `
    )
    .join('');
}

function renderTimeline(timeline) {
  const container = document.getElementById('timelineList');

  if (!timeline || timeline.length === 0) {
    container.innerHTML = '<div class="text-center text-muted py-3">No data available</div>';
    return;
  }

  container.innerHTML = timeline
    .map(
      (t) => `
    <div class="list-group-item d-flex justify-content-between align-items-center border-0 px-0">
      <div class="fw-semibold">${t.month}</div>
      <span class="text-muted">${t.count} CVEs</span>
    </div>
  `
    )
    .join('');
}

function renderPriorityAlerts(alerts) {
  const container = document.getElementById('priorityAlertsList');

  if (!alerts || alerts.length === 0) {
    container.innerHTML = '<div class="text-center text-muted py-3">No critical alerts</div>';
    return;
  }

  container.innerHTML = alerts
    .map(
      (alert) => `
    <div class="list-group-item border-0 px-0 py-3">
      <div class="d-flex justify-content-between align-items-start">
        <div class="flex-grow-1">
          <div class="fw-bold mb-1">
            <span class="badge badge-severity-critical me-2">CRITICAL</span>
            ${escapeHtml(alert.cve_id)}
          </div>
          <div class="text-muted small mb-1">${escapeHtml(alert.title)}</div>
          <div class="small text-muted">
            ${escapeHtml(alert.vendor || 'Unknown')} • ${formatDate(alert.published_at)}
          </div>
        </div>
      </div>
    </div>
  `
    )
    .join('');
}

// Utility functions
function escapeHtml(text) {
  if (!text) return '';
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

