// Catalog of POS Consumables

// 1)  DOM refs

const API_PORT = 5000;
const API_BASE =
  window.location.protocol + "//" + window.location.hostname + ":" + API_PORT;

const categories = [
  { id: "All", name: "All" },
  { id: "Breakfast", name: "Breakfast" },
  { id: "Main Meals", name: "Main Meal" },
  { id: "Dessert", name: "Dessert" },
  { id: "Soft Drink", name: "Soft Drink" },
  { id: "Hot Drink", name: "Hot Drink" },
  { id: "Alcoholic", name: "Alcoholic Drink" },
];

let products = [];

async function loadProducts() {
  try {
    const res = await fetch(API_BASE + "/api/consumables");
    if (!res.ok) throw new Error(await res.text());

    products = await res.json();
    renderProducts();
  } catch (err) {
    console.error(err);
    alert("Couldn't load products, check the server.");
  }
}

loadProducts();

/* DOM helpers */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

/* CATEGORY NAVIGATION */
const catNav = $("#category-nav");
let activeCategory = "All";

function renderCategories() {
  catNav.innerHTML = "";
  categories.forEach((cat) => {
    const btn = document.createElement("button");
    btn.textContent = cat.name;
    btn.dataset.id = cat.id;
    btn.className = `relative pb-1 whitespace-nowrap font-medium transition text-sm ${
      cat.id === activeCategory
        ? "text-amber-600 border-b-2 border-amber-500"
        : "hover:text-amber-600 text-gray-600 dark:text-gray-300"
    }`;
    btn.addEventListener("click", () => {
      activeCategory = cat.id;
      renderCategories();
      renderProducts();
    });
    catNav.appendChild(btn);
  });
}

/* PRODUCT GRID (filter + search) */
const grid = $("#product-grid");

function renderProducts() {
  const term = $("#search-input").value.toLowerCase();
  grid.innerHTML = "";
  products
    .filter((p) => activeCategory === "All" || p.cat === activeCategory)
    .filter((p) => p.name.toLowerCase().includes(term))
    .forEach((p) => {
      const card = document.createElement("button");
      card.className =
        "bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex flex-col justify-between hover:ring-2 hover:ring-amber-500 transition text-left";
      card.innerHTML = `<span class="font-semibold">${
        p.name
      }</span><span class="text-sm text-gray-500 dark:text-gray-400">£${p.price.toFixed(
        2
      )}</span>`;
      card.addEventListener("click", () => addToOrder(p));
      grid.appendChild(card);
    });
}

/* ORDER MANAGEMENT */
const orderLinesEl = $("#order-lines");
let lines = [];

function addToOrder(product) {
  const existing = lines.find((l) => l.id === product.id);
  if (existing) {
    existing.qty++;
  } else {
    lines.push({ ...product, qty: 1 });
  }
  updateOrderUI();
}

function updateOrderUI() {
  orderLinesEl.innerHTML = "";
  let total = 0;
  lines.forEach((l) => {
    total += l.price * l.qty;
    const lineEl = document.createElement("div");
    lineEl.className = "flex justify-between";
    lineEl.innerHTML = `<span>${l.qty} x ${l.name}</span><span>£${(
      l.price * l.qty
    ).toFixed(2)}</span>`;
    orderLinesEl.appendChild(lineEl);
  });
  $("#grand-total").textContent = `£${total.toFixed(2)}`;
}

/* COMPLETE ORDER – API POST */
const completeBtn = $("#complete-btn");

async function completeOrder() {
  if (!lines.length) {
    alert("No items on the order.");
    return;
  }

  const apiLines = lines.map((l) => ({ cons_id: l.id, qty: l.qty }));

  const payload = {
    timestamp: new Date().toISOString(),
    lines: apiLines,
  };

  try {
    const res = await fetch(API_BASE + "/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(await res.text());

    alert("Order saved! ✔️");
    lines = [];
    updateOrderUI();
  } catch (err) {
    console.error(err);
    alert("Failed to save order, see console for details.");
  }
}

completeBtn?.addEventListener("click", completeOrder);

/* SEARCH LISTENER */
$("#search-input").addEventListener("input", renderProducts);

/* INITIAL RENDER */
renderCategories();
renderProducts();
