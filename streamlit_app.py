import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get(f"https://fruityvice/api/fruit/{this_fruit_choice}")
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
    return f"Thanks for adding {new_fruit}" 
 

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit') 

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:   
    fruityvice_result = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_result)
except URLError as e:
  streamlit.error()  

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_data_row = get_fruit_load_list(my_cnx)
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_response = insert_row_snowflake(add_my_fruit)
  streamlit.text(insert_response)


