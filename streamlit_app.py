import streamlit as st
from datetime import date, timedelta
from db import init_db, get_connection, get_pack_sizes, record_order

# ============================================================
# Setup — runs every time the app starts, but only creates
# tables/seeds data the FIRST time (safe to leave in)
# ============================================================
init_db()

st.markdown("# Bahay Bites Master Form")

# ============================================================
# Pull current ingredient prices from the database instead of
# a hardcoded dict. Now updating a price = editing a database
# row, not editing this file.
# ============================================================
def get_ingredient_prices():
    conn = get_connection()
    rows = conn.execute("""
        SELECT ingredient_name, unit_cost FROM ingredient_prices
        GROUP BY ingredient_name
        HAVING effective_date = MAX(effective_date)
    """).fetchall()
    conn.close()
    return {row["ingredient_name"]: row["unit_cost"] for row in rows}

ingredient_prices = get_ingredient_prices()

# ============================================================
# Cost of each item (same formulas as before — these are still
# Python functions, just reading prices from the DB now)
# ============================================================

def pandesal_cost(scale):
    return (
        8   * 4.25  * ingredient_prices['bread_flour']  +
        0.5 * 8.0   * ingredient_prices['bread_flour']  +
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

def spanish_bread_cost(scale):
    # NOTE: placeholder formula — your original code never actually had
    # a real Spanish Bread recipe, it was accidentally using ube_crinkle's.
    # Fill this in with your real Spanish Bread ingredient amounts.
    return (
        3   * 4.25  * ingredient_prices['bread_flour']  +
        0.5 * 7.05  * ingredient_prices['sugar']        +
        3   * 0.35  * ingredient_prices['yeast']        +
        4   * 0.5   * ingredient_prices['butter']       +
        1   * 0.2   * ingredient_prices['salt']         +
        0.5 * 8.0   * ingredient_prices['milk']) * scale * 1.075

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

COST_FUNCTIONS = {
    "Pandesal": pandesal_cost,
    "Ensaymada": ensaymada_cost,
    "Spanish Bread": spanish_bread_cost,
    "Ube Crinkle Cookies": ube_crinkle_cost,
}
BASE_BATCH = {"Pandesal": 48, "Ensaymada": 30, "Spanish Bread": 30, "Ube Crinkle Cookies": 18}

# ============================================================
# Preorders — pack sizes now pulled from the database instead
# of being separate hardcoded st.number_input calls per size
# ============================================================
st.markdown("## Preorders")

pack_sizes = get_pack_sizes()  # list of rows: item_name, label, units_per_pack, price, pack_size_id
quantities = {}  # pack_size_id -> quantity entered

cols = st.columns(len(pack_sizes))
for col, pack in zip(cols, pack_sizes):
    with col:
        quantities[pack["pack_size_id"]] = st.number_input(
            f"**{pack['item_name']}** ({pack['label']})",
            min_value=0, value=0, step=1,
            key=f"qty_{pack['pack_size_id']}"
        )

# ============================================================
# Totals per item, cost, profit — same math as before, just
# driven by the pack_sizes/quantities from the DB now
# ============================================================
item_totals = {}       # item_name -> total units ordered
item_scale = {}        # item_name -> scale factor for cost functions
item_revenue = {}      # item_name -> revenue from this order

for pack in pack_sizes:
    qty = quantities[pack["pack_size_id"]]
    if qty == 0:
        continue
    name = pack["item_name"]
    units = qty * pack["units_per_pack"]
    item_totals[name] = item_totals.get(name, 0) + units
    item_revenue[name] = item_revenue.get(name, 0) + qty * pack["price"]

for name, total_units in item_totals.items():
    if name in BASE_BATCH:
        item_scale[name] = total_units / BASE_BATCH[name]

total_cost = sum(COST_FUNCTIONS[name](scale) for name, scale in item_scale.items())

st.markdown("## Finances")
st.markdown("### Expected Cost to Make")
cost_cols = st.columns(len(item_scale) + 2 if item_scale else 1)
for col, (name, scale) in zip(cost_cols, item_scale.items()):
    col.markdown(f"**{name}:** ${COST_FUNCTIONS[name](scale):.2f}")
if item_scale:
    cost_cols[-2].markdown(f"**Misc (gas, packaging, utilities):** ${total_cost * 0.50:.2f}")
    cost_cols[-1].markdown(f"**Total Cost Overall:** ${total_cost * 1.50:.2f}")

st.markdown("### Expected Profit")
total_revenue = sum(item_revenue.values())
total_profit = total_revenue - total_cost
st.markdown(f"**Total Expected Profit:** ${total_profit:.2f}")
st.markdown("---")

# ============================================================
# Save this week's order to the database
# ============================================================
st.markdown("## Save This Order")
col1, col2 = st.columns(2)
with col1:
    week_start = st.date_input("Week Start (Monday orders opened)", value=date.today())
with col2:
    pickup_date = st.date_input("Pickup Date (Sunday)", value=date.today() + timedelta(days=(6 - date.today().weekday())))

if st.button("💾 Save Order to Database"):
    line_items = [
        {"pack_size_id": pack["pack_size_id"], "quantity": quantities[pack["pack_size_id"]]}
        for pack in pack_sizes if quantities[pack["pack_size_id"]] > 0
    ]
    if line_items:
        order_id = record_order(str(week_start), str(pickup_date), line_items)
        st.success(f"Saved order #{order_id} with {len(line_items)} line item(s)!")
    else:
        st.warning("Enter at least one item before saving.")

st.markdown("---")

# ============================================================
# Grocery List (same logic, driven by item_scale from the DB path)
# ============================================================
st.markdown("## Grocery List")

if item_scale:
    shopping = {
        'cups bread flour': 0, 'cups sugar': 0, 'tsp yeast': 0, 'cups instant mash': 0,
        'tbsp butter': 0, 'tsp salt': 0, 'eggs': 0, 'cups water': 0, 'cups oil': 0,
        'cups breadcrumbs': 0, 'cups milk': 0, 'tbsp cornstarch': 0,
        'cups ube halaya jam': 0, 'tsp ube extract': 0, 'tsp vanilla extract': 0,
        'cups confectioners sugar': 0, 'tsp baking powder': 0,
    }

    if "Pandesal" in item_scale:
        s = item_scale["Pandesal"]
        shopping['cups bread flour']  += 8   * s
        shopping['cups sugar']        += 0.5 * s
        shopping['tsp yeast']         += 4   * s
        shopping['cups instant mash'] += 1   * s
        shopping['tsp salt']          += 2   * s
        shopping['cups water']        += 3   * s
        shopping['cups oil']          += 0.5 * s
        shopping['cups breadcrumbs']  += 1   * s

    if "Ensaymada" in item_scale:
        s = item_scale["Ensaymada"]
        shopping['cups bread flour']  += 4   * s
        shopping['cups sugar']        += 1   * s
        shopping['tsp yeast']         += 6   * s
        shopping['cups instant mash'] += 0.5 * s
        shopping['tbsp butter']       += 6   * s
        shopping['tsp salt']          += 0.5 * s
        shopping['eggs']              += 3   * s
        shopping['cups milk']         += 1   * s
        shopping['tbsp cornstarch']   += 4   * s

    if "Ube Crinkle Cookies" in item_scale:
        s = item_scale["Ube Crinkle Cookies"]
        shopping['cups bread flour']         += 1.75 * s
        shopping['cups sugar']               += 1    * s
        shopping['tbsp butter']              += 0.5  * s
        shopping['tsp salt']                 += 0.25 * s
        shopping['eggs']                     += 1    * s
        shopping['cups ube halaya jam']      += 0.5  * s
        shopping['tsp ube extract']          += 2    * s
        shopping['tsp vanilla extract']      += 0.5  * s
        shopping['cups confectioners sugar'] += 1    * s
        shopping['tsp baking powder']        += 1    * s

    for ingredient, amount in shopping.items():
        if amount > 0:
            st.write(f"- {amount:.2f} {ingredient}")
else:
    st.info("Enter your preorders above to generate a grocery list!")

# ============================================================
# Order History — new section, only possible now that orders
# are actually saved
# ============================================================
st.markdown("## Order History")
conn = get_connection()
history = conn.execute("""
    SELECT o.week_start, i.name AS item_name, ps.label,
           SUM(oli.quantity) AS packs, SUM(oli.line_revenue) AS revenue
    FROM order_line_items oli
    JOIN orders o ON oli.order_id = o.order_id
    JOIN pack_sizes ps ON oli.pack_size_id = ps.pack_size_id
    JOIN items i ON ps.item_id = i.item_id
    GROUP BY o.week_start, i.name, ps.label
    ORDER BY o.week_start DESC
""").fetchall()
conn.close()

if history:
    st.dataframe([dict(row) for row in history], use_container_width=True)
else:
    st.info("No saved orders yet — save your first order above to start building history.")
