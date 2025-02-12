#!/usr/bin/env python
# coding: utf-8

# # Pengolahan Data Pasang Surut
# Dalam notebook ini, akan dilakukan **pengolahan data elevasi muka air** yang diperoleh dari situs [IOC-Sea Level Monitoring](http://www.ioc-sealevelmonitoring.org/).
# 
# Pengolahan yang dilakukan adalah meliputi:
# - Deskripsi statistik
# - Visualisasi data
# - Filtering

# ### Deksripsi Data yang Digunakan
# - **Parameter**: elevasi muka air laut
# - **Satuan**: mm
# - **Periode data yang digunakan**: Juni 1994
# - **Resolusi (periode pengukuran)**: 60 menit
# - **Lokasi**: Kolinamil,Jakarata port
# - **Koordinat lokasi (lon/lat)**: 106.89083/-6.10667

# ## Rules Penggunaan Notebook
# - Mengganti variabel data `data_TAHUN_BULAN` sesuai pembagian tugas, misal `data_1994_sep`
# - Mengganti variabel data `data_TAHUN_TANGGAL_BULAN` sesuai pembagian tugas, misal `data_1994_18_sep`
# - Ketika bertemu dengan intruksi **#YOUR CODE HERE**, artinya anda harus membuat code disitu
# 
# Notes:
# Jika rules ini ada yang tidak terpenuhi maka akan ada pengurangan nilai untuk modul 1 ini.
# 

# ### Instalasi Library
# Dalam pengolahan yang dilakukan, akan digunakan beberapa library dari **python**. Untuk itu perlu dilakukan instalasi library tersebut. Library yang akan digunakan pada pengolahan data di modul 1 ini meliputi:
# - **Pandas**: untuk manipulasi data
# - **Numpy**: berfungsi untuk melakukan operasi vektor dan matriks dengan mengolah array dan array multidimensi.
# - **Math**: operasi matematis
# - **Matplotlib**: untuk visualisasi data
# - **Plotly**: untuk membuat visualisasi data interaktif
# - **Folium**: untuk membuat peta interaktif
# 
# Note:
# Instalasi dilakukan hanya 1 kali saja, untuk penggunaan selanjutnya tidak perlu menginstall library tersebut.

# In[17]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install math')
get_ipython().system('pip install matplotlib')
get_ipython().system('pip install plotly')
get_ipython().system('pip install folium')


# In[16]:


# Import library
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")


# ### Plot Daerah Kajian

# In[10]:


import folium

# Koordinat lokasi
Daerah_Kajian = 'Kolinamil'
Lat = -6.10667
Lon = 106.89083

# Membuat interaktif map
my_map = folium.Map(location=[Lat, Lon ], ## format: lat, lon 
                   zoom_start=10.5)

# Membuat penanda lokasi 
folium.Marker([Lat, Lon], # format: lat, lon
               popup = Daerah_Kajian, icon=folium.Icon(color='blue')).add_to(my_map)

display(my_map)


# In[4]:


# load data
path_data = '/content/pasut_kolinamil.csv'
raw_data = pd.read_csv(path_data)

raw_data.head()


# In[11]:


# Merapihkan data: memberikan header
header_data = ['tahun','bulan', 'tanggal','jam','elevasi_mm'] # isi list ini dgn meng-copy list berikut 'tahun','bulan','tanggal','jam','elevasi_mm'
raw_data = pd.read_csv(path_data, names = header_data)

display(raw_data.head())
display(raw_data.tail())


# In[15]:


# melihat informasi data
raw_data.info()


# In[14]:


# ingin melihat 24 baris pertama pada data kita
raw_data.head(24)


# In[12]:


# Filtering data berdasarkan tahun dan bulan yang ditentukan
def ambil_data_1bulan(raw_data, tahun, bulan):
  # Filter data sesuai tahun dan bulan yang ditentukan
  data_1bulan = raw_data[(raw_data['tahun'] == tahun) &
                         (raw_data['bulan'] == bulan)]
  return data_1bulan                                            


# In[13]:


tahun = 1994
bulan = 6
data_1994_Jun = ambil_data_1bulan(raw_data, tahun, bulan) # ganti kata 'TAHUN' dan 'BULAN' sesuai dgn pembagian datanya

data_1994_Jun


# In[10]:


# konversi elevasi jadi meter
data_1994_Jun['elevasi_m'] = data_1994_Jun['elevasi_mm'] / 1000

data_1994_Jun.head()


# In[11]:


# hilangkan kolom elevasi yg memiliki satuan 'mm'
data_1994_Jun.drop('elevasi_mm', axis=1, inplace=True)

data_1994_Jun.head()


# In[12]:


# Membuat kolom baru yang isinya tahun-bulan-tanggal jam:menit
data_1994_Jun['tanggal_lengkap'] = (data_1994_Jun.tahun.astype(str)+'-'
                                    +data_1994_Jun.bulan.astype(str)+'-'
                                    +data_1994_Jun.tanggal.astype(str)+' '
                                    +data_1994_Jun.jam.astype(str)+':00')

data_1994_Jun.head()


# In[13]:


# Menjadikan kolom 'tanggal_lengkap' sebagai index data
data_1994_Jun = data_1994_Jun.set_index(data_1994_Jun['tanggal_lengkap'])

data_1994_Jun.head()


# In[14]:


# menghilangkan duplikasi kolom 'tanggal_lengkap'
data_1994_Jun.drop('tanggal_lengkap', axis=1, inplace=True)

data_1994_Jun.head()


# In[15]:


# Mencari informasi statistika deskriptif
data_1994_Jun[['elevasi_m']].describe()


# ### Plot Raw Data

# In[16]:


# plot data
data_1994_Jun['elevasi_m'].plot(color='blue', linewidth=2, figsize=(13,5))
plt.title('Elevasi Muka Air di Kolinamil pada 1994')
plt.xlabel('Waktu', fontsize=14, fontweight='bold')
plt.ylabel('Elevasi [m]', fontsize=14, fontweight='bold')
plt.xticks(np.linspace(0, len(data_1994_Jun), 5), # pembagian jumlah ticks nya
           ['1 Jun', '8 Jun', '15 Jun', '22 Jun', '29 Jun']) # 1 bulan dibagi 4
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['axes.labelweight'] = 'bold'
plt.grid()


# In[17]:


# Interaktif Plot dgn plotly.express
from IPython.display import HTML
import plotly.express as px

fig = px.line(y = data_1994_Jun['elevasi_m'], x = data_1994_Jun.index, labels={
    'value':'Elevasi [m]',
    'index':'Waktu',
    'variable':'Kolinamil'
})

HTML(fig.to_html())


# ## Filter Data Pasut

# In[18]:


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

Ts = 3600 # periode pengambilan data dalam sekon
fs = 1/Ts  # Frekuensi sampling, satuan Hz

fc = 1/(3600*6)  # Frekuensi cut-off = 6 jam, satuan 1/s atau Hz
w = fc / (fs / 2) # Normalisasi frekuensi

b, a = signal.butter(5, w, 'low') # desain filter untuk 'low pass'
elevasi_filter = signal.filtfilt(b, a, data_1994_Jun['elevasi_m']) # implementasi filter ke data


# ### Menggabungkan data hasil filter ke dataframe raw data

# In[19]:


data_1994_Jun['elevasi filter'] = elevasi_filter # menambahkan data hasil filter, dgn memberinya nama kolom 'filter elevasi'
data_1994_Jun.head()


# In[20]:


# plot raw data vs filter data
data_1994_Jun['elevasi_m'].plot(color='blue', linewidth=2, figsize=(13,5))
data_1994_Jun['elevasi filter'].plot(color='red', linewidth=2, figsize=(13,5))
plt.title('Elevasi Muka Air di Kolinamil\n pada Juni 1994')
plt.xlabel('Waktu', fontsize=14, fontweight='bold')
plt.ylabel('Elevasi [m]', fontsize=14, fontweight='bold')
plt.xticks(np.linspace(0, len(data_1994_Jun), 5), # pembagian jumlah ticks nya
           ['1 Jun', '8 Jun', '15 Jun', '22 Jun', '29 Jun']) # 1 bulan dibagi 4
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['axes.labelweight'] = 'bold'
plt.grid()


