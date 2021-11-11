import numpy as np
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader import data as wb
from pandas_datareader._utils import RemoteDataError
from datetime import date, timedelta, datetime
import csv
import streamlit as st
import time


st.set_page_config(
     page_title="Bist Trader",
     page_icon="💲",
)
st.title("""
BIST TRADER

""")
subheader = '<p style="font-family:Courier; color:red; font-size: 20px;">Analiz Etmeden Hisse alma</p>'
st.markdown(subheader, unsafe_allow_html=True)
tickerList = pd.read_csv("docs/Viop.csv")
ticker_all_List = pd.read_csv("docs/bist.csv")
tickers=tickerList["Ticker"]
tickers_all=ticker_all_List["Ticker"]
start_date=(date.today()-timedelta(days=360))
data_source='yahoo'
user_input = st.selectbox('Hisse',tickers_all,index=147,help='Analiz Etmek İstediğiniz Hisseyi Seçebilirsiniz.')
if user_input:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        ticker=user_input
        ticker_data=wb.DataReader(ticker,data_source=data_source,start=start_date)
        df=pd.DataFrame(ticker_data)
        ticker_date=ticker_data.index
        last_10_days_lastDayExcluded=ticker_date[-10:-1]
        c=df['Close']
        h=df['High']
        l=df['Low']
        last_price=c[-1]
        maxInDate=max(h[ticker_date])
        minInDate=min(l[ticker_date])
        max10=max(h[last_10_days_lastDayExcluded])
        min10=min(l[last_10_days_lastDayExcluded])
        potentialReward=max10-last_price
        risk=last_price-min10
        recommendationList=['Yeni Dip Yapıyor Pozisyona Girme','Yeni Zirve Arayışı','AL','Pozisyona Girme']
        new_low=str(recommendationList[0])
        new_high=str(recommendationList[1])
        buy=str(recommendationList[2])
        dontBuy=str(recommendationList[3])
        @st.cache
        def tradeable():
            if (last_price<min10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_low
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_stopLoss=str("{:.2f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.2f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.2f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.2f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    str_stopLoss=str("{:.2f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except KeyError:
        pass
    with st.container():
        st.subheader(tradeable()[0])
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.write('**Öneri**')
            st.write(tradeable()[1])
        with col2:
            st.write('**Son Fiyat**')
            st.write(tradeable()[2])
        with col3:
            st.write('**Hedef**')
            st.write(tradeable()[5])
        with col4:
            st.write('**Zarar Kes**')
            st.write(tradeable()[6])
        with col5:
            st.write('**Kar Hedefi**')
            st.write(tradeable()[3])
        with col6:
            st.markdown('**Zarar Pot.**')
            st.write(tradeable()[4])
st.subheader('BIST50 Al Tavsiyeleri')
#Analyze ALL
analyze_all_btn = st.button('BIST50 Hisselerini Analiz Et')
if analyze_all_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    definition = st.write('Bu biraz zaman alabilir bütün hisseler tek tek analiz ediliyor...')
    # '''
    # Bu biraz zaman alabilir
    # bütün hisseler tek tek analiz ediliyor...
    # '''
    # analyze_bar = st.progress(0)
    analyze_bar = st.progress(0)
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.write('**Hisse**')
        with col2:
            st.write('**Öneri**')
        with col3:
            st.write('**Son Fiyat**')
        with col4:
            st.write('**Hedef**')
        with col5:
            st.write('**Zarar Kes**')
        with col6:
            st.write('**Kar Hedefi**')
        with col7:
            st.markdown('**Zarar Pot.**')
    for i in tickers:
        with st.spinner(text='Analiz Edilen --    ' + tradeable()[0] ):
            time.sleep(1)
        for precent_complete in range(100):
                time.sleep(0.000000001)
                analyze_bar.progress(precent_complete + 1)
        try:
            ticker = i
            ticker_data=wb.DataReader(ticker,data_source=data_source,start=start_date)
            df=pd.DataFrame(ticker_data)
            ticker_date=ticker_data.index
            last_10_days_lastDayExcluded=ticker_date[-10:-1]
            c=df['Close']
            h=df['High']
            l=df['Low']
            last_price=c[-1]
            maxInDate=max(h[ticker_date])
            minInDate=min(l[ticker_date])
            max10=max(h[last_10_days_lastDayExcluded])
            min10=min(l[last_10_days_lastDayExcluded])
            potentialReward=max10-last_price
            risk=last_price-min10
            recommendationList=['Yeni Dip Yapıyor Pozisyona Girme','Yeni Zirve Arayışı','AL','Pozisyona Girme']
            new_low=str(recommendationList[0])
            new_high=str(recommendationList[1])
            buy=str(recommendationList[2])
            dontBuy=str(recommendationList[3])
            @st.cache
            def tradeable():
                # analyze_bar = st.progress(0)
                # for precent_complete in range(100):
                #     time.sleep(0.1)
                #     analyze_bar.progress(precent_complete + 1)
                if (last_price<min10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_low
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.2f} ".format(c[-1]))
                        str_stopLoss=str("{:.2f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.2f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.2f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.2f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*2):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.2f}".format(min10))
                        str_lastPrice=str("{:.2f} ".format(c[-1]))
                        str_earn_potential=str("{:.2f}".format(potentialReward))
                        str_loss_potential=str("{:.2f}".format(risk))
                        str_target_SalePrice=str("{:.2f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.2f}".format(min10))
                        str_lastPrice=str("{:.2f} ".format(c[-1]))
                        str_earn_potential=str("{:.2f}".format(potentialReward))
                        str_loss_potential=str("{:.2f}".format(risk))
                        str_target_SalePrice=str("{:.2f}".format(max10))
                        str_stopLoss=str("{:.2f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            # with st.container():
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
                with col1:
                    st.write(tradeable()[0])
                with col2:
                    st.write(tradeable()[1])
                with col3:
                    st.write(tradeable()[2])
                with col4:
                    st.write(tradeable()[5])
                with col5:
                    st.write(tradeable()[6])
                with col6:
                    st.write(tradeable()[3])
                with col7:
                    st.write(tradeable()[4])
            else:
                pass

        except KeyError:
            pass
    analzye_finished = '<p style="font-family:Courier; color:red; font-size: 20px;">Analiz Bitti!</p>'
    st.markdown(analyze_finished, unsafe_allow_html=True)
    definition = st.write('İşte Sana Bugünkü Al Listem :-)')
    delete_button = st.button('Sil')