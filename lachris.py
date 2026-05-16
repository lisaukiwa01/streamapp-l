import streamlit as st
import stripe
import base64

# PAGE CONFIG
# This controls the browser tab settings for your website.
# page_title = text shown on the browser tab
# page_icon = small icon shown on browser tab
# layout = makes the page wider like a real website instead of narrow

st.set_page_config(
    page_title="LaChris",
    page_icon="logo2.png",
    layout="wide"
)

# STRIPE
# Stripe is what will eventually handle payments.
# The API key connects your app to your Stripe account.
# Right now you're using a TEST key, not real money.
# Replace later with environment variable
stripe.api_key = "sk_test_key_here"

# SESSION STATE
# Session state is basically the app's memory.
# Without this, the cart would reset every time you click something.
# Streamlit reruns the entire file every interaction,
# so session_state helps save information between reruns.
# This creates a variable called "page"
# and sets the default page to home.
if "page" not in st.session_state:
    st.session_state.page = "home"

# This creates the shopping cart.
# The cart is just a Python list.
if "cart" not in st.session_state:
    st.session_state.cart = []

# This stores whichever product the user clicks on.
# Later the product page uses this information.
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

# CSS / STYLING
st.markdown("""
<style>
@import url('https://fonts.cdnfonts.com/css/maharlika');

html, body, p, h1, h2, h3, h4, h5, h6, span, label, div {
    font-family: 'Maharlika', sans-serif;
}

.stApp {
    background-color: #fff4f8;
}


      

/* HERO SECTION */
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

header, footer {visibility: hidden;}


/* BUTTONS */
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

/* ANNOUNCEMENT BAR */
.announcement {
    background-color: black;
    color: white;
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-size: 15px;
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 40px;
    color: #666666;
}

/* IMAGE HOVER */
a img:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)


# IMAGE TO BASE64
# HTML cannot directly display local Streamlit images inside custom links.
# So this function converts images into a long text string (base64).
# That lets us make clickable images like a real ecommerce website.


def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# PRODUCTS

# This is your product database for now.
# Later you can replace this with a real database like Firebase or Supabase.
# Each product is stored as a dictionary.

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


# QUERY PARAMS FOR CLICKABLE IMAGES

query_params = st.query_params

if "product" in query_params:
    index = int(query_params["product"])

    selected = all_products[index]

    st.session_state.selected_product = selected
    st.session_state.page = "product"

    st.query_params.clear()
    st.rerun()


# TOP BAR

left, right = st.columns([8, 1])

with left:
    logo_col, title_col = st.columns([1, 5])

    with logo_col:
        st.image("logo2.png", width=80)

    with title_col:
        st.markdown("<a href='home' target='_self' style='text-decoration:none; color:black;'>" "<h1>LaChris</h1>", unsafe_allow_html=True)
        st.caption("Beauty • Hair • Nails • Jewelry")
with right:
    if st.button(f"🛒 {len(st.session_state.cart)}", key="cart_button"):
        st.session_state.page = "cart"
        st.rerun()


# CART PAGE

# If the user clicks the cart button,
# the website switches to the cart page.
# st.stop() later prevents the homepage from rendering underneath it.

if st.session_state.page == "cart":

    st.title("Your Cart 🛒")

    total = 0

    if len(st.session_state.cart) == 0:
        st.write("Your cart is empty 🛒")

    else:
        # gets information for each item in the cart and displays it in a row with 3 columns:
        for index, item in enumerate(st.session_state.cart):

            col1, col2, col3 = st.columns([6, 2, 1])

            with col1:
                st.write(item["name"])

            with col2:
                st.write(f"${item['price']}")

            with col3:
                if st.button("❌", key=f"remove_{index}"):
                    st.session_state.cart.pop(index)
                    st.rerun()

            total += item["price"]

        st.divider()
        st.subheader(f"Subtotal: ${total}")

        if st.button("Proceed to Checkout"):
            st.success("Stripe checkout coming soon 💳")

    if st.button("Clear Cart"):
        st.session_state.cart = []
        st.rerun()

    if st.button("← Continue Shopping"):
        st.session_state.page = "home"
        st.rerun()

    st.stop()


# PRODUCT PAGE

# This is the full product page.
# When someone clicks a product image,
# the selected product gets saved in session_state.
# Then the app switches to this page.

if st.session_state.page == "product":

    product = st.session_state.selected_product

    gallery = product.get("gallery", [product["image"]])
    img_param = st.query_params.get("img_idx", 0)
    
    # Ensure the index is valid
    try:
        current_img_idx = int(img_param)
    except:
        current_img_idx = 0
    
    main_image_path = gallery[current_img_idx]

    if product is None:
        st.session_state.page = "home"
        st.rerun()

    if "main_view_img" not in st.session_state:
        st.session_state.main_view_img = product["image"]

    col1, col2 = st.columns([1,1])

    with col1:
        st.image(product["image"], use_container_width=True)
    with col2:
        st.title(product["name"])
        st.subheader(f"${product['price']}")

        st.write(product["description"])

        st.divider()

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
            min_value=1,
            max_value=10,
            value=1
        )

        if st.button("Add To Cart", key="product_add"):

            for _ in range(quantity):
                st.session_state.cart.append({
                    "name": f"{product['name']} ({option})",
                    "price": product["price"]
                })

            st.success("Added to cart 🛍️")
            st.rerun()

        st.divider()

        st.markdown("### Why You'll Love It ✨")
        st.write("✔ Premium quality")
        st.write("✔ Beginner friendly")
        st.write("✔ Long-lasting wear")
        st.write("✔ Luxury packaging")
    st.stop()

# HOME PAGE
# This is the main storefront

# Announcement bar
st.markdown(
    """
    <div class='announcement'>
        FREE SHIPPING ON ORDERS OVER $250 ✨
    </div>
    """,
    unsafe_allow_html=True
)

# Hero section
st.markdown(
    """
    <div class='hero' style='text-align: center;'>
        <h1>Elevate Your Look</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Navigation
page = st.radio(
    "",
    ["Home", "Shop All", "Hair", "Nails", "Jewelry"],
    horizontal=True
)

st.divider()

# Filter products
if page == "Home" or page == "Shop All":
    products = all_products
else:
    #Only keep products that match category
    products = [p for p in all_products if p["category"] == page]

# PRODUCT GRID
cols = st.columns(3)

for i, product in enumerate(products):

    with cols[i % 3]:

        st.markdown("<div class='product-card'>", unsafe_allow_html=True)

        #turn img into a string so we can put it inside a custom link
        img_base64 = get_image_base64(product["image"])

        st.markdown(f"""
        <a href='?product={i}' target='_self'>
            <img src='data:image/png;base64,{img_base64}'
                 style='width:100%; border-radius:18px;' />
        </a>
        """, unsafe_allow_html=True)

        st.markdown(f"### {product['name']}")
        st.write(f"${product['price']}")
        st.caption(product["description"])

        #every product card has its own unique button key so they don't interfere with each other
        if st.button("Add To Cart", key=f"cart_{i}"#{i} makes the key unique for each product
):
            st.session_state.cart.append({
                "name": product["name"],
                "price": product["price"]
            })
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# REVIEWS SECTION
st.divider()

st.markdown("## Customer Favorites 💕")

review1, review2, review3 = st.columns(3)

with review1:
    st.markdown("⭐ ⭐ ⭐ ⭐ ⭐")
    st.write("'The hair quality is AMAZING.'")

with review2:
    st.markdown("⭐ ⭐ ⭐ ⭐ ⭐")
    st.write("'Cute packaging and fast shipping.'")

with review3:
    st.markdown("⭐ ⭐ ⭐ ⭐ ⭐")
    st.write("'The nails lasted me 3 weeks!'")

# FOOTER
st.markdown(
    """
    <div class='footer'>
        © 2026 LaChris Beauty — All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)
