// Catalog of POS Consumables

const catalog = [
  { id: 1, name: "Full English Plate", price: 10.5, cat: "breakfast" },
  {
    id: 2,
    name: "Smoked Salmon & Scrambled Eggs on Sourdough",
    price: 9.8,
    cat: "breakfast",
  },
  {
    id: 3,
    name: "Avocado-Chili Smash, Feta & Poached Egg",
    price: 8.9,
    cat: "breakfast",
  },
  {
    id: 4,
    name: "Cinnamon Brioche French Toast",
    price: 7.5,
    cat: "breakfast",
  },
  { id: 5, name: "Maple-Pecan Granola Bowl", price: 6.2, cat: "breakfast" },
  {
    id: 6,
    name: "Breakfast Burrito with Chorizo",
    price: 8.4,
    cat: "breakfast",
  },
  {
    id: 7,
    name: 'Vegan "Sunrise" Tofu Scramble Wrap',
    price: 7.9,
    cat: "breakfast",
  },
  {
    id: 8,
    name: "Buttermilk Pancakes, Berry Compote, Crème Fraîche",
    price: 7.8,
    cat: "breakfast",
  },
  {
    id: 9,
    name: "Porridge with Honey, Banana & Seeds",
    price: 4.8,
    cat: "breakfast",
  },
  {
    id: 10,
    name: "Chargrilled Rib-Eye Steak, Chimichurri, Fries",
    price: 23.5,
    cat: "main_meal",
  },
  {
    id: 11,
    name: "Pan-Seared Sea Bass, Lemon-Caper Butter",
    price: 18.9,
    cat: "main_meal",
  },
  {
    id: 12,
    name: "Slow-Cooked Lamb Shank, Rosemary Jus",
    price: 19.8,
    cat: "main_meal",
  },
  {
    id: 13,
    name: "Wild-Mushroom Risotto, Truffle Oil",
    price: 14.6,
    cat: "main_meal",
  },
  {
    id: 14,
    name: "Chicken Katsu Curry, Sticky Rice",
    price: 15.2,
    cat: "main_meal",
  },
  {
    id: 15,
    name: "BBQ Jackfruit Burger, Sweet-Potato Fries",
    price: 13.4,
    cat: "main_meal",
  },
  {
    id: 16,
    name: "Handmade Spinach & Ricotta Ravioli",
    price: 13.9,
    cat: "main_meal",
  },
  {
    id: 17,
    name: "Pulled Pork Tacos (3) & Pico de Gallo",
    price: 14.2,
    cat: "main_meal",
  },
  {
    id: 18,
    name: "Harissa-Roasted Cauliflower Steak, Tahini Drizzle",
    price: 12.8,
    cat: "main_meal",
  },
  {
    id: 19,
    name: "Dark Chocolate Fondant, Vanilla Ice Cream",
    price: 7.6,
    cat: "dessert",
  },
  {
    id: 20,
    name: "Classic Sticky Toffee Pudding",
    price: 6.9,
    cat: "dessert",
  },
  {
    id: 21,
    name: "Lemon Posset, Shortbread Crumble",
    price: 6.5,
    cat: "dessert",
  },
  { id: 22, name: "Salted Caramel Cheesecake", price: 6.8, cat: "dessert" },
  { id: 23, name: "Affogato al Caffè", price: 5.2, cat: "dessert" },
  { id: 24, name: "Eton Mess with Strawberries", price: 6.4, cat: "dessert" },
  {
    id: 25,
    name: "Baked Apple & Cinnamon Crumble",
    price: 6.3,
    cat: "dessert",
  },
  { id: 26, name: "Pistachio Gelato Trio", price: 5.8, cat: "dessert" },
  {
    id: 27,
    name: "Vegan Chocolate-Avocado Mousse",
    price: 6,
    cat: "dessert",
  },
  { id: 28, name: "Flat White", price: 3.2, cat: "hot_drink" },
  { id: 29, name: "Cappuccino", price: 3, cat: "hot_drink" },
  { id: 30, name: "Americano", price: 2.7, cat: "hot_drink" },
  { id: 31, name: "Espresso (single)", price: 2.1, cat: "hot_drink" },
  { id: 32, name: "Mocha", price: 3.4, cat: "hot_drink" },
  { id: 33, name: "Matcha Latte", price: 3.6, cat: "hot_drink" },
  {
    id: 34,
    name: "Loose-Leaf English Breakfast Tea",
    price: 2.4,
    cat: "hot_drink",
  },
  { id: 35, name: "Earl Grey Tea", price: 2.5, cat: "hot_drink" },
  {
    id: 36,
    name: "Fresh Mint & Honey Infusion",
    price: 2.7,
    cat: "hot_drink",
  },
  {
    id: 37,
    name: "Fresh-Pressed Orange Juice",
    price: 3.5,
    cat: "soft_drink",
  },
  {
    id: 38,
    name: "Homemade Elderflower Lemonade",
    price: 3.2,
    cat: "soft_drink",
  },
  {
    id: 39,
    name: "Sparkling Apple & Ginger Fizz",
    price: 3.3,
    cat: "soft_drink",
  },
  {
    id: 40,
    name: "Still Mineral Water (750 ml)",
    price: 2.9,
    cat: "soft_drink",
  },
  {
    id: 41,
    name: "Sparkling Mineral Water (750 ml)",
    price: 3.1,
    cat: "soft_drink",
  },
  { id: 42, name: "Cola (bottle)", price: 2.7, cat: "soft_drink" },
  { id: 43, name: "Diet Cola (bottle)", price: 2.7, cat: "soft_drink" },
  {
    id: 44,
    name: "Raspberry & Hibiscus Iced Tea",
    price: 3.4,
    cat: "soft_drink",
  },
  { id: 45, name: "Coconut Water (can)", price: 3, cat: "soft_drink" },
  { id: 46, name: "Draught Pale Ale (pint)", price: 5.8, cat: "alcoholic" },
  { id: 47, name: "House Red Wine, 175 ml", price: 6.2, cat: "alcoholic" },
  { id: 48, name: "House White Wine, 175 ml", price: 6.2, cat: "alcoholic" },
  { id: 49, name: "Prosecco, 125 ml", price: 7, cat: "alcoholic" },
  { id: 50, name: "Classic Gin & Tonic", price: 7.5, cat: "alcoholic" },
  { id: 51, name: "Passion-Fruit Martini", price: 8.4, cat: "alcoholic" },
  { id: 52, name: "Old Fashioned", price: 8.6, cat: "alcoholic" },
  { id: 53, name: "Aperol Spritz", price: 7.8, cat: "alcoholic" },
  {
    id: 54,
    name: "Alcohol-Free Lager (bottle)",
    price: 4.6,
    cat: "alcoholic",
  },
];