# In[4]:


# plot data hasil filter
import plotly.graph_objs as go

fig = go.Figure()

fig.add_trace(go.Scatter(
    y = data_1994_Jun['elevasi_m'],
    x = data_1994_Jun.index,
    line = dict(shape = 'spline'),
    name = 'Elevasi [m]'
))

fig.add_trace(go.Scatter(
    y = data_1994_Jun['elevasi filter'],
    x = data_1994_Jun.index,
    line = dict(shape = 'spline'),
    name = 'Elevasi filter [m]'
))

fig.show()


# In[5]:


# Mencari informasi statistika deskriptif
data_1994_Jun[['elevasi_m','elevasi filter']].describe()


# ### Inspeksi (memeriksa) pola data pada 1 hari di tanggal tertentu

# In[6]:


data_1994_18_Jun = data_1994_Jun[data_1994_Jun['tanggal'] == 18] # memilih elevasi pada tanggal 18

data_1994_18_Jun


# ### Plot raw data vs filter data untuk 1 hari

# In[7]:


# Plot raw data vs filter data untuk 1 hari
# plot raw data vs filter data
data_1994_18_Jun['elevasi_m'].plot(color='blue', linewidth=2, figsize=(13,5))
data_1994_18_Jun['elevasi filter'].plot(color='red', linewidth=2, figsize=(13,5))
plt.title('Elevasi Muka Air di Kolinamil\n pada 18 Juni 1994')
plt.xlabel('Waktu', fontsize=14, fontweight='bold')
plt.ylabel('Elevasi [m]', fontsize=14, fontweight='bold')
#plt.xticks(np.linspace(0, len(data_1994_Jun), 5), # pembagian jumlah ticks nya
#           ['1 Jun', '8 Jun', '15 Jun', '22 Jun', '29 Jun']) # 1 bulan dibagi 4
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['axes.labelweight'] = 'bold'
plt.grid()


# In[8]:


# plot data 1 hari dgn interactive plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    y = data_1994_18_Jun['elevasi_m'],
    x = data_1994_18_Jun.index,
    line = dict(shape = 'spline'),
    name = 'Elevasi [m]'
))

fig.add_trace(go.Scatter(
    y = data_1994_18_Jun['elevasi filter'],
    x = data_1994_18_Jun.index,
    line = dict(shape = 'spline'),
    name = 'Elevasi filter [m]'
))

fig.show()


# In[26]:


# Mencari informasi statistika deskriptif
data_1994_18_Jun[['elevasi_m','elevasi filter']].describe()


# ## Persiapan Data untuk Metode Admiralty
# 

# In[27]:


#from IPython.display import Image, display
#display(Image('/content/ilustrasi_tabel.jpg', width="500"))


# In[28]:


data_29hari = data_1994_Jun[['tanggal','jam','elevasi filter']].reset_index() 
data_29hari = data_29hari[data_29hari['tanggal'] <= 29] # mem-filter hanya sampai 29 hari saja
data_29hari = data_29hari.drop('tanggal_lengkap', axis=1) # menghilangkan kolom yg tidak diperlukan

data_29hari


# In[29]:


data_admiralty_29hari = data_29hari.pivot_table(index='tanggal', columns='jam', values='elevasi filter')

data_admiralty_29hari


# ### Menyimpan file data input admiralty 29 hari ke excel

# In[30]:


data_admiralty_29hari.to_excel('/content/ADMIRALTY_12918030_rawdata.xlsx') 


# In[31]:


data_admiralty_29hari.to_excel('/content/ADMIRALTY_12918030.xlsx') 


# In[33]:


# menggabungkan data
data_1994_Jun['elevasi filter 12 jam'] = (elevasi_filter_12)
data_1994_Jun['elevasi filter 24 jam'] = (elevasi_filter_24)

data_1994_Jun.head()

