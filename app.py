from nsepython import *
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from time import gmtime, strftime
# from IPython.display import clear_output 
import matplotlib.pyplot as plt
from pytz import timezone 
from deta import Deta 
# from st_aggrid import AgGrid
import warnings
warnings.filterwarnings("ignore")

def get_data():
    a=(nse_fno("BANKNIFTY"))
#     last_prices=round(nse_quote_ltp("BANKNIFTY"))
    global open1,last_prices,high,low,strike
    price=(nse_quote_meta("BANKNIFTY","latest","Fut"))
    open1=price['openPrice']
    last_prices=round(price['lastPrice'])
    high=price['highPrice']
    low=price['lowPrice']
    print(open1,high,low,last_prices)
    
    exp=list(set(a['expiryDates']))
    exp.sort(key = lambda date: datetime.strptime(date, '%d-%b-%Y')) 
    if last_prices%100>50:
        x=(last_prices-last_prices%100+100)
        strike=[x-200,x-100,x,x+100,x+200]
    elif last_prices%100<50:
        x=(last_prices-last_prices%100)
        strike=[x-200,x-100,x,x+100,x+200]
    d={'call change op':[],
        'call vwap':[],
        '% change op':[],
        'strike':[],
        'put change op':[],
        'put vwap':[],
        '% change op put':[]
        }
    for i in a['stocks']:
        for sp in strike: 
            if i['metadata']['expiryDate']==exp[0] and i['metadata']['optionType']=='Call' and i['metadata']['strikePrice']==sp:
                d['strike'].append(sp)
                d['call change op'].append(i['marketDeptOrderBook']['tradeInfo']['changeinOpenInterest'])
                d['% change op'].append(i['marketDeptOrderBook']['tradeInfo']['pchangeinOpenInterest'])
                d['call vwap'].append(i['marketDeptOrderBook']['tradeInfo']['vmap'])

            elif i['metadata']['expiryDate']==exp[0] and i['metadata']['optionType']=='Put' and i['metadata']['strikePrice']==sp:
                d['put change op'].append(i['marketDeptOrderBook']['tradeInfo']['changeinOpenInterest'])
                d['% change op put'].append(i['marketDeptOrderBook']['tradeInfo']['pchangeinOpenInterest'])
                d['put vwap'].append(i['marketDeptOrderBook']['tradeInfo']['vmap'])

    out=pd.json_normalize(d)
    
    out=out.explode(list(out.columns)).reset_index(drop = True)
    out.fillna(0,inplace=True)
    x=out.astype(float).round(2)
    x.sort_values("strike", axis = 0, ascending = True,inplace = True)
    return x
def get_info(dataset):
#     df= pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per'])
    value= dataset['put change op'].sum() - dataset['call change op'].sum()
    pcr= dataset['put change op'].sum()/dataset['call change op'].sum()
    cal_per= dataset['% change op'].mean()
    put_per= dataset['% change op put'].mean()
    new_row={'time':datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p'),'value':value, 'pcr':round(pcr,2), 'cal_per':round(cal_per,2), 'put_per':round(put_per,2),'open': round(open1),'high':round(high),'low':round(low),'close':round(last_prices)}
#     df = df.append(new_row,ignore_index=True, verify_integrity=False, sort=None)
    pcr_dataset=pd.DataFrame(new_row,index=[0])
    deta_key="d0iqnepq4nn_BgRSHUYswKQEwYxUJEFnFgH4FTfwm8EH"
    deta = Deta(deta_key)
    db = deta.Base("bullcartal1")
    def insert_user(row):
         return db.put(row)
    insert_user(new_row)
    return pcr_dataset 

def ploting():
        try:
            global final
        except:
             df = pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per'])
        dataset= get_data()
        main= get_info(dataset)
        main1=main[['value', 'pcr', 'cal_per','put_per','time']]
#         final =final.append(main1,ignore_index=True, verify_integrity=False, sort=None)
        final=pd.concat([final,main1],ignore_index=True)
        final=np.array(final)
#         deta_key="d0iqnepq4nn_BgRSHUYswKQEwYxUJEFnFgH4FTfwm8EH"
#         deta = Deta(deta_key)
#         db = deta.Base("bullcartal1")
#         def insert_user(row):
#              return db.put( row)
#         insert_user(row)
        
        return dataset,final

final = pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per','time'])


if __name__=='__main__':
    
    st.title('WELCOME BULLS CARTEL')
    today_date =strftime("%d %b %Y", gmtime()),datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
    st.markdown(f"as at {today_date}")
    option= st.selectbox(
    'How would you like to be contacted?',
    ('5', '10', '15')) 
    st.write('You selected:', option)
    st.header('Important Information')
    st.markdown(""" CALL % INCREASE MEANS MARKET GOES DOWN  
             PUT % INCREASE MEANS MARKET GOES UP
             """)    
    while True:
        current_time=datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
        dataset,final=ploting()
        p1=st.empty()
        p2=st.empty()
        p3=st.empty()
#         p1.dataframe(dataset.style.highlight_max(['% change op put','% change op'],axis=0)) #Column hightlight 
# #         final=np.array(final,column=['value', 'pcr', 'cal_per','put_per','time'])
#         p2.dataframe(final.style.highlight_max(['cal_per','put_per'],axis=1,)) # row highlight
        p1.dataframe(dataset.style.highlight_max(['% change op put','% change op'],axis=0)) #Column hightlight 
        p2.dataframe(final) # row highlight
#         p2.write(final[:100])
#         p2.AgGrid(final,height=500,fit_columns_on_grid_load=True)
#         p2.write(final[:100])
        fig, ax = plt.subplots(figsize=(6, 2)) 
        ax.plot(final['time'],final['pcr'])
        ax.axhline(y=0, color='black', linestyle='solid') # 0 line graph
        fig.autofmt_xdate(rotation=70)
        p3.pyplot(fig)
        time.sleep(3*60) # how to the start again code check upper condition min * sec
        p1.empty() # then clean all data frame 
        p2.empty()
        p3.empty()
