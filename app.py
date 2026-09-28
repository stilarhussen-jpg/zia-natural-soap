from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
from pathlib import Path
from datetime import datetime
import json
import urllib.parse

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

# =========================================================
# ZIA NATURAL SOAP COLLECTION
# Edit product names/prices/descriptions here.
# =========================================================

WHATSAPP_NUMBER = "919702656967"
BUSINESS_NAME = "ZIA Natural Soap Collection"
CURRENCY = "₹"

PRODUCTS = [
    {
        "id": 1,
        "name": "Coffee Rice Soap",
        "price": 120,
        "description": "Handmade soap with a coffee and rice inspired natural-care theme.",
        "emoji": "☕",
        "image_position": "2% 35%",
    },
    {
        "id": 2,
        "name": "Neem Soap",
        "price": 120,
        "description": "Handmade neem soap for a fresh, clean bathing routine.",
        "emoji": "🌿",
        "image_position": "50% 35%",
    },
    {
        "id": 3,
        "name": "D Tan Soap",
        "price": 120,
        "description": "Handmade soap with a turmeric and citrus inspired formulation theme.",
        "emoji": "🍊",
        "image_position": "98% 35%",
    },
    {
        "id": 4,
        "name": "Charcoal Soap",
        "price": 120,
        "description": "Handmade charcoal soap designed for a deep-clean feeling.",
        "emoji": "🖤",
        "image_position": "2% 100%",
    },
    {
        "id": 5,
        "name": "Multani Mitti Soap",
        "price": 120,
        "description": "Handmade soap featuring a traditional Multani Mitti inspired theme.",
        "emoji": "🤎",
        "image_position": "50% 100%",
    },
    {
        "id": 6,
        "name": "Beetroot Soap",
        "price": 120,
        "description": "Handmade beetroot inspired soap for a fresh bathing experience.",
        "emoji": "❤️",
        "image_position": "98% 100%",
    },
]

ORDERS_FILE = Path("orders.json")


def get_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def cart_items():
    cart = session.get("cart", {})
    items = []
    total = 0

    for product_id, qty in cart.items():
        product = get_product(int(product_id))
        if product:
            qty = int(qty)
            subtotal = product["price"] * qty
            items.append({
                **product,
                "qty": qty,
                "subtotal": subtotal
            })
            total += subtotal

    return items, total


