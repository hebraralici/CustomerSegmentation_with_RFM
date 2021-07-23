######################################
# Customer Segmention with RFM
######################################

# Kütüphaneler ve gerekli ayarlar
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)  # Bütün sutunları gösterir.
pd.set_option('display.max_rows', None) # Bütün satırları gösterir.
pd.set_option('display.float_format', lambda x: '%.2f' % x) # Virgülden sonra 2 basamak verir.

df_ = pd.read_excel("datasets/online_retail_II.xlsx",sheet_name="Year 2010-2011" )
df = df_.copy()
df.head()

##########################################
# Veri setinin yapısal olarak incelenmesi
##########################################
def check_df(dataframe):
    print("################ Shape ####################")
    print(dataframe.shape)
    print("############### Columns ###################")
    print(dataframe.columns)
    print("############### Types #####################")
    print(dataframe.dtypes)
    print("############### Head ######################")
    print(dataframe.head())
    print("############### Tail ######################")
    print(dataframe.tail())
    print("############### Describe ###################")
    print(dataframe.describe().T)

check_df(df)

# Eksik Gözlemler
df.isnull().any()
df.isnull().sum()
df.dropna(inplace=True) # eksik değerlerin kalıcı olarak silinmesi

# Eşsiz ürün sayısı
df["StockCode"].nunique()

# Hangi üründen kaçar adet olduğu
df.groupby("StockCode")["Quantity"].sum()

# En çok sipariş edilen 5 ürünün azalan şekilde sıralanması
df.groupby("StockCode").agg({"Quantity":"sum"}).sort_values(by="Quantity", ascending=False).head()

# Faturalardaki iptal edilen işlemlerin veri setinden çıkarılması
df = df[~df["Invoice"].str.contains("C", na=False)]

# Her bir faturanın toplam bedeli
df["TotalPrice"] = df["Price"] * df["Quantity"]

######################################
# RFM Metriklerinin Oluşturulması
######################################
# recency: bugün ile müşterinin en son satın alma tarihi arasındaki fark, gün cinsinden
# frequency: müşterinin alışveriş sıklığı
# monetary: müşterinin ödediği toplam para

df["InvoiceDate"].max()
today_date = dt.datetime(2011, 12, 11) # analizin yapıldığı tarih

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda InvıiceDate: (today_date- InvıiceDate.max()).days,
                                    "Invoice": lambda Invoice: Invoice.nunique(),
                                    "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

rfm.columns = ["recency","frequency","monetary"]
rfm = rfm[rfm["monetary"] > 0] # monetory: min değeri 0 ,işlem yapılmamış para girişi yok bunu çıkarmam gerek.

##################################
# RFM Skorlarının Hesaplanması
##################################
## Recency
# En son tarih skoru.Burada 1 en yakın, 5 en uzak tarihi temasil eder.
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

## Frequency
# Alışveriş sıklığı skoru. Burada 1 en az sıklığı, 5 en fazla sıklığı temsil eder.
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

## Monetary
# Müşternin bize bıraktığı para miktarı. Burada 1 en az miktarı,5 en fazla miktarı temsil eder.
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

## RFM Skoru
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
rfm.head()

rfm.describe().T

rfm[rfm["RFM_SCORE"] == "55"].head()  # champions

rfm[rfm["RFM_SCORE"] == "11"].head()  # hibernating

############################################################
# RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi
############################################################
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

# regular expression
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)  # birleştirilen skorlar seg_map ile değiştirildi
rfm.head()

# Segmentlere göre RFM ortalama ve sıklık değerlerini gruplama
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

rfm[rfm["segment"] == "need_attention"].head()  # Need Attention sınıfını gösterir.
rfm[rfm["segment"] == "new_customers"].index  # yeni müşterilerin müşteri numaralarını listeler.

# Seçilen segmentlerin incelenmesi
seg_list = ["at_Risk", "hibernating", "cant_loose", "loyal_customers"]
for i in seg_list:
    print(F" {i.upper()} ".center(50, "*"))
    print(rfm[rfm["segment"]==i].describe().T)

# Seçilen bir segmentin excele alınması
rfm[rfm["segment"] == "loyal_customers"].index
loyalCus_df = pd.DataFrame()
loyalCus_df["loyal_customersId"] = rfm[rfm["segment"] == "loyal_customers"].index
loyalCus_df.head()

loyalCus_df.to_csv("loyal_customers.csv")

###########################################
# Tüm Sürecin Fonksiyonlaştırılması
###########################################

def create_rfm(dataframe):

    # Veriyi Hazırlama
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM Metriklerinin Hazırlanması
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM Skorlarının Hesaplanması
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklenmesi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # Segmentlerin İsimlendirilmesi
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    return rfm

df = df_.copy()
rfm_new = create_rfm(df)
rfm_new.head()


