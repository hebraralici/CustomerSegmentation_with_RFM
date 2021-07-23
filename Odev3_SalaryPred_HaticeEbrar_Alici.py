##############################################
# Salary Prediction with Machine Learning
##############################################

#######################
# İŞ PROBLEMİ
#######################
"""
Maaş bilgileri ve 1986 yılına ait kariyer istatistikleri paylaşılan beyzbol
oyuncularının maaş tahminleri için bir makine öğrenmesi projesi gerçekleştirilebilir mi?
"""

#############################
# Veri Seti Hikayesi
#############################
"""
- Bu veri seti orijinal olarak Carnegie Mellon Üniversitesi'nde bulunan StatLib 
kütüphanesinden alınmıştır.
- Veri seti 1988 ASA Grafik Bölümü Poster Oturumu'nda kullanılan verilerin bir 
parçasıdır.
- Maaş verileri orijinal olarak Sports Illustrated, 20 Nisan 1987'den alınmıştır. 
- 1986 ve kariyer istatistikleri, Collier Books, Macmillan Publishing Company, New 
York tarafından yayınlanan 1987 Beyzbol Ansiklopedisi Güncellemesinden elde 
edilmiştir.
"""
####################
# Değikenler
####################
"""
- AtBat: 1986-1987 sezonunda bir beyzbol sopası ile topa yapılan vuruş sayısı
- Hits: 1986-1987 sezonundaki isabet sayısı
- HmRun: 1986-1987 sezonundaki en değerli vuruş sayısı
- Runs: 1986-1987 sezonunda takımına kazandırdığı sayı
- RBI: Bir vurucunun vuruş yaptıgında koşu yaptırdığı oyuncu sayısı
- Walks: Karşı oyuncuya yaptırılan hata sayısı
- Years: Oyuncunun major liginde oynama süresi (sene)
- CAtBat: Oyuncunun kariyeri boyunca topa vurma sayısı
- CHits: Oyuncunun kariyeri boyunca yaptığı isabetli vuruş sayısı
- CHmRun: Oyucunun kariyeri boyunca yaptığı en değerli sayısı
- CRuns: Oyuncunun kariyeri boyunca takımına kazandırdığı sayı
- CRBI: Oyuncunun kariyeri boyunca koşu yaptırdırdığı oyuncu sayısı
- CWalks: Oyuncun kariyeri boyunca karşı oyuncuya yaptırdığı hata sayısı
- League: Oyuncunun sezon sonuna kadar oynadığı ligi gösteren A ve N seviyelerine sahip bir faktör
- Division: 1986 sonunda oyuncunun oynadığı pozisyonu gösteren E ve W seviyelerine sahip bir faktör
- PutOuts: Oyun icinde takım arkadaşınla yardımlaşma
- Assits: 1986-1987 sezonunda oyuncunun yaptığı asist sayısı
- Errors: 1986-1987 sezonundaki oyuncunun hata sayısı
- Salary: Oyuncunun 1986-1987 sezonunda aldığı maaş(bin uzerinden)
- NewLeague: 1987 sezonunun başında oyuncunun ligini gösteren A ve N seviyelerine sahip bir faktör

"""
####################
# GÖREV
####################
"""
Veri ön işleme ve özellik mühendisliği tekniklerini kullanarak maaş
tahmin modeli geliştiriniz.
"""

# Gerekli Kütüphaneler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler, RobustScaler

# çalışma dizinimde fonksiyonları tuttuğum dosyaların import edilmesi
from helpers.eda import *
from helpers.data_prep import *

# gerekli ayarlar
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 170)

df = pd.read_csv("datasets/hitters.csv")
df.head()

########################
# Keşifçi Veri Analizi
########################
check_df(df)

cat_cols, num_cols, cat_but_car = grab_col_names(df)

# kategorik değişkenlerin incelenmesi
for col in cat_cols:
    cat_summary(df, col, plot=True)

# nümerik değişkenlerin incelenmesi
for col in num_cols:
    num_summary(df, col, plot=True)

# nümerik kolonların target ile ilişkisi
for col in num_cols:
    target_summary_with_num(df, "Salary", col)

##########################
# Data Preprocessing (Veri Ön İşleme)
##########################

# MISSING VALUES
missing_values_table(df) # bağımlı değişkende eksik gözlemler var

df["Salary"].fillna(df["Salary"].median(), inplace=True)
df.isnull().sum()

# Label Encoding
binary_cols = [col for col in df.columns if df[col].dtype not in [np.int64, np.float64]
               and df[col].nunique() == 2]

for col in binary_cols:
    df = label_encoder(df, col)

df.head()

# Standardizasyon
for col in num_cols:
    transformer = RobustScaler().fit(df[[col]])
    df[col] = transformer.transform(df[[col]])


##########################
# Model
##########################

X = df.drop('Salary', axis=1)
y = df[["Salary"]]

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.20, random_state=1)

reg_model = LinearRegression().fit(X_train, y_train)

# sabit (b - bias)
reg_model.intercept_

# coefficients (w - weights)
reg_model.coef_

# Train RMSE
reg_model.score(X_train, y_train)
# 0.4335994395874614
# Test RMSE
y_pred = reg_model.predict(X_test)
np.sqrt(mean_squared_error(y_test, y_pred))
#  0.765214758567241
# Test RKARE
reg_model.score(X_test, y_test)
# 0.4548304456567662
# 10 Katlı CV RMSE
np.mean(np.sqrt(-cross_val_score(reg_model,
                                 X,
                                 y,
                                 cv=10,
                                 scoring="neg_mean_squared_error")))

# 0.685372603983996
