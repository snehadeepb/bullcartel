from nsepython import *
import seaborn as sns
import pandas as pd
import streamlit as st
from datetime import datetime
from time import gmtime, strftime
from IPython.display import clear_output 
import matplotlib.pyplot as plt
from pytz import timezone 

def get_data():
  a=(nse_fno("BANKNIFTY"))
  last_prices=round(nse_quote_ltp("BANKNIFTY"))
  exp=list(set(a['expiryDates']))
#   today_date =strftime("%d %b %Y", gmtime())
  exp.sort(key = lambda date: datetime.strptime(date, '%d-%b-%Y'))
#   exp[0] 
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
  x=pd.DataFrame(d)
  x.sort_values("strike", axis = 0, ascending = True,inplace = True)
  x=x.round(2)
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
#             print('not error')
        except:
             df = pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per'])
#              print('error')
        dataset= get_data()
        main= get_info(dataset)
        final =final.append(main,ignore_index=True, verify_integrity=False, sort=None)
        return dataset,final

final = pd.DataFrame(columns=['value', 'pcr', 'cal_per','put_per','time'])
    
def app_layout():
    st.title('WELCOME BULLS CARTEL')

 
if __name__=='__main__':
    
    st.title('WELCOME BULLS CARTEL')
    today_date =strftime("%d %b %Y", gmtime()),datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
    st.markdown(f"as at {today_date}")
    option= st.selectbox(
    'How would you like to be contacted?',
    ('5', '10', '15')) 
    st.write('You selected:', option)
    st.header('Important Information')
    st.markdown(""" CALL % INCREASE MEANS MARKET GOES UP  
             PUT % INCREASE MEANS MARKET GOES DOWN
             """)

    
    while True:
        try:
            start_time='09.15 AM'
            stop_time='03.30 PM'
            current_time=datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
            print(current_time)
            today = datetime.today().strftime('%w')
    #           print(today)
            if today not in '60':
            
              # print(current_time)
                if current_time<stop_time:
                    current_time=datetime.now(timezone("Asia/Kolkata")).strftime('%I.%M %p')
    #                 print(current_time)
                    dataset,final=ploting()
                    p1=st.empty()
                    p2=st.empty()
                    p3=st.empty()

                    p1.dataframe(dataset.style.highlight_max(['% change op put','% change op'],axis=0))
                    p2.dataframe(final.style.highlight_max(['cal_per','put_per'],axis=1))
                    fig, ax = plt.subplots(figsize=(6, 2)) 
                    ax.plot(final['time'],final['pcr'])
                    ax.axhline(y=0, color='black', linestyle='solid') # 0 line graph
                    fig.autofmt_xdate(rotation=70)
                    p3.pyplot(fig)
#                     time.sleep(50)
                    
                    time.sleep(3*60) # how to the start again code check upper condition min * sec
                    p1.empty()
                    p2.empty()
                    p3.empty()
                      
                else:
                    time.sleep(480*60)# calculate again market start time put min  there  8 hours 
            else:
                time.sleep(42000*2) #saturday and sunday all the time sleep mode that is the calculated (how to go else part at which tiem  then monday start time )
                # print('error')

        except:
            print("Error message is:",'some kind problem restart 10 min')
            time.sleep(10*60)
            continue

        
        
        
        


        

# st.dataframe(df['column_name'].style.highlight_max(axis=1)) #   we have two values   row wise hightlight  axis=1
# st.dataframe(dataset[].style.highlight_max(axis=0)) #column wise increase % change op put 
# #stemlit time was the showing the wrong
