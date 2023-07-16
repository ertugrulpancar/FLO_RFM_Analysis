########################################################################################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
########################################################################################################################

########################################################################################################################
# İş Problemi (Business Problem)
########################################################################################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

########################################################################################################################
# Veri Seti Hikayesi
########################################################################################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan
# müşterilerin geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

########################################################################################################################
# GÖREVLER
########################################################################################################################

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade
#               etmektedir. Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların
#               dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

# GÖREV 2: RFM Metriklerinin Hesaplanması

# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye
#               kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları
#                       genel müşteri tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için
#                       ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık
#                       müşterilerinden(champions,loyal_customers), ortalama 250 TL üzeri ve kadın kategorisinden
#                       alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id
#                       numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili
#                       kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir alışveriş yapmayan
#                       kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef
#                       alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına
#                       indirim_hedef_müşteri_ids.csv olarak kaydediniz.


# GÖREV 6: Tüm süreci fonksiyonlaştırınız.

########################################################################################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
########################################################################################################################
import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# 1. flo_data_20K.csv verisini okuyunuz.

df_ = pd.read_csv(r"crmAnalytics/Cases/FLOMusteriSegmentasyonu/flo_data_20k.csv")
df = df_.copy()


# 2. Veri setinde

df.head(10)         # a. İlk 10 gözlem,
df.columns          # b. Değişken isimleri,
df.shape            # c. Boyut,
df.describe().T     # d. Betimsel istatistik,
df.isnull().sum()   # e. Boş değer,
df.dtypes           # f. Değişken tipleri, incelemesi yapınız.


# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.

df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
df.head(10)
df.dtypes

# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)

df.dtypes
df["first_order_date"] = df["first_order_date"].apply(pd.to_datetime)
df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)
df["last_order_date_online"] = pd.to_datetime(df["last_order_date_online"])
df["last_order_date_offline"] = pd.to_datetime(df["last_order_date_offline"])

# Alternatif:
date_col = [col for col in df.columns if "date" in str(col)]
for col in date_col:
    df[col] = pd.to_datetime(df[col])

for col in date_col:
    print(f"{col}: {df[col].dtype}")


date_cols = df.columns[df.columns.str.contains("date")]
df[date_cols] = df[date_cols].apply(pd.to_datetime)

for i in df:
    if str(i).__contains__("date"):
       df[i] = df[i].astype("datetime64")

# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız.



df.groupby("order_channel").agg({"master_id": "count",
                                 "customer_value_total_ever_offline": "mean",
                                 "customer_value_total_ever_online": "mean",
                                 "order_num_total_ever_offline": "mean",
                                 "order_num_total_ever_online": "mean",
                                 "order_num_total": "mean",
                                 "customer_value_total": "mean"})

df.groupby("order_channel")[["master_id", "order_num_total", "customer_value_total"]].describe().T

# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

(df.groupby("master_id").agg({"customer_value_total": "sum"}).sort_values(by="customer_value_total", ascending=False)
 .head(10))

df.sort_values(by="customer_value_total", ascending=False).head(10)

# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.

df.groupby("master_id").agg({"order_num_total": "sum"}).sort_values(by="order_num_total", ascending=False).head(10)

df.sort_values(by="order_num_total", ascending=False).head(10)

# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.


def data_preparation(dataframe, head=10):
    print("################################ ilk on gözlem ################################\n", dataframe.head(head))
    print("################################ değişken listesi ################################\n", dataframe.columns)
    print("################################ betimsel istatistik ################################\n", dataframe.describe().T)
    print("################################ boş değerler ################################\n", dataframe.isnull().sum())
    print("################################ genel bilgi ################################\n", dataframe.info())

    # Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturulması
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = (dataframe["customer_value_total_ever_online"] +
                                         dataframe["customer_value_total_ever_offline"])

    # Tarih ifade eden değişkenlerin tipini date'e çevrilmesi
    date_col = [col for col in dataframe.columns if "date" in str(col)]
    for col in date_col:
        dataframe[col] = pd.to_datetime(dataframe[col])

    for col in date_col:
        print(f"{col}: {type(dataframe[col])}")
    print("date değişkenlerinin tipi değiştirildi...\n", dataframe.dtypes)

    # Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımı
    print(
        "Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımı:")
    print(dataframe.groupby("order_channel")[["master_id", "order_num_total", "customer_value_total"]].describe().T)

    # En fazla kazancı getiren ilk 10 müşteri
    print("En fazla kazancı getiren ilk 10 müşteri:")
    most_value = pd.DataFrame(dataframe.groupby("master_id").agg({"customer_value_total": "sum"})
                              .sort_values(by="customer_value_total", ascending=False))
    print(most_value.head(head))

    # En fazla siparişi veren ilk 10 müşteri
    print("En fazla siparişi veren ilk 10 müşteri:")
    most_order = pd.DataFrame(dataframe.groupby("master_id").agg({"order_num_total": "sum"})
                              .sort_values(by="order_num_total", ascending=False))
    print(most_order.head(head))

    return dataframe, most_value, most_order


new_df, value, order = data_preparation(df)
########################################################################################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
########################################################################################################################

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi

df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)

# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe

rfm = df.groupby("master_id").agg({"last_order_date": lambda date: (today_date - date.mean()).days,
                                   "order_num_total": lambda order: order.sum(),
                                   "customer_value_total": lambda value: value.sum()})

rfm.columns = ["recency", "frequency", "monetary"]

rfm.describe().T
########################################################################################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
########################################################################################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi

rfm["RF_SCORE"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)

########################################################################################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
########################################################################################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile
# RF_SCORE'u segmentlere çevirme

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

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

########################################################################################################################
# GÖREV 5: Aksiyon zamanı!
########################################################################################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["count", "mean"])

# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
#    tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel
#    olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve kadın kategorisinden alışveriş yapan kişiler
#    olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.

rfm.reset_index(inplace=True)
rfm_final = df.merge(rfm, on="master_id", how="left")
rfm_final[(rfm_final["interested_in_categories_12"].str.contains("KADIN")) &
          (rfm_final["segment"] == "loyal_customers")]["master_id"].shape\
           .to_csv("yeni_marka_hedef_müşteri_id.csv")


# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen
#    geçmişte iyi müşterilerden olan ama uzun süredir alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef
#    alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv olarak
#    kaydediniz.

rfm_final[(rfm_final["interested_in_categories_12"].str.contains("ERKEK")) &
          (rfm_final["interested_in_categories_12"].str.contains("COCUK")) &
          ((rfm_final["segment"] == "new_customers") |
          (rfm_final["segment"] == "cant_loose"))]["master_id"].to_csv("indirim_hedef_müşteri_ids.csv")
