import streamlit as st

# ============================================================
# Title
# ============================================================

st.markdown("# Bahay Bites Master Form")

# ============================================================
# Prices revised as of May 22, 2026
# ============================================================
ingredient_prices = {
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
        8   * 4.25  * ingredient_prices['bread_flour']  +
        0.5 * 7.05  * ingredient_prices['sugar']        +
        4   * 0.35  * ingredient_prices['yeast']        +
        1   * 3.5   * ingredient_prices['instant_mash'] +
        0.5 * 8.0   * ingredient_prices['oil']          +
        2   * 0.2   * ingredient_prices['salt']) * scale * 1.075

def ensaymada_cost(scale):
    return (
        4   * 4.25  * ingredient_prices['bread_flour']  +
        1   * 8.0   * ingredient_prices['milk']         +
        2   * 1     * ingredient_prices['egg']          +
        1   * 1     * ingredient_prices['egg']          +  # egg yolk
        6   * 0.5   * ingredient_prices['butter']       +
        0.5 * 0.2   * ingredient_prices['salt']         +
        4   * 0.35  * ingredient_prices['yeast']        +
        1   * 7.05  * ingredient_prices['sugar']        +
        4   * 0.3   * ingredient_prices['cornstarch']   +
        0.5 * 3.5   * ingredient_prices['instant_mash'] ) * scale * 1.075

def ube_crinkle_cost(scale):
    return (
        1.75 * 4.25 * ingredient_prices['bread_flour']    +
        1    * 0.167* ingredient_prices['baking_powder']   +
        0.25 * 0.2  * ingredient_prices['salt']            +
        1    * 7.0  * ingredient_prices['sugar']           +
        0.5  * 8.0  * ingredient_prices['butter']          +
        1    * 1    * ingredient_prices['egg']             +
        0.5  * 9.5  * ingredient_prices['ube_jam']         +
        2    * 0.17 * ingredient_prices['ube_extract']     +
        0.5  * 0.17 * ingredient_prices['vanilla_extract'] +
        1    * 4.0  * ingredient_prices['confectioners']) * scale * 1.075

# ============================================================
# Preorder Results
# ============================================================
st.markdown("## Preorders")

col1, col2,col3, col4, col5, col6 = st.columns(6)
with col1:
    pandesal_halfdozen = st.number_input(("**Pandesal** (Half Dozen)"), min_value=0, value=0, step=1)
with col2:
    pandesal_dozen = st.number_input(("**Pandesal** (Dozen)"), min_value=0, value=0, step=1)
with col3:
    ensaymada_four = st.number_input(("**Ensaymada** (Four)"), min_value=0, value=0, step=1)
with col4:
    ensaymada_halfdozen = st.number_input(("**Ensaymada** (Half Dozen)"), min_value=0, value=0, step=1)
with col5:
    spanish_bread_four = st.number_input(("**Spanish Bread** (Four)"), min_value=0, value=0, step=1)
with col6:
    spanish_bread_halfdozen = st.number_input(("**Spanish Bread** (Half Dozen)"), min_value=0, value=0, step=1)
    

# ============================================================
# Total Cost Calculation
# ============================================================
pandesal_base = 35
ensaymada_base = 30
ube_base = 18

total_pandesal_order = (pandesal_halfdozen * 6) +  (pandesal_dozen * 12)
total_ensaymada_order = (ensaymada_four * 4) + (ensaymada_halfdozen * 6)
total_ube_crinkle_order = (spanish_bread_four * 4) + (spanish_bread_halfdozen * 6)

pandesal_scale = total_pandesal_order / pandesal_base if total_pandesal_order > 0 else 0
ensaymada_scale = total_ensaymada_order / ensaymada_base if total_ensaymada_order > 0 else 0
ube_crinkle_scale = total_ube_crinkle_order / ube_base if total_ube_crinkle_order > 0 else 0

total_cost = pandesal_cost(pandesal_scale) + ensaymada_cost(ensaymada_scale) + ube_crinkle_cost(ube_crinkle_scale)

pandesal_unitcost = pandesal_cost(pandesal_scale)/total_pandesal_order if total_pandesal_order > 0 else 0
ensaymada_unitcost = ensaymada_cost(ensaymada_scale)/total_ensaymada_order if total_ensaymada_order > 0 else 0
ube_crinkle_unitcost = ube_crinkle_cost(ube_crinkle_scale)/total_ube_crinkle_order if total_ube_crinkle_order > 0 else 0

st.markdown("## Finances")
st.markdown("### Expect Cost to Make")
col1, col2, col3, col4, col5 = st.columns(5)
col1.markdown(f"**Pandesal:** ${pandesal_cost(pandesal_scale):.2f}")
col2.markdown(f"**Ensaymada:** ${ensaymada_cost(ensaymada_scale):.2f}")
col3.markdown(f"**Ube Crinkles:** ${ube_crinkle_cost(ube_crinkle_scale):.2f}")
col4.markdown(f"**Miscellaneous Expenses (gas, packaging, utlities):** ${total_cost *0.50 :.2f}")
col5.markdown(f"**Total Cost Overral:** ${total_cost * 1.50:.2f}")                                        