def save_order(order):
    orders = []
    if ORDERS_FILE.exists():
        try:
            orders = json.loads(ORDERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            orders = []

    orders.append(order)
    ORDERS_FILE.write_text(
        json.dumps(orders, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ business_name }}</title>

<style>
:root{
    --green:#0d5c2b;
    --green2:#167a38;
    --light:#f6f4df;
    --cream:#fffdf2;
    --gold:#d79b20;
    --dark:#12351e;
    --red:#c92b20;
    --shadow:0 12px 30px rgba(0,0,0,.10);
}

*{box-sizing:border-box;scroll-behavior:smooth}

body{
    margin:0;
    font-family:Arial,Helvetica,sans-serif;
    background:var(--cream);
    color:#17321e;
}

.navbar{
    position:sticky;
    top:0;
    z-index:50;
    background:rgba(255,255,255,.97);
    box-shadow:0 3px 15px rgba(0,0,0,.08);
    padding:14px 5%;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
}

.logo{
    display:flex;
    align-items:center;
    gap:12px;
    font-weight:900;
    color:var(--green);
    font-size:21px;
}

.logo img{
    width:52px;
    height:52px;
    object-fit:cover;
    border-radius:50%;
}

.navlinks{
    display:flex;
    gap:22px;
    align-items:center;
}

.navlinks a{
    text-decoration:none;
    color:#21452b;
    font-weight:700;
}

.cart-btn{
    background:var(--green);
    color:white!important;
    padding:11px 17px;
    border-radius:25px;
}

.hero{
    padding:30px 5% 45px;
    background:
      radial-gradient(circle at top right, rgba(30,120,55,.18), transparent 35%),
      linear-gradient(135deg,#fffdf0,#edf5df);
}

.hero-grid{
    max-width:1250px;
    margin:auto;
    display:grid;
    grid-template-columns:1.05fr .95fr;
    gap:35px;
    align-items:center;
}

.hero-text h1{
    font-size:clamp(40px,6vw,78px);
    margin:0;
    line-height:.95;
    color:var(--green);
}

.hero-text h1 span{
    color:#111;
    font-size:.48em;
    display:block;
    letter-spacing:3px;
    margin-top:18px;
}

.hero-text p{
    font-size:20px;
    line-height:1.6;
    max-width:620px;
}

.offer{
    display:inline-block;
    background:var(--red);
    color:#fff;
    padding:14px 24px;
    border-radius:12px;
    font-size:27px;
    font-weight:900;
    margin:10px 0 18px;
    box-shadow:var(--shadow);
}

.cta-row{
    display:flex;
    flex-wrap:wrap;
    gap:12px;
}

.btn{
    display:inline-block;
    border:0;
    cursor:pointer;
    text-decoration:none;
    padding:14px 22px;
    border-radius:30px;
    font-size:16px;
    font-weight:800;
}

.btn-green{background:var(--green);color:#fff}
.btn-light{background:#fff;color:var(--green);border:2px solid var(--green)}
.btn-whatsapp{background:#1fae55;color:#fff}

.hero-poster{
    background:#fff;
    padding:10px;
    border-radius:24px;
    box-shadow:var(--shadow);
}

.hero-poster img{
    width:100%;
    display:block;
    border-radius:17px;
}

.section{
    padding:70px 5%;
}

.section-title{
    text-align:center;
    color:var(--green);
    font-size:38px;
    margin:0 0 12px;
}

.section-sub{
    text-align:center;
    color:#5a6d5e;
    margin:0 auto 38px;
    max-width:700px;
    line-height:1.6;
}

.products{
    max-width:1200px;
    margin:auto;
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:22px;
}

.card{
    background:#fff;
    border-radius:20px;
    overflow:hidden;
    box-shadow:var(--shadow);
    border:1px solid #e7eadf;
}

.product-image{
    height:210px;
    background-image:url("/static/poster.jpg");
    background-repeat:no-repeat;
    background-size:319% auto;
    background-position:var(--img-pos);
    border-bottom:1px solid #e7eadf;
}

.card-body{padding:20px}

.card h3{
    color:var(--green);
    margin:0 0 8px;
    font-size:23px;
}

.price{
    color:var(--red);
    font-size:24px;
    font-weight:900;
    margin:12px 0;
}

.card p{
    color:#657267;
    line-height:1.5;
    min-height:48px;
}

.card-actions{
    display:flex;
    gap:8px;
}

.card-actions .btn{
    flex:1;
    text-align:center;
}

.features{
    max-width:1150px;
    margin:auto;
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:18px;
}

.feature{
    background:#fff;
    border-radius:18px;
    padding:25px;
    text-align:center;
    box-shadow:var(--shadow);
}

.feature .icon{font-size:38px}
.feature h3{color:var(--green)}

.checkout{
    max-width:850px;
    margin:auto;
    background:#fff;
    padding:30px;
    border-radius:24px;
    box-shadow:var(--shadow);
}

.form-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
}

.field{margin-bottom:15px}
.field.full{grid-column:1/-1}

label{
    display:block;
    font-weight:700;
    margin-bottom:7px;
}

input,textarea,select{
    width:100%;
    padding:14px;
    border:1px solid #ccd7ca;
    border-radius:11px;
    font-size:16px;
    outline:none;
}

input:focus,textarea:focus,select:focus{
    border-color:var(--green);
}

.order-summary{
    background:#f3f8ed;
    border-radius:15px;
    padding:18px;
    margin:10px 0 20px;
}

.summary-row{
    display:flex;
    justify-content:space-between;
    padding:7px 0;
}

.total{
    border-top:1px solid #ccd7ca;
    margin-top:8px;
    padding-top:12px;
    font-size:21px;
    font-weight:900;
}

footer{
    background:#0c3419;
    color:#fff;
    padding:45px 5%;
    text-align:center;
}

footer h2{margin-top:0}
footer a{color:#fff}

.notice{
    max-width:900px;
    margin:0 auto 20px;
    background:#fff7d6;
    border:1px solid #ead78a;
    padding:15px;
    border-radius:12px;
    line-height:1.5;
}

@media(max-width:850px){
    .hero-grid{grid-template-columns:1fr}
    .products{grid-template-columns:repeat(2,1fr)}
    .features{grid-template-columns:repeat(2,1fr)}
}

@media(max-width:600px){
    .navbar{flex-wrap:wrap}
    .navlinks{width:100%;justify-content:center;gap:12px;font-size:14px}
    .products{grid-template-columns:1fr}
    .features{grid-template-columns:1fr}
    .form-grid{grid-template-columns:1fr}
    .field.full{grid-column:auto}
    .hero{padding-top:20px}
}
</style>
</head>

<body>

<nav class="navbar">
    <div class="logo">
        <img src="/static/poster.jpg" alt="ZIA">
        <div>
            ZIA<br>
            <small>NATURAL SOAP</small>
        </div>
    </div>

    <div class="navlinks">
        <a href="#home">Home</a>
        <a href="#products">Soaps</a>
        <a href="#about">About</a>
        <a href="#checkout" class="cart-btn">🛒 Cart (<span id="cartCount">{{ cart_count }}</span>)</a>
    </div>
</nav>

<section class="hero" id="home">
    <div class="hero-grid">
        <div class="hero-text">
            <h1>ZIA <span>NATURAL SOAP COLLECTION</span></h1>

            <p>
                Handmade soap collection inspired by natural ingredients.
                Shop your favourite soap online and place your order directly.
            </p>

            <div class="offer">BUY ANY SOAP ₹120 ONLY</div>

            <div class="cta-row">
                <a class="btn btn-green" href="#products">SHOP NOW</a>
                <a class="btn btn-whatsapp"
                   href="https://wa.me/{{ whatsapp }}?text={{ whatsapp_intro|urlencode }}"
                   target="_blank">📱 WhatsApp Order</a>
            </div>
        </div>

        <div class="hero-poster">
            <img src="/static/poster.jpg" alt="ZIA Natural Soap Collection">
        </div>
    </div>
</section>

<section class="section" id="products">
    <h2 class="section-title">Our Natural Soap Collection</h2>
    <p class="section-sub">
        Choose your soap, add it to the cart and complete your order.
        Prices can be changed later in the Python product list.
    </p>

    <div class="products">
        {% for p in products %}
        <article class="card">
            <div class="product-image"
                 style="--img-pos: {{ p.image_position }};"
                 aria-label="{{ p.name }}"></div>
            <div class="card-body">
                <h3>{{ p.name }}</h3>
                <div class="price">₹{{ p.price }}</div>
                <p>{{ p.description }}</p>

                <div class="card-actions">
                    <button class="btn btn-green" onclick="addToCart({{ p.id }})">
                        Add to Cart
                    </button>
                    <a class="btn btn-light" href="#checkout">Buy</a>
                </div>
            </div>
        </article>
        {% endfor %}
    </div>
</section>

<section class="section" id="about">
    <h2 class="section-title">Why ZIA?</h2>
    <p class="section-sub">
        A simple online store for your handmade soap business.
    </p>

    <div class="features">
        <div class="feature">
            <div class="icon">🌿</div>
            <h3>Natural Theme</h3>
            <p>Products presented with a clean, natural brand style.</p>
        </div>
        <div class="feature">
            <div class="icon">🧼</div>
            <h3>Handmade</h3>
            <p>Showcase your handmade soap collection online.</p>
        </div>
        <div class="feature">
            <div class="icon">📦</div>
            <h3>Easy Ordering</h3>
            <p>Customers can add products to a cart and submit an order.</p>
        </div>
        <div class="feature">
            <div class="icon">📱</div>
            <h3>WhatsApp</h3>
            <p>Customers can contact your business directly through WhatsApp.</p>
        </div>
    </div>
</section>

<section class="section" id="checkout">
    <h2 class="section-title">Place Your Order</h2>
    <p class="section-sub">
        Fill in your delivery details. The order will be saved in your local
        <b>orders.json</b> file and a WhatsApp message can also be sent.
    </p>

    <div class="checkout">

        <div class="notice">
            <b>Important:</b> This starter version supports Cash on Delivery
            and WhatsApp ordering. Online UPI/card payment can be connected later.
        </div>

        <div class="order-summary" id="summary">
            <b>Your Cart</b>
            <div id="summaryItems">
                Loading cart...
            </div>
            <div class="summary-row total">
                <span>Total</span>
                <span id="summaryTotal">₹0</span>
            </div>
        </div>

        <form method="POST" action="{{ url_for('checkout') }}">
            <div class="form-grid">

                <div class="field">
                    <label>Customer Name *</label>
                    <input name="name" required placeholder="Your full name">
                </div>

                <div class="field">
                    <label>Mobile Number *</label>
                    <input name="phone" required placeholder="10 digit mobile number">
                </div>

                <div class="field full">
                    <label>Delivery Address *</label>
                    <textarea name="address" rows="3" required
                              placeholder="House number, street, area"></textarea>
                </div>

                <div class="field">
                    <label>City *</label>
                    <input name="city" required placeholder="City">
                </div>

                <div class="field">
                    <label>State *</label>
                    <input name="state" required placeholder="State">
                </div>

                <div class="field">
                    <label>PIN Code *</label>
                    <input name="pincode" required placeholder="PIN code">
                </div>

                <div class="field">
                    <label>Payment</label>
                    <select name="payment">
                        <option>Cash on Delivery</option>
                        <option>UPI - Coming Soon</option>
                    </select>
                </div>

                <div class="field full">
                    <button class="btn btn-green" style="width:100%" type="submit">
                        ✅ PLACE ORDER
                    </button>
                </div>

            </div>
        </form>

    </div>
</section>

<footer>
    <h2>{{ business_name }}</h2>
    <p>Natural Handmade Soap Collection</p>
    <p>📱 WhatsApp: +91 9702656967</p>
    <p>
        <a href="https://wa.me/{{ whatsapp }}?text={{ whatsapp_intro|urlencode }}"
           target="_blank">Chat on WhatsApp</a>
    </p>
</footer>

<script>
async function addToCart(productId){
    const response = await fetch("/api/cart/add", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({product_id:productId})
    });

    const data = await response.json();
    document.getElementById("cartCount").innerText = data.count;
    loadCart();

    alert("Added to cart!");
}

async function removeFromCart(productId){
    await fetch("/api/cart/remove", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({product_id:productId})
    });

    loadCart();
}

async function loadCart(){
    const response = await fetch("/api/cart");
    const data = await response.json();

    document.getElementById("cartCount").innerText = data.count;

    const box = document.getElementById("summaryItems");

    if(data.items.length === 0){
        box.innerHTML = "<p>Your cart is empty. Please select a soap above.</p>";
        document.getElementById("summaryTotal").innerText = "₹0";
        return;
    }

    box.innerHTML = data.items.map(item => `
        <div class="summary-row">
            <span>
                ${item.name} × ${item.qty}
                <button onclick="removeFromCart(${item.id})"
                        style="border:0;background:none;color:#c92b20;cursor:pointer">
                    Remove
                </button>
            </span>
            <span>₹${item.subtotal}</span>
        </div>
    `).join("");

    document.getElementById("summaryTotal").innerText = "₹" + data.total;
}

loadCart();
</script>

</body>
</html>
"""


@app.route("/")
def home():
    items, total = cart_items()
    cart_count = sum(item["qty"] for item in items)

    return render_template_string(
        HTML,
        products=PRODUCTS,
        business_name=BUSINESS_NAME,
        whatsapp=WHATSAPP_NUMBER,
        whatsapp_intro=f"Hello {BUSINESS_NAME}, I want to order your natural soaps.",
        cart_count=cart_count
    )


@app.post("/api/cart/add")
def add_to_cart():
    data = request.get_json(silent=True) or {}
    product_id = int(data.get("product_id", 0))
    product = get_product(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + 1
    session["cart"] = cart
    session.modified = True

    return jsonify({
        "ok": True,
        "count": sum(int(v) for v in cart.values())
    })


@app.post("/api/cart/remove")
def remove_from_cart():
    data = request.get_json(silent=True) or {}
    product_id = str(int(data.get("product_id", 0)))

    cart = session.get("cart", {})
    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return jsonify({"ok": True})


@app.get("/api/cart")
def api_cart():
    items, total = cart_items()
    count = sum(item["qty"] for item in items)

    return jsonify({
        "items": items,
        "total": total,
        "count": count
    })


@app.post("/checkout")
def checkout():
    items, total = cart_items()

    if not items:
        return redirect(url_for("home") + "#products")

    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    state = request.form.get("state", "").strip()
    pincode = request.form.get("pincode", "").strip()
    payment = request.form.get("payment", "Cash on Delivery")

    order_id = "ZIA-" + datetime.now().strftime("%Y%m%d%H%M%S")

    order = {
        "order_id": order_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "customer": {
            "name": name,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "pincode": pincode
        },
        "items": items,
        "total": total,
        "payment": payment,
        "status": "Pending"
    }

    save_order(order)
    session["cart"] = {}

    message_lines = [
        f"Hello {BUSINESS_NAME},",
        f"New Order: {order_id}",
        "",
        f"Customer: {name}",
        f"Phone: {phone}",
        f"Address: {address}, {city}, {state} - {pincode}",
        "",
        "Products:"
    ]

    for item in items:
        message_lines.append(
            f"- {item['name']} x {item['qty']} = ₹{item['subtotal']}"
        )

    message_lines += [
        "",
        f"Total: ₹{total}",
        f"Payment: {payment}"
    ]

    whatsapp_url = (
        "https://wa.me/" + WHATSAPP_NUMBER +
        "?text=" + urllib.parse.quote("\n".join(message_lines))
    )

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Order Confirmed</title>
      <style>
        body{font-family:Arial;background:#f3f7eb;margin:0;padding:30px}
        .box{max-width:650px;margin:50px auto;background:#fff;padding:35px;
             border-radius:22px;box-shadow:0 12px 30px rgba(0,0,0,.1);text-align:center}
        h1{color:#0d5c2b}
        .id{font-size:25px;font-weight:900;color:#c92b20}
        a{display:inline-block;padding:14px 22px;margin:8px;border-radius:25px;
          text-decoration:none;font-weight:800}
        .green{background:#0d5c2b;color:#fff}
        .wa{background:#1fae55;color:#fff}
      </style>
    </head>
    <body>
      <div class="box">
        <div style="font-size:60px">✅</div>
        <h1>Order Received!</h1>
        <p>Your order has been saved successfully.</p>
        <p>Order ID</p>
        <div class="id">{{ order_id }}</div>
        <p>Total: <b>₹{{ total }}</b></p>

        <a class="wa" href="{{ whatsapp_url }}" target="_blank">
          📱 Send Order on WhatsApp
        </a>

        <a class="green" href="{{ url_for('home') }}">
          Continue Shopping
        </a>
      </div>
    </body>
    </html>
    """, order_id=order_id, total=total, whatsapp_url=whatsapp_url)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

