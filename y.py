import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
import csv
import streamlit as st
import time
import yfinance as yf
import locale

locale.setlocale(locale.LC_ALL, '')
st.set_page_config(
     page_title="Bist Trader",
     page_icon="💲",
)
st.title("""
BIST TRADER

""")
subheader = '<p style="font-family:Courier; color:red; font-size: 20px;">Analiz Etmeden Hisse Alma</p>'
st.markdown(subheader, unsafe_allow_html=True)
ViopList = pd.read_csv("docs/Viop.csv")
ticker_all_List = pd.read_csv("docs/bist.csv")
tickers=ViopList["Ticker"]
ViopList_len=len(tickers)
tickers_all=ticker_all_List["Ticker"]
user_input = st.selectbox('Hisse',tickers_all,index=147,help='Analiz Etmek İstediğiniz Hisseyi Seçebilirsiniz.')
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        daily_btn = st.button('Günlük Analiz')
    with col2:
        FiveM_btn = st.button('5 Dk. Analiz')
    with col3:
        Hour_btn = st.button('60 Dk. Analiz')
ticker=user_input
# Günlük Analiz
if daily_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ticker_data=yf.download(ticker,period="1y",interval="1d")
    try:
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
        st.caption("Günlük Analiz")
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
            st.write('**Kar Pot.**')
            st.write(tradeable()[3])
        with col6:
            st.markdown('**Zarar Pot.**')
            st.write(tradeable()[4])
# 5 Dakikalık Analiz
elif FiveM_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ticker_data=yf.download(ticker,period="1d",interval="5m")
    try:
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
        st.caption('5 Dakikalık Analiz')
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
            st.write('**Kar Pot.**')
            st.write(tradeable()[3])
        with col6:
            st.markdown('**Zarar Pot.**')
            st.write(tradeable()[4])
# 60 Dakikalık Analiz
elif Hour_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ticker_data=yf.download(ticker,period="1mo",interval="60m")
    try:
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
        st.caption('60 Dakikalık Analiz')
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
            st.write('**Kar Pot.**')
            st.write(tradeable()[3])
        with col6:
            st.markdown('**Zarar Pot.**')
            st.write(tradeable()[4])
st.subheader('BIST50 Al Tavsiyeleri')
#Analyze ALL
analyze_all_btn = st.button('BIST50 Hisselerini Analiz Et')
if analyze_all_btn:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
            st.write('**Kar Pot.**')
        with col7:
            st.markdown('**Zarar Pot.**')
    for i in tickers:
        # with st.spinner(text='Analiz Edilen --    ' + tradeable()[0] ):
        #     time.sleep(1)
        # for precent_complete in ticker_data:
        #         time.sleep(0.000000001)
        #         analyze_bar.progress(precent_complete + 1)
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1y")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(53):
                time.sleep(0)
                analyze_bar.progress(percent_complete)
            # for precent_complete in range(100):
            #     time.sleep(0.000000001)
            #     analyze_bar.progress(precent_complete)
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
            # with st.container():
            with st.spinner(text='Analiz Edilen --    ' + tradeable()[0] ):
                time.sleep(0)
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
                with col1:
                    st.info(tradeable()[0])
                with col2:
                    st.success(tradeable()[1])
                with col3:
                    st.info(tradeable()[2])
                with col4:
                    st.success(tradeable()[5])
                with col5:
                    st.error(tradeable()[6])
                with col6:
                    st.success(tradeable()[3])
                with col7:
                    st.warning(tradeable()[4])
            else:
                pass
        except KeyError:
            pass
    analzye_finished = '<p style="font-family:Courier; color:red; font-size: 20px;">Analiz Bitti!</p>'
    st.markdown(analzye_finished, unsafe_allow_html=True)
    st.caption('İşte Sana Bugünkü Al Listem :-)')
    delete_button = st.button('Sil')