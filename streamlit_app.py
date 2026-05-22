import streamlit as st

# Prices per oz
flour_price = 0.03
baking_powder_price = 0.262
salt_price = 0.139
granulated_sugar_price = 0.049
unsalted_butter_price = 0.279
egg_price = 0.121
ube_halaya_jam_price = 0.90
ube_extract_price = 0.845
vanilla_extract_price = 3.00
confectioners_sugar_price = 0.062

# Oz per unit used in base recipe
OzFlour = 4.25
OzBakingPowder = 0.167
OzSalt = 0.2
OzGranulatedSugar = 7
OzUnsaltedButter = 8.0
OzUbeHalayaJam = 9.5
OzUbeExtract = 0.17
OzVanillaExtract = 0.17
OzConfectionersSugar = 4

# Base costs
cost_flour = 1.75 * OzFlour * flour_price
cost_baking_powder = 1 * OzBakingPowder * baking_powder_price
cost_salt = 0.25 * OzSalt * salt_price
cost_granulated_sugar = 1 * OzGranulatedSugar * granulated_sugar_price
cost_butter = 0.5 * OzUnsaltedButter * unsalted_butter_price
cost_egg = egg_price
cost_ube_jam = 0.5 * OzUbeHalayaJam * ube_halaya_jam_price
cost_ube_extract = 2 * OzUbeExtract * ube_extract_price
cost_vanilla_extract = 0.5 * OzVanillaExtract * vanilla_extract_price
cost_confectioners_sugar = 1 * OzConfectionersSugar * confectioners_sugar_price

ube_total_cost = (cost_flour + cost_baking_powder + cost_salt +
                  cost_granulated_sugar + cost_egg + cost_ube_jam +
                  cost_ube_extract + cost_vanilla_extract + cost_confectioners_sugar)

ube_base_servings = 18
ube_cost_per_cookie = ube_total_cost / ube_base_servings

# --- UI ---
st.markdown("<h1 style='color:#6b21a8;'>🍪 Ube Crinkle Cookies</h1>", unsafe_allow_html=True)
st.write("Soft and chewy Filipino ube cookies rolled in powdered sugar")

desired_cookies = st.number_input("How many cookies do you want?", min_value=1, value=18)
scale = desired_cookies / ube_base_servings

st.markdown("---")
st.markdown("<h3 style='color:#6b21a8;'>Ingredients</h3>", unsafe_allow_html=True)
st.write(f"- {1.75 * scale:.2f} cups all-purpose flour")
st.write(f"- {1 * scale:.2f} tsp baking powder")
st.write(f"- {0.25 * scale:.2f} tsp kosher salt")
st.write(f"- {1 * scale:.2f} cups granulated sugar")
st.write(f"- {0.5 * scale:.2f} cups unsalted butter")
st.write(f"- {1 * scale:.1f} large egg(s)")
st.write(f"- {0.5 * scale:.2f} cups ube halaya jam")
st.write(f"- {2 * scale:.2f} tsp ube extract")
st.write(f"- {0.5 * scale:.2f} tsp pure vanilla extract")
st.write(f"- {1 * scale:.2f} cups confectioners sugar")

st.markdown("---")
st.markdown("<h3 style='color:#6b21a8;'>Instructions</h3>", unsafe_allow_html=True)
st.write("1. Preheat oven to 350°F.")
st.write("2. In a bowl whisk together the flour, baking powder, and salt.")
st.write("3. In another bowl combine the sugar and butter and beat until light and fluffy.")
st.write("4. Add egg and beat until combined.")
st.write("5. Add the ube halaya jam, ube extract, and vanilla extract. Beat until completely purple.")
st.write("6. Gradually add the dry ingredients and beat until just combined.")
st.write("7. Chill overnight.")
st.write("8. Roll into 3 tbsp balls and coat generously with confectioners sugar.")
st.write("9. Bake for 12-15 minutes.")

st.markdown("---")
st.markdown("<h3 style='color:#6b21a8;'>Cost</h3>", unsafe_allow_html=True)
st.write(f"💰 Total cost: **${ube_total_cost * scale:.2f}**")
st.write(f"🍪 Cost per cookie: **${ube_cost_per_cookie:.2f}**")