st.markdown("### Expected Profit")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
col1.markdown(f"**Pandesal Half Dozen:** ${(pandesal_halfdozen * 6) - (pandesal_unitcost * 6):.2f}")
col2.markdown(f"**Pandesal Dozen:** ${pandesal_dozen * 12 - (pandesal_unitcost * 12):.2f}")
col3.markdown(f"**Ensaymada (4):** ${ensaymada_four * 4 - (ensaymada_unitcost * 6):.2f}")
col4.markdown(f"**Ensaymada Half Dozen:** ${ensaymada_halfdozen * 6 - (ensaymada_unitcost * 6):.2f}")
col5.markdown(f"**Spanish Bread (4):** ${spanish_bread_four * 4 - (pandesal_unitcost * 4):.2f}")
col6.markdown(f"**Spanish Bread Half Dozen:** ${spanish_bread_halfdozen * 6 - (pandesal_unitcost * 6):.2f}")
col7.markdown(f"**Total Expected Profit:** ${
    ((pandesal_halfdozen * 6) - (pandesal_unitcost * 6) +
    (pandesal_dozen * 12 - (pandesal_unitcost * 12)) +
    (ensaymada_four * 4 - (ensaymada_unitcost * 6)) +
    (ensaymada_halfdozen * 6 - (ensaymada_unitcost * 6)) +
    (spanish_bread_four * 4 - (pandesal_unitcost * 4)) +
    (spanish_bread_halfdozen * 6 - (pandesal_unitcost * 6))):.2f}"
             )
st.markdown("---")

# ============================================================
# Shopping List
# ============================================================

st.markdown("## Grocery List")

if total_pandesal_order > 0 or total_ensaymada_order > 0 or total_ube_crinkle_order > 0:
    
    shopping = {
        'cups bread flour':         0,
        'cups sugar':               0,
        'tsp yeast':                0,
        'cups instant mash':        0,
        'tbsp butter':              0,
        'tsp salt':                 0,
        'eggs':                     0,
        'cups water':               0,
        'cups oil':                 0,
        'cups breadcrumbs':         0,
        'cups milk':                0,
        'tbsp cornstarch':          0,
        'cups ube halaya jam':      0,
        'tsp ube extract':          0,
        'tsp vanilla extract':      0,
        'cups confectioners sugar': 0,
        'tsp baking powder':        0, }

    if total_pandesal_order > 0:
        shopping['cups bread flour']  += 8   * pandesal_scale
        shopping['cups sugar']        += 0.5 * pandesal_scale
        shopping['tsp yeast']         += 4   * pandesal_scale
        shopping['cups instant mash'] += 1   * pandesal_scale
        shopping['tsp salt']          += 2   * pandesal_scale
        shopping['cups water']        += 3   * pandesal_scale
        shopping['cups oil']          += 0.5 * pandesal_scale
        shopping['cups breadcrumbs']  += 1   * pandesal_scale

    if total_ensaymada_order > 0:
        shopping['cups bread flour']  += 4   * ensaymada_scale
        shopping['cups sugar']        += 1   * ensaymada_scale
        shopping['tsp yeast']         += 6   * ensaymada_scale
        shopping['cups instant mash'] += 0.5 * ensaymada_scale
        shopping['tbsp butter']       += 6   * ensaymada_scale
        shopping['tsp salt']          += 0.5 * ensaymada_scale
        shopping['eggs']              += 3   * ensaymada_scale
        shopping['cups milk']         += 1   * ensaymada_scale
        shopping['tbsp cornstarch']   += 4   * ensaymada_scale

    if total_ube_crinkle_order > 0:
        shopping['cups bread flour']         += 1.75 * ube_crinkle_scale
        shopping['cups sugar']               += 1    * ube_crinkle_scale
        shopping['tbsp butter']              += 0.5  * ube_crinkle_scale
        shopping['tsp salt']                 += 0.25 * ube_crinkle_scale
        shopping['eggs']                     += 1    * ube_crinkle_scale
        shopping['cups ube halaya jam']      += 0.5  * ube_crinkle_scale
        shopping['tsp ube extract']          += 2    * ube_crinkle_scale
        shopping['tsp vanilla extract']      += 0.5  * ube_crinkle_scale
        shopping['cups confectioners sugar'] += 1    * ube_crinkle_scale
        shopping['tsp baking powder']        += 1    * ube_crinkle_scale

    for ingredient, amount in shopping.items():
        if amount > 0:
            st.write(f"- {amount:.2f} {ingredient}")

else:
    st.info("Enter your preorders above to generate a grocery list!")

# ============================================================
# Recipe Cards
# ============================================================
st.markdown("## Recipe Cards")

if total_pandesal_order > 0:
    s = pandesal_scale
    with st.expander("Pandesal", expanded=True):
        st.write(f"**Servings:** {total_pandesal_order} rolls")
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
        st.info(f"Estimated Price per roll: ${pandesal_cost(pandesal_scale)/total_pandesal_order:.2f}")

if total_ensaymada_order > 0:
    s = ensaymada_scale
    with st.expander("Ensaymada", expanded=True):
        st.write(f"**Servings:** {total_ensaymada_order} pieces")
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
        st.info(f"Estimated Per piece: ${ensaymada_cost(ensaymada_scale)/total_ensaymada_order:.2f}")

if total_ube_crinkle_order > 0:
    s = ube_crinkle_scale
    with st.expander("Ube Crinkle Cookies", expanded=True):
        st.write(f"**Servings:** {total_ube_crinkle_order} cookies")
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
        st.success(f"Estimated Batch Cost: ${ube_crinkle_cost(ube_crinkle_scale):.2f}")
        st.info(f"Estimated Per cookie: ${ube_crinkle_cost(ube_crinkle_scale)/total_ube_crinkle_order:.2f}")

if total_pandesal_order == 0 and total_ensaymada_order == 0 and total_ube_crinkle_order == 0:
    st.info("Enter your preorder quantities above to see your scaled recipes!")
