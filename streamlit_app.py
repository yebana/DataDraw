import streamlit as st
import pandas as pd

# Create a list of data to be represented in x-axis 
days = [ 'Saturday' , 'Sunday' , 'Monday' , 'Tuesday' , 
        'Wednesday' , 'Thursday' , 'Friday' ] 
  
# Create a list of data to be  
# represented in y-axis 
calories = [ 1670 , 2011 , 1853 , 2557 , 
            1390 , 2118 , 2063 ] 
  
# Create a dataframe using the two lists 
df_days_calories = pd.DataFrame( 
    { 'day' : days , 'calories' : calories }) 
  
df_days_calories

# use plot() method on the dataframe 
df_days_calories.plot( 'day' , 'calories' ) 

# Alternatively, you can use .set_index 
# to set the data of each axis as follows: 
# df_days_calories.set_index('day')['calories'].plot(); 

