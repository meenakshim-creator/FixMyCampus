/**
 * FixMyCampus — Interactive Client-Side Engine
 * Minimalist, mature interactions: zero-reload search, tab switching,
 * clean AJAX upvoting, and expand/collapse feed controls.
 */

document.addEventListener('DOMContentLoaded', () => {
  initFeedManagement();
  initAjaxUpvotes();
  initImageUploadPreview();
  initInteractiveModal();
  initFaqAccordion();
});

/* ==========================================================================
   1. Feed Filtering, Search & Tab Controls (Restrained & Fast)
   ========================================================================== */
function initFeedManagement() {
  const searchInput = document.querySelector('.canopy-search-input');
  const buildingSelect = document.querySelector('.canopy-building-select');
  const tabButtons = document.querySelectorAll('.feed-tabs-row .tab-btn');
  const ticketCards = document.querySelectorAll('.photo-card, .ticket-card');
  const expandRow = document.getElementById('expandFeedRow');
  const toggleBtn = document.getElementById('btnToggleFeed');

  let activeTab = 'trending'; // 'trending' | 'urgent' | 'resolved' | 'all'
  let isExpanded = false;

  function filterAndDisplayCards() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const selectedBuilding = buildingSelect ? buildingSelect.value : 'All';

    let matchedCards = [];

    ticketCards.forEach(card => {
      const title = (card.querySelector('.photo-card-title, .ticket-title')?.textContent || '').toLowerCase();
      const desc = (card.querySelector('.photo-card-desc, .ticket-description')?.textContent || '').toLowerCase();
      const category = (card.getAttribute('data-category') || '').toLowerCase();
      const building = card.getAttribute('data-building') || '';
      const status = card.getAttribute('data-status') || '';
      const priority = card.getAttribute('data-priority') || '';

      const matchesSearch = !query || title.includes(query) || desc.includes(query) || category.includes(query);
      const matchesBuilding = selectedBuilding === 'All' || building.toLowerCase() === selectedBuilding.toLowerCase();

      let matchesTab = true;
      if (activeTab === 'trending') {
        matchesTab = true; // Handled by limit below
      } else if (activeTab === 'urgent') {
        matchesTab = (priority === 'Urgent' || priority === 'High') && status !== 'Resolved';
      } else if (activeTab === 'resolved') {
        matchesTab = status === 'Resolved';
      } else if (activeTab === 'all') {
        matchesTab = true;
      }

      if (matchesSearch && matchesBuilding && matchesTab) {
        matchedCards.push(card);
      } else {
        card.classList.add('d-none');
      }
    });

    // Control visibility based on tab and expand state
    matchedCards.forEach((card, index) => {
      if (activeTab === 'trending') {
        if (!isExpanded && index >= 4) {
          card.classList.add('d-none');
        } else {
          card.classList.remove('d-none');
        }
      } else if (activeTab === 'all') {
        if (!isExpanded && index >= 6) {
          card.classList.add('d-none');
        } else {
          card.classList.remove('d-none');
        }
      } else {
        card.classList.remove('d-none');
      }
    });

    // Toggle button visibility
    if (expandRow && toggleBtn) {
      if ((activeTab === 'trending' && matchedCards.length > 4) || (activeTab === 'all' && matchedCards.length > 6)) {
        expandRow.style.display = 'block';
        toggleBtn.querySelector('span').textContent = isExpanded 
          ? 'Show fewer reports' 
          : `View all ${matchedCards.length} reports`;
      } else {
        expandRow.style.display = 'none';
      }
    }
  }

  // Search input event
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      isExpanded = true; // Auto-expand when user actively searches
      filterAndDisplayCards();
    });
  }

  // Building select event
  if (buildingSelect) {
    buildingSelect.addEventListener('change', () => {
      isExpanded = true;
      filterAndDisplayCards();
    });
  }

  // Tab click events
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeTab = btn.getAttribute('data-tab');
      isExpanded = false;
      filterAndDisplayCards();
    });
  });

  // Toggle button click
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      isExpanded = !isExpanded;
      filterAndDisplayCards();
    });
  }

  // Run on load
  filterAndDisplayCards();
}

/* ==========================================================================
   2. Sleek AJAX Upvotes (Endorsements)
   ========================================================================== */
function initAjaxUpvotes() {
  document.querySelectorAll('.upvote-btn, .upvote-btn-editorial').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const form = button.closest('form');
      if (!form) return;

      const actionUrl = form.getAttribute('action');
      const issueId = actionUrl.split('/').pop();
      const countEl = button.querySelector('.upvote-count');

      if (!countEl) return;

      // Optimistic increment
      let currentVal = parseInt(countEl.textContent, 10) || 0;
      countEl.textContent = currentVal + 1;
      button.classList.add('upvoted');

      try {
        const response = await fetch(`/api/upvote/${issueId}`, { method: 'POST' });
        const data = await response.json();
        if (data.success && data.upvotes) {
          countEl.textContent = data.upvotes;
        }
        showToast(`Endorsed issue #${issueId}. Facilities notified.`);
      } catch (err) {
        form.submit();
      }
    });
  });
}

/* ==========================================================================
   3. File Upload Preview
   ========================================================================== */
function initImageUploadPreview() {
  const fileInput = document.querySelector('input[name="photo"]');
  if (!fileInput) return;

  const previewWrap = document.createElement('div');
  previewWrap.className = 'upload-preview-box';
  previewWrap.style.cssText = 'display:none; margin-top:0.75rem; border-radius:8px; overflow:hidden; border:1px solid #E5E5DF; padding:4px; max-width:200px;';

  const img = document.createElement('img');
  img.style.cssText = 'width:100%; height:110px; object-fit:cover; border-radius:6px; display:block;';
  previewWrap.appendChild(img);

  fileInput.parentNode.appendChild(previewWrap);

  fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (loadEvent) => {
        img.src = loadEvent.target.result;
        previewWrap.style.display = 'block';
      };
      reader.readAsDataURL(file);
    } else {
      previewWrap.style.display = 'none';
    }
  });
}

/* ==========================================================================
   4. Minimalist Notification Toast (No Emojis)
   ========================================================================== */
let toastContainer = null;

function showToast(message) {
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-center-box';
    toastContainer.style.cssText = `
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 10000;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.style.cssText = `
    pointer-events: auto;
    background: #14231C;
    color: #F8FAF9;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
    font-weight: 500;
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.25);
    display: flex;
    align-items: center;
    gap: 8px;
    opacity: 0;
    transform: translateY(12px);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  `;

  toast.innerHTML = `
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <span>${message}</span>
  `;

  toastContainer.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
  });

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    setTimeout(() => toast.remove(), 250);
  }, 3000);
}

/* ==========================================================================
   5. Modal Dialog ESC & Backdrop Dismiss
   ========================================================================== */
function initInteractiveModal() {
  const modal = document.querySelector('#report-modal');
  if (!modal) return;

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && window.location.hash === '#report-modal') {
      window.location.hash = '';
    }
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      window.location.hash = '';
    }
  });
}

/* ==========================================================================
   6. Interactive FAQ Accordion
   ========================================================================== */
function initFaqAccordion() {
  document.querySelectorAll('.faq-question').forEach(button => {
    button.addEventListener('click', () => {
      const item = button.closest('.faq-item');
      if (!item) return;
      const isOpen = item.classList.contains('open');

      // Close all items
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

      // If it wasn't open, open it
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });
}
