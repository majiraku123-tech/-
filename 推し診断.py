import streamlit as st
import math
import time

# === ページ設定 ===
st.set_page_config(page_title="K-POP 推し診断 2026", page_icon="👑")

# === スタイリッシュなデザイン設定 (CSS) ===
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stRadio > label { font-weight: bold; color: #00d4ff; font-size: 1.2rem; }
    .stButton > button { width: 100%; border-radius: 20px; border: 1px solid #00d4ff; }
    .result-card { padding: 20px; border-radius: 15px; background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# === アーティストデータベース (2026年最新版) ===
ARTISTS = [
    {"name": "Girls' Generation", "v": [5, 4, 8, 6, 0], "desc": "永遠のレジェンド。完璧な群舞と大所帯の魅力を確立したK-POPの教科書。"},
    {"name": "TWICE", "v": [4, 3, 9, 7, 2], "desc": "大衆性の頂点。ハッピーなエネルギーとキャッチーなメロディで世界を魅了します。"},
    {"name": "BLACKPINK", "v": [7, 9, 4, 8, 2], "desc": "K-POPを世界基準に引き上げたカリスマ。ラグジュアリーで圧倒的なガールクラッシュ。"},
    {"name": "Red Velvet", "v": [6, 6, 5, 4, 2], "desc": "「Red」のポップさと「Velvet」のR&B。予測不能なコンセプトの天才たち。"},
    {"name": "MAMAMOO", "v": [3, 7, 4, 2, 2], "desc": "ライブパフォーマンスの鬼。圧倒的な歌唱力と自由なステージングが最高。"},
    {"name": "ITZY", "v": [7, 8, 5, 9, 4], "desc": "自己肯定感爆上がりのメッセージと、骨の髄まで響く激しいダンスパフォーマンス。"},
    {"name": "(G)I-DLE", "v": [6, 8, 5, 4, 4], "desc": "自作ドルとしての矜持。枠に囚われない強烈なメッセージ性と芸術的なコンセプト。"},
    {"name": "aespa", "v": [9, 9, 4, 6, 4], "desc": "KWANGYAから来た電脳戦士。ハイパーポップな楽曲と異次元のボーカル力。"},
    {"name": "IVE", "v": [5, 4, 6, 5, 4], "desc": "ナルシシズムを美しく昇華した「完成型」。優雅でロイヤルな雰囲気が漂います。"},
    {"name": "LE SSERAFIM", "v": [6, 7, 5, 9, 4], "desc": "恐れを知らぬマッスル＆シック。腹筋が割れるほどの高難度パフォーマンス。"},
    {"name": "NewJeans", "v": [2, 1, 5, 6, 4], "desc": "Y2Kの再解釈。イージーリスニングの波を起こした、日常に溶け込むエモい魅力。"},
    {"name": "NMIXX", "v": [8, 6, 6, 8, 4], "desc": "MIXX POPという新ジャンル。全員がメインボーカル＆メインダンサー級のバケモノ集団。"},
    {"name": "BABYMONSTER", "v": [8, 9, 7, 8, 8], "desc": "YGの最高傑作。デビューから完成されたバチバチのヒップホップとボーカル。"},
    {"name": "KISS OF LIFE", "v": [3, 8, 4, 2, 8], "desc": "Y2K R&Bの再来。セクシーで成熟したボーカルと、実力派ならではの余裕。"},
    {"name": "ILLIT", "v": [2, 2, 5, 4, 8], "desc": "プラグンBと夢かわいいビジュアル。脳内ループが止まらない中毒性。"},
    {"name": "MEOVV", "v": [7, 8, 5, 7, 9], "desc": "TEDDYプロデュースの極致。重厚なベースと洗練された猫のようなクールネス。"},
    {"name": "izna", "v": [5, 6, 7, 8, 9], "desc": "I-LAND2から誕生した実力派。ハイティーンの熱量と完璧なパフォーマンス。"},
    {"name": "KiiiKiii", "v": [4, 3, 5, 5, 10], "desc": "2026年のトレンドセッター！明るいエネルギーとVibe重視のニュースター。"},
    {"name": "RESCENE", "v": [3, 4, 5, 4, 9], "desc": "「香り」をコンセプトにしたエレガントで神秘的な世界観。"},
    {"name": "UNIS", "v": [5, 5, 8, 6, 8], "desc": "グローバルオーディション発。多様な魅力が詰まったエネルギッシュな大所帯。"}
]

QUESTIONS = [
    {"q": "Q1. 音楽は「重低音バチバチのEDMやヒップホップ」がテンション上がる？", "dim": 0, "weight": 2.5},
    {"q": "Q2. 休日のプレイリストは「カフェで流れるようなR&Bやアコースティック」が多い？", "dim": 0, "weight": -2.5},
    {"q": "Q3. 曲の途中でビートが急変するような「実験的なサウンド」にゾクゾクする？", "dim": 0, "weight": 2.0},
    {"q": "Q4. コンセプトは「清純・キュート」よりも「ダーク・クール」が好き？", "dim": 1, "weight": 3.0},
    {"q": "Q5. メンバーには「親しみやすさ」より「近寄りがたいカリスマ性」を求める？", "dim": 1, "weight": 2.0},
    {"q": "Q6. 衣装は「制服やY2Kカジュアル」より「ハイブランドやサイバーパンク」が良い？", "dim": 1, "weight": 2.0},
    {"q": "Q7. メンバー数は「4〜5人の少数精鋭」より「7人以上の大人数」が良い？", "dim": 2, "weight": 3.0},
    {"q": "Q8. ステージでは「個人の自由なノリ」より「一糸乱れぬフォーメーション」を見たい？", "dim": 2, "weight": 2.0},
    {"q": "Q9. 「推しケミ」よりも「グループ全体のわちゃわちゃ感」が好き？", "dim": 2, "weight": 1.5},
    {"q": "Q10. ステージ映像で一番重視するのは「口から音源レベルの生歌」だ？", "dim": 3, "weight": -3.0},
    {"q": "Q11. いや、一番重視するのは「骨が折れそうなほど激しいダンス」だ？", "dim": 3, "weight": 3.0},
    {"q": "Q12. 曲の中の「高速ラップパート」は絶対に必要だ？", "dim": 3, "weight": 1.5},
    {"q": "Q13. 最近の曲より、黄金期の曲をよく聴く？", "dim": 4, "weight": -3.0},
    {"q": "Q14. まだ誰も知らない「デビューしたての新人」を発掘するのが好き？", "dim": 4, "weight": 3.0},
    {"q": "Q15. TikTokのダンスチャレンジでよく流れてくる最新曲を追っている？", "dim": 4, "weight": 2.0},
]

def calculate_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0

# === セッション状態の初期化 ===
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.user_vector = [5.0, 5.0, 5.0, 5.0, 5.0]
    st.session_state.finished = False

# === メインUI ===
st.title("💎 K-POP STAR FINDER 2026")

if not st.session_state.finished:
    # 進捗バー
    progress = st.session_state.step / len(QUESTIONS)
    st.progress(progress)
    
    # 質問表示
    q_idx = st.session_state.step
    if q_idx < len(QUESTIONS):
        st.subheader(QUESTIONS[q_idx]["q"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("YES (はい)"):
                st.session_state.user_vector[QUESTIONS[q_idx]["dim"]] += QUESTIONS[q_idx]["weight"]
                st.session_state.step += 1
                st.rerun()
        with col2:
            if st.button("NO (いいえ)"):
                st.session_state.user_vector[QUESTIONS[q_idx]["dim"]] -= QUESTIONS[q_idx]["weight"] * 0.5
                st.session_state.step += 1
                st.rerun()
    else:
        st.session_state.finished = True
        st.rerun()

else:
    # 診断結果の計算
    user_v = [max(0.0, min(10.0, v)) for v in st.session_state.user_vector]
    results = []
    for artist in ARTISTS:
        score = calculate_similarity(user_v, artist["v"])
        results.append((artist, score))
    results.sort(key=lambda x: x[1], reverse=True)

    # 演出
    with st.spinner('次元ベクトル・コサイン類似度を計算中...'):
        time.sleep(1.5)
    
    st.balloons()
    
    # 結果表示
    top_artist, top_score = results[0]
    st.markdown(f"""
    <div class="result-card">
        <h2 style='text-align: center; color: #ffcc00;'>👑 あなたの運命のメイン推しは...</h2>
        <h1 style='text-align: center;'>{top_artist['name']}</h1>
        <p style='text-align: center; font-size: 1.2rem;'>マッチ度: <b>{top_score * 100:.1f}%</b></p>
        <hr>
        <p>{top_artist['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.subheader("🎧 サブで推すべきグループ")
    for i in range(1, 4):
        artist, score = results[i]
        st.write(f"**{i+1}位: {artist['name']}** (マッチ度: {score * 100:.1f}%)")

    if st.button("最初からやり直す"):
        st.session_state.step = 0
        st.session_state.user_vector = [5.0, 5.0, 5.0, 5.0, 5.0]
        st.session_state.finished = False
        st.rerun()