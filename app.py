<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>KDD STUDIO | Official</title>

    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">

    <style>
        :root {
            --bg: #030712;
            --card: rgba(15, 23, 42, 0.7);
            --primary: #00e5ff;
            --secondary: #ff2fd0;
            --text: #ffffff;
            --muted: #94a3b8;
            --radius: 20px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        
        body { 
            background: var(--bg); 
            color: var(--text); 
            line-height: 1.6;
            overflow-x: hidden;
            background-image: radial-gradient(circle at top right, rgba(0, 229, 255, 0.1), transparent 40%);
        }

        /* --- NAVIGATION --- */
        header {
            position: fixed; top: 0; width: 100%;
            background: rgba(3, 7, 18, 0.95);
            backdrop-filter: blur(15px);
            z-index: 2000;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        nav {
            max-width: 1200px; margin: auto;
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px 20px;
            position: relative;
        }
        nav h1 {
            font-size: 22px; font-weight: 800;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--primary));
            background-size: 200% auto;
            -webkit-background-clip: text; color: transparent;
            animation: shineText 3s linear infinite;
        }

        /* MENU ICON (Mobile only) */
        .menu-icon {
            display: none;
            font-size: 30px;
            color: var(--primary);
            cursor: pointer;
        }

        /* NAVIGATION MENU */
        .nav-links { display: flex; gap: 10px; list-style: none; }
        .nav-links a {
            color: var(--text); text-decoration: none; font-weight: 600; font-size: 13px;
            padding: 8px 15px; border-radius: 50px; transition: 0.3s;
            border: 1px solid transparent;
        }
        .nav-links a:hover { background: rgba(0, 229, 255, 0.1); border-color: var(--primary); }

        /* --- BUTTONS --- */
        .btn {
            padding: 12px 24px; border: none; border-radius: 50px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: #000; font-weight: 700; cursor: pointer;
            transition: 0.3s; box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
            font-size: 14px; text-transform: uppercase;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 0 25px rgba(255, 47, 208, 0.5); }

        /* --- SECTIONS --- */
        section { min-height: 100vh; padding: 100px 20px 60px; max-width: 1100px; margin: auto; }
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.6s ease-out; }

        /* HERO AREA */
        .hero { display: flex; flex-direction: column; gap: 40px; align-items: center; text-align: center; }
        .hero-text h2 { font-size: 42px; line-height: 1.2; font-weight: 800; }
        .hero-text span { color: var(--primary); }
        
        .hero-img {
            width: 100%; max-width: 500px; border-radius: var(--radius);
            position: relative; overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: float 5s infinite ease-in-out;
        }
        .hero-img img { width: 100%; display: block; }
        .hero-img::after {
            content: ""; position: absolute; top: 0; left: -150%; width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transform: skewX(-20deg); animation: shineSwipe 4s infinite;
        }

        /* --- SERVICE CARDS --- */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
        .card {
            background: var(--card); padding: 30px; border-radius: var(--radius);
            text-align: center; border: 1px solid rgba(255, 255, 255, 0.05);
            transition: 0.3s;
        }
        .card:hover { border-color: var(--primary); transform: translateY(-10px); }
        .card i { font-size: 45px; color: var(--primary); margin-bottom: 15px; }

        /* --- DiNuX AI UI --- */
        .ai-container {
            background: rgba(0, 0, 0, 0.4); border: 2px solid var(--primary);
            border-radius: var(--radius); padding: 25px; margin-top: 40px;
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.2);
        }
        .ai-chat-box { height: 200px; overflow-y: auto; margin-bottom: 15px; padding: 10px; text-align: left; }
        .ai-input-group { display: flex; gap: 10px; }
        .ai-input-group input { 
            flex: 1; padding: 12px; border-radius: 30px; border: 1px solid var(--muted);
            background: #000; color: #fff; outline: none;
        }

        /* --- FORMS --- */
        .order-box { background: var(--card); padding: 25px; border-radius: var(--radius); margin-top: 20px; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 10px; border: none; background: #0f172a; color: #fff; }

        /* --- ANIMATIONS --- */
        @keyframes shineText { 0% { background-position: 0%; } 100% { background-position: 200%; } }
        @keyframes shineSwipe { 0% { left: -150%; } 30% { left: 150%; } 100% { left: 150%; } }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* --- MOBILE OPTIMIZATION (WITH EXPANDABLE MENU) --- */
        @media (max-width: 768px) {
            .menu-icon { display: block; }
            .nav-links {
                display: none; /* Hidden by default */
                flex-direction: column;
                position: absolute;
                top: 60px; left: 0; width: 100%;
                background: rgba(3, 7, 18, 0.98);
                padding: 20px;
                text-align: center;
                border-bottom: 1px solid var(--primary);
                gap: 15px;
            }
            .nav-links.active { display: flex; } /* Show when toggled */
            .nav-links a { font-size: 16px; padding: 10px; display: block; width: 100%; }
            .hero-text h2 { font-size: 30px; }
            section { padding: 80px 15px 40px; }
            .grid { grid-template-columns: 1fr; }
            .ai-input-group { flex-direction: column; }
        }
    </style>
</head>

<body>

<header>
    <nav>
        <h1>KDD STUDIO</h1>
        <div class="menu-icon" onclick="toggleMenu()">
            <i class='bx bx-menu-alt-right'></i>
        </div>
        <ul class="nav-links" id="navLinks">
            <li><a href="#" onclick="showPage('home')">HOME</a></li>
            <li><a href="#" onclick="showPage('services')">SERVICES</a></li>
            <li><a href="#" onclick="showPage('cart')">CART (<span id="cartCount">0</span>)</a></li>
            <li><button class="btn" style="width: 100%;" onclick="showPage('services')">Order Now</button></li>
        </ul>
    </nav>
</header>

<!-- HOME -->
<section id="home" class="page active">
    <div class="hero">
        <div class="hero-text">
            <h2>3D <span>Home Designing</span><br>Modern Architecture</h2>
            <p style="color: var(--muted); margin: 15px 0;">Professional 3D house designs, realistic renders & walkthrough videos.</p>
            <button class="btn" onclick="showPage('services')">Explore Services</button>
        </div>
        <div class="hero-img">
            <img src="./dvni9.png" alt="3D Work">
        </div>
    </div>
</section>

<!-- SERVICES -->
<section id="services" class="page">
    <h2 style="text-align: center;">Our Services</h2>
    <div class="grid">
        <div class="card" onclick="showPage('service3d')">
            <i class='bx bxs-home-heart'></i>
            <h3>3D Home Designing</h3>
        </div>
        <div class="card" onclick="showPage('servicetiktok')">
            <i class='bx bxl-tiktok'></i>
            <h3>TikTok Promotion</h3>
        </div>
        <div class="card" onclick="showPage('servicegraphic')">
            <i class='bx bxs-paint-roll'></i>
            <h3>Graphic Designing</h3>
        </div>
    </div>

    <!-- DiNuX AI INTEGRATED -->
    <div class="ai-container">
        <h3><i class='bx bxs-bot'></i> Talk with DiNuX AI</h3>
        <div class="ai-chat-box" id="chatBox">
            <p style="color: var(--muted);">DiNuX: Hello! How can I help you today?</p>
        </div>
        <div class="ai-input-group">
            <input type="text" id="userInput" placeholder="Type a message...">
            <button class="btn" onclick="aiReply()">Send</button>
        </div>
    </div>
</section>

<!-- SERVICE DETAIL: 3D -->
<section id="service3d" class="page">
    <h2>3D HOME DESIGNING</h2>
    <div class="hero-img" style="margin: 20px 0;"><img src="front.png"></div>
    <div class="card">
        <h3>Package Pricing</h3>
        <p>Standard: Rs. 100,000.00+</p>
        <p>Full Animation: Rs. 250,000.00+</p>
        <br>
        <button class="btn" onclick="addToCart('3D Home Designing', 100000)">Add to Cart</button>
    </div>
</section>

<!-- CART & ORDER -->
<section id="cart" class="page">
    <h2>Your Cart</h2>
    <div id="cartItems" style="margin: 20px 0; min-height: 50px;"></div>
    
    <div class="order-box">
        <h3>Order Details</h3>
        <input id="name" placeholder="Your Name">
        <input id="phone" placeholder="Phone Number">
        <textarea id="note" placeholder="Project details..."></textarea>
        <button class="btn" style="width: 100%;" onclick="sendWhatsApp()">Confirm via WhatsApp</button>
    </div>
</section>

<footer style="text-align: center; padding: 40px; border-top: 1px solid rgba(255,255,255,0.05);">
    <p>© 2026 KDD STUDIO | Developed by Dinush Dilhara</p>
</footer>

<script>
    let cart = [];

    // --- MENU TOGGLE LOGIC ---
    function toggleMenu() {
        document.getElementById('navLinks').classList.toggle('active');
    }

    function showPage(id) {
        // Close menu on link click (Mobile)
        document.getElementById('navLinks').classList.remove('active');
        
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        window.scrollTo({top: 0, behavior: 'smooth'});
    }

    function addToCart(name, price) {
        cart.push({name, price});
        document.getElementById('cartCount').innerText = cart.length;
        renderCart();
        alert(name + " added!");
    }

    function renderCart() {
        let html = "", total = 0;
        cart.forEach(i => {
            total += i.price;
            html += `<p>✅ ${i.name} - Rs.${i.price.toLocaleString()}</p>`;
        });
        html += `<hr style='margin:10px 0; opacity:0.2'><b>Total: Rs.${total.toLocaleString()}</b>`;
        document.getElementById('cartItems').innerHTML = html;
    }

    function aiReply() {
        let input = document.getElementById('userInput');
        let box = document.getElementById('chatBox');
        if(input.value.trim() == "") return;
        
        box.innerHTML += `<p><b>You:</b> ${input.value}</p>`;
        setTimeout(() => {
            box.innerHTML += `<p style="color:var(--primary)"><b>DiNuX:</b> I am processing your request for KDD Studio services! How else can I assist?</p>`;
            box.scrollTop = box.scrollHeight;
        }, 800);
        input.value = "";
    }

    function sendWhatsApp() {
        if(cart.length == 0) { alert("Cart is empty!"); return; }
        let msg = `*New Order from KDD Studio*%0A`;
        cart.forEach(i => msg += `- ${i.name}%0A`);
        msg += `%0A*Details:*%0AName: ${document.getElementById('name').value}%0APhone: ${document.getElementById('phone').value}`;
        window.open(`https://wa.me/94779956510?text=${msg}`);
    }
</script>

</body>
</html>
