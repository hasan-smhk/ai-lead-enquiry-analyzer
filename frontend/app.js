const API_BASE = "/api/v1/enquiries";

const form = document.getElementById("enquiry-form");
const submitBtn = document.getElementById("submit-btn");
const resultBox = document.getElementById("result-box");
const errorBox = document.getElementById("error-box");
const tableBody = document.getElementById("enquiry-table-body");
const filterCategory = document.getElementById("filter-category");
const filterPriority = document.getElementById("filter-priority");
const refreshBtn = document.getElementById("refresh-btn");

const KNOWN_CATEGORIES = [
  "Website Development", "E-commerce Development", "Training/Courses",
  "Data Analytics", "Chatbot", "Mobile App", "AI/ML Solution", "Automation"
];
KNOWN_CATEGORIES.forEach(cat => {
  const opt = document.createElement("option");
  opt.value = cat;
  opt.textContent = cat;
  filterCategory.appendChild(opt);
});

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
  resultBox.classList.add("hidden");
}

function showResult(data) {
  errorBox.classList.add("hidden");
  resultBox.innerHTML = `
    <strong>Category:</strong> ${data.predicted_category}
    (${(data.category_confidence * 100).toFixed(1)}% confidence)<br/>
    <strong>Priority:</strong> <span class="badge badge-${data.predicted_priority}">${data.predicted_priority}</span><br/>
    <strong>Insight:</strong> ${data.insight}<br/>
    ${data.extracted_email ? `<strong>Email found:</strong> ${data.extracted_email}<br/>` : ""}
    ${data.extracted_phone ? `<strong>Phone found:</strong> ${data.extracted_phone}<br/>` : ""}
  `;
  resultBox.classList.remove("hidden");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = "Analyzing...";

  const payload = {
    enquiry_text: document.getElementById("enquiry_text").value.trim(),
    industry: document.getElementById("industry").value.trim() || null,
    budget_inr: document.getElementById("budget_inr").value
      ? parseFloat(document.getElementById("budget_inr").value)
      : null,
    urgency_hint: document.getElementById("urgency_hint").value || null,
  };

  try {
    const res = await fetch(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Request failed with status ${res.status}`);
    }

    const data = await res.json();
    showResult(data);
    form.reset();
    loadEnquiries();
  } catch (err) {
    showError(err.message || "Something went wrong. Please try again.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Analyze Enquiry";
  }
});

async function loadEnquiries() {
  tableBody.innerHTML = `<tr><td colspan="7">Loading...</td></tr>`;

  const params = new URLSearchParams();
  if (filterCategory.value) params.append("category", filterCategory.value);
  if (filterPriority.value) params.append("priority", filterPriority.value);

  try {
    const res = await fetch(`${API_BASE}?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to load enquiries");
    const data = await res.json();

    if (data.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7">No enquiries found.</td></tr>`;
      return;
    }

    tableBody.innerHTML = data.map(row => `
      <tr>
        <td>${row.id}</td>
        <td class="text-cell" title="${escapeHtml(row.enquiry_text)}">${escapeHtml(row.enquiry_text)}</td>
        <td>${row.predicted_category}</td>
        <td><span class="badge badge-${row.predicted_priority}">${row.predicted_priority}</span></td>
        <td>${row.industry || "-"}</td>
        <td>${row.budget_inr ? "₹" + Number(row.budget_inr).toLocaleString() : "-"}</td>
        <td>${new Date(row.created_at).toLocaleString()}</td>
      </tr>
    `).join("");
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="7">Error loading enquiries: ${err.message}</td></tr>`;
  }
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

refreshBtn.addEventListener("click", loadEnquiries);
filterCategory.addEventListener("change", loadEnquiries);
filterPriority.addEventListener("change", loadEnquiries);

loadEnquiries();
