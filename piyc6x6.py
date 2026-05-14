import streamlit as st
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="PIYC Elite 6x6", layout="centered")

# 1. Oyun Hafızası
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.winner = None

# 2. Mantık Fonksiyonları
def check_move(board, row, col, val):
    if val in board[row, :] or val in board[:, col]:
        return False
    return True

def can_move_anywhere(board):
    for r in range(6):
        for c in range(6):
            if board[r, c] == 0:
                for v in range(1, 7):
                    if check_move(board, r, c, v):
                        return True
    return False

# 3. Başlık
st.title("🔢 PIYC: 6x6 Elite")

# Durum Bilgisi
if not st.session_state.game_over:
    st.info(f"Sıradaki: **Oyuncu {st.session_state.turn}**")
else:
    st.success(f"🏆 Kazanan: **Oyuncu {st.session_state.winner}**")

# 4. Rakam Seçimi (Mobilde en güvenli seçim kutusu)
selected_num = st.radio("Bir rakam seçin ve kutuya dokunun:", [1, 2, 3, 4, 5, 6], horizontal=True)

# 5. IZGARA (HTML/CSS Kullanarak)
# Streamlit butonları yerine kendi ızgaramızı oluşturuyoruz
st.write("---")

# 6x6'lık tabloyu oluşturmak için Streamlit'in kendi içindeki padding'leri daraltalım
st.markdown("""
<style>
    .stButton > button {
        width: 100% !important;
        height: 50px !important;
        padding: 0 !important;
        font-size: 18px !important;
    }
    /* Mobilde sütunları yan yana tutmak için en güçlü CSS */
    div[data-testid="column"] {
        width: 15% !important;
        flex: 1 1 15% !important;
        min-width: 45px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }
</style>
""", unsafe_allow_html=True)

# Tahtayı Çiz
for r in range(6):
    cols = st.columns(6)
    for c in range(6):
        with cols[c]:
            val = st.session_state.board[r, c]
            label = str(int(val)) if val != 0 else " "
            
            # Butona basıldığında yapılacaklar
            if st.button(label, key=f"btn_{r}_{c}", disabled=st.session_state.game_over):
                if val == 0:
                    if check_move(st.session_state.board, r, c, selected_num):
                        st.session_state.board[r, c] = selected_num
                        next_player = 2 if st.session_state.turn == 1 else 1
                        
                        if not can_move_anywhere(st.session_state.board):
                            st.session_state.game_over = True
                            st.session_state.winner = st.session_state.turn
                        else:
                            st.session_state.turn = next_player
                        st.rerun()
                    else:
                        st.toast(f"Çakışma: {selected_num}", icon="❌")

# 6. Kontroller
st.write("---")
if st.button("🔄 Yeni Oyun Başlat"):
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.rerun()
