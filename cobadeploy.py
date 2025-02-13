import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from Sensitivity import run_sensitivity
from Fuzzy import run_fuzzy
from streamlit_extras.stylable_container import stylable_container

# Set Page ------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="App FullThesis")

# Background Web ------------------------------------------------------------------------------------------------------------
st.markdown("""
    <style>
    body, .stApp {
        background-color: #F6F6F6;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HIDDEN AUTO DARI STREAMLIT ------------------------------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Sembunyikan header default Streamlit */
    header {
        visibility: hidden;
    }
    /* Sembunyikan footer default Streamlit */
    footer {
        visibility: hidden;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# HEADER --------------------------------------------------------------------------------------------------------------------
with stylable_container(
    key="header",
    css_styles=["""
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 80px;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: white; /* Warna latar header */
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Bayangan header */
            z-index: 9999; /* Agar header berada di atas elemen lain */
            font-size: 30px;
            font-weight: bold;
        }
        """        
        ]
    ):
        st.markdown("""
            <div class='fixed-header'>
                SIMULASI MODEL PERTUMBUHAN TUMOR GOMPERTZIAN
            </div>
        """, unsafe_allow_html=True)


# HELP PAGE -----------------------------------------------------------------------------
def show_help_page():
    
    with stylable_container(
        key="help_button",
        css_styles=["""
        .help-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        """,
        """
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        """,  
        """
        p {
            text-align: justify;
        }
        """, 
        """
        ul {
            margin-left: 20px;
        }
        """, 
        """
        .stButton{
            display:flex;
            flex-direction: row;
            justify-content: center;
            margin-top: 30px;
        }
        """, 
        """
        .st-key-help_button button{
            background-color: white; 
            color: #CACACC;
            border: 2px solid #CACACC;
            width: 100px;
            height: 40px;
            border-radius: 30px;
            cursor: pointer;
            z-index: 1000;
            transition: background-color 0.3s, color 0.3s;
        }
        """, 
        """
        .st-key-help_button:hover Button{
            background-color: #CACACC; 
            color: white;
            border: 2px solid #CACACC;
        }
        """, 
        ]
    ):
    
        st.markdown("""
            <h2>PETUNJUK PENGGUNAAN APLIKASI</h2>
            <div class="help-container">
                <p>Berikut adalah langkah-langkah untuk menggunakan aplikasi ini:</p>
                <ol>
                    <li><strong>Pilih Jenis Simulasi</strong> 
                        <p>Pada halaman awal, pilih jenis simulasi yang ingin Anda jalankan (Sensitivity atau Fuzzy).<p>
                    </li>
                    <li><strong>Masukkan Parameter Input:</strong> 
                        <p>Setelah memilih jenis simulasi, Anda akan diminta untuk mengisi parameter yang diperlukan.</p>
                    </li>
                    <li><strong>Jalankan Simulasi:</strong> 
                        <p>Klik tombol "Simulasi" untuk memulai proses simulasi. Pastikan semua parameter telah terisi dengan benar.</p>
                    </li>
                    <li><strong>Lihat Hasil:</strong> 
                        <p>Hasil simulasi akan ditampilkan dalam bentuk grafik dan tabel. Anda juga dapat mengunduh data hasil simulasi dalam format CSV.</p>
                    </li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Back", key="help_button"):
            st.session_state['current_page'] = 'choose_simulation' 

# HELP BUTTON -----------------------------------------------------------------------------
def show_help_button():

    with stylable_container(
        key="help_button",
        css_styles=["""
        .st-key-help_button button{
            background-color: white; 
            color: #FF7575;
            border: 2px solid #FF7575;
            width: 40px;
            height: 40px;
            position: fixed;
            top: 110px;
            right: 50px; 
            border-radius: 50%;
            cursor: pointer;
            z-index: 1000;
            transition: background-color 0.3s, color 0.3s;
        }
        """,
        """
        .st-key-help_button:hover Button{
            background-color: #FF7575; 
            color: white;
            border: 2px solid #FF7575;
        }
        """  
        ]
    ):

        if st.button("?", key="help_button"):
            st.session_state['previous_page'] = st.session_state['current_page']
            st.session_state['current_page'] = 'help'

