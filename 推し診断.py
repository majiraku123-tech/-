import streamlit as st
import pandas as pd
import numpy as np
import time

# === 1. サイバー・ラグジュアリーUI (Glassmorphism) ===
st.set_page_config(page_title="K-POP GENESIS 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* フォントフォールバック設定 */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+JP:wght@300;500;700&display=swap');
    
    .main { 
        background-color: #050505; 
        color: #e0e0e0; 
        font-family: 'Noto Sans JP', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, rgba(0, 242, 254, 0.05) 0%, transparent 70%);
    }
    h1, h2, h3 { font-family: 'Orbitron', 'Noto Sans JP', sans-serif; letter-spacing: 1px; }
    
    /* ガラスモーフィズム・パネル */
    .glass-panel {
        background: rgba(0, 242, 254, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    /* ボタンカスタマイズ */
    .stButton>button {
        background: linear-gradient(90deg, rgba(0, 242, 254, 0.1) 0%, rgba(174, 0, 255, 0.1) 100%);
        color: #00f2fe;
        border: 1px solid #00f2fe;
        border-radius: 30px;
        height: 3.5em; width: 100%;
        transition: all 0.4s ease;
        font-weight: 700; letter-spacing: 2px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00f2fe 0%, #ae00ff 100%);
        color: #050505;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.5);
        transform: translateY(-2px);
        border: none;
    }

    /* ラジオボタン（7段階評価）のUI調整 */
    div[role="radiogroup"] {
        justify-content: center;
        gap: 2rem;
        margin: 20px 0 40px 0;
    }
    
    /* ローディングアニメーション */
    .loader-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        color: #00f2fe;
        text-align: center;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.5; text-shadow: 0 0 10px #00f2fe; }
        50% { opacity: 1; text-shadow: 0 0 30px #00f2fe, 0 0 50px #ae00ff; }
        100% { opacity: 0.5; text-shadow: 0 0 10px #00f2fe; }
    }
    
    /* カスタムプログレスバー */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00f2fe, #ae00ff);
    }
    </style>
    """, unsafe_allow_html=True)

# === 2. 2026年最新データベース ===
# 次元: [Sound, Concept, Scale, Skill, Era] (各0〜10)
ARTISTS = [
    {"name": "aespa", "v": [9, 9, 4, 7, 6], "color": "#ae00ff", "desc": "電脳世界の女王。ハイパーポップの到達点。"},
    {"name": "NewJeans", "v": [2, 1, 5, 6, 5], "color": "#87ceeb", "desc": "時代の境界線。エモーショナルな自然体。"},
    {"name": "BABYMONSTER", "v": [9, 8, 7, 9, 8], "color": "#ff0000", "desc": "YGの最高傑作。圧倒的な実力の暴力。"},
    {"name": "MEOVV", "v": [8, 8, 5, 8, 9], "color": "#e0e0e0", "desc": "TEDDYプロデュース。しなやかさと重厚なビート。"},
    {"name": "IVE", "v": [4, 3, 6, 5, 5], "color": "#ff007f", "desc": "完成された美学。高潔なナルシシズム。"},
    {"name": "LE SSERAFIM", "v": [7, 7, 5, 9, 5], "color": "#64e9ff", "desc": "恐れを知らない不屈の意志と肉体美。"},
    {"name": "izna", "v": [6, 7, 7, 8, 9], "color": "#f1a7e1", "desc": "2026年の最前線。サバイバルから生まれた輝き。"},
    {"name": "KiiiKiii", "v": [8, 8, 6, 7, 10], "color": "#ff00ff", "desc": "2026年彗星の如く現れた、AIと人間を繋ぐ超新星。"},
    {"name": "BLACKPINK", "v": [8, 9, 4, 8, 2], "color": "#ff66c4", "desc": "世界を平伏させるガールクラッシュ。"},
    {"name": "TWICE", "v": [3, 2, 9, 7, 2], "color": "#ffb6c1", "desc": "大衆性の頂点。多幸感あふれるエネルギー。"},
    {"name": "XG", "v": [9, 9, 7, 9, 7], "color": "#00ffcc", "desc": "宇宙規模のスキル。全編英語詞の衝撃。"},
    {"name": "ILLIT", "v": [2, 2, 5, 4, 8], "color": "#c1e1c1", "desc": "夢かわいいビジュアルとプラグンB。"}
]

# === 3. 7段階評価用・15の質問 ===
# wは1回答あたりの影響度（0.5〜0.6に設定し、10点満点に収束させる）
QUESTIONS = [
    {"q": "重低音が響く、破壊的で激しいビートの曲が好きだ。", "dim": 0, "w": 0.6},
    {"q": "落ち着いたR&Bや、カフェで流れるアコースティックな曲をよく聴く。", "dim": 0, "w": -0.6},
    {"q": "ダークで近未来的、あるいはミステリアスな世界観に強く惹かれる。", "dim": 1, "w": 0.6},
    {"q": "明るくて可愛い、王道のアイドルらしさこそ至高だと思う。", "dim": 1, "w": -0.6},
    {"q": "大人数（7人以上）による、万華鏡のような迫力ある群舞が見たい。", "dim": 2, "w": 0.6},
    {"q": "少数精鋭（4〜5人）で、メンバー一人一人の個性がぶつかるのが好きだ。", "dim": 2, "w": -0.6},
    {"q": "ステージでは何よりも「圧倒的なダンスのキレ」を重視する。", "dim": 3, "w": 0.6},
    {"q": "ダンスよりも、口から音源レベルの「生歌のうまさやラップ」に震えたい。", "dim": 3, "w": -0.6},
    {"q": "デビューしたての「新人」を発掘し、成長を見守るのが好きだ。", "dim": 4, "w": 0.6},
    {"q": "何年経っても色褪せない「レジェンド級」のグループに安心する。", "dim": 4, "w": -0.6},
    {"q": "予想できない展開の「実験的なサウンド」にワクワクする。", "dim": 0, "w": 0.4},
    {"q": "親しみやすさよりも、近寄りがたいほどの「カリスマ性」を求める。", "dim": 1, "w": 0.4},
    {"q": "一糸乱れぬ動きより、ステージ上の「自由な遊びやアドリブ」が好きだ。", "dim": 2, "w": -0.4},
    {"q": "K-POP界の歴史や黄金期のサウンドをリスペクトしている。", "dim": 4, "w": -0.4},
    {"q": "TikTokなどで流行っている、キャッチーなトレンド曲は必ずチェックする。", "dim": 0, "w": 0.3}
]

# 選択肢と倍率のマッピング
OPTIONS = {
    "強く同意": 3, "同意": 2, "少し同意": 1, 
    "中立": 0, 
    "少し反対": -1, "反対": -2, "強く反対": -3
}

# === 4. セッションと計算ロジック ===
if 'step' not in st.session_state:
    st.session_state.update({'step': 0, 'v': [5.0]*5, 'loading': False})

def get_sim(v1, v2):
    v1_arr, v2_arr = np.array(v1), np.array(v2)
    norm = np.linalg.norm(v1_arr) * np.linalg.norm(v2_arr)
    return np.dot(v1_arr, v2_arr) / norm if norm != 0 else 0

# === 5. メインUI描画 ===
st.markdown("<h1 style='text-align: center; color: #00f2fe; margin-bottom: 30px;'>K-POP GENESIS ENGINE 2026</h1>", unsafe_allow_html=True)

# ローディング画面の演出
if st.session_state.loading:
    st.markdown("<div style='margin-top: 100px;'><div class='loader-text'>SYSTEM ANALYZING YOUR VIBE...</div></div>", unsafe_allow_html=True)
    time.sleep(2.0) # 2秒間の没入感ある待機
    st.session_state.loading = False
    st.session_state.step += 1
    st.rerun()

# 診断中UI
elif st.session_state.step < len(QUESTIONS):
    progress = st.session_state.step / len(QUESTIONS)
    st.progress(progress)
    st.write(f"<p style='text-align: right; color: #888;'>PHASE {st.session_state.step + 1} / {len(QUESTIONS)}</p>", unsafe_allow_html=True)
    
    q = QUESTIONS[st.session_state.step]
    
    st.markdown(f"<div class='glass-panel'><h2 style='text-align: center; margin-bottom: 40px;'>{q['q']}</h2>", unsafe_allow_html=True)
    
    # 7段階ラジオボタン
    choice = st.radio(
        "あなたのスタンスを選択", 
        list(OPTIONS.keys()), 
        index=3, # デフォルトは「中立」
        horizontal=True,
        label_visibility="collapsed"
    )
    
    col_space1, col_btn, col_space2 = st.columns([1, 2, 1])
    with col_btn:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("NEXT ❯"):
            # 選択された倍率 × 重みを加算
            st.session_state.v[q['dim']] += OPTIONS[choice] * q['w']
            
            # 最後の質問ならローディング状態へ
            if st.session_state.step == len(QUESTIONS) - 1:
                st.session_state.loading = True
            else:
                st.session_state.step += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 結果表示UI
else:
    # ベクトルを0〜10の範囲に正規化（エラー完全防止）
    final_v = [max(0.1, min(10.0, val)) for val in st.session_state.v]
    res = sorted([(a, get_sim(final_v, a['v'])) for a in ARTISTS], key=lambda x: x[1], reverse=True)
    top, score = res[0]
    
    st.balloons()
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown(f"""
            <div class="glass-panel" style="border-color: {top['color']}; box-shadow: 0 0 30px {top['color']}44;">
                <h4 style="color: {top['color']};">MATCHING RATE: {score*100:.1f}%</h4>
                <h1 style="color: {top['color']}; font-size: 3.5rem; text-shadow: 0 0 20px {top['color']}; margin: 10px 0;">{top['name']}</h1>
                <p style="font-size: 1.2rem; line-height: 1.6;">{top['desc']}</p>
            </div>
            <div class="glass-panel">
                <h4>SUB-MATCHES</h4>
                <p>2位: <b>{res[1][0]['name']}</b> ({res[1][1]*100:.1f}%)</p>
                <p>3位: <b>{res[2][0]['name']}</b> ({res[2][1]*100:.1f}%)</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        # Plotlyを使わず、ピュアなHTML/CSSで美しいパラメータバーを描画
        st.markdown("<div class='glass-panel'><h3>NEURAL PARAMETERS</h3>", unsafe_allow_html=True)
        
        labels = ['Sound (重低音)', 'Concept (闇/芸術)', 'Scale (規模)', 'Performance (実力)', 'Modernity (最新性)']
        for i, val in enumerate(final_v):
            percent = (val / 10.0) * 100
            st.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px;">
                        <span>{labels[i]}</span>
                        <span style="color: #00f2fe;">{val:.1f} / 10</span>
                    </div>
                    <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 10px; height: 12px; overflow: hidden;">
                        <div style="width: {percent}%; background: linear-gradient(90deg, #00f2fe, {top['color']}); height: 100%; border-radius: 10px; box-shadow: 0 0 10px {top['color']};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("REBOOT SYSTEM (再診断)"):
            st.session_state.update({'step': 0, 'v': [5.0]*5, 'loading': False})
            st.rerun()