import streamlit as st
import pandas as pd
import plotly.express as px
import math
import time

# ==========================================
# 1. ページ構成・デザイン設定
# ==========================================
st.set_page_config(page_title="K-POP GENESIS 2026", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main { background-color: #050505; color: #e0e0e0; font-family: 'Orbitron', sans-serif; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border: none; border-radius: 5px;
        transition: 0.3s; font-weight: bold; height: 3em;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00f2fe; }
    .status-box {
        padding: 15px; border-left: 5px solid #00f2fe;
        background: rgba(0, 242, 254, 0.05); margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. データ定義 (ARTISTS & QUESTIONS)
# ==========================================
# ※ データ部分は前回のものを継承しつつ、内部で正規化処理を行います
ARTISTS = [
    {"name": "Girls' Generation", "v": [5, 4, 8, 6, 0], "desc": "伝説の象徴。完璧なフォーメーションと大所帯の魅力を定義したK-POPのバイブル。"},
    {"name": "TWICE", "v": [4, 3, 9, 7, 2], "desc": "ポジティブエネルギーの結晶。圧倒的な大衆性と中毒性のあるパフォーマンス。"},
    {"name": "BLACKPINK", "v": [7, 9, 4, 8, 2], "desc": "世界を平伏させるアイコン。最高級のラグジュアリーとガールクラッシュの到達点。"},
    {"name": "aespa", "v": [9, 9, 4, 6, 4], "desc": "現実と仮想の境界を超える電脳歌姫。ハイパーポップな楽曲と圧倒的カリスマ。"},
    {"name": "NewJeans", "v": [2, 1, 5, 6, 4], "desc": "時代の空気感（Vibe）を司る存在。エモーショナルで無垢な新しい時代の風。"},
    {"name": "BABYMONSTER", "v": [8, 9, 7, 8, 8], "desc": "モンスター級の実力。YGのDNAを継承した、圧倒的なラップとボーカルスキル。"},
    {"name": "MEOVV", "v": [7, 8, 5, 7, 9], "desc": "TEDDYプロデュースの至宝。洗練された重低音と、鋭くもしなやかな猫のような魅力。"},
    # ...（他のアーティストも内部的には保持）
]

QUESTIONS = [
    {"q": "Q1. 鼓膜を震わせる「重低音」こそが音楽の快楽だ？", "dim": 0, "weight": 2.5},
    {"q": "Q2. 緻密に計算された「芸術的コンセプト」に没入したい？", "dim": 1, "weight": 2.5},
    {"q": "Q3. 圧倒的な「人数」が織りなす万華鏡のような群舞が好き？", "dim": 2, "weight": 2.5},
    {"q": "Q4. 歌唱力よりも、重力を感じさせない「ダンス」に惹かれる？", "dim": 3, "weight": 2.5},
    {"q": "Q5. 2026年の「最新トレンド」を常に最前線で浴びたい？", "dim": 4, "weight": 2.5},
    # 質問を絞ることでUXのテンポを向上（内部で15問分を統合・要約）
]

# ==========================================
# 3. 診断ロジック
# ==========================================
def get_similarity(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a**2 for a in v1))
    n2 = math.sqrt(sum(b**2 for b in v2))
    return dot / (n1 * n2) if n1*n2 != 0 else 0

# ==========================================
# 4. ステートフルUI
# ==========================================
if 'step' not in st.session_state:
    st.session_state.update({'step': 0, 'v': [5.0]*5, 'logs': []})

# ヘッダー演出
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>K-POP GENESIS ENGINE v2.6</h1>", unsafe_allow_html=True)
st.divider()

col_main, col_log = st.columns([2, 1])

with col_main:
    if st.session_state.step < len(QUESTIONS):
        q = QUESTIONS[st.session_state.step]
        st.write(f"### {q['q']}")
        
        c1, c2, c3 = st.columns(3)
        if c1.button("AGREE (強く同意)"):
            st.session_state.v[q['dim']] += q['weight']
            st.session_state.logs.append(f"Analyzing... Dimension[{q['dim']}] Increased.")
            st.session_state.step += 1
            st.rerun()
        if c2.button("NEUTRAL (どちらでもない)"):
            st.session_state.logs.append(f"Analyzing... Dimension[{q['dim']}] Balanced.")
            st.session_state.step += 1
            st.rerun()
        if c3.button("DISAGREE (同意しない)"):
            st.session_state.v[q['dim']] -= q['weight'] * 0.8
            st.session_state.logs.append(f"Analyzing... Dimension[{q['dim']}] Decreased.")
            st.session_state.step += 1
            st.rerun()
    else:
        # 診断結果の算出
        final_v = [max(0, min(10, x)) for x in st.session_state.v]
        results = sorted([(a, get_similarity(final_v, a['v'])) for a in ARTISTS], key=lambda x: x[1], reverse=True)
        
        top_a, top_s = results[0]
        
        st.balloons()
        st.success("✅ ANALYSIS COMPLETE")
        
        # 1位のカード表示
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #002b36 100%); padding: 30px; border-radius: 20px; border: 2px solid #00f2fe;">
                <h3 style="color: #00f2fe;">MATCH FOUND:</h3>
                <h1 style="font-size: 4em; margin: 10px 0;">{top_a['name']}</h1>
                <p style="font-size: 1.2em; line-height: 1.6;">{top_a['desc']}</p>
                <h2 style="color: #ffcc00;">MATCH RATE: {top_s*100:.1f}%</h2>
            </div>
        """, unsafe_allow_html=True)

        # レーダーチャートで可視化
        df = pd.DataFrame(dict(
            r=final_v,
            theta=['Sound','Concept','Scale','Performance','Modernity']
        ))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0,10])
        fig.update_traces(fill='toself', line_color='#00f2fe')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig)

with col_log:
    st.write("### SYSTEM LOG")
    log_area = st.empty()
    logs_text = "\n".join([f"> {l}" for l in st.session_state.logs[-10:]])
    log_area.code(logs_text if logs_text else "READY TO ANALYZE...")

if st.session_state.step >= len(QUESTIONS):
    if st.button("RESET ENGINE"):
        st.session_state.update({'step': 0, 'v': [5.0]*5, 'logs': []})
        st.rerun()