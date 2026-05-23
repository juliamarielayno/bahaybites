import streamlit as st

# ============================================================
# Title
# ============================================================

st.markdown(""" <style> @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato&display=swap');
    h1 {font-family: 'Playfair Display', serif; color: #ab6f2b;}p, div {font-family: 'Lato', sans-serif; }
    </style>
    <h1>Bahay Bites Master Form</h1>
    
""", unsafe_allow_html=True)

# ============================================================
# Prices revised as of May 22, 2026
# ============================================================
PRICES = {
    'bread_flour':      0.074,   # per oz
    'sugar':            0.049,   # per oz
    'yeast':            0.0137,  # per oz
    'instant_mash':     0.186,   # per oz
    'oil':              0.073,   # per fl oz
    'salt':             0.032,   # per oz
    'butter':           0.279,   # per oz
    'egg':              0.137,   # per egg 
    'milk':             0.022,   # per fl oz 
    'cornstarch':       0.026,   # per oz 
    'ube_jam':          0.90,    # per oz
    'ube_extract':      0.845,   # per oz
    'vanilla_extract':  3.00,    # per oz
    'confectioners':    0.062,   # per oz
    'baking_powder':    0.262,   # per oz
}

# ============================================================
# Cost of each item
# ============================================================

def pandesal_cost(scale):
    return (
        8   * 4.25  * PRICES['bread_flour']  +
        0.5 * 7.05  * PRICES['sugar']        +
        4   * 0.35  * PRICES['yeast']        +
        1   * 3.5   * PRICES['instant_mash'] +
        0.5 * 8.0   * PRICES['oil']          +
        2   * 0.2   * PRICES['salt']) * scale

def ensaymada_cost(scale):
    return (
        4   * 4.25  * PRICES['bread_flour']  +
        1   * 8.0   * PRICES['milk']         +
        2   * 1     * PRICES['egg']          +
        1   * 1     * PRICES['egg']          +  # egg yolk
        6   * 0.5   * PRICES['butter']       +
        0.5 * 0.2   * PRICES['salt']         +
        4   * 0.35  * PRICES['yeast']        +
        1   * 7.05  * PRICES['sugar']        +
        4   * 0.3   * PRICES['cornstarch']   +
        0.5 * 3.5   * PRICES['instant_mash'] ) * scale

def ube_cookie_cost(scale):
    return (
        1.75 * 4.25 * PRICES['bread_flour']    +
        1    * 0.167* PRICES['baking_powder']   +
        0.25 * 0.2  * PRICES['salt']            +
        1    * 7.0  * PRICES['sugar']           +
        0.5  * 8.0  * PRICES['butter']          +
        1    * 1    * PRICES['egg']             +
        0.5  * 9.5  * PRICES['ube_jam']         +
        2    * 0.17 * PRICES['ube_extract']     +
        0.5  * 0.17 * PRICES['vanilla_extract'] +
        1    * 4.0  * PRICES['confectioners']) * scale

# ============================================================
# Preorder Results
# ============================================================
st.markdown("## Preorders")

col1, col2, col3 = st.columns(3)
with col1:
    pandesal_orders = st.number_input("Pandesal", min_value=0, value=0, step=1)
with col2:
    ensaymada_orders = st.number_input("Ensaymada", min_value=0, value=0, step=1)
with col3:
    ube_orders = st.number_input("Ube Crinkles", min_value=0, value=0, step=1)

st.markdown("---")

# ============================================================
# Total Cost Calculation
# ============================================================
pandesal_base = 35
ensaymada_base = 25
ube_base = 18

pandesal_scale    = pandesal_orders / pandesal_base if pandesal_orders > 0 else 0
ensaymada_scale   = ensaymada_orders / ensaymada_base if ensaymada_orders > 0 else 0
ube_scale         = ube_orders / ube_base if ube_orders > 0 else 0

total_cost = pandesal_cost(pandesal_scale) + ensaymada_cost(ensaymada_scale) + ube_cookie_cost(ube_scale)

st.markdown("## Expected Cost to Make")
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Pandesal:** ${pandesal_cost(pandesal_scale):.2f}")
col2.markdown(f"**Ensaymada:** ${ensaymada_cost(ensaymada_scale):.2f}")
col3.markdown(f"**Ube Crinkles:** ${ube_cookie_cost(ube_scale):.2f}")
col4.markdown(f"**Total Cost Overral:** ${total_cost:.2f}")

st.markdown("---")

# ============================================================
# Recipe Cards
# ============================================================
st.markdown("## Recipe Cards")