# HALAMAN 1: PILIH SIMULASI --------------------------------------------------
def show_choose_simulation_page():
    
    show_help_button()

    col1, col2, col3 = st.columns([1, 2, 1]) 
    
    with col2:
        with stylable_container(
            key="my_form",
            css_styles=["""
            {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: white;
                border: 2px solid #D9DDDC;
                border-radius: 20px;
                padding: 2em;
                width: 20%;
                margin: 0 auto;
                text-align: center;
            }
            """,
            """
            div[data-testid="stForm"] {
                border: none !important;
                box-shadow: none !important;
            }
            """,
            """
            .big-font {
                font-size: 20px;
                font-weight: bold;
            }
            """        
            ]
        ):
            with st.form(key="my_form"):
                st.markdown('<p class="big-font">PILIH JENIS SIMULASI</p>', unsafe_allow_html=True)
            
                simulation_type = st.selectbox(
                    "", 
                    options=["Sensitivity", "Fuzzy"],
                    index=0,
                    key="simulation_select",
                    label_visibility="collapsed"
                )
            
                # Center the "Pilih" button
                if st.form_submit_button("Pilih"):
                    if simulation_type == "Sensitivity" or "Fuzzy":
                        st.session_state['simulation_type'] = simulation_type.lower()
                        st.session_state['current_page'] = 'input'
                    else:
                        st.error("Silakan pilih jenis simulasi terlebih dahulu")


