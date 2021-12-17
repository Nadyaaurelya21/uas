#Nama : Nadya Aurelya
#NIM  : 12220241

#import module yang dipperlukan
import json
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from pandas.core.indexes.base import Index
import streamlit as st

#input file json dan csv
open_json = open("kode_negara_lengkap.json")
datajson = json.loads(open_json.read())
file_csv = pd.read_csv("produksi_minyak_mentah.csv")
file_json = pd.DataFrame(datajson)

#MEMBUAT DATAFRAME UTAMA
known_code = []

for i in list(file_csv['kode_negara']) :
    if i in list(file_json['alpha-3']) :
        known_code.append(i)

nama_negara = []
region_negara = []
sub_region = []

for i in known_code :
    for j in range(len(file_json)) :
        if i == file_json['alpha-3'][j] :
            nama_negara.append(file_json['name'][j])
            region_negara.append(file_json['region'][j])
            sub_region.append(file_json['sub-region'][j])

jumlah_produksi = []
tahun_produksi = []
for i in range(len(file_csv)) :
    if list(file_csv['kode_negara'])[i] in list(file_json['alpha-3']) :
        jumlah_produksi.append(list(file_csv['produksi'])[i])
        tahun_produksi.append(list(file_csv['tahun'])[i])


df=pd.DataFrame(nama_negara,columns=['nama negara'])
df['kode negara']=known_code
df['jumlah produksi']=jumlah_produksi
df['tahun produksi']=tahun_produksi
df['region']=region_negara
df['subregion']=sub_region

####    TITLE
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("punya aurel pokoknya")
st.markdown("*uas prokom*")
####

### 1ST COLUMN
st.subheader("Grafik")
masukan_n = st.selectbox("Pilih Negara", nama_negara)

#Membuat plot untuk jumlah produksi negara tiap tahunnya
data_frame_1=df.loc[df["nama negara"] == masukan_n]

produksi1 = data_frame_1['jumlah produksi']
tahun1 = data_frame_1['tahun produksi']

fig, ax = plt.subplots(figsize=(16, 5))
plt.plot(tahun1,produksi1)
plt.show()
st.pyplot(fig)
### 1ST COLUMN

### 2ND COLUMN
st.subheader("Grafik")
T = st.number_input("Pilih Tahun", min_value=1971, max_value=2015, value=1990)
B1 = st.number_input("Pilih Banyaknya Negara", min_value=1, max_value=None, value=10)
dftahun = df[df['tahun produksi'] == T].sort_values(by=['jumlah produksi'], ascending=False)
dftahunb1 = dftahun[:B1]

negara2 = dftahunb1['nama negara']
produksi2 = dftahunb1['jumlah produksi']

fig, ax = plt.subplots(figsize=(16, 5))
plt.bar(negara2, produksi2)
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)
### 2ND COLUMN

#membuat dataframe kumulatif
nama_kumulatif = []
for i in df['nama negara']:
    if i not in nama_kumulatif:
        nama_kumulatif.append(i)
sum= 0
produksi_kumulatif =[]
for i in nama_kumulatif:
    for j in range(len(df)) :
        if i == df.loc[j, "nama negara"] :
           sum = sum + df.loc[j, "jumlah produksi"]
    produksi_kumulatif.append(sum)
    sum = 0

subreg_kumulatif = []
reg_kumulatif =[]
tahun = []
kode = []
for i in nama_kumulatif :
    for j in range(len(file_json)) :
        if i == file_json['name'][j] :
            subreg_kumulatif.append(df['subregion'][j])
            reg_kumulatif.append(df['region'][j])
            tahun.append(df['tahun produksi'][j])
            kode.append(df['kode negara'][j])

dfk=pd.DataFrame(nama_kumulatif,columns=['nama negara'])
dfk['jumlah produksi']=produksi_kumulatif
dfk['region']=reg_kumulatif
dfk['subregion']=subreg_kumulatif
dfk['tahun produksi']=tahun
dfk['kode negara']=kode
print(dfk)

#cleansing data kumulatif
df_summary_clean = dfk.set_index("jumlah produksi")
df_summary_clean.head()
df_summary_clean = df_summary_clean.drop([0])
df_summary_clean.reset_index(drop=False, inplace=True)
print(df_summary_clean)

#cleansing data awal
df_summary_clean1 = df.set_index("jumlah produksi")
df_summary_clean1.head()
df_summary_clean1 = df_summary_clean1.drop([0])
df_summary_clean1.reset_index(drop=False, inplace=True)
print(df_summary_clean1)

datakosong = df.loc[df['jumlah produksi']==0]
datakosong = datakosong.set_index('jumlah produksi')
datakosong.head()


### 3RD COLUMN
#mplot data kumulatif
st.subheader("Grafik")
Banyaknegara = st.number_input("Banyak Negara", min_value=1, max_value=None, value=10, key="int1")
dataplot = dfk.sort_values(["jumlah produksi"], ascending=[0])

dataplot = dataplot[:Banyaknegara]
negara = dataplot['nama negara']
produksiminyak = dataplot['jumlah produksi']

fig, ax = plt.subplots(figsize=(16, 5))
plt.bar(negara, produksiminyak)
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)
### 3RD COLUMN

### 4TH COLUMN
#Menampilkan summary data kumulatif
print(df_summary_clean.loc[54])
st.markdown(df_summary_clean.loc[54])
print(df_summary_clean.loc[87])
st.markdown(df_summary_clean.loc[87])
print(dfk.loc[dfk['jumlah produksi']==0])
st.dataframe(dfk.loc[dfk['jumlah produksi']==0])
### 4TH COLUMN

### 5TH COLUMN
input_tahun = st.number_input("Pilih Tahun", min_value=1971, max_value=2015, value=1990, key="int3)

#menampilkan summary data berdasarkan input tahun user
data_max = df_summary_clean1.loc[df_summary_clean1['tahun produksi']==input_tahun]
data_sorting = data_max.sort_values(["jumlah produksi"], ascending=[0])
st.markdown(data_sorting.iloc[0])

data_min= df_summary_clean1.loc[df_summary_clean1['tahun produksi']==input_tahun]
data_sorting = data_min.sort_values(["jumlah produksi"], ascending=[1])
st.markdown(data_sorting.iloc[0])

data = datakosong.loc[datakosong['tahun produksi']==input_tahun]
print(data)
st.dataframe(data)
### 5TH COLUMN