if pandesal_orders > 0:
    s = pandesal_scale
    with st.expander("Pandesal", expanded=True):
        st.write(f"**Servings:** {pandesal_orders} rolls")
        st.markdown("**Ingredients:**")
        st.write(f"- {4*s:.1f} cups warm water")
        st.write(f"- {0.5*s:.2f} cups sugar")
        st.write(f"- {4*s:.1f} tbsp yeast")
        st.write(f"- {8*s:.1f} cups bread flour")
        st.write(f"- {1*s:.2f} cups instant mashed potatoes")
        st.write(f"- {0.5*s:.2f} cups oil")
        st.write(f"- {2*s:.1f} tsp salt")
        st.write(f"- {1*s:.2f} cups breadcrumbs")
        st.markdown("**Instructions:**")
        st.write("1. Wet ingredients: Mix warm water, sugar, and yeast in a bowl.")
        st.write("2. Dry ingredients: Mix bread flour, instant mash, oil, and salt.")
        st.write("3. Pour dry into wet and knead until fully combined (add water if too dry).")
        st.write("4. Roll into a log and cut into pieces 1.5 inches wide.")
        st.write("5. Coat each piece in breadcrumbs.")
        st.write("6. Proof in oven at 100°F for 20 minutes or until desired size.")
        st.write("7. Bake at 350°F for 15-20 minutes until golden.")
        st.success(f"Estimated Batch Cost: ${pandesal_cost(pandesal_scale):.2f}")
        st.info(f"Price per roll: ${pandesal_cost(pandesal_scale)/pandesal_orders:.2f}")

if ensaymada_orders > 0:
    s = ensaymada_scale
    with st.expander("Ensaymada", expanded=True):
        st.write(f"**Servings:** {ensaymada_orders} pieces")
        st.markdown("**Ingredients:**")
        st.write(f"- {1*s:.2f} cups milk")
        st.write(f"- {2*s:.1f} eggs")
        st.write(f"- {1*s:.1f} egg yolk(s)")
        st.write(f"- {6*s:.1f} tbsp butter")
        st.write(f"- {0.5*s:.2f} tsp salt")
        st.write(f"- {4*s:.1f} cups bread flour")
        st.write(f"- {4*s:.1f} tbsp cornstarch")
        st.write(f"- {0.5*s:.2f} cups instant mashed potatoes")
        st.write(f"- {6*s:.1f} tsp instant yeast")
        st.write(f"- {1*s:.2f} cups sugar")
        st.markdown("**Instructions:**")
        st.write("1. Combine yeast and warm milk. Let bubble for 10-15 minutes.")
        st.write("2. Add eggs, egg yolk, salt, sugar, and chopped butter.")
        st.write("3. Add bread flour and cornstarch (1 tbsp cornstarch per 1 cup flour).")
        st.write("4. Add instant mashed potatoes.")
        st.write("5. Set bread machine to setting 7 and run for 1.5 hours.")
        st.write("6. After 10 minutes check dough and scrape sides. Check again in 1 hour.")
        st.success(f"Estimated Batch Cost: ${ensaymada_cost(ensaymada_scale):.2f}")
        st.info(f"Per piece: ${ensaymada_cost(ensaymada_scale)/ensaymada_orders:.2f}")

if ube_orders > 0:
    s = ube_scale
    with st.expander("Ube Crinkle Cookies", expanded=True):
        st.write(f"**Servings:** {ube_orders} cookies")
        st.markdown("**Ingredients:**")
        st.write(f"- {1.75*s:.2f} cups all-purpose flour")
        st.write(f"- {1*s:.2f} tsp baking powder")
        st.write(f"- {0.25*s:.2f} tsp kosher salt")
        st.write(f"- {1*s:.2f} cups granulated sugar")
        st.write(f"- {0.5*s:.2f} cups unsalted butter")
        st.write(f"- {1*s:.1f} large egg(s)")
        st.write(f"- {0.5*s:.2f} cups ube halaya jam")
        st.write(f"- {2*s:.2f} tsp ube extract")
        st.write(f"- {0.5*s:.2f} tsp pure vanilla extract")
        st.write(f"- {1*s:.2f} cups confectioners sugar")
        st.markdown("**Instructions:**")
        st.write("1. Preheat oven to 350°F.")
        st.write("2. Whisk together flour, baking powder, and salt.")
        st.write("3. Beat sugar and butter until light and fluffy.")
        st.write("4. Add egg and beat until combined.")
        st.write("5. Add ube jam, ube extract, and vanilla. Beat until completely purple.")
        st.write("6. Gradually add dry ingredients and beat until just combined.")
        st.write("7. Chill overnight.")
        st.write("8. Roll into 3 tbsp balls and coat generously with confectioners sugar.")
        st.write("9. Bake for 12-15 minutes.")
        st.success(f"Estimated Batch Cost: ${ube_cookie_cost(ube_scale):.2f}")
        st.info(f"Per cookie: ${ube_cookie_cost(ube_scale)/ube_orders:.2f}")

if pandesal_orders == 0 and ensaymada_orders == 0 and ube_orders == 0:
    st.info("Enter your preorder quantities above to see your scaled recipes!")


