import streamlit as st
import pandas as pd
import plotly.express as px
import math

# === 1. クオリティ最優先のUI設定 ===
st.set_page_config(page_title="K-POP GENESIS 2026", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #030303; color: #00f2fe; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button {
        background: rgba(0, 242, 254, 0.05); color: #00f2fe; border: 1px solid #00f2fe;
        height: 4em; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background: #00f2fe; color: #030303; box-shadow: 0 0 20px #00f2fe; }
    .result-card {
        border: 2px solid #00f2fe; padding: 40px; background: rgba(0,0,0,0.8);
        border-radius: 15px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# === 2. アーティストデータベース (25組) ===
ARTISTS = [
    {"name": "aespa", "v": [9, 9, 4, 7, 6], "color": "rgb(174, 0, 255)", "desc": "電脳世界の女王。ハイパーポップの到達点。"},
    {"name": "NewJeans", "v": [2, 1, 5, 6, 5], "color": "rgb(135, 206, 235)", "desc": "時代の境界線。エモーショナルな自然体。"},
    {"name": "BABYMONSTER", "v": [9, 8, 7, 9, 8], "color": "rgb(255, 0, 0)", "desc": "YGの最高傑作。圧倒的な実力の暴力。"},
    {"name": "MEOVV", "v": [8, 8, 5, 8, 9], "color": "rgb(200, 200, 200)", "desc": "TEDDYプロデュース。しなやかさと重厚なビート。"},
    {"name": "IVE", "v": [4, 3, 6, 5, 5], "color": "rgb(255, 0, 127)", "desc": "完成された美学。高潔なナルシシズム。"},
    {"name": "LE SSERAFIM", "v": [7, 7, 5, 9, 5], "color": "rgb(100, 233, 255)", "desc": "恐れを知らない不屈の意志と肉体美。"},
    {"name": "izna", "v": [6, 7, 7, 8, 9], "color": "rgb(241, 167, 225)", "desc": "2026年の最前線。サバイバルから生まれた輝き。"},
    {"name": "BLACKPINK", "v": [8, 9, 4, 8, 2], "color": "rgb(255, 102, 196)", "desc": "世界を平伏させるガールクラッシュ。"},
    {"name": "TWICE", "v": [3, 2, 9, 7, 2], "color": "rgb(255, 182, 193)", "desc": "大衆性の頂点。多幸感あふれるエネルギー。"},
    {"name": "ITZY", "v": [7, 8, 5, 10, 4], "color": "rgb(255, 170, 0)", "desc": "K-POP界最高峰のシンクロダンス。"},
    {"name": "NMIXX", "v": [8, 6, 6, 8, 5], "color": "rgb(0, 85, 255)", "desc": "MIXX POPを歌いこなすバケモノ集団。"},
    {"name": "XG", "v": [9, 9, 7, 9, 7], "color": "rgb(0, 255, 204)", "desc": "宇宙規模のスキル。全編英語詞の衝撃。"},
    {"name": "ILLIT", "v": [2, 2, 5, 4, 8], "color": "rgb(193, 225, 193)", "desc": "夢かわいいビジュアルとプラグンB。"},
    {"name": "KISS OF LIFE", "v": [4, 7, 4, 3, 8], "color": "rgb(139, 0, 0)", "desc": "Y2K R&Bの再来。成熟した実力。"},
    {"name": "STAYC", "v": [3, 2, 6, 5, 5], "color": "rgb(255, 105, 180)", "desc": "全員センター級。TEENFRESHの真髄。"},
    {"name": "Girls' Generation", "v": [4, 3, 8, 6, 0], "color": "rgb(255, 102, 178)", "desc": "永遠のレジェンド。K-POPのバイブル。"},
    {"name": "2NE1", "v": [8, 9, 4, 7, 0], "color": "rgb(255, 255, 0)", "desc": "元祖ガールクラッシュの伝説。"},
    {"name": "Red Velvet", "v": [5, 6, 5, 4, 2], "color": "rgb(255, 50, 50)", "desc": "予測不能な芸術的コンセプト。"},
    {"name": "(G)I-DLE", "v": [6, 8, 5, 4, 4], "color": "rgb(180, 0, 0)", "desc": "自らをプロデュースする天才たち。"},
    {"name": "MAMAMOO", "v": [3, 6, 4, 2, 2], "color": "rgb(0, 212, 255)", "desc": "圧倒的な生歌とライブパフォーマンス。"},
    {"name": "Kep1er", "v": [6, 5, 9, 8, 4], "color": "rgb(255, 204, 102)", "desc": "爆発的なシンクロダンス。"},
    {"name": "RESCENE", "v": [3, 4, 5, 4, 9], "color": "rgb(255, 255, 255)", "desc": "「香り」を纏う、2026年の新星。"},
    {"name": "UNIS", "v": [5, 5, 8, 6, 8], "color": "rgb(255, 215, 0)", "desc": "エネルギッシュな大所帯グループ。"},
    {"name": "NiziU", "v": [3, 2, 9, 7, 4], "color": "rgb(255, 100, 200)", "desc": "虹のような笑顔。抜群のチームワーク。"},
    {"name": "BABYVOX", "v": [5, 7, 5, 4, 0], "color": "rgb(100, 100, 100)", "desc": "第1・2世代の架け橋となった名グループ。"}
]

# === 3. 究極の15質問 ===
QUESTIONS = [
    {"q": "Q1. 重低音が響く、破壊的なヒップホップ・EDMが好き？", "dim": 0, "w": 3.0},
    {"q": "Q2. 落ち着いたR&Bやアコースティック曲をよく聴く？", "dim": 0, "w": -3.0},
    {"q": "Q3. ダークで近未来的な、ミステリアスな世界観に惹かれる？", "dim": 1, "w": 3.0},
    {"q": "Q4. 明るくて可愛い、王道のアイドルらしさを求めている？", "dim": 1, "w": -3.0},
    {"q": "Q5. 10人前後の大人数による迫力ある群舞が見たい？", "dim": 2, "w": 3.0},
    {"q": "Q6. 4～5人の少数精鋭で、個性がぶつかり合うのが好き？", "dim": 2, "w": -3.0},
    {"q": "Q7. ステージでは何よりも「ダンスのキレ」を重視する？", "dim": 3, "w": 3.0},
    {"q": "Q8. ダンスよりも「生歌のうまさ・ラップ」に震えたい？", "dim": 3, "w": -3.0},
    {"q": "Q9. デビューしたての「新人」を発掘するのが好き？", "dim": 4, "w": 3.5},
    {"q": "Q10. 何年経っても色褪せない「レジェンド」に安心する？", "dim": 4, "w": -3.5},
    {"q": "Q11. 予想できない展開の「実験的な曲」にワクワクする？", "dim": 0, "w": 1.5},
    {"q": "Q12. メンバーに「親しみやすさ」より「カリスマ」を求める？", "dim": 1, "w": 1.5},
    {"q": "Q13. メンバー間の「わちゃわちゃ感」が一番の癒やしだ？", "dim": 2, "w": 1.5},
    {"q": "Q14. 2010年代のK-POP黄金期のサウンドが忘れられない？", "dim": 4, "w": -1.5},
    {"q": "Q15. TikTokで流行るような、キャッチーな曲が好き？", "dim": 0, "w": 1.0}
]

# === 4. システムロジック ===
if 'step' not in st.session_state:
    st.session_state.update({'step': 0, 'v': [5.0]*5})

def get_sim(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    n1, n2 = math.sqrt(sum(a**2 for a in v1)), math.sqrt(sum(b**2 for b in v2))
    return dot / (n1 * n2) if n1*n2 != 0 else 0

# === 5. メイン描画 ===
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>K-POP GENESIS ENGINE 2026</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>ANALYSIS: {st.session_state.step}/{len(QUESTIONS)}</p>", unsafe_allow_html=True)

if st.session_state.step < len(QUESTIONS):
    q = QUESTIONS[st.session_state.step]
    st.write(f"<h2 style='text-align: center;'>{q['q']}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("YES / そう思う"):
            st.session_state.v[q['dim']] += q['w']
            st.session_state.step += 1
            st.rerun()
        if st.button("NO / そう思わない"):
            st.session_state.v[q['dim']] -= q['w'] * 0.5
            st.session_state.step += 1
            st.rerun()
else:
    # 診断実行
    final_v = [max(0.1, min(10.0, val)) for val in st.session_state.v]
    res = sorted([(a, get_sim(final_v, a['v'])) for a in ARTISTS], key=lambda x: x[1], reverse=True)
    top, score = res[0]
    
    st.balloons()
    st.markdown(f"""
        <div class="result-card" style="border-color: {top['color']};">
            <h3 style="color: {top['color']};">MATCHING RATE: {score*100:.1f}%</h3>
            <h1 style="color: {top['color']}; font-size: 4.5rem;">{top['name']}</h1>
            <p style="font-size: 1.3rem;">{top['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # グラフ描画 (エラー回避型)
    df = pd.DataFrame(dict(r=final_v, theta=['Sound','Concept','Scale','Skill','Era']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0,10])
    fig.update_traces(fill='toself', line_color=top['color'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#00f2fe', polar=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig, use_container_width=True)
    
    # サブ推し表示
    st.write("### サブで推すべきグループ")
    for i in range(1, 4):
        a, s = res[i]
        st.write(f"**{i+1}位: {a['name']}** (適合率: {s*100:.1f}%)")

    if st.button("REBOOT SYSTEM (最初からやり直す)"):
        st.session_state.update({'step': 0, 'v': [5.0]*5})
        st.rerun()