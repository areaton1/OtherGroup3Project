// Saved Vulnerabilities Page JavaScript

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
    loadSavedVulnerabilities();
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

// Load saved vulnerabilities
async function loadSavedVulnerabilities() {
  try {
    const response = await fetch('/api/saved-vulnerabilities');
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to load saved vulnerabilities');
    }

    renderSavedItems(data.saved);
  } catch (error) {
    console.error('Failed to load saved vulnerabilities:', error);
    document.getElementById('savedItemsContainer').innerHTML = `
      <div class="col-12 text-center text-danger py-4">
        Failed to load saved vulnerabilities. Please try again.
      </div>
    `;
  }
}

function renderSavedItems(items) {
  const container = document.getElementById('savedItemsContainer');
  document.getElementById('savedCount').textContent = `${items.length} saved item${items.length !== 1 ? 's' : ''}`;

  if (!items || items.length === 0) {
    container.innerHTML = `
      <div class="col-12 text-center py-5">
        <span class="fs-1 text-muted">📋</span>
        <h4 class="mt-3 text-muted">No saved vulnerabilities yet</h4>
        <p class="text-muted">Visit the <a href="/alerts.html">Alerts page</a> to save CVEs to your list.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = items
    .map(
      (item) => `
    <div class="col-md-6 col-lg-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <h5 class="card-title mb-0">${escapeHtml(item.cve_id)}</h5>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteSaved(${item.id})">
              Delete
            </button>
          </div>

          <div class="mb-2">
            ${
              item.severity
                ? `<span class="badge badge-severity-${item.severity.toLowerCase()}">${item.severity}</span>`
                : ''
            }
            ${
              item.bio_relevance
                ? `<span class="badge badge-bio-${item.bio_relevance.toLowerCase()} ms-1">${item.bio_relevance}</span>`
                : ''
            }
          </div>

          <h6 class="card-subtitle text-muted mb-3">${escapeHtml(item.vulnerability_name || 'N/A')}</h6>

          <div class="mb-2">
            <strong>Vendor:</strong> ${escapeHtml(item.vendor_project || 'N/A')}
          </div>

          <div class="mb-2">
            <strong>Product:</strong> ${escapeHtml(item.product || 'N/A')}
          </div>

          <div class="mb-2">
            <strong>Saved:</strong> ${formatDate(item.date_added)}
          </div>

          ${
            item.short_description
              ? `
            <div class="mt-3">
              <strong>Description:</strong>
              <p class="text-muted small">${escapeHtml(item.short_description)}</p>
            </div>
          `
              : ''
          }

          ${
            item.notes
              ? `
            <div class="mt-3">
              <strong>Notes:</strong>
              <p class="text-muted small">${escapeHtml(item.notes)}</p>
            </div>
          `
              : ''
          }
        </div>
      </div>
    </div>
  `
    )
    .join('');
}

// Delete saved vulnerability
async function deleteSaved(id) {
  if (!confirm('Are you sure you want to remove this from your saved list?')) {
    return;
  }

  try {
    const response = await fetch('/api/delete-saved', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.error || 'Failed to delete');
      return;
    }

    // Reload the list
    loadSavedVulnerabilities();
  } catch (error) {
    console.error('Failed to delete saved vulnerability:', error);
    alert('Failed to delete. Please try again.');
  }
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

