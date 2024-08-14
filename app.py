## Importing the packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

## Setting the title 'Sales Forecasting'
st.title(":blue[Sales Forecasting]  :sunglasses:")

## Taking the user inputs for the model in order to forecast
def getting_inputs():
    #num is the forecasting days
    num = st.number_input('For how many days do you want to Forecast',min_value=1,step = 1)

    #ex_flag is for indicating the presence or absence of exogenous variable
    ex_flag = st.selectbox('Would you like to add Holiday as exogenous variable',('Yes','No'))

    return num,ex_flag


##Loading the sarima model for forecasting without exogenous variable
def sarima_predict(num):

    #Loading the pickle file of the model and forecasting
    with open('sarima.pkl','rb') as file:
        sarima = pickle.load(file)
        return sarima.forecast(num)


def check_exog(flag):
    ## If we want to add exogenous variable than we take the holiday inputs
    if flag=='Yes':
        ex = st.text_input('Please enter the holidays as shown, 1: for holiday and 0: for non holiday',placeholder='1,1,0,1,1')
        try:
            # Converting the input to integer
            l = ex.split(',')
            if len(l)>=1:
                l_int = [int(s) for s in l]
            return l_int
        except:
            st.write("Please enter the Holidays if you would like to add an exogenous variable")
    else:
        return -1


## Loading the sarimax model for exogenous forecasting
def load_sarimax(num,exog):
    #Loading the sarimax file
    with open('sarimax.pkl','rb') as file:
        sarimax = pickle.load(file)
        return sarimax.forecast(num,exog = exog)


#Checking if the holiday inputs matches the number of days given for forecasting
def check_holiday(exog,num):
    try:
        if len(exog)!=num:
            st.write(":red[Number of holidays do not match the number of forecasting days]")
    except:
        pass


## Plotting the forecasted sales
def plot_forecast(sales):
    st.line_chart(sales)


## The main flow 
def main():
    num,ex_flag = getting_inputs()
    exog = check_exog(ex_flag)
    if exog==-1:
        st.write('Predicting Sales without exogenous variable')
    else:
        check_holiday(exog,num)
        st.write('Predicting Sales with exogenous variable')
    button = st.button('Predict Sales')
    if((button==True) and (exog==-1) ):
        sales = np.round(sarima_predict(num),2)
        st.dataframe(sales)
        plot_forecast(sales)
    elif((button==True) and (exog!=-1)):
        sales_ex = np.round(load_sarimax(num,exog),2)
        st.dataframe(sales_ex)
        plot_forecast(sales_ex)

main()
        













    

