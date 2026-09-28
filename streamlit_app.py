import streamlit as st

# Create Snowflake connection
conn = st.connection("snowflake")

# Get Snowflake session
session = conn.session()

# App title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")


# Get fruit options
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select("FRUIT_NAME")
)

# Convert to Python list
fruit_names = [
    row["FRUIT_NAME"]
    for row in my_dataframe.collect()
]


# Select ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)


if ingredients_list:

    # Convert list to string
    ingredients_string = " ".join(ingredients_list)

    st.write("Your smoothie contains:")
    st.write(ingredients_string)

    # Handle apostrophes
    ingredients_string_sql = ingredients_string.replace("'", "''")

    # Insert into ORDERS table
    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS)
        VALUES ('{ingredients_string_sql}')
    """

    session.sql(my_insert_stmt).collect()

    st.success("Your Smoothie is ordered! :white_check_mark:")
