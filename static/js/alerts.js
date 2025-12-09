// Alerts Page JavaScript

let currentUser = null;
let currentPage = 1;
let filterOptions = {};
let currentAlert = null;

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
    loadFilterOptions();
    loadAlerts();
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

// Load filter options
async function loadFilterOptions() {
  try {
    const response = await fetch('/api/filter-options');
    filterOptions = await response.json();

    // Populate vendor dropdown
    const vendorSelect = document.getElementById('filterVendor');
    filterOptions.vendors.forEach((vendor) => {
      const option = document.createElement('option');
      option.value = vendor;
      option.textContent = vendor;
      vendorSelect.appendChild(option);
    });

    // Populate product dropdown
    const productSelect = document.getElementById('filterProduct');
    filterOptions.products.forEach((product) => {
      const option = document.createElement('option');
      option.value = product;
      option.textContent = product;
      productSelect.appendChild(option);
    });
  } catch (error) {
    console.error('Failed to load filter options:', error);
  }
}

// Apply filters button
document.getElementById('applyFiltersBtn').addEventListener('click', () => {
  currentPage = 1;
  loadAlerts();
});

// Reset filters button
document.getElementById('resetFiltersBtn').addEventListener('click', () => {
  document.getElementById('filterVendor').value = '';
  document.getElementById('filterProduct').value = '';
  document.getElementById('filterBioRelevance').value = '';
  document.getElementById('filterDateFrom').value = '';
  document.getElementById('filterDateTo').value = '';
  document.getElementById('filterSearch').value = '';
  document.getElementById('filterKEV').checked = false;
  currentPage = 1;
  loadAlerts();
});