# HALAMAN 2: INPUTAN ---------------------------------------------------------
def show_input_page():

    show_help_button()
    
    # SENSITIVITY ------------------------------------------------------------
    if st.session_state['simulation_type'] in ['fuzzy', 'sensitivity']:
        col1, col2, col3 = st.columns([1, 2, 1]) 
        with col2: 
            with stylable_container(
                key="input_styles",
                css_styles=["""
                    {
                        background-color: white;
                        border: 2px solid #D9DDDC;
                        border-radius: 10px;
                    }
                    """,
                    """
                    div[data-testid="stForm"] {
                            border: none !important;
                            box-shadow: none !important;
                    }
                    """,
                    """
                    .help-and-colon {
                        display: flex;
                        align-items: center;
                        gap: 5px;
                        justify-content: flex-end;
                    }
                    .help-icon {
                        font-size: 14px;
                        color: #007bff;
                        cursor: help;
                    }
                    .custom-colon {
                        font-weight: bold;
                        margin-left: 5px;
                    }
                    .unit-label {
                        font-size: 14px;
                        color: #6c757d;
                        margin-top: 10px;
                    }
                    .stTextInput > div > input {
                        border: 2px solid #A9A9A9;
                        border-radius: 8px;
                        padding: 8px;
                        width: 100%;
                    }
                    .stNumberInput > div > input {
                        border: 2px solid #A9A9A9;
                        border-radius: 8px;
                        padding: 8px;
                        width: 100%;
                    }
                    .stButton > button {
                        border: solid 3px #A9A9A9;
                        border-radius: 50px;
                        color: #A9A9A9;
                        background-color: white;
                        width: 120px;
                        position: fixed;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        margin: 20px auto;
                        padding: 10px;
                        font-weight: bold;
                    }
                    .stButton > button:hover {
                        background-color: #A9A9A9;
                        color: white;
                        border: solid 1px #A9A9A9;
                    }
                    """
                ]
            ):
                
                with st.form("simulation_form"):
                    def create_input_name(label, help_text, unit_label, key):
                        col1, col2, col3, col4 = st.columns([2, 1, 2, 1]) 
                        with col1:
                            st.text("")
                            st.text("")
                            st.markdown(f"**Nama**")
                        with col2:
                            st.text("")
                            st.text("")
                            st.markdown(
                                f'<div class="help-and-colon">'
                                f'<span class="help-icon">'
                                f'<div title="{help_text}" style="cursor: help; color: gray;">ℹ️</div>' 
                                f'</span>'
                                f'<span class="custom-colon">:</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                        with col3:
                            value = st.text_input("", placeholder="Masukkan nama Anda", key="Nama")
                            # html:
                            # <div class="stTextInput">
                            #     <div>
                            #         <input type="text" placeholder="Masukkan nama Anda">
                            #     </div>
                            # </div>
                        with col4:
                            st.text("")
                        return value
        
                    nama = create_input_name("Nama", "Masukkan nama Anda", "", "nama")
                
                    def create_input_row(label, help_text, unit_label, key):
                        col1, col2, col3, col4 = st.columns([2, 1, 2, 1]) 
                        with col1:
                            st.text("")
                            st.text("")
                            st.markdown(f"**{label}**")
                        with col2:
                            st.text("")
                            st.text("")
                            st.markdown(
                                f'<div class="help-and-colon">'
                                f'<span class="help-icon">'
                                f'<div title="{help_text}" style="cursor: help; color: gray;">ℹ️</div>' 
                                f'</span>'
                                f'<span class="custom-colon">:</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                        with col3:
                            value = st.number_input("", format="%.4f", step=0.0001, key=key)
                            
                        with col4:
                            st.text("")
                            st.text("")
                            st.markdown(f'<p class="unit-label">{unit_label}</p>', unsafe_allow_html=True)
                        return value
    
                    if st.session_state['simulation_type'] in ['fuzzy', 'sensitivity']:
                        if st.session_state['simulation_type'] in ['fuzzy', 'sensitivity']:
                            # Input buat sensitivity dan fuzzy
                            x = create_input_row("Populasi dari sel bukan kanker (X0)", "Masukkan populasi sel bukan kanker", "number/mL", "x0")
                            y = create_input_row("Populasi dari sel kanker (Y0)", "Masukkan populasi sel kanker", "number/mL", "y0")
                            t_awal = create_input_row("Time (t_awal)", "Masukkan waktu simulasi", "day", "t_awal")
                            t_akhir = create_input_row("Time (t_akhir)", "Masukkan waktu simulasi", "day", "t_akhir")
                            h = create_input_row("Jarak waktu (h)", "Masukkan jarak waktu yang diinginkan", "day", "h")

                            if st.session_state['simulation_type'] == 'sensitivity':
                                # Inputan sensitivity
                                u = create_input_row("Rate pertumbuhan dari sel bukan kanker (u)", "Masukkan rate pertumbuhan sel bukan kanker", "/day", "u")
                                m = create_input_row("Rate pertumbuhan dari sel kanker (m)", "Masukkan rate pertumbuhan sel kanker", "/day", "m")
                                alpha = create_input_row("Rate kematian sel kanker akibat pengobatan (alpha)", "Masukkan rate kematian sel kanker", "/day", "alpha")
                                beta = create_input_row("Rate kematian sel tidak kanker dan tergantikan dengan sel kanker (beta)", "Masukkan rate kematian sel tidak kanker", "number.mL/day", "beta")
                                delta = create_input_row("Rate kematian sel tidak kanker akibat imun (delta)", "Masukkan rate kematian sel tidak kanker akibat imun", "/day", "delta")
                                k = create_input_row("Jumlah maksimum yang memungkinkan dari keseluruhan sel tumor (k)", "Masukkan jumlah maksimum sel tumor", "number.mL/day", "k")
                        
                                params = {
                                    "x": x, "y": y, "t_awal": t_awal, "t_akhir": t_akhir, "h": h,
                                    "u": u, "m": m, "alpha": alpha, "beta": beta, 
                                    "delta": delta, "k": k
                                }
                            
                            elif st.session_state['simulation_type'] == 'fuzzy':
                                # Inputan fuzzy
                                u = create_input_row("Rate pertumbuhan dari sel bukan kanker (u)", "Masukkan rate pertumbuhan sel bukan kanker", "/day", "u")
                                m = create_input_row("Rate pertumbuhan dari sel kanker (m)", "Masukkan rate pertumbuhan sel kanker", "/day", "m")
                                ohm = create_input_row("Banyaknya pengobatan yang diberikan (ohm)", "Masukkan banyaknya pengobatan yang diberikan", "/day", "ohm")
                                ohm_min = create_input_row("Minimum pengobatan (ohm_min)", "Masukkan batas minimum pengobatan", "/day", "ohm_min")
                                ohm_0 = create_input_row("Efektif pengobatan (ohm_0)", "Masukkan batas pengobatan yang efektif", "/day", "ohm_0")
                                ohm_max = create_input_row("Maximum pengobatan (ohm_max)", "Masukkan batas maksimum pengobatan", "/day", "ohm_max")
                                alpha_min = create_input_row("Minimum kematian sel kanker akibat pengobatan (alpha_min)", "Masukkan batas minimum kematian sel kanker", "/day", "alpha_min")
                                beta = create_input_row("Rate kematian sel tidak kanker dan tergantikan dengan sel kanker (beta)", "Masukkan rate kematian sel tidak kanker", "number.mL/day", "beta")
                                delta = create_input_row("Rate kematian sel tidak kanker akibat imun (delta)", "Masukkan rate kematian sel tidak kanker akibat imun", "/day", "delta")
                                k = create_input_row("Jumlah maksimum yang memungkinkan dari keseluruhan sel tumor (k)", "Masukkan jumlah maksimum sel tumor", "number.mL/day", "k")
                        
                                params = {
                                    "x": x, "y": y, "t_awal": t_awal, "t_akhir": t_akhir, "h": h,
                                    "u": u, "m": m, "ohm": ohm, "ohm_min": ohm_min, "ohm_0": ohm_0, 
                                    "ohm_max": ohm_max, "alpha_min": alpha_min, "beta": beta, 
                                    "delta": delta, "k": k
                                }
                    
                            # Simulasi button
                            col1, col2, col3 = st.columns([2, 1, 3])  # Adjust button layout
                            with col3:
                                submit = st.form_submit_button("Simulasi")


                            
                            if submit:
                                # Validasi ketika klik "Simulasi"
                                valid = True
                                invalid_inputs = []

                                # validasi buat sensitivity sama fuzzy
                                if h == 0:
                                    invalid_inputs.append("h tidak boleh 0")
                                if t_akhir == 0:
                                    invalid_inputs.append("t_akhir tidak boleh 0")
                                if k == 0:
                                    invalid_inputs.append("k tidak boleh 0")
                        
                        
                                # validasi buat fuzzy
                                if st.session_state['simulation_type'] == 'fuzzy':
                                    if ohm_min > ohm_0:
                                        invalid_inputs.append("Pastikan nilai: ohm_min <= ohm_0")
                                    if ohm_0 > ohm_max:
                                        invalid_inputs.append("Pastikan nilai: ohm_0 <= ohm_max")
                        
                                # error kalau invalid
                                if invalid_inputs:
                                    valid = False
                                    for error in invalid_inputs:
                                        st.error(error)
                        
                                if valid:
                                    try:
                                        if st.session_state['simulation_type'] == 'fuzzy':
                                            time_values, x_values, y_values = run_fuzzy(**params)
                                            st.session_state['fuzzy_results'] = (time_values, x_values, y_values)
                                        elif st.session_state['simulation_type'] == 'sensitivity':
                                            time_values, results = run_sensitivity(**params)
                                            st.session_state['simulation_results'] = (time_values, results)
                                            st.session_state['simulation_params'] = params
                                        st.session_state['current_page'] = 'output'
                                    except Exception as e:
                                        st.error(f"Error during simulation: {str(e)}")


# OUTPUT --------------------------------------------------------------------
def output_left():
    st.subheader("Hasil Input")
    st.write("Berikut adalah parameter yang Anda masukkan:")
    
    # Parameter yang perlu ditampilkan
    param_keys = [
        "x0", "y0",                  # initial conditions
        "t_awal", "t_akhir", "h",    # time parameters
        "u", "m",                    # rate parameters
        "ohm", "ohm_min", "ohm_0", "ohm_max",  # omega parameters
        "alpha_min", "alpha",        # alpha parameters
        "beta", "delta", "k"         # other parameters
    ]
    
    unit_labels = {
        "x0": "number/mL",
        "y0": "number/mL",
        "t_awal": "day",
        "t_akhir": "day",
        "h": "day",
        "u": "/day",
        "m": "/day",
        "ohm": "/day",
        "ohm_min": "/day",
        "ohm_0": "/day",
        "ohm_max": "/day",
        "alpha_min": "/day",
        "alpha": "/day",
        "beta": "number.mL/day",
        "delta": "/day",
        "k": "number.mL/day"
    }
    
    # Cek apakah ada parameter yang tersedia
    available_params = [key for key in param_keys if key in st.session_state]
    
    if available_params:
        for key in available_params:
            value = st.session_state[key]
            unit_label = unit_labels.get(key, "")
            
            col_left, col_middle, col_value, col_unit = st.columns([2, 0.2, 1, 2])
            with col_left:
                st.write(f"**{key}**")
            with col_middle:
                st.write(":")
            with col_value:
                st.write(f"{value}")
            with col_unit:
                st.write(f"{unit_label}")
    else:
        st.write("Tidak ada data input yang tersedia.")
def output_sensitivity():
    if 'simulation_results' in st.session_state:
        time_values, results = st.session_state['simulation_results']
            
        labels = [
            "x_u", "x_m", "x_delta", "x_beta", "x_alpha",
            "y_u", "y_m", "y_delta", "y_beta", "y_alpha"
        ]
        colors = ['blue', 'green', 'red', 'purple', 'orange'] * 2
        st.subheader("Hasil Simulasi Sensitivitas")
    
        # Grafik Sel Bukan Kanker
        fig1 = go.Figure()
        for j in range(5):
            fig1.add_trace(go.Scatter(
                x=time_values,
                y=results[:, 0, j],
                mode='lines',
                name=labels[j],
                line=dict(color=colors[j])
            ))
        fig1.update_layout(
            title="Sel Bukan Kanker",
            xaxis_title="Waktu (days)",
            yaxis_title="Banyaknya sel",
        )
        st.plotly_chart(fig1)
    
        # Grafik Sel Kanker
        fig2 = go.Figure()
        for j in range(5):
            fig2.add_trace(go.Scatter(
                x=time_values,
                y=results[:, 1, j],
                mode='lines',
                name=labels[j+5],
                line=dict(color=colors[j+5])
            ))
        fig2.update_layout(
            title="Sel Kanker",
            xaxis_title="Waktu (days)",
            yaxis_title="Banyaknya sel",
        )
        st.plotly_chart(fig2)
    
        # Tabel Sensitivity
        display_results_table(time_values, results, labels)

def output_fuzzy():
    if 'fuzzy_results' in st.session_state and st.session_state['fuzzy_results'] is not None:
        fuzzy_time, fuzzy_x, fuzzy_y = st.session_state['fuzzy_results']
            
        st.subheader("Hasil Simulasi Fuzzy")
            
        # Grafik Fuzzy
        fig_fuzzy = go.Figure()
        fig_fuzzy.add_trace(go.Scatter(
            x=fuzzy_time, 
            y=fuzzy_x, 
            mode='lines', 
            name='Non-cancer Cells (x)', 
            line=dict(color='blue')
        ))
        fig_fuzzy.add_trace(go.Scatter(
            x=fuzzy_time, 
            y=fuzzy_y, 
            mode='lines', 
            name='Cancer Cells (y)', 
            line=dict(color='red')
        ))
        fig_fuzzy.update_layout(
            xaxis_title="Time (days)",
            yaxis_title="Cell Population",
        )
        st.plotly_chart(fig_fuzzy)
            
        # Tabel Fuzzy
        display_fuzzy_table(fuzzy_time, fuzzy_x, fuzzy_y)

def display_results_table(time_values, results, labels):
    st.subheader("Tabel Nilai Hasil Simulasi Sensitivitas")
    data = {"Time": np.around(time_values, 1)}
    for i, label in enumerate(labels[:5]):
        data[label] = results[:, 0, i]
    for i, label in enumerate(labels[5:]):
        data[label] = results[:, 1, i]
    
    display_table(pd.DataFrame(data))

def display_fuzzy_table(time, x, y):
    st.subheader("Tabel Nilai Hasil Simulasi Fuzzy")
    data = {
        "Time": np.around(time, 1),
        "Non-cancer Cells (x)": x,
        "Cancer Cells (y)": y
    }
    display_table(pd.DataFrame(data))

def display_table(df):
    # Reset index untuk memulai dari 1
    df.index = df.index + 1
    
    # Tentukan jumlah baris per halaman
    rows_per_page = 10
    total_rows = len(df)
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page
            
    # Layout untuk kontrol halaman dan tombol unduh CSV
    col_page, col_download = st.columns([3, 1])
            
    with col_page:
        page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1, step=1)
            
    with col_download:
        csv = df.to_csv(index=False).encode('utf-8')
        if st.download_button(
            label="CSV",
            data=csv,
            mime="text/csv"
        ):
            st.success("Data berhasil diunduh!")
                        
    start_idx = (page - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)
            
    current_page_data = df.iloc[start_idx:end_idx]
    st.dataframe(current_page_data, use_container_width=True)
            
    st.write(f"Menampilkan baris {start_idx + 1} hingga {end_idx} dari total {total_rows} baris.")

def show_output_page():
    col1, col2 = st.columns([0.6, 2])

    with col1:
        output_left()

    with col2:
        output_sensitivity()
        output_fuzzy()

# RNAVIGASI HALAMAN =========================================================================================================
def main():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'choose_simulation'
    
    if st.session_state['current_page'] == 'choose_simulation':
        show_choose_simulation_page()
    elif st.session_state['current_page'] == 'input':
        show_input_page()
    elif st.session_state['current_page'] == 'output':
        show_output_page()
    elif st.session_state['current_page'] == 'help':
        show_help_page()

main()
