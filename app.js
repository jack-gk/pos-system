// --- Catalog
const catalog = [
  /* Drinks */
  { id: 1, name: "Coffee", price: 2.5 },
  { id: 2, name: "Espresso", price: 2.0 },
  { id: 3, name: "Cappuccino", price: 3.0 },
  { id: 4, name: "Latte", price: 3.2 },
  { id: 5, name: "Hot Chocolate", price: 2.8 },
  { id: 6, name: "Tea", price: 2.0 },
  { id: 7, name: "Orange Juice", price: 2.0 },
  { id: 8, name: "Soda (Can)", price: 1.3 },
  { id: 9, name: "Bottled Water", price: 1.0 },

  /* Pastries & snacks */
  { id: 10, name: "Bagel", price: 1.8 },
  { id: 11, name: "Bagel w/ Cream Cheese", price: 2.2 },
  { id: 12, name: "Croissant", price: 2.4 },
  { id: 13, name: "Muffin", price: 2.2 },
  { id: 14, name: "Donut", price: 1.5 },
  { id: 15, name: "Cookie", price: 1.2 },
  { id: 16, name: "Brownie", price: 2.0 },

  /* Sandwiches & light meals */
  { id: 17, name: "Ham & Cheese Sandwich", price: 4.5 },
  { id: 18, name: "Tuna Sandwich", price: 4.8 },
  { id: 19, name: "Chicken Panini", price: 5.0 },
  { id: 20, name: "Garden Salad (Small)", price: 3.5 },
];

// --- DOM refs
const $products = document.getElementById("products");
const $orderItems = document.getElementById("order-items");
const $orderTotal = document.getElementById("order-total");
const $completeBtn = document.getElementById("complete-btn");

// --- Order state
const orderLines = [];

function addToOrder(item) {
  const line = orderLines.find((l) => l.id === item.id);
  if (line) {
    line.qty += 1;
    line.lineTotal = (line.qty * item.price).toFixed(2);
  } else {
    orderLines.push({ ...item, qty: 1, lineTotal: item.price.toFixed(2) });
  }
  renderOrder();
}

function renderOrder() {
  // list items
  $orderItems.innerHTML = orderLines
    .map((l) => `<li>${l.qty} × ${l.name} – £${l.lineTotal}</li>`)
    .join("");

  // grand total
  const total = orderLines.reduce((sum, l) => sum + l.qty * l.price, 0);
  $orderTotal.textContent = total.toFixed(2);
}

// --- Build product buttons dynamically
function initCatalog() {
  $products.innerHTML = catalog
    .map(
      (item) => `<button class="product-btn" data-id="${item.id}">
                 ${item.name}<br>£${item.price}
               </button>`
    )
    .join("");

  // delegate clicks
  $products.addEventListener("click", (e) => {
    if (!e.target.dataset.id) return;
    const id = Number(e.target.dataset.id);
    const item = catalog.find((p) => p.id === id);
    addToOrder(item);
  });
}

// --- Complete / send order
$completeBtn.addEventListener("click", async () => {
  if (!orderLines.length) return alert("No items on the order.");

  const payload = {
    timestamp: new Date().toISOString(),
    lines: orderLines,
  };

  try {
    // Send to Python API
    const res = await fetch("http://localhost:5000/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(await res.text());
    alert("Order saved!");
    orderLines.length = 0; // clear array in-place
    renderOrder(); // refresh UI
  } catch (err) {
    console.error(err);
    alert("Failed to save order.");
  }
});

// --- init
initCatalog();
