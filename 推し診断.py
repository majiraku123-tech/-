import math
import time
import sys

# === スタイリッシュなUIのためのANSIエスケープシーケンス ===
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def type_text(text, delay=0.03, color=Colors.ENDC):
    """文字をタイピング風に出力する演出"""
    for char in text:
        sys.stdout.write(color + char + Colors.ENDC)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# === アーティストデータベース (2026年最新版) ===
# ベクトル次元: [Music(0:Easy~10:Heavy), Concept(0:Natural~10:Dark), Size(0:Small~10:Large), Strength(0:Vocal~10:Dance), Era(0:Gen2~10:Gen6)]
ARTISTS = [
    # Gen 2 & 3
    {"name": "Girls' Generation", "v": [5, 4, 8, 6, 0], "desc": "永遠のレジェンド。完璧な群舞と大所帯の魅力を確立したK-POPの教科書。"},
    {"name": "TWICE", "v": [4, 3, 9, 7, 2], "desc": "大衆性の頂点。ハッピーなエネルギーとキャッチーなメロディで世界を魅了します。"},
    {"name": "BLACKPINK", "v": [7, 9, 4, 8, 2], "desc": "K-POPを世界基準に引き上げたカリスマ。ラグジュアリーで圧倒的なガールクラッシュ。"},
    {"name": "Red Velvet", "v": [6, 6, 5, 4, 2], "desc": "「Red」のポップさと「Velvet」のR&B。予測不能なコンセプトの天才たち。"},
    {"name": "MAMAMOO", "v": [3, 7, 4, 2, 2], "desc": "ライブパフォーマンスの鬼。圧倒的な歌唱力と自由なステージングが最高。"},
    
    # Gen 4
    {"name": "ITZY", "v": [7, 8, 5, 9, 4], "desc": "自己肯定感爆上がりのメッセージと、骨の髄まで響く激しいダンスパフォーマンス。"},
    {"name": "(G)I-DLE", "v": [6, 8, 5, 4, 4], "desc": "自作ドルとしての矜持。枠に囚われない強烈なメッセージ性と芸術的なコンセプト。"},
    {"name": "aespa", "v": [9, 9, 4, 6, 4], "desc": "KWANGYAから来た電脳戦士。ハイパーポップな楽曲と異次元のボーカル力。"},
    {"name": "IVE", "v": [5, 4, 6, 5, 4], "desc": "ナルシシズムを美しく昇華した「完成型」。優雅でロイヤルな雰囲気が漂います。"},
    {"name": "LE SSERAFIM", "v": [6, 7, 5, 9, 4], "desc": "恐れを知らぬマッスル＆シック。腹筋が割れるほどの高難度パフォーマンス。"},
    {"name": "NewJeans", "v": [2, 1, 5, 6, 4], "desc": "Y2Kの再解釈。イージーリスニングの波を起こした、日常に溶け込むエモい魅力。"},
    {"name": "NMIXX", "v": [8, 6, 6, 8, 4], "desc": "MIXX POPという新ジャンル。全員がメインボーカル＆メインダンサー級のバケモノ集団。"},
    
    # Gen 5 & 6 (2024~2026)
    {"name": "BABYMONSTER", "v": [8, 9, 7, 8, 8], "desc": "YGの最高傑作。デビューから完成されたバチバチのヒップホップとボーカル。"},
    {"name": "KISS OF LIFE", "v": [3, 8, 4, 2, 8], "desc": "Y2K R&Bの再来。セクシーで成熟したボーカルと、実力派ならではの余裕。"},
    {"name": "ILLIT", "v": [2, 2, 5, 4, 8], "desc": "プラグンBと夢かわいいビジュアル。脳内ループが止まらない中毒性。"},
    {"name": "MEOVV", "v": [7, 8, 5, 7, 9], "desc": "TEDDYプロデュースの極致。重厚なベースと洗練された猫のようなクールネス。"},
    {"name": "izna", "v": [5, 6, 7, 8, 9], "desc": "I-LAND2から誕生した実力派。ハイティーンの熱量と完璧なパフォーマンス。"},
    {"name": "KiiiKiii", "v": [4, 3, 5, 5, 10], "desc": "2026年のトレンドセッター！明るいエネルギーとVibe重視のニュースター。"},
    {"name": "RESCENE", "v": [3, 4, 5, 4, 9], "desc": "「香り」をコンセプトにしたエレガントで神秘的な世界観。"},
    {"name": "UNIS", "v": [5, 5, 8, 6, 8], "desc": "グローバルオーディション発。多様な魅力が詰まったエネルギッシュな大所帯。"}
]

