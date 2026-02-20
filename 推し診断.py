import streamlit as st
import pandas as pd
import plotly.express as px
import math
import time

# === 1. 究極のカスタムUI設定 (CSS) ===
st.set_page_config(page_title="K-POP GENESIS 2026", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;700&family=Orbitron:wght@400;900&display=swap');
    
    .main { background: #050505; color: #00f2fe; font-family: 'Exo 2', sans-serif; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    
    /* ボタンのカスタマイズ */
    .stButton>button {
        background: transparent;
        color: #00f2fe;
        border: 2px solid #00f2fe;
        border-radius: 0px;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.4s ease;
        height: 4em;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00f2fe;
        color: #050505;
        box-shadow: 0 0 20px #00f2fe;
        transform: translateY(-3px);
    }
    
    /* ログセクションの装飾 */
    .log-container {
        background: rgba(0, 242, 254, 0.05);
        border: 1px solid rgba(0, 242, 254, 0.2);
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

# === 2. 高度なアーティストデータベース ===
ARTISTS = [
    {"name": "aespa", "v": [9, 9, 4, 6, 4], "color": "#ae00ff", "desc": "KWANGYAの覇者。ハイパーポップとメタバースを融合させた唯一無二の電脳カリスマ。"},
    {"name": "NewJeans", "v": [2, 1, 5, 6, 4], "color": "#ffffff", "desc": "2020年代のパラダイムシフト。飾らない自然体と、聴くほどに深まるエモーショナルな楽曲。"},
    {"name": "BABYMONSTER", "v": [8, 9, 7, 8, 8], "color": "#ff0000", "desc": "YGの最高傑作。圧倒的なラップスキルとボーカル力で、ヒップホップの真髄を証明。"},
    {"name": "MEOVV", "v": [7, 8, 5, 7, 9], "color": "#333333", "desc": "TEDDYプロデュースの極致。重厚なビートとしなやかな強さを兼ね備えた、ネクストレベルのグループ。"},
    {"name": "IVE", "v": [5, 4, 6, 5, 4], "color": "#ff007f", "desc": "「完成型」の美学。ナルシシズムを気高く昇華させ、全ての視線を釘付けにする。"},
    {"name": "LE SSERAFIM", "v": [6, 7, 5, 9, 4], "color": "#64e9ff", "desc": "恐れを知らぬマッスル＆シック。極限まで鍛え上げられたパフォーマンスと、不屈の意志。"},
    {"name": "BLACKPINK", "v": [7, 9, 4, 8, 2], "color": "#f1a7e1", "desc": "世界のアイコン。圧倒的なカリスマ性と、音楽・ファッションを支配する絶対女王。"},
    {"name": "NMIXX", "v": [8, 6, 6, 8, 4], "color": "#0000ff", "desc": "実力のバケモノ集団。MIXX POPという実験的ジャンルを歌いこなす、圧倒的歌唱の衝撃。"}
]

QUESTIONS = [
    {"q": "システムは『重低音』と『破壊的なビート』を求めている？", "dim": 0, "weight": 2.5},
    {"q": "現実を忘れるほどの『ダークで芸術的な世界観』に沈みたい？", "dim": 1, "weight": 2.5},
    {"q": "『大人数』による、一糸乱れぬ幾何学的なフォーメーションを見たい？", "dim": 2, "weight": 2.5},
    {"q": "『激しいダンス』と、それを見事にこなす身体能力に興奮する？", "dim": 3, "weight": 2.5},
    {"q": "過去の栄光よりも、2026年の『最新のサウンド』を浴びたい？", "dim": 4, "weight": 2.5},
]

# === 3. セッション管理と演出ロジック ===
if 'step' not in st.session_state:
    st.session_state.update({'step': 0, 'v': [5.0]*5, 'logs': ["SYSTEM INITIALIZED..."]})

def get_similarity(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a**2 for a in v1))
    n2 = math.sqrt(sum(b**2 for b in v2))
    return dot / (n1 * n2) if n1*n2 != 0 else 0

# === 4. メインレンダリング ===
st.markdown("<h1 style='text-align: center;'>K-POP Genesis Engine v2.6</h1>", unsafe_allow_html=True)

col_main, col_side = st.columns([3, 1])

with col_main:
    if st.session_state.step < len(QUESTIONS):
        q = QUESTIONS[st.session_state.step]
        st.write(f"### [SIGNAL_{st.session_state.step + 1}]")
        st.write(f"## {q['q']}")
        
        c1, c2 = st.columns(2)
        if c1.button("YES / 同意"):
            st.session_state.v[q['dim']] += q['weight']
            st.session_state.logs.append(f"LOG: Dimension {q['dim']} updated (positive).")
            st.session_state.step += 1
            st.rerun()
        if c2.button("NO / 否定"):
            st.session_state.v[q['dim']] -= q['weight'] * 0.7
            st.session_state.logs.append(f"LOG: Dimension {q['dim']} updated (negative).")
            st.session_state.step += 1
            st.rerun()
    else:
        # 診断結果の算出
        final_v = [max(0.1, min(10, x)) for x in st.session_state.v]
        results = sorted([(a, get_similarity(final_v, a['v'])) for a in ARTISTS], key=lambda x: x[1], reverse=True)
        top_a, top_s = results[0]
        
        st.success("✅ 解析が完了しました。")
        
        # 演出用背景カラー
        st.markdown(f"""<style>.main {{ background: radial-gradient(circle, {top_a['color']}33 0%, #050505 100%); }}</style>""", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="border: 4px solid {top_a['color']}; padding: 40px; border-radius: 10px; background: rgba(0,0,0,0.8);">
                <h3 style="color: {top_a['color']};">運命の適合率: {top_s*100:.1f}%</h3>
                <h1 style="font-size: 5rem; margin-bottom: 20px;">{top_a['name']}</h1>
                <p style="font-size: 1.5rem; color: #ddd;">{top_a['desc']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # レーダーチャート表示
        df = pd.DataFrame(dict(
            r=final_v,
            theta=['サウンド','コンセプト','規模','ダンス','最新性']
        ))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself', line_color=top_a['color'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', polar=dict(bgcolor='rgba(0,0,0,0.2)'))
        st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.write("### SYSTEM LOG")
    log_content = "\n".join(st.session_state.logs[-12:])
    st.markdown(f"<div class='log-container'><pre style='color: #00f2fe; background: transparent; border: none;'>{log_content}</pre></div>", unsafe_allow_html=True)
    
    if st.session_state.step >= len(QUESTIONS):
        if st.button("REBOOT SYSTEM"):
            st.session_state.update({'step': 0, 'v': [5.0]*5, 'logs': ["SYSTEM REBOOTED..."]})
            st.rerun()