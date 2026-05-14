import streamlit as st
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(page_title="PIYC Elite 6x6", layout="centered")

# --- GELİŞMİŞ MOBİL VE GENEL IZGARA CSS ---
st.markdown("""
    <style>
    /* Ana konteynır boşluklarını sıfırla */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Sütunların mobilde alt alta geçmesini kesin olarak engelle */
    [data-testid="column"] {
        width: calc(16.66% - 2px) !important;
        flex: 1 1 calc(16.66% - 2px) !important;
        min-width: calc(16.66% - 2px) !important;
        padding: 1px !important;
    }

    /* Sütunlar arası boşluğu (gap) kaldır */
    [data-testid="stHorizontalBlock"] {
        gap: 2px !important;
    }

    /* Buton tasarımı */
    .stButton>button {
        height: 50px !important;
        width: 100% !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        padding: 0px !important;
        background-color: #262730;
    }

    /* Üstteki seçim düğmelerini (pills) ortala */
    div[data-testid="stMarkdownContainer"] > p {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Oyun Hafızası
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.winner = None

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

# 3. Başlık ve Durum
st.title("🔢 PIYC: 6x6 Elite")

if not st.session_state.game_over:
    st.write(f"Sıradaki: **Oyuncu {st.session_state.turn}**")
else:
    st.success(f"🏆 Kazanan: **Oyuncu {st.session_state.winner}**")

# 4. Rakam Seçimi (Mobilde daha az yer kaplar)
selected_num = st.pills("Seç:", [1, 2, 3, 4, 5, 6], selection_mode="single", default=1)

# 5. Oyun Tahtası
for r in range(6):
    cols = st.columns(6)
    for c in range(6):
        with cols[c]:
            val = st.session_state.board[r, c]
            label = str(int(val)) if val != 0 else " "
            
            if st.button(label, key=f"b_{r}_{c}", disabled=st.session_state.game_over):
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

# Alt Kısım Kontrolleri
st.divider()
if st.button("🔄 Yeni Oyun"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