# === 質問リスト ===
# q: 質問文, dim: 影響する次元インデックス, weight: 加算/減算する値 (Yesの場合)
QUESTIONS = [
    {"q": "Q1. 音楽は「重低音バチバチのEDMやヒップホップ」がテンション上がる？", "dim": 0, "weight": 2.5},
    {"q": "Q2. 休日のプレイリストは「カフェで流れるようなR&Bやアコースティック」が多い？", "dim": 0, "weight": -2.5},
    {"q": "Q3. 曲の途中でビートが急変するような「実験的なサウンド」にゾクゾクする？", "dim": 0, "weight": 2.0},
    {"q": "Q4. コンセプトは「清純・キュート」よりも「ダーク・クール」が好き？", "dim": 1, "weight": 3.0},
    {"q": "Q5. メンバーには「親しみやすさ」より「近寄りがたいカリスマ性」を求める？", "dim": 1, "weight": 2.0},
    {"q": "Q6. 衣装は「制服やY2Kカジュアル」より「ハイブランドやサイバーパンク」が良い？", "dim": 1, "weight": 2.0},
    {"q": "Q7. メンバー数は「4〜5人の少数精鋭」より「7人以上の大人数」が良い？", "dim": 2, "weight": 3.0},
    {"q": "Q8. ステージでは「個人の自由なノリ」より「一糸乱れぬフォーメーション」を見たい？", "dim": 2, "weight": 2.0},
    {"q": "Q9. 「推しケミ（特定の2人の絡み）」よりも「グループ全体のわちゃわちゃ感」が好き？", "dim": 2, "weight": 1.5},
    {"q": "Q10. ステージ映像で一番重視するのは「口から音源レベルの生歌」だ？", "dim": 3, "weight": -3.0},
    {"q": "Q11. いや、一番重視するのは「骨が折れそうなほど激しいダンス」だ？", "dim": 3, "weight": 3.0},
    {"q": "Q12. 曲の中の「高速ラップパート」は絶対に必要だ？", "dim": 3, "weight": 1.5},
    {"q": "Q13. 最近の曲より、2010年代のK-POP黄金期の曲をよく聴く？", "dim": 4, "weight": -3.0},
    {"q": "Q14. まだ誰も知らない「デビューしたての新人（ルーキー）」を発掘するのが好き？", "dim": 4, "weight": 3.0},
    {"q": "Q15. TikTokのダンスチャレンジでよく流れてくる最新トレンド曲を追っている？", "dim": 4, "weight": 2.0},
]

def calculate_similarity(vec1, vec2):
    """コサイン類似度を計算"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot_product / (norm_a * norm_b)

def main():
    print(Colors.CYAN + "=================================================" + Colors.ENDC)
    type_text("  ██╗  ██╗       ██████╗  ██████╗ ██████╗ ", 0.005, Colors.BOLD + Colors.BLUE)
    type_text("  ██║ ██╔╝       ██╔══██╗██╔═══██╗██╔══██╗", 0.005, Colors.BOLD + Colors.BLUE)
    type_text("  █████╔╝  █████╗██████╔╝██║   ██║██████╔╝", 0.005, Colors.BOLD + Colors.BLUE)
    type_text("  ██╔═██╗  ╚════╝██╔═══╝ ██║   ██║██╔═══╝ ", 0.005, Colors.BOLD + Colors.BLUE)
    type_text("  ██║  ██╗       ██║     ╚██████╔╝██║     ", 0.005, Colors.BOLD + Colors.BLUE)
    type_text("  ╚═╝  ╚═╝       ╚═╝      ╚═════╝ ╚═╝     ", 0.005, Colors.BOLD + Colors.BLUE)
    print(Colors.CYAN + "=================================================" + Colors.ENDC)
    type_text("  [ NEXT-GEN PERSONALITY DIAGNOSIS ENGINE 2026 ]", 0.02, Colors.WARNING)
    print()
    type_text("システムを起動中... ユーザーの脳波とSpotifyの履歴を同期（嘘）...", 0.05)
    print()

    # ユーザーベクトルの初期値 (すべての中央値である5に設定)
    user_vector = [5.0, 5.0, 5.0, 5.0, 5.0]

    type_text("以下の15の質問に [ y ] (Yes) または [ n ] (No) で答えてください。", 0.02, Colors.GREEN)
    print("-" * 50)

    for q_data in QUESTIONS:
        while True:
            ans = input(Colors.BOLD + q_data["q"] + " (y/n): " + Colors.ENDC).strip().lower()
            if ans in ['y', 'yes']:
                user_vector[q_data["dim"]] += q_data["weight"]
                break
            elif ans in ['n', 'no']:
                user_vector[q_data["dim"]] -= q_data["weight"] * 0.5 # Noの場合は少し逆方向に補正
                break
            else:
                print(Colors.FAIL + "⚠️ 'y' または 'n' で入力してください。" + Colors.ENDC)

    # 値を0〜10の範囲にクリッピング
    user_vector = [max(0.0, min(10.0, v)) for v in user_vector]

    print()
    type_text("データ解析中...", 0.05, Colors.WARNING)
    time.sleep(1)
    type_text("多次元ベクトル・コサイン類似度を計算中...", 0.05, Colors.WARNING)
    time.sleep(1)
    print()

    # 診断実行
    results = []
    for artist in ARTISTS:
        score = calculate_similarity(user_vector, artist["v"])
        results.append((artist, score))
    
    # スコア順にソート
    results.sort(key=lambda x: x[1], reverse=True)

    print(Colors.CYAN + "================ DIAGNOSIS RESULT ================" + Colors.ENDC)
    
    # 1位の発表
    top_artist, top_score = results[0]
    type_text(f"👑 あなたの運命のメイン推しは... 【 {top_artist['name']} 】 です！", 0.05, Colors.BOLD + Colors.WARNING)
    print(Colors.GREEN + f"📊 マッチ度: {top_score * 100:.1f}%" + Colors.ENDC)
    type_text(f"📝 {top_artist['desc']}", 0.03)
    print()

    # 2位、3位の発表
    type_text("🎧 サブで推すべき・プレイリストに入れるべきグループ:", 0.03, Colors.BLUE)
    for i in range(1, 3):
        artist, score = results[i]
        print(f"  {i+1}位: {artist['name']} (マッチ度: {score * 100:.1f}%)")
    
    print(Colors.CYAN + "==================================================" + Colors.ENDC)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colors.FAIL + "\n診断が中断されました。現実世界に帰還します。" + Colors.ENDC)