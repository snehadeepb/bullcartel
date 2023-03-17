from nsepython import *
import seaborn as sns
import pandas as pd
import streamlit as st
from datetime import datetime
from time import gmtime, strftime
from IPython.display import clear_output 
import matplotlib.pyplot as plt
from pytz import timezone 
import json

def get_data():
#     a=None
#     last_prices=None
    a =(nse_fno("BANKNIFTY"))
    last_prices=round(nse_quote_ltp("BANKNIFTY"))
    while a==None and last_prices ==None:
        a=(nse_fno("BANKNIFTY"))
        last_prices=round(nse_quote_ltp("BANKNIFTY"))
#         try:
            
#         except json.decoder.JSONDecodeError:
#             print('The file contains invalid JSON')  # 👇️ this runs
#             time.sleep(1*60)
    exp=list(set(a['expiryDates']))
    exp.sort(key = lambda date: datetime.strptime(date, '%d-%b-%Y')) 
    if last_prices%100>50:
        x=(last_prices-last_prices%100+100)
        strike=[x-200,x-100,x,x+100,x+200]
    elif last_prices%100<=50:
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
    df= pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per'])
    value= dataset['put change op'].sum() - dataset['call change op'].sum()
    pcr= dataset['put change op'].sum()/dataset['call change op'].sum()
    cal_per= dataset['% change op'].mean()
    put_per= dataset['% change op put'].mean()
    new_row={'time':datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p'),'value':value, 'pcr':round(pcr,2), 'cal_per':round(cal_per,2), 'put_per':round(put_per,2)}
    df = df.append(new_row,ignore_index=True, verify_integrity=False, sort=None)
    return df  
def ploting():
        try:
            global final
        except:
             df = pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per'])
        dataset= get_data()
        main= get_info(dataset)
        final =final.append(main,ignore_index=True, verify_integrity=False, sort=None)
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
        dataset,final=ploting()
        p1=st.empty()
        p2=st.empty()
        p3=st.empty()
        p1.dataframe(dataset.style.highlight_max(['% change op put','% change op'],axis=0)) #Column hightlight 
        p2.dataframe(final.style.highlight_max(['cal_per','put_per'],axis=1)) # row highlight
        fig, ax = plt.subplots(figsize=(6, 2)) 
        ax.plot(final['time'],final['pcr'])
        ax.axhline(y=0, color='black', linestyle='solid') # 0 line graph
        fig.autofmt_xdate(rotation=70)
        p3.pyplot(fig)
        time.sleep(3*60) # how to the start again code check upper condition min * sec
        p1.empty() # then clean all data frame 
        p2.empty()
        p3.empty()

#             start_time='09.14 AM'
#             stop_time='06.05 PM'
#             current_time=datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
#             today = datetime.today().strftime('%w') # DAY WITH NO AND SAT AND SUNDAY IS 60
#             if today not in '60':
#                 if current_time>stop_time:
# #                     current_time=datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
                                          
# #                 else:
# #             else:
#                        break #time.sleep(15*60) #saturday and sunday all the time sleep mode that is the calculated (how to go else part at which tiem  then monday start time )
#         except:
#             st.write("Error message is:",'some kind problem restart 10 min')
#             time.sleep(10*60)
