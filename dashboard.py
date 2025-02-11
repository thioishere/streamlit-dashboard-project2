#import library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
# Menonaktifkan semua warning
import warnings # Import the warnings module
warnings.filterwarnings("ignore")
import streamlit as st


# Menu sidebar

# HEADER WEB - HARUS PALING AWAL
st.set_page_config(
    page_title='Dashboard Prediksi Harga Komoditas Sembako',
    page_icon="🍽",
    layout='wide'
)

# Sidebar dengan pengantar dan menu utama

menu_utama = st.sidebar.selectbox("Menu Utama", ["Beranda", "Menu Lanjutan"])

if menu_utama == "Menu Lanjutan":
    menu = st.sidebar.selectbox("Pilih Menu", ["Panduan", "Dashboard Forecast"])

    if menu == "Panduan":
        st.write("### Panduan Penggunaan Aplikasi 📘")
        st.write("Berikut adalah panduan lengkap untuk membantu Anda menggunakan aplikasi ini...")
        st.markdown("""
        1. Pilih menu **Dashboard Forecast** untuk melakukan analisis, pada dashboard pengguna akan diberi pilihan 
           untuk memilih komoditas sembako yang ingin diprediksi. Komoditas yang dipilih akan di*input* oleh pengguna berdasarkan angka yang merepresentasikan komodtas sembako.
           Berikut merupakan keterangan dari setiap angka yang merepresentasikan komoditas sembako:
           - **1**: Beras Premium  
           - **2**: Kedelai Biji Kering (*Impor*)  
           - **3**: Cabai Merah Keriting  
           - **4**: Bawang Merah  
           - **5**: Gula Konsumsi  
           - **6**: Minyak Goreng Kemasan Sederhana  
           - **7**: Daging Sapi Murni  
           - **8**: Daging Ayam Ras  
           - **9**: Telur Ayam Ras 
        2. Dibawah tabel **Masukkan Komoditas**, akan ada *warning* dan *error* dengan pernyataan 
           *"NameError: This app has encountered an error."*. Pernyataan *error* tersebut dapat diabaikan karena pengguna belum memasukkan
           komoditas yang ingin dipilih. Masukkanlah **komoditas** yang diinginkan lalu *enter*.
        3. Dashboard akan menampilkan data terkini/terakhir dari komoditas disusul dengan grafik 
           harga komoditas tahun 2022-2024. Dashboard juga akan menampilkan visualisasi peramalan  harga komoditas 
           menggunakan model terbaik diantara ***Additive*** dan ***Multiplicative*** serta hasil evaluasi dari model.
        4. Selanjutnya terdapat *section* **Simulasi Daya Beli Masyarakat**. *Section* ini bertujuan untuk menghitung 
           daya beli masyarakat berdasarkan perubahan harga di tahun prediksi terhadap tahun sebelumnya pada bulan yang diinginkan.
           Masukkan secara manual bulan yang ingin dipilih dengan format (YYYY-MM-DD). Untuk tanggal (DD) selalu masukkan tanggal **01**,
           karena perhitungan fokus di bulan saja bukan di per hari. Untuk tahun (YYYY) selalu masukkan **2025**, karena kita melihat perubahan harga dari 2025 terhadap 2024.
           Selanjutnya masukkan pendapatan masyarakat secara manual dan dianjuran kepada pengguna untuk memasukkan pendapatan yang dialokasikan untuk membayar kebutuhan konsumsi. 
           Jangan lupa untuk menekan *enter* setelah memasukkan setiap nilai yang diinginkan. 
        5. Informasi daya beli masyarakat akan ditampilkan setelah pengguna menekan tombol **Hitung Inflasi dan Daya Beli**.          
        """)

    elif menu == "Dashboard Forecast":
        # HEADER WEB
        #st.title('Dashboard Prediksi Harga Komoditas Sembako', page_icon= ":fork and knife with plate:", layout='wide')

        # Custom title with centered text
        st.markdown(
            """
            <h1 style='text-align: center;'>
            Forecast Harga Komoditas Sembako 🥬🥩
            </h1>
            """,
            unsafe_allow_html=True
        )   

        # Tambahkan spasi dengan elemen kosong
        st.write("\n" * 5)  # Menambahkan tiga baris kosong

        data = pd.read_excel('Harga Sembako 2022-2024.xlsx')

        # Menampilkan data
        with st.container():
                st.markdown("<h2 style='margin-top: 50px;'>Data Harga Sembako 2022-2024</h2>", unsafe_allow_html=True)
                st.write("---")
                st.dataframe(data)  # Menampilkan DataFrame di Streamlit


        # Ubah kolom 'Bulan' menjadi datetime dan set sebagai index
        data['Bulan'] = pd.to_datetime(data['Bulan'], format='%Y-%m')

        # Set kolom 'Bulan' sebagai index
        data.set_index('Bulan', inplace=True)

        #pemilihan komoditas yang akan diprediksi
        komoditas_dict = {
            "1": "Beras Premium",
            "2": "Kedelai Biji Kering (Impor)",
            "3": "Cabai Merah Keriting",
            "4": "Bawang Merah",
            "5": "Gula Konsumsi",
            "6": "Minyak Goreng Kemasan Sederhana",
            "7": "Daging Sapi Murni",
            "8": "Daging Ayam Ras",
            "9": "Telur Ayam Ras"
        }
        df_kom = pd.DataFrame(list(komoditas_dict.items()), columns=['No', 'Komoditas'])

        # Set kolom 'Bulan' sebagai index
        df_kom.set_index('No', inplace=True)

        # Input komoditas menggunakan Streamlit
        komoditas = st.text_input("Masukkan Komoditas (pilih diantara 1-9)")

        import pandas as pd

        if komoditas: 
            try:
                komoditas_d = komoditas_dict[komoditas]
                kom = data[komoditas_d]
                # Buat DataFrame untuk tabel
                data_tabel = pd.DataFrame({
                    "Komoditas": [komoditas_d],
                    "Data Terakhir": [f"Rp{kom.iloc[-1]:,.2f}"],
                    "Tanggal": [kom.index.strftime('%Y-%m-%d')[-1]]
                })
                st.table(data_tabel)
            except KeyError:
                st.error(f"Column '{komoditas}' not found in df.")


        plt.figure(figsize=(10, 6))
        plt.plot(kom.index, kom.values)
        plt.title(f'Harga {komoditas_d} dari Januari 2022 - Desember 2024')
        plt.xlabel('Bulan')
        plt.ylabel('Harga')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()

        # Tampilkan plot di Streamlit
        st.pyplot(plt)


        train = kom[:-12]  # Data train untuk 2022-2023
        test = kom[-12:]  # Data test untuk 2024

        # Display the train data as a DataFrame
        print("Data Train:")
        #display(train.head())

        # Display the train data as a DataFrame
        print("Data Test:")
        #display(test.head())

        #mendefinisikan model
        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        model_additive = ExponentialSmoothing(train,
                                            trend='add',
                                            seasonal='add',
                                            seasonal_periods=12)

        # Fitting model aditif
        fit_additive = model_additive.fit()

        model_multiplicative = ExponentialSmoothing(train,
                                            trend='mul',
                                            seasonal='mul',
                                            seasonal_periods=12)

        # Fitting model aditif
        fit_multiplicative = model_multiplicative.fit()


        #memprediksi data test menggunakan model additive
        predictions_additive = {}

        # Forecast untuk data test (sesuaikan panjangnya dengan data test)
        forecast_additive = fit_additive.forecast(len(test))  # Prediksi untuk panjang data test

        # Simpan hasil prediksi dengan nama kolom yang relevan
        # Gunakan string sebagai key, misalnya nama komoditas
        predictions_additive[komoditas_d] = forecast_additive

        # Convert hasil prediksi menjadi DataFrame
        predictions_additive_df = pd.DataFrame(predictions_additive, index=test.index)

        # Fungsi untuk plot dalam Streamlit
        def plot_forecasts(forecasts: list[float], title: str):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train.index, y=train.values, name='Train'))
            fig.add_trace(go.Scatter(x=test.index, y=test.values, name='Test'))
            fig.add_trace(go.Scatter(x=test.index, y=forecasts, name='Forecast'))
            fig.update_layout(template="simple_white", font=dict(size=18), title_text=title,
                            width=900, title_x=0.5, height=600, xaxis_title='Date',
                            yaxis_title='Harga')
            return fig

        # Plot dan tampilkan di Streamlit
        fig = plot_forecasts(predictions_additive_df[komoditas_d].values, 'Holt-Winters Additive')


        #memprediksi data test menggunakan model multiplicative
        predictions_multiplicative = {}

        # Forecast untuk data test (sesuaikan panjangnya dengan data test)
        forecast_multiplicative = fit_multiplicative.forecast(len(test))  # Prediksi untuk panjang data test

        # Simpan hasil prediksi dengan nama kolom yang relevan
        # Gunakan string sebagai key, misalnya nama komoditas
        predictions_multiplicative[komoditas_d] = forecast_multiplicative

        # Convert hasil prediksi menjadi DataFrame
        predictions_multiplicative_df = pd.DataFrame(predictions_multiplicative, index=test.index)



        # Fungsi untuk plot dalam Streamlit
        def plot_forecasts(forecasts: list[float], title: str):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train.index, y=train.values, name='Train'))
            fig.add_trace(go.Scatter(x=test.index, y=test.values, name='Test'))
            fig.add_trace(go.Scatter(x=test.index, y=forecasts, name='Forecast'))
            fig.update_layout(template="simple_white", font=dict(size=18), title_text=title,
                            width=900, title_x=0.5, height=600, xaxis_title='Date',
                            yaxis_title='Komoditas')
            return fig

        # Plot dan tampilkan di Streamlit
        fig = plot_forecasts(predictions_multiplicative_df[komoditas_d].values, 'Holt-Winters Multiplicative')



        import pandas as pd
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        import math
        import numpy as np

        # Kalkulasi MAE, MSE, and RMSE for additive model
        mae_additive = mean_absolute_error(test, predictions_additive_df[komoditas_d])
        mse_additive = mean_squared_error(test, predictions_additive_df[komoditas_d])
        rmse_additive = math.sqrt(mse_additive)
        mape_additive = np.mean(np.abs((test - predictions_additive_df[komoditas_d]) / test)) * 100

        # Kalkulasi MAE, MSE, and RMSE for multiplicative model
        mae_multiplicative = mean_absolute_error(test, predictions_multiplicative_df[komoditas_d])
        mse_multiplicative = mean_squared_error(test, predictions_multiplicative_df[komoditas_d])
        rmse_multiplicative = math.sqrt(mse_multiplicative)
        mape_multiplicative = np.mean(np.abs((test - predictions_multiplicative_df[komoditas_d]) / test)) * 100

        # Membuat DataFrame
        data = {'Model': ['Additive', 'Multiplicative'],
                'MAE': [mae_additive, mae_multiplicative],
                'MSE': [mse_additive, mse_multiplicative],
                'RMSE': [rmse_additive, rmse_multiplicative],
                'MAPE': [mape_additive, mape_multiplicative]}  # Simpan MAPE sebagai angka
        df_metrics = pd.DataFrame(data)


        # Mencari nilai dengan nilai MAPE terkecil
        min_mape_row = df_metrics.loc[df_metrics['MAPE'].idxmin()]

        if min_mape_row['Model'] == 'Multiplicative':
            seas = 'Multiplicative'
        else:
            seas = 'Additive'




        #Melakukan peramalan (forecast) untuk memprediksi data periode berikutnya
        models = {}
        forecasts_mul = {}

        # Initialize and fit the model (menggunakan model multiplicative)
        model = ExponentialSmoothing(kom, trend=seas, seasonal=seas, seasonal_periods=12).fit()
        forecasts = model.forecast(12)  # Prediksi untuk 12 periode ke depan

        # Store the model and forecasts
        models[komoditas_d] = model  # Store the model
        forecasts_mul[komoditas_d] = forecasts  # Store the forecasts

        # Gabungkan hasil forecast dalam satu dataframe
        forecast_df_mul = pd.DataFrame(forecasts_mul)


        # Plot di Plotly

        #Memplot data asli dan hasil forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=kom.index, y=kom.values, name='Data', line=dict(color='blue')))
        #Memplot data asli dan hasil forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=kom.index, y=kom.values, name='Data', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=forecast_df_mul.index, y=forecast_df_mul[f'{komoditas_d}'], name='Forecast (Future)', line=dict(color='orange')))

        fig.update_layout(template="simple_white", font=dict(size=18), title_text=f'Peramalan Menggunakan Model {min_mape_row["Model"]}',
                        width=900, title_x=0.5, height=600, xaxis_title='Tanggal',
                        yaxis_title=f'{komoditas_d}')



        st.write("")  # Baris kosong sebagai spasi
        with st.container():
            st.markdown("<h2 style='margin-top: 50px;'>Peramalan Harga Komoditas</h2>", unsafe_allow_html=True)
            st.write("---")
        # Tampilkan di Streamlit
        st.plotly_chart(fig)


        st.write("")  # Baris kosong sebagai spasi
        # Tampilkan hasil di Streamlit
        with st.container():
            st.markdown("<h2 style='margin-top: 50px;'>Evaluasi Model</h2>", unsafe_allow_html=True)
            st.write("---")

            # Teks dengan HTML untuk font yang lebih besar
            st.markdown(
                f"<strong>Model dengan MAPE terkecil adalah: {min_mape_row['Model']}</strong>", 
                unsafe_allow_html=True
            )
            
            # Mengatur ukuran font untuk metrik lainnya
            st.markdown(f"<p style='font-size:18px;'>MAPE: {min_mape_row['MAPE']:.2f}%</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px;'>RMSE: {min_mape_row['RMSE']:.2f}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px;'>MSE: {min_mape_row['MSE']:.2f}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px;'>MAE: {min_mape_row['MAE']:.2f}</p>", unsafe_allow_html=True)
            
        st.write("")  # Baris kosong sebagai spasi
        #forecast_df_mul

        #----------------------------------------SIMULASI MODEL--------------------------------------------------

        with st.container():
            st.markdown("<h2 style='margin-top: 50px;'>Simulasi Daya Beli Masyarakat 🛒</h2>", unsafe_allow_html=True)
            st.write("---")

        # Gabungkan data prediksi 2024 dan 2025
        data_gabungan = pd.concat([kom, forecast_df_mul])

        #Memisahkan data 2024 dan 2025
        data_gabungan_2024_2025 = data_gabungan[(data_gabungan.index.year == 2024) | (data_gabungan.index.year == 2025)]

        #Mengubah format indeks
        df = data_gabungan_2024_2025
        df = df.reset_index()
        df = df.rename(columns={'index': 'Bulan'})

        def hitung_inflasi_komoditas(df, komoditas, bulan_input, pendapatan):

            # Pastikan tanggal tersedia dalam index
            index_month = df[df['Bulan'] == bulan_input].index[0]
            index_sebelum = df.loc[index_month - 12, 'Bulan']
            index_sebelum = index_sebelum.strftime('%Y-%m-%d')
            # Accessing using komoditas_dict[komoditas] to get column name
            harga_bulan_ini = df.loc[index_month, komoditas_dict[komoditas]]  
            harga_bulan_sebelumnya = df.loc[index_month - 12, komoditas_dict[komoditas]]

            # Perhitungan inflasi
            inflasi = ((harga_bulan_ini - harga_bulan_sebelumnya) / harga_bulan_sebelumnya) * 100

            daya_beli_sebelum_inflasi = pendapatan / harga_bulan_sebelumnya if harga_bulan_sebelumnya > 0 else 0
            daya_beli_setelah_inflasi = pendapatan / harga_bulan_ini if harga_bulan_ini > 0 else 0

            # Return semua nilai termasuk index_sebelum
            return harga_bulan_sebelumnya, inflasi, harga_bulan_ini, daya_beli_setelah_inflasi, daya_beli_sebelum_inflasi, index_sebelum

        #bulan_input = input("Masukkan bulan yang diinginkan menggunakan format (YYYY-MM-DD): ")
        #pendapatan_input = float(input("\nMasukkan pendapatan masyarakat: "))
        # # bulan_input = pd.to_datetime(bulan_input, format='%Y-%m-%d')

        bulan_input = st.text_input("Masukkan bulan yang diinginkan menggunakan format (YYYY-MM-DD)")

        pendapatan_input = st.number_input("Masukkan pendapatan masyarakat", min_value=0, step=1000)# subsidi_input = float(input("Masukkan subsidi yang diberikan: "))



        if st.button("📋 Hitung Inflasi dan Daya Beli"):     
            try:
                harga_sebelumnya, inflasi, harga_setelah_inflasi, daya_beli_setelah_inflasi, daya_beli_sebelum_inflasi, index_sebelum = hitung_inflasi_komoditas(df, komoditas, bulan_input, pendapatan_input)

        # Menampilkan informasi yang akan ditampilkan
                # Display results
                # st.write(f"\n📊 Analisis untuk Komoditas: {komoditas_d} - Bulan {bulan_input}:")
                st.markdown(
                    f"""
                    <h4 style='text-align: left; font-weight: bold; color: #333; margin-bottom: 5px;'>
                    📊 Analisis untuk Komoditas: {komoditas_d} - Bulan {bulan_input}
                    </h4>
                    <hr style='border: 1px solid #bbb; margin: 5px 0;'>
                    """, 
                    unsafe_allow_html=True
                )
                st.write(f"💸 Harga {komoditas_d} pada tahun sebelumnya ({index_sebelum}): Rp{harga_sebelumnya:,.2f}")
                # Logika inflasi atau deflasi
                if inflasi > 0:
                    perubahan_harga = "setelah inflasi"
                    st.write(f"📈 Terjadi inflasi sebesar: {inflasi:.2f}% dibandingkan tahun sebelumnya sehingga daya beli masyarakat terhadap {komoditas_d} akan turun.")
                elif inflasi < 0:
                    perubahan_harga = "setelah deflasi"
                    st.write(f"📉 Terjadi deflasi sebesar: {(inflasi):.2f}% dibandingkan tahun sebelumnya sehingga daya beli masyarakat terhadap {komoditas_d} akan naik.")
                else:
                    perubahan_harga = "karena tidak ada perubahan harga"
                    st.write("🔄 Tidak ada inflasi maupun deflasi karena harga tetap sama sehingga daya beli masyarakat terhadap {komoditas_d} tetap.")
                st.write(f"💸 Harga {komoditas_d} {perubahan_harga}: Rp{harga_setelah_inflasi:,.2f}")
                st.write(f"🛒 Daya beli masyarakat untuk {komoditas_d} pada saat tahun sebelumnya: {daya_beli_sebelum_inflasi:.2f} unit")
                st.write(f"**🛒 Daya beli masyarakat untuk {komoditas_d} pada saat {bulan_input}: {daya_beli_setelah_inflasi:.2f} unit**")
            except Exception as e:
                print('error:)')
        
else:
    st.write("### Selamat Datang di Aplikasi Dashboard Prediksi Harga Komoditas Sembako 👋")
    st.markdown(
        """
        Pilih **Menu Lanjutan** pada menu utama untuk membaca panduan serta melakukan analisis di dashboard.
        Sebelum memulai analisis, harap membaca **Panduan** terlebih dahulu agar dapat memahami cara menggunakan aplikasi ini dengan maksimal.  
        Setelah itu, silakan menuju ke **Dashboard Forecast** untuk analisis lebih lanjut.
        """
    )

