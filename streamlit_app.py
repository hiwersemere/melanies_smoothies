# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Custom Your Smoothie:cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!:")


NAME_ON_ORDER = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be ", NAME_ON_ORDER)


cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:'
, my_dataframe
, max_selections = 5
)
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen  + ' Nutrition Information')
        
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/all")
        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)
        # st.text(smoothiefroot_response)

        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""

    
    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    # st.write(my_insert_stmt)

    # st.stop()
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests


# helpful_links = [
#     "https://docs.streamlit.io",
#     "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
#     "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
#     "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
# ]

# # Write directly to the app
# st.title(":cup_with_straw: Custom Your Smoothie:cup_with_straw:")
# st.write("Choose the fruits you want in your custom Smoothie!:")


# NAME_ON_ORDER = st.text_input("Name on Smoothie: ")
# st.write("The name on your smoothie will be ", NAME_ON_ORDER)


# cnx = st.connection('snowflake')
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()
# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


# ingredients_list = st.multiselect('Choose up to 5 ingredients:'
# , my_dataframe
# , max_selections = 5
# )
# if ingredients_list:
#     ingredients_string = ''
    
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '
#         st.subheader(fruit_chosen  + ' Nutrition Information')
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)
#         sd_fd = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

        
#         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')    
        
#         fruityvice_response = requests.get("https://my.fruityvice.com/api/fruit/" + search_on)
#         fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
            
#         st.text(smoothiefroot_response.json())

#         sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    
#     # st.write(ingredients_string)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
#             values ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""

    
#     # st.write(my_insert_stmt)
#     time_to_insert = st.button("Submit Order")
#     st.write(my_insert_stmt)

#     # st.stop()
    
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
