# Import python packages
import streamlit as st
import requests
import pandas as pd_df
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothi!
    """)

name_on_order =  st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# option = st.selectbox(
#     'What is your favorite fruit?',
#     ('Banana', 'Strawberries', 'Peaches'))


# st.write('Your favorite fruit is:', option)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list = st.multiselect(
    'Choose up to 5 ingredient:'
    ,my_dataframe
    ,max_selections=5
)
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)

    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string  += fruit_chosen +' '
        st.subheader(fruit_chosen + 'Nutrition Information')        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        # st.text(fruityvice_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

    # st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""
    st.write(my_insert_stmt)
    # st.stop()
    # st.write(my_insert_stmt)
    time_to_start = st.button('Submit Orders')
    if time_to_start:
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()

# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# # Get the current credentials
# session = get_active_session()

# # Use an interactive slider to get user input
# hifives_val = st.slider(
#     "Number of high-fives in Q3",
#     min_value=0,
#     max_value=90,
#     value=60,
#     help="Use this to enter the number of high-fives you gave in Q3",
# )

# #  Create an example dataframe
# #  Note: this is just some dummy data, but you can easily connect to your Snowflake data
# #  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
# created_dataframe = session.create_dataframe(
#     [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
#     schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
# )

# # Execute the query and convert it into a Pandas dataframe
# queried_data = created_dataframe.to_pandas()

# # Create a simple bar chart
# # See docs.streamlit.io for more types of charts
# st.subheader("Number of high-fives")
# st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

# st.subheader("Underlying data")
# st.dataframe(queried_data, use_container_width=True)