// 1)  DOM refs

const $filters = document.getElementById("filters");
const $products = document.getElementById("products");
const $orderItems = document.getElementById("order-items");
const $orderTotal = document.getElementById("order-total");
const $completeBtn = document.getElementById("complete-btn");

// 2)  Order state

const orderLines = [];
let currentCat = "breakfast";

// 3)  Build filter buttons

function initFilters() {
  const cats = Array.from(new Set(catalog.map((p) => p.cat)));
  const allButtonsHtml = [...cats]
    .map((cat) => `<button class="cat-btn" data-cat="${cat}">${cat}</button>`)
    .join("");
  $filters.innerHTML = allButtonsHtml;

  $filters.addEventListener("click", (e) => {
    if (!e.target.dataset.cat) return;
    currentCat = e.target.dataset.cat;
    renderCatalog();
  });
}

// 4)  Build product buttons

function renderCatalog() {
  const items =
    currentCat === "breakfast"
      ? catalog
      : catalog.filter((p) => p.cat === currentCat);

  $products.innerHTML = items
    .map(
      (item) => `<button class="product-btn" data-id="${item.id}">
                   ${item.name}<br>£${item.price}
                 </button>`
    )
    .join("");
}

// 5)  Add-to-order logic

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
  $orderItems.innerHTML = orderLines
    .map((l) => `<li>${l.qty} × ${l.name} – £${l.lineTotal}</li>`)
    .join("");

  const total = orderLines.reduce((sum, l) => sum + l.qty * l.price, 0);
  $orderTotal.textContent = total.toFixed(2);
}

// 6)  Delegate product-button clicks

$products.addEventListener("click", (e) => {
  if (!e.target.dataset.id) return;
  const id = Number(e.target.dataset.id);
  const item = catalog.find((p) => p.id === id);
  addToOrder(item);
});

// 7)  Complete-order handler

$completeBtn.addEventListener("click", async () => {
  if (!orderLines.length) return alert("No items on the order.");

  const apiLines = orderLines.map((l) => ({ cons_id: l.id, qty: l.qty }));

  const payload = {
    timestamp: new Date().toISOString(),
    lines: apiLines,
  };

  try {
    const res = await fetch("http://localhost:5000/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(await res.text());
    alert("Order saved!");
    orderLines.length = 0;
    renderOrder();
  } catch (err) {
    console.error(err);
    alert("Failed to save order.");
  }
});

// 8)  Init

initFilters();
renderCatalog();
