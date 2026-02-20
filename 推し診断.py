import streamlit as st
import pandas as pd
import plotly.express as px
import math
import time

# === 1. 究極のサイバーパンクUI (CSS) ===
st.set_page_config(page_title="K-POP GENESIS ENGINE 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* 全体の背景とフォント */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+JP:wght@300;700&display=swap');
    .main { background-color: #030303; color: #00f2fe; font-family: 'Noto Sans JP', sans-serif; }
    h1, h2, h3 { font-family: 'Orbitron', 'Noto Sans JP', sans-serif; letter-spacing: 2px; text-transform: uppercase; }
    
    /* 診断カードの圧倒的装飾 */
    .result-card {
        border: 2px solid #00f2fe;
        padding: 50px;
        background: radial-gradient(circle, rgba(0, 242, 254, 0.1) 0%, rgba(0,0,0,0.8) 100%);
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.3), inset 0 0 20px rgba(0, 242, 254, 0.1);
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        backdrop-filter: blur(5px);
    }

    /* ボタンのサイバー・ネオンエフェクト */
    .stButton>button {
        background: rgba(0, 242, 254, 0.05);
        color: #00f2fe;
        border: 1px solid #00f2fe;
        font-family: 'Orbitron', monospace;
        letter-spacing: 2px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        width: 100%;
        height: 4.5em;
        font-weight: bold;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #00f2fe;
        color: #030303;
        box-shadow: 0 0 25px #00f2fe;
        transform: scale(1.02);
    }

    /* システムログのコンソール風デザイン */
    .log-container {
        background: #0a0a0a;
        border: 1px solid #333;
        border-left: 3px solid #00f2fe;
        padding: 15px;
        height: 100%;
        border-radius: 5px;
    }
    .log-text {
        font-family: 'Courier New', Courier, monospace;
        color: #00f2fe;
        font-size: 0.85rem;
        margin-bottom: 4px;
        opacity: 0.8;
    }
    .log-text.latest { opacity: 1.0; font-weight: bold; text-shadow: 0 0 5px #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# === 2. データベース (20組以上・多次元ベクトル) ===
# 次元構成: [0:Sound(0:軽~10:重), 1:Concept(0:明~10:暗), 2:Scale(0:少~10:多), 3:Dance(0:歌~10:踊), 4:Era(0:過去~10:最新)]
ARTISTS = [
    {"name": "aespa", "v": [9.0, 9.0, 4.0, 7.0, 6.0], "color": "#ae00ff", "desc": "KWANGYAの覇者。ハイパーポップとメタバースが交差する電脳世界の女王。"},
    {"name": "NewJeans", "v": [2.0, 1.0, 5.0, 6.0, 5.0], "color": "#87ceeb", "desc": "時代の境界線。日常に溶け込むエモーショナルな楽曲と、計算された自然体。"},
    {"name": "BABYMONSTER", "v": [9.0, 8.0, 7.0, 9.0, 8.0], "color": "#ff0000", "desc": "圧倒的な『実力』の暴力。YGのDNAを継承した、次世代ヒップホップの最高峰。"},
    {"name": "MEOVV", "v": [8.0, 8.0, 5.0, 8.0, 9.0], "color": "#e0e0e0", "desc": "TEDDYプロデュースの鋭利な牙。しなやかさと重厚なビートを併せ持つカリスマ。"},
    {"name": "IVE", "v": [4.0, 3.0, 6.0, 5.0, 5.0], "color": "#ff007f", "desc": "完成された美学。自分を愛する高潔なナルシシズムが生む、圧倒的華やかさ。"},
    {"name": "LE SSERAFIM", "v": [7.0, 7.0, 5.0, 9.0, 5.0], "color": "#64e9ff", "desc": "恐れを知らない不屈の意志。鍛え上げられた肉体美と、限界を超えるパフォーマンス。"},
    {"name": "izna", "v": [6.0, 7.0, 7.0, 8.0, 9.0], "color": "#f1a7e1", "desc": "2026年の最前線。過酷なサバイバルから生まれた、予測不能な化学反応と輝き。"},
    {"name": "BLACKPINK", "v": [8.0, 9.0, 4.0, 8.0, 3.0], "color": "#ff66c4", "desc": "世界を平伏させるアイコン。最高級のラグジュアリーとガールクラッシュの到達点。"},
    {"name": "TWICE", "v": [3.0, 2.0, 9.0, 7.0, 3.0], "color": "#ffb6c1", "desc": "大衆性の頂点。多幸感あふれるエネルギーとキャッチーなメロディで世界を魅了。"},
    {"name": "ITZY", "v": [7.0, 8.0, 5.0, 10.0, 4.0], "color": "#ffaa00", "desc": "自己肯定感の権化。骨の髄まで響く激しいビートと、K-POP界最高峰のシンクロダンス。"},
    {"name": "(G)I-DLE", "v": [6.0, 8.0, 5.0, 4.0, 4.0], "color": "#cc0000", "desc": "自らをプロデュースする天才たち。枠に囚われない強烈なメッセージと芸術性。"},
    {"name": "NMIXX", "v": [8.0, 6.0, 6.0, 8.0, 5.0], "color": "#0055ff", "desc": "全員がエース級。MIXX POPという激しい展開を完璧に歌いこなす実力のバケモノ集団。"},
    {"name": "ILLIT", "v": [2.0, 2.0, 5.0, 4.0, 8.0], "color": "#c1e1c1", "desc": "プラグンBと夢かわいいビジュアル。脳内ループが止まらない中毒性の塊。"},
    {"name": "KISS OF LIFE", "v": [4.0, 7.0, 4.0, 3.0, 8.0], "color": "#8b0000", "desc": "Y2K R&Bの再来。セクシーで成熟したボーカルと、実力派ならではの圧倒的な余裕。"},
    {"name": "XG", "v": [9.0, 9.0, 7.0, 9.0, 6.0], "color": "#00ffcc", "desc": "宇宙規模のスケール感。全編英語詞と異次元のラップ・ダンススキルで世界を蹂躙する。"},
    {"name": "UNIS", "v": [5.0, 4.0, 8.0, 6.0, 8.0], "color": "#ffd700", "desc": "グローバルオーディション発。多様な個性がぶつかり合う、エネルギッシュな大所帯。"},
    {"name": "Red Velvet", "v": [5.0, 6.0, 5.0, 4.0, 2.0], "color": "#ff0000", "desc": "予測不能なコンセプトの天才。「Red」の狂気と「Velvet」の妖艶さを操る芸術家。"},
    {"name": "Girls' Generation", "v": [4.0, 3.0, 8.0, 6.0, 0.0], "color": "#ff66b2", "desc": "伝説の象徴。完璧なフォーメーションと大所帯の魅力を定義したK-POPのバイブル。"},
    {"name": "2NE1", "v": [8.0, 9.0, 4.0, 7.0, 0.0], "color": "#000000", "desc": "元祖ガールクラッシュ。誰にも媚びない強さと、ステージを破壊するほどのカリスマ性。"},
    {"name": "STAYC", "v": [3.0, 2.0, 6.0, 5.0, 5.0], "color": "#ff69b4", "desc": "全員がセンター級のビジュアルと「TEENFRESH」な魅力。生歌への強いこだわり。"}
]

# === 3. 診断ロジック (全10問) ===
QUESTIONS = [
    {"q": "Q01. 重低音が内臓に響くような、攻撃的で激しいビートを求めている。", "dim": 0, "weight": 2.5},
    {"q": "Q02. 休日はカフェで流れるような、チルでアコースティックなサウンドが好きだ。", "dim": 0, "weight": -2.5},
    {"q": "Q03. 明るくキュートな笑顔より、近寄りがたいダークなカリスマに惹かれる。", "dim": 1, "weight": 2.5},
    {"q": "Q04. 難解な芸術的コンセプトより、等身大で親しみやすい姿に共感する。", "dim": 1, "weight": -2.5},
    {"q": "Q05. 大人数だからこそできる、万華鏡のような一糸乱れぬフォーメーションが見たい。", "dim": 2, "weight": 2.5},
    {"q": "Q06. メンバーそれぞれの個性が際立つ、少数精鋭のグループが至高だ。", "dim": 2, "weight": -2.5},
    {"q": "Q07. ボーカルよりも、骨が折れそうなほど激しいダンスパフォーマンスを重視する。", "dim": 3, "weight": 2.5},
    {"q": "Q08. ダンスの激しさより、口から音源レベルの圧倒的な生歌・ラップスキルに震えたい。", "dim": 3, "weight": -2.5},
    {"q": "Q09. K-POP黄金期の懐かしいメロディラインや、レトロな雰囲気が好きだ。", "dim": 4, "weight": -2.5},
    {"q": "Q10. 常に最先端。2026年の誰も見たことがない最新トレンドの目撃者になりたい。", "dim": 4, "weight": 2.5},
]

# === 4. システム初期化 ===
if 'step' not in st.session_state:
    st.session_state.update({'step': 0, 'v': [5.0]*5, 'logs': ["SYSTEM BOOT SEQUENCE INITIATED..."]})

def get_similarity(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a**2 for a in v1))
    n2 = math.sqrt(sum(b**2 for b in v2))
    return dot / (n1 * n2) if n1*n2 != 0 else 0

# === 5. メイン画面構築 ===
st.markdown("<h1 style='text-align: center; color: #00f2fe; text-shadow: 0 0 10px #00f2fe;'>K-POP GENESIS ENGINE v2.6</h1>", unsafe_allow_html=True)
st.progress(st.session_state.step / len(QUESTIONS) if st.session_state.step < len(QUESTIONS) else 1.0)
st.divider()

col_left, col_right = st.columns([7, 3])

with col_left:
    if st.session_state.step < len(QUESTIONS):
        q = QUESTIONS[st.session_state.step]
        st.write(f"<h3 style='color: #888;'>[ NEURAL_LINK_ESTABLISHED : SIGNAL {st.session_state.step + 1:02d}/{len(QUESTIONS):02d} ]</h3>", unsafe_allow_html=True)
        st.write(f"<h2 style='margin-bottom: 30px; line-height: 1.4;'>{q['q']}</h2>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("YES / 強く同意する"):
            st.session_state.v[q['dim']] += q['weight']
            st.session_state.logs.append(f"> SIGNAL_{st.session_state.step + 1:02d}: POSITIVE RESPONSE LOGGED.")
            st.session_state.step += 1
            st.rerun()
        if c2.button("NO / 同意しない"):
            st.session_state.v[q['dim']] -= q['weight'] * 0.5 # NOの時は逆方向に少し補正
            st.session_state.logs.append(f"> SIGNAL_{st.session_state.step + 1:02d}: NEGATIVE RESPONSE LOGGED.")
            st.session_state.step += 1
            st.rerun()
            
    else:
        # 診断計算フェーズ (ベクトルを0~10の範囲に正規化してエラーを防ぐ)
        final_v = [max(0.0, min(10.0, val)) for val in st.session_state.v]
        results = sorted([(a, get_similarity(final_v, a['v'])) for a in ARTISTS], key=lambda x: x[1], reverse=True)
        top_a, top_s = results[0]
        
        st.balloons()
        
        # 結果カード
        st.markdown(f"""
            <div class="result-card" style="border-color: {top_a['color']}; box-shadow: 0 0 40px {top_a['color']}44;">
                <h3 style="color: {top_a['color']}; letter-spacing: 3px;">SYNCHRONIZATION RATE: {top_s*100:.1f}%</h3>
                <h1 style="font-size: 5rem; color: {top_a['color']}; text-shadow: 0 0 20px {top_a['color']}; margin: 10px 0;">{top_a['name']}</h1>
                <p style="font-size: 1.4rem; color: #ddd; line-height: 1.6;">{top_a['desc']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # サイバーパンク・レーダーチャート描画
        st.write("<br><h3 style='text-align: center;'>MULTI-DIMENSIONAL ANALYSIS</h3>", unsafe_allow_html=True)
        df = pd.DataFrame(dict(
            r=final_v,
            theta=['Sound (サウンド)', 'Concept (世界観)', 'Scale (規模)', 'Performance (実力)', 'Modernity (最新性)']
        ))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0, 10])
        fig.update_traces(fill='toself', fillcolor=f"{top_a['color']}66", line_color=top_a['color'], line_width=3)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0, 242, 254, 0.05)',
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='#333', linecolor='#333', tickfont=dict(color='#666')),
                angularaxis=dict(gridcolor='#333', tickfont=dict(color='#00f2fe', size=14))
            ),
            font_color='white',
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("<div class='log-container'>", unsafe_allow_html=True)
    st.write("<h4 style='color: #00f2fe; margin-top:0;'>SYSTEM LOGS</h4>", unsafe_allow_html=True)
    
    # ログ表示 (最新のものほど明るく)
    display_logs = st.session_state.logs[-15:]
    for i, log in enumerate(display_logs):
        css_class = "log-text latest" if i == len(display_logs) - 1 else "log-text"
        st.markdown(f"<div class='{css_class}'>{log}</div>", unsafe_allow_html=True)
    
    if st.session_state.step >= len(QUESTIONS):
        st.write("<br>", unsafe_allow_html=True)
        if st.button("SYSTEM REBOOT"):
            st.session_state.update({'step': 0, 'v': [5.0]*5, 'logs': ["SYSTEM REBOOTED...", "> AWAITING NEW CONNECTION..."]})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)