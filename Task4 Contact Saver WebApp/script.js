const apiBase = "https://5jzbi27uh2.execute-api.us-east-1.amazonaws.com/prod/";
let allContacts = []; // Store all contacts for filtering
let sortDirection = 'asc'; // Track sort direction
let editingEmail = null; // Track currently editing contact email

// Toast notification function
function showToast(message, type = 'success') {
  const toastContainer = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  let icon;
  switch(type) {
    case 'success': icon = '<i class="fas fa-check-circle"></i>'; break;
    case 'error': icon = '<i class="fas fa-exclamation-circle"></i>'; break;
    case 'warning': icon = '<i class="fas fa-exclamation-triangle"></i>'; break;
    default: icon = '<i class="fas fa-info-circle"></i>';
  }
  
  toast.innerHTML = `${icon} ${message}`;
  toastContainer.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function escapeHtml(text) {
  if (!text) return "";
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Fetch and display contacts
async function loadContacts() {
  const contactsDiv = document.getElementById("contactsList");
  contactsDiv.innerHTML = `
    <div class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading contacts...</p>
    </div>
  `;
  
  try {
    const response = await fetch(`${apiBase}/contacts`);
    const contacts = await response.json();
    allContacts = contacts;
    renderContacts(contacts);
    showToast('Contacts loaded successfully');
  } catch (error) {
    contactsDiv.innerHTML = `
      <div class="error-message">
        <i class="fas fa-exclamation-triangle"></i>
        <p>Error loading contacts. Please try again.</p>
      </div>
    `;
    console.error(error);
    showToast('Failed to load contacts', 'error');
  }
}

// Render contact cards with delete and edit buttons working
function renderContacts(contacts) {
  const contactsDiv = document.getElementById("contactsList");
  
  if (!contacts.length) {
    contactsDiv.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-address-book"></i>
        <p>No contacts found. Add your first contact!</p>
      </div>
    `;
    return;
  }

  let html = '<div class="contacts-list">';
  contacts.forEach((contact, index) => {
    html += `
      <div class="card animate__animated animate__fadeInUp" style="animation-delay: ${index * 0.1}s">
        ${contact.imageUrl ? `<img src="${escapeHtml(contact.imageUrl)}" alt="Image" class="contact-image">` : ""}
        <h3>${escapeHtml(contact.name)}</h3>
        <p><strong>Email:</strong> ${escapeHtml(contact.email)}</p>
        <p><em>${escapeHtml(contact.message)}</em></p>
        <small>Added: ${new Date(contact.submittedAt).toLocaleString()}</small>
        <div class="card-actions">
          <button class="action-btn edit-btn" data-email="${contact.email}">
            <i class="fas fa-edit"></i>
          </button>
          <button class="action-btn delete-btn" data-email="${contact.email}">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    `;
  });
  html += "</div>";
  contactsDiv.innerHTML = html;
  
  // Add event listeners to delete buttons
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const email = btn.getAttribute('data-email');
      if (confirm(`Are you sure you want to delete contact: ${email}?`)) {
        try {
          const response = await fetch(`${apiBase}/contact?email=${encodeURIComponent(email)}`, {
          method: "DELETE"
        });
          const result = await response.json();
          if (response.ok) {
            showToast(`Deleted contact: ${email}`);
            loadContacts();
          } else {
            showToast(result.error || 'Failed to delete contact', 'error');
          }
        } catch (error) {
          showToast('Network error while deleting', 'error');
          console.error(error);
        }
      }
    });
  });
  
  // Add event listeners to edit buttons
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const email = btn.getAttribute('data-email');
      const contact = allContacts.find(c => c.email === email);
      if (!contact) {
        showToast('Contact not found', 'error');
        return;
      }
      // Prefill form with contact data
      document.getElementById("name").value = contact.name;
      document.getElementById("email").value = contact.email;
      document.getElementById("email").disabled = true; // disable editing email as it's key
      document.getElementById("message").value = contact.message;
      editingEmail = email;

      const responseEl = document.getElementById("response");
      responseEl.textContent = `Editing contact: ${email}`;
      responseEl.className = "response-message info";

      // Change submit button text
      const submitBtn = document.querySelector('.submit-btn');
      submitBtn.innerHTML = '<span class="btn-text">Update Contact</span><i class="fas fa-save btn-icon"></i>';
    });
  });
}

// Sort contacts by name
function sortContacts() {
  sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
  
  allContacts.sort((a, b) => {
    const nameA = a.name.toLowerCase();
    const nameB = b.name.toLowerCase();
    
    if (sortDirection === 'asc') {
      return nameA.localeCompare(nameB);
    } else {
      return nameB.localeCompare(nameA);
    }
  });
  
  renderContacts(allContacts);
  showToast(`Contacts sorted ${sortDirection === 'asc' ? 'A-Z' : 'Z-A'}`);
}

// Handle search input with debounce
let searchTimeout;
document.getElementById("searchInput").addEventListener("input", function () {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    const query = this.value.trim().toLowerCase();
    const filtered = allContacts.filter(contact =>
      contact.name.toLowerCase().includes(query) ||
      contact.email.toLowerCase().includes(query)
    );
    renderContacts(filtered);
  }, 300);
});

// Handle form submission for create or update
document.getElementById("contactForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const messageInput = document.getElementById("message");
  const responseEl = document.getElementById("response");

  const name = nameInput.value.trim();
  const email = emailInput.value.trim();
  const message = messageInput.value.trim();

  if (!name || !email || !message) {
    responseEl.textContent = "Please fill all required fields.";
    responseEl.className = "response-message error";
    setTimeout(() => {
      responseEl.textContent = "";
      responseEl.className = "response-message";
    }, 3000);
    return;
  }

  try {
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.innerHTML = '<div class="mini-spinner"></div>';
    submitBtn.disabled = true;

    let method = 'POST';
    let url = `${apiBase}/SaveContactForm`;

    // If editing, use PUT and different endpoint
    if (editingEmail) {
      method = 'PUT';
      url = `${apiBase}/contact`;
    }

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, message }),
    });

    const result = await response.json();

    if (response.status === 400 && result.error === "Email already exists!") {
      responseEl.textContent = "This email is already registered.";
      responseEl.className = "response-message error";
      showToast('Email already exists!', 'error');
    } else if (!response.ok) {
      responseEl.textContent = "Submission failed. Please try again.";
      responseEl.className = "response-message error";
      showToast('Submission failed!', 'error');
    } else {
      responseEl.textContent = editingEmail ? "Contact updated successfully!" : "Contact saved successfully!";
      responseEl.className = "response-message success";
      showToast(editingEmail ? 'Contact updated!' : 'Contact saved!');

      // Reset form and editing state
      nameInput.value = "";
      emailInput.value = "";
      emailInput.disabled = false;
      messageInput.value = "";
      editingEmail = null;

      // Reset submit button text
      submitBtn.innerHTML = '<span class="btn-text">Save Contact</span><i class="fas fa-paper-plane btn-icon"></i>';

      loadContacts();
    }

    setTimeout(() => {
      responseEl.textContent = "";
      responseEl.className = "response-message";
    }, 4000);

  } catch (error) {
    responseEl.textContent = "Network error. Please try again.";
    responseEl.className = "response-message error";
    showToast('Network error occurred!', 'error');
    console.error(error);
  } finally {
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.disabled = false;
  }
});

// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const advancedFields = document.querySelector('.advanced-fields');
    if (btn.dataset.tab === 'advanced') {
      advancedFields.style.display = 'block';
      advancedFields.classList.add('animate__animated', 'animate__fadeIn');
    } else {
      advancedFields.style.display = 'none';
    }
  });
});

// Initialize app
loadContacts();