// Load alerts with filters
async function loadAlerts() {
  try {
    const params = new URLSearchParams({
      page: currentPage,
      per_page: 50,
      vendor: document.getElementById('filterVendor').value,
      product: document.getElementById('filterProduct').value,
      bio_relevance: document.getElementById('filterBioRelevance').value,
      kev_only: document.getElementById('filterKEV').checked,
      search: document.getElementById('filterSearch').value,
      date_from: document.getElementById('filterDateFrom').value,
      date_to: document.getElementById('filterDateTo').value
    });

    const response = await fetch(`/api/alerts?${params}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to load alerts');
    }

    renderAlerts(data.alerts);
    renderPagination(data.page, data.total_pages, data.total);
  } catch (error) {
    console.error('Failed to load alerts:', error);
    document.getElementById('alertsTableBody').innerHTML = `
      <tr>
        <td colspan="6" class="text-center text-danger py-4">
          Failed to load alerts. Please try again.
        </td>
      </tr>
    `;
  }
}

function renderAlerts(alerts) {
  const tbody = document.getElementById('alertsTableBody');

  if (!alerts || alerts.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center text-muted py-4">
          No alerts found matching your filters.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = alerts
    .map(
      (alert) => `
    <tr onclick="showAlertDetail('${escapeHtml(alert.cve_id)}')">
      <td>
        <span class="badge badge-severity-${(alert.severity || 'low').toLowerCase()}">
          ${escapeHtml(alert.severity || 'N/A')}
        </span>
      </td>
      <td class="fw-semibold">${escapeHtml(alert.cve_id)}</td>
      <td class="text-truncate" style="max-width: 300px;">${escapeHtml(alert.title || 'N/A')}</td>
      <td>${formatDate(alert.published_at)}</td>
      <td>
        ${
          alert.bio_relevance
            ? `<span class="badge badge-bio-${alert.bio_relevance.toLowerCase()}">${alert.bio_relevance}</span>`
            : '<span class="text-muted">N/A</span>'
        }
      </td>
      <td class="text-center">
        <button class="btn btn-sm btn-success" onclick="event.stopPropagation(); saveAlert('${escapeHtml(
          alert.cve_id
        )}')">
          Save
        </button>
      </td>
    </tr>
  `
    )
    .join('');
}

function renderPagination(page, totalPages, total) {
  document.getElementById('resultsInfo').textContent = `Showing page ${page} of ${totalPages} (${total} total alerts)`;

  const pagination = document.getElementById('pagination');

  if (totalPages <= 1) {
    pagination.innerHTML = '';
    return;
  }

  let html = '';

  // Previous button
  html += `
    <li class="page-item ${page === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${page - 1}); return false;">Previous</a>
    </li>
  `;

  // Page numbers
  const maxVisible = 5;
  let startPage = Math.max(1, page - Math.floor(maxVisible / 2));
  let endPage = Math.min(totalPages, startPage + maxVisible - 1);

  if (endPage - startPage < maxVisible - 1) {
    startPage = Math.max(1, endPage - maxVisible + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    html += `
      <li class="page-item ${i === page ? 'active' : ''}">
        <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
      </li>
    `;
  }

  // Next button
  html += `
    <li class="page-item ${page === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${page + 1}); return false;">Next</a>
    </li>
  `;

  pagination.innerHTML = html;
}

function changePage(page) {
  currentPage = page;
  loadAlerts();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show alert detail modal
async function showAlertDetail(cveId) {
  const modal = new bootstrap.Modal(document.getElementById('alertDetailModal'));
  currentAlert = cveId;

  document.getElementById('modalCVEId').textContent = cveId;
  document.getElementById('modalBody').innerHTML = `
    <div class="text-center py-5">
      <div class="spinner-border text-success"></div>
    </div>
  `;

  modal.show();

  try {
    const params = new URLSearchParams({ search: cveId, per_page: 1 });
    const response = await fetch(`/api/alerts?${params}`);
    const data = await response.json();

    if (data.alerts && data.alerts.length > 0) {
      const alert = data.alerts[0];
      renderAlertDetail(alert);
    } else {
      document.getElementById('modalBody').innerHTML = '<p class="text-danger">Alert not found.</p>';
    }
  } catch (error) {
    console.error('Failed to load alert details:', error);
    document.getElementById('modalBody').innerHTML = '<p class="text-danger">Failed to load details.</p>';
  }
}

function renderAlertDetail(alert) {
  document.getElementById('modalBody').innerHTML = `
    <div class="mb-3">
      <strong>CVE ID:</strong> ${escapeHtml(alert.cve_id)}
    </div>
    <div class="mb-3">
      <strong>Title:</strong> ${escapeHtml(alert.title || 'N/A')}
    </div>
    <div class="mb-3">
      <strong>Severity:</strong>
      <span class="badge badge-severity-${(alert.severity || 'low').toLowerCase()}">
        ${escapeHtml(alert.severity || 'N/A')}
      </span>
    </div>
    <div class="mb-3">
      <strong>Vendor:</strong> ${escapeHtml(alert.vendor || 'N/A')}
    </div>
    <div class="mb-3">
      <strong>Product:</strong> ${escapeHtml(alert.product || 'N/A')}
    </div>
    <div class="mb-3">
      <strong>Published:</strong> ${formatDate(alert.published_at)}
    </div>
    <div class="mb-3">
      <strong>Bio-Relevance:</strong>
      ${
        alert.bio_relevance
          ? `<span class="badge badge-bio-${alert.bio_relevance.toLowerCase()}">${alert.bio_relevance}</span>`
          : '<span class="text-muted">N/A</span>'
      }
    </div>
    ${alert.bio_impact ? `<div class="mb-3"><strong>Bio Impact:</strong> ${escapeHtml(alert.bio_impact)}</div>` : ''}
    <div class="mb-3">
      <strong>KEV:</strong> ${alert.kev_flag ? '<span class="badge bg-danger">Yes</span>' : 'No'}
    </div>
    <div class="mb-3">
      <strong>Summary:</strong>
      <p class="text-muted">${escapeHtml(alert.summary || 'No summary available.')}</p>
    </div>
  `;
}

// Save alert button in modal
document.getElementById('saveAlertBtn').addEventListener('click', async () => {
  if (currentAlert) {
    await saveAlert(currentAlert);
  }
});

// Save alert function
async function saveAlert(cveId) {
  try {
    const response = await fetch('/api/save-vulnerability', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cve_id: cveId })
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.error || 'Failed to save vulnerability');
      return;
    }

    alert('Vulnerability saved successfully!');
  } catch (error) {
    console.error('Failed to save vulnerability:', error);
    alert('Failed to save vulnerability. Please try again.');
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

