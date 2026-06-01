import streamlit as st
import stripe
import base64
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = "https://upcswibeskkrhqxksyuq.supabase.co"
supabase_key = "sb_secret_c_aEVNo85Bc1ZHoshuCLbg_DID7rV4a"

supabase: Client = create_client(supabase_url, supabase_key)

stripe.api_key = "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"
stripe_publishable_key = "pk_live_51TPD366ZpkfcZ03whypcb9l09000PRZnqkGK2efYuPTISMLTXbBpM6GHtBaKWQ2FbWfo3dgLtqLAsSOapAuNS5T800pjakfCEz"

params = st.query_params


if params.get("cancel") == "true":

    st.warning("Payment cancelled.")

st.set_page_config(
    page_title="LaChris",
    page_icon="logo2.png",
    layout="wide"
)


if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "user" not in st.session_state:
    st.session_state.user = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "loaded_cart" not in st.session_state:
    st.session_state.loaded_cart = False

if "session_restored" not in st.session_state:
    st.session_state.session_restored = False


st.markdown("""
<style>
@import url('https://fonts.cdnfonts.com/css/maharlika');

html, body, p, h1, h2, h3, h4, h5, h6, span, label, div {
    font-family: 'Maharlika', sans-serif;
}

header, footer {visibility: hidden;}

.stApp {
    background-color: #fff4f8;
}

.hero {
    background: linear-gradient(to right, #ffd6e7, #fff0f6);
    border-radius: 24px;
    padding: 60px;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 64px;
    margin-bottom: 10px;
    color: #111111;
}

.hero p {
    font-size: 22px;
    color: #555555;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    background-color: #ff69b4;
    color: white;
    border: none;
    padding: 12px;
    font-size: 16px;
}

.stButton > button:hover {
    background-color: #ffb6d9;
    color: black;
}

.announcement {
    background-color: black;
    color: white;
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-size: 15px;
}

.footer {
    text-align: center;
    padding: 40px;
    color: #666666;
}

a img:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)


def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


all_products = [
    {
        "name": "Body Wave Human Hair Bundles - 4 Bundles",
        "price": 120,
        "image": "assets/bundles(02).png",
        "description": "Soft premium quality hair with natural shine and volume.",
        "category": "Hair",
        "tags": ["black", "bundles", "body wave", "human hair", "volume"]
    },
    {
        "name": "Test!",
        "price": 0.50,
        "image": "assets/bundles(02).png",
        "description": "Soft premium quality hair with natural shine and volume.",
        "category": "Hair",
        "tags": ["black", "bundles", "body wave", "human hair", "volume"]
    },
    {
        "name": "Press-On Nails",
        "price": 25,
        "image": "assets/Coming Soon.png",
        "description": "Glossy salon-quality press-ons. Summer themed, tropical nails",
        "category": "Nails",
        "tags": ["nails", "press-on", "summer", "tropical", "glossy"]
    },
    {
        "name": "Emmy Gold Necklace",
        "price": 40,
        "image": "assets/Coming Soon.png",
        "description": "Elegant jewelry piece for everyday wear.",
        "category": "Jewelry",
        "tags": ["jewelry", "necklace", "gold"]
    },
    {
        "name": "Body Wave Human Hair Bundles",
        "price": 120,
        "image": "assets/Coming Soon.png",
        "description": "Soft premium quality hair with natural shine and volume.",
        "category": "Hair",
        "tags": ["hair", "bundles", "body wave", "synthetic", "volume"]
    },
    {
        "name": "Press-On Nails",
        "price": 25,
        "image": "assets/Coming Soon.png",
        "description": "Glossy salon-quality press-ons.",
        "category": "Nails",
        "tags": ["nails", "press-on", "summer", "tropical", "glossy"]
    },
    {
        "name": "Emmy Silver Necklace",
        "price": 40,
        "image": "assets/Coming Soon.png",
        "description": "Elegant jewelry piece for everyday wear.",
        "category": "Jewelry",
        "tags": ["jewelry", "necklace", "silver"]
    }
]

def save_cart():
    if not st.session_state.user:
        return

    supabase.table("carts").upsert(
        {
            "user_id": st.session_state.user.id,
            "cart": st.session_state.cart
        },
        on_conflict="user_id"
    ).execute()


def load_cart():
    if not st.session_state.user:
        return

    response = supabase.table("carts").select("*").eq(
        "user_id",
        st.session_state.user.id
    ).execute()

    if response.data and len(response.data) > 0:
        st.session_state.cart = response.data[0]["cart"] or []
    else:
        st.session_state.cart = []


def save_order():

    if not st.session_state.user:
        return

    total = sum(item["price"] for item in st.session_state.cart)

    supabase.table("orders").insert({
        "user_id": st.session_state.user.id,
        "items": st.session_state.cart,
        "total": total
    }).execute()

if params.get("success") == "true":

    if len(st.session_state.cart) > 0:
        save_order()

    st.success("Payment successful! 🎉")

    st.session_state.cart = []

    save_cart()

if not st.session_state.session_restored:

    try:
        session_response = supabase.auth.get_session()

        if session_response:
            current_session = session_response.session

            if current_session:
                st.session_state.user = current_session.user
                st.session_state.access_token = current_session.access_token

    except:
        pass

    st.session_state.session_restored = True


if st.session_state.user and not st.session_state.loaded_cart:
    load_cart()
    st.session_state.loaded_cart = True


query_params = st.query_params

if "product" in query_params:
    index = int(query_params["product"])

    selected = all_products[index]

    st.session_state.selected_product = selected
    st.session_state.page = "product"

    st.query_params.clear()
    st.rerun()

if "login" in query_params:
    st.session_state.page = "login"

    st.query_params.clear()
    st.rerun()


left, right = st.columns([8, 1])

with left:
    logo_col, title_col, login_col, orders_col = st.columns([1, 5, .7, .7])

    with logo_col:
        st.image("logo2.png", width=80)

    with title_col:
        st.markdown(
            "<a href='home' target='_self' style='text-decoration:none; color:black;'>"
            "<h1 style='font-size:48px; margin:0;'>LaChris</h1>"
            "</a>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<p style='font-size:16px; margin:1; color:#444;'>Beauty • Hair • Nails • Jewelry</p>",
            unsafe_allow_html=True,
        )

    with login_col:

        if st.session_state.user:

            if st.button("Logout"):

                supabase.auth.sign_out()

                st.session_state.user = None
                st.session_state.access_token = None
                st.session_state.cart = []
                st.session_state.loaded_cart = False
                st.session_state.session_restored = False
                st.session_state.page = "home"

                st.rerun()

        else:

            if st.button("➜]", key="login_button"):
                st.session_state.page = "login"
with orders_col:
    if st.button("📦", key="orders_button"):
        st.session_state.page = "orders"
        st.rerun()
with right:

    if st.button(f"🛒 {len(st.session_state.cart)}", key="cart_button"):
        st.session_state.page = "cart"
        st.rerun()

def load_orders():

    if not st.session_state.user:
        return []

    response = supabase.table("orders").select("*").eq(
        "user_id",
        st.session_state.user.id
    ).order(
        "created_at",
        desc=True
    ).execute()

    return response.data

if st.session_state.page == "orders":

    st.title("📦 Order History")

    orders = load_orders()

    if not orders:
        st.info("No orders yet.")
    else:

        for order in orders:

            st.subheader(
                f"Order #{order['id']}"
            )

            st.write(
                f"Placed: {order['created_at']}"
            )

            st.write(
                f"Total: ${order['total']}"
            )

            for item in order["items"]:
                st.write(
                    f"• {item['name']} - ${item['price']}"
                )

            st.divider()

    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()

    st.stop()

def signup(email, password):
    try:
        return supabase.auth.sign_up({
            "email": email,
            "password": password
        })
    except:
        return None


def login(email, password):
    try:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    except:
        return None


def auth_screen():

    choice = st.radio(
        "Welcome!",
        ["Signup", "Login"],
        horizontal=True
    )

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if choice == "Signup" and st.button("Signup"):

        signup(email, password)

        st.success(
            "Sign up successful. Check your email for authentication link."
        )

    if choice == "Login" and st.button("Login"):

        user = login(email, password)

        if user and user.user:

            st.session_state.user = user.user

            st.session_state.access_token = (
                user.session.access_token
            )

            load_cart()

            st.session_state.loaded_cart = True

            st.session_state.page = "home"

            st.rerun()


if st.session_state.page == "login":

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown(
            "<h1 style='font-size:40px; margin-left:8rem;'>Welcome Back! 💝</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='font-size:20px; text-align:center;'>Login or Signup</p>",
            unsafe_allow_html=True
        )

        auth_screen()

    st.stop()

def create_checkout_session(cart_items):

    line_items = []

    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item["name"]
                },
                "unit_amount": int(item["price"] * 100)
            },
            "quantity": 1
        })

    session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    line_items=line_items,
    mode="payment",

    shipping_address_collection={
        "allowed_countries": ["US"]
    },
        success_url="https://lachriss.streamlit.app/?success=true",
        cancel_url="https://lachriss.streamlit.app/?cancel=true"
    )

    return session.url

if st.session_state.page == "cart":

    st.title("Your Cart 🛒")

    total = 0

    if len(st.session_state.cart) == 0:

        st.write("Your cart is empty 🛒")

    else:

        for index, item in enumerate(st.session_state.cart):

            col1, col2, col3 = st.columns([6, 2, 1])

            with col1:
                st.write(item["name"])

            with col2:
                st.write(f"${item['price']}")

            with col3:

                if st.button("❌", key=f"remove_{index}"):

                    st.session_state.cart.pop(index)

                    save_cart()

                    st.rerun()

            total += item["price"]

        st.divider()

        st.subheader(f"Subtotal: ${total}")

    if st.button("Clear Cart"):

        st.session_state.cart = []

        save_cart()

        st.rerun()
    if st.button("Proceed to Checkout"):
        st.session_state.page = "checkout"
        st.rerun()
    if st.button("← Continue Shopping"):

        st.session_state.page = "home"

        st.rerun()

    st.stop()

if st.session_state.page == "checkout":
    st.subheader("Order Summary")

    for item in st.session_state.cart:
        st.write(f"• {item['name']} - ${item['price']}")

    st.divider()

    if st.button("Pay Now 💖"):

        checkout_url = create_checkout_session(
            st.session_state.cart
        )

        st.link_button(
            "Continue to Secure Payment",
            checkout_url
        )
    if st.button("← Back to Cart"):
        st.session_state.page = "cart"
        st.rerun()

    st.stop()

if st.session_state.page == "product":

    product = st.session_state.selected_product

    if product is None:
        st.session_state.page = "home"
        st.rerun()

    option = ""

    if product["category"] == "Hair":

        option = st.selectbox(
            "Select Length",
            ["12 inch", "16 inch", "20 inch", "24 inch"]
        )

    if product["category"] == "Nails":

        option = st.selectbox(
            "Select Size",
            ["Small", "Medium", "Large"]
        )

    quantity = st.number_input(
        "Quantity",
        1,
        10,
        1
    )

    if st.button("Add To Cart"):

        for _ in range(quantity):

            name = product["name"]

            if option:
                name = f"{product['name']} ({option})"

            st.session_state.cart.append({
                "name": name,
                "price": product["price"]
            })

        save_cart()

        st.rerun()

    st.stop()


st.markdown("""
<div class='announcement'>
FREE SHIPPING ON ORDERS OVER $250 ✨
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero' style='text-align:center;'>
<h1>Elevate Your Look</h1>
</div>
""", unsafe_allow_html=True)

page = st.radio(
    "",
    ["Home", "Shop All", "Hair", "Nails", "Jewelry"],
    horizontal=True
)

if page == "Home" or page == "Shop All":
    products = all_products
else:
    products = [
        p for p in all_products
        if p["category"] == page
    ]

cols = st.columns(3)

for i, product in enumerate(products):

    with cols[i % 3]:

        img_base64 = get_image_base64(product["image"])

        st.markdown(f"""
        <a href='?product={i}' target='_self'>
            <img src='data:image/png;base64,{img_base64}'
                 style='width:100%;border-radius:18px;'/>
        </a>
        """, unsafe_allow_html=True)

        st.write(product["name"])

        st.write(f"${product['price']}")

        if st.button("Add To Cart", key=f"cart_{i}"):

            st.session_state.cart.append({
                "name": product["name"],
                "price": product["price"]
            })

            save_cart()

            st.rerun()

st.stop()
