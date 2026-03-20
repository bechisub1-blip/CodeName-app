import streamlit as st
import random
import os
from streamlit_autorefresh import st_autorefresh

# --- 1. 共有データの設定 ---
@st.cache_resource
def get_global_state():
    return {"rooms": {}}

global_data = get_global_state()

def cleanup_rooms():
    rooms = global_data["rooms"]
    # プレイヤーが0人の部屋を掃除
    to_delete = [r_id for r_id, r_data in rooms.items() if not r_data.get("players") and r_data.get("status") != "setup"]
    for r_id in to_delete:
        del rooms[r_id]

cleanup_rooms()
st_autorefresh(interval=2500, key="global_sync_trigger")

# --- 2. デザイン設定（CSS） ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
    div.stButton > button {
        width: 100% !important; height: 100px !important;
        background-color: white !important; color: black !important;
        border: 1px solid #333 !important; font-weight: bold !important;
        border-radius: 4px !important;
    }
    .flipped-card {
        height: 100px; width: 100%; border-radius: 4px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .player-tag-text {
        padding: 8px 12px; color: white; font-weight: bold; 
        flex-grow: 1; font-size: 0.85rem; border-radius: 4px; margin-bottom: 4px;
    }
    .hint-area {
        background-color: #ffffff; padding: 20px; border-radius: 4px;
        text-align: center; border: 2px solid #000; margin-bottom: 25px;
    }
    .stSidebar .stButton > button {
        height: 32px !important; padding: 0 !important;
        background-color: #ff4b4b !important; color: white !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_default_words():
    # ★ ミミさんが用意してくれた200個の単語に換装！
    return [
        "シャープペンシル", "冷蔵庫", "消しゴム", "洗濯機", "ボールペン", "炊飯器", "修正テープ", "電子レンジ", "定規", "掃除機",
        "ハサミ", "テレビ", "カッターナイフ", "エアコン", "ホッチキス", "空気清浄機", "のり", "ドライヤー", "付箋", "電気ケトル",
        "ノート", "トースター", "コンパス", "加湿器", "分度器", "除湿器", "色鉛筆", "扇風機", "万年筆", "食洗機",
        "サインペン", "コーヒーメーカー", "蛍光ペン", "アイロン", "鉛筆削り", "ホットプレート", "バインダー", "電気毛布", "クリアファイル", "温水洗浄便座",
        "クリップ", "ズボンプレッサー", "パンチ", "布団乾燥機", "画鋲", "電話機", "メジャー", "翻訳機", "穴あけパンチ", "デジタルカメラ",
        "粘着テープ", "ビデオカメラ", "マスキングテープ", "プロジェクター", "穴あき定規", "スピーカー", "レターセット", "ヘッドホン", "封筒", "イヤホン",
        "原稿用紙", "ラジオ", "画用紙", "レコードプレーヤー", "スケッチブック", "コンポ", "単語帳", "ICレコーダー", "筆箱", "電子辞書",
        "下敷き", "ノートパソコン", "修正液", "デスクトップPC", "彫刻刀", "モニター", "習字セット", "キーボード", "絵の具", "マウス",
        "パレット", "外付けHDD", "筆", "USBメモリ", "文鎮", "プリンター", "スズランテープ", "スキャナー", "セロハンテープ", "コピー機",
        "両面テープ", "シュレッダー", "クラフトパンチ", "ラミネーター", "裁断機", "電卓", "コンパス", "ストップウォッチ", "三角定規", "スマートフォン",
        "テンプレート", "タブレット", "雲形定規", "スマートウォッチ", "製図ペン", "モバイルバッテリー", "烏口", "充電器", "トレーシングペーパー", "懐中電灯",
        "カーボン紙", "ランタン", "模造紙", "ミキサー", "折り紙", "ジューサー", "履歴書", "フードプロセッサー", "便箋", "電気圧力鍋",
        "ぽち袋", "低温調理器", "祝儀袋", "ホームベーカリー", "芳名録", "ハンドミキサー", "印鑑", "ワッフルメーカー", "朱肉", "かき氷機",
        "スタンプ台", "電気フライヤー", "認印", "ワインセラー", "訂正印", "生ごみ処理機", "デスクマット", "浄水器", "ブックエンド", "電気スタンド",
        "本立て", "シーリングライト", "ペン立て", "サーキュレーター", "書類トレー", "こたつ", "名刺入れ", "電気ストーブ", "カードケース", "石油ファンヒーター",
        "パスケース", "オイルヒーター", "ペンケース", "電気カーペット", "マグネット", "体重計", "ホワイトボード", "体組成計", "黒板", "血圧計",
        "チョーク", "電動歯ブラシ", "黒板消し", "電気シェーバー", "掲示板", "脱毛器", "コルクボード", "美顔器", "カレンダー", "スチーマー",
        "手帳", "マッサージチェア", "日記帳", "フットマッサージャー", "家計簿", "ハンディマッサージャー", "地図", "デジタルフォトフレーム", "地球儀", "ブルーレイレコーダー",
        "虫眼鏡", "セットトップボックス", "老眼鏡", "ゲーム機", "顕微鏡", "VRゴーグル", "望遠鏡", "電子ピアノ", "分別シール", "キーボード（楽器）",
        "ラベルライター", "アンプ", "タックシール", "チューナー", "インデックス", "メトロノーム", "穴あき補強シール", "ミシン", "荷札", "毛玉取り機"
    ]

# --- 3. ログイン画面 ---
if "room_id" not in st.session_state:
    st.title("CodeName")
    r_id = st.text_input("ルームIDを入力").strip()
    u_name = st.text_input("プレイヤー名を入力").strip()
    
    if st.button("入室する"):
        if r_id and u_name:
            if r_id not in global_data["rooms"]:
                global_data["rooms"][r_id] = {
                    "host": u_name, "status": "setup", "board": [], "players": {}, 
                    "current_team": "red", "phase": "giving_clue", "hint": {"word": "", "count": 0}, 
                    "winner": None, "word_packs": {"標準パック": get_default_words()}, "selected_pack": "標準パック"
                }
            if u_name not in global_data["rooms"][r_id]["players"]:
                global_data["rooms"][r_id]["players"][u_name] = {"side": "赤チーム", "role": "観戦者"}
            st.session_state.room_id = r_id
            st.session_state.user_name = u_name
            st.rerun()
    
    st.divider()
    with st.expander("システム管理"):
        if st.button("サーバー上の全ルームを強制削除"):
            global_data["rooms"] = {}
            st.rerun()
    st.stop()

# --- 4. ルーム継続チェック ---
room_id = st.session_state.room_id
user_name = st.session_state.user_name
if room_id not in global_data["rooms"]:
    del st.session_state.room_id
    st.rerun()
room = global_data["rooms"][room_id]
if user_name not in room["players"]:
    del st.session_state.room_id
    st.rerun()

is_host = (room["host"] == user_name)

# --- 5. サイドバー：メンバー一覧 ---
with st.sidebar:
    st.title("メンバー一覧")
    for name, info in list(room["players"].items()):
        p_color = "#d9534f" if info["side"] == "赤チーム" else "#428bca"
        cols = st.columns([4, 1])
        with cols[0]:
            st.markdown(f'<div class="player-tag-text" style="background-color:{p_color}">{info["side"][0]} | {info["role"][:2]} : {name}</div>', unsafe_allow_html=True)
        with cols[1]:
            if is_host and name != user_name:
                if st.button("X", key=f"kick_{name}"):
                    del room["players"][name]
                    st.rerun()
    st.divider()
    if is_host:
        if st.button("試合リセット"):
            room["status"] = "setup"; room["winner"] = None; room["hint"] = {"word": "", "count": 0}
            st.rerun()
    if st.button("ルームから退出"):
        if user_name in room["players"]: del room["players"][user_name]
        del st.session_state.room_id
        st.rerun()

# --- 6. セットアップ画面 ---
if room["status"] == "setup":
    st.title(f"ルームID: {room_id}")
    col_l, col_r = st.columns(2)
    with col_l: my_side = st.radio("あなたのチーム", ["赤チーム", "青チーム"], index=0 if room["players"][user_name]["side"] == "赤チーム" else 1)
    with col_r: my_role = st.radio("あなたの役職", ["プレイヤー", "スパイマスター", "観戦者"], index=["プレイヤー", "スパイマスター", "観戦者"].index(room["players"][user_name]["role"]))
    room["players"][user_name] = {"side": my_side, "role": my_role}

    st.divider()
    st.subheader("単語パック設定")
    if is_host:
        uploaded_file = st.file_uploader("単語パックを追加 (.txt)", type="txt")
        if uploaded_file:
            raw_data = uploaded_file.read()
            content = ""
            for enc in ["utf-8", "cp932", "euc-jp"]:
                try: content = raw_data.decode(enc); break
                except: continue
            new_words = [line.strip() for line in content.splitlines() if line.strip()]
            if len(new_words) >= 25:
                pack_name = uploaded_file.name
                if pack_name not in room["word_packs"]:
                    room["word_packs"][pack_name] = new_words
                    st.success(f"パック '{pack_name}' を保存")
            else: st.error(f"不足: {len(new_words)}個")

        room["selected_pack"] = st.selectbox("使用パック", list(room["word_packs"].keys()), index=list(room["word_packs"].keys()).index(room.get("selected_pack", "標準パック")))
        st.divider()
        if st.button("試合開始", use_container_width=True):
            source = room["word_packs"][room["selected_pack"]]
            selected_words = random.sample(source, 25)
            roles = (["red"] * 9) + (["blue"] * 8) + (["neutral"] * 7) + (["assassin"] * 1)
            random.shuffle(roles)
            room["board"] = [{"word": s, "role": r, "is_flipped": False} for s, r in zip(selected_words, roles)]
            room["current_team"] = "red"; room["phase"] = "giving_clue"; room["winner"] = None; room["status"] = "playing"
            st.rerun()
    else:
        st.info(f"使用パック: {room.get('selected_pack', '標準パック')}")
        st.write("ホストが開始するのを待っています")

# --- 7. 試合画面 ---
else:
    my_info = room["players"].get(user_name, {"side": "赤チーム", "role": "観戦者"})
    curr_team_code = room["current_team"]
    curr_team_name = "赤チーム" if curr_team_code == "red" else "青チーム"
    curr_color = "#d9534f" if curr_team_code == "red" else "#428bca"

    if room["winner"]:
        win_color = "#d9534f" if room["winner"] == "red" else "#428bca"
        st.markdown(f'<div style="background-color:{win_color}; color:white; font-size:2.5rem; text-align:center; border-radius:4px; padding:20px; margin-bottom:20px;">{"赤チーム" if room["winner"]=="red" else "青チーム"} の勝利</div>', unsafe_allow_html=True)

    st.title(f"{my_info['side']} / {my_info['role']}")
    r_left = sum(1 for c in room["board"] if c["role"] == "red" and not c["is_flipped"])
    b_left = sum(1 for c in room["board"] if c["role"] == "blue" and not c["is_flipped"])
    st.write(f"残り枚数: <span style='color:#d9534f; font-weight:bold;'>赤 {r_left}</span> / <span style='color:#428bca; font-weight:bold;'>青 {b_left}</span>", unsafe_allow_html=True)

    if room["hint"]["word"]:
        st.markdown(f'<div class="hint-area">ヒント：<b style="font-size:1.8rem; color:{curr_color}">{room["hint"]["word"]}</b> ({room["hint"]["count"]}枚)</div>', unsafe_allow_html=True)

    if not room["winner"] and room["phase"] == "guessing" and my_info["role"] == "プレイヤー" and my_info["side"] == curr_team_name:
        if st.button("回答を終了して交代", use_container_width=True):
            room["current_team"] = "blue" if curr_team_code == "red" else "red"; room["phase"] = "giving_clue"; room["hint"] = {"word": "", "count": 0}; st.rerun()

    if not room["winner"] and room["phase"] == "giving_clue" and my_info["role"] == "スパイマスター" and my_info["side"] == curr_team_name:
        with st.expander("ヒントを出す", expanded=True):
            h_word = st.text_input("単語"); h_count = st.number_input("枚数", 1, 9, 1)
            if st.button("送信"): room["hint"] = {"word": h_word, "count": h_count}; room["phase"] = "guessing"; st.rerun()

    bg_colors = {"red": "#d9534f", "blue": "#428bca", "neutral": "#CCCCCC", "assassin": "#333333"}
    for i in range(5):
        cols = st.columns(5)
        for j in range(5):
            idx = i * 5 + j
            card = room["board"][idx]
            with cols[j]:
                if card["is_flipped"]:
                    st.markdown(f'<div class="flipped-card" style="background-color:{bg_colors[card["role"]]}; color:{"white" if card["role"]!="neutral" else "black"};">{card["word"]}</div>', unsafe_allow_html=True)
                else:
                    if my_info["role"] in ["スパイマスター", "観戦者"]:
                        st.markdown(f'<div class="flipped-card" style="border:4px solid {bg_colors[card["role"]]}; background-color:white; color:black;">{card["word"]}</div>', unsafe_allow_html=True)
                    elif not room["winner"] and my_info["role"] == "プレイヤー" and room["phase"] == "guessing" and my_info["side"] == curr_team_name:
                        if st.button(card["word"], key=f"btn_{idx}", use_container_width=True):
                            card.update({"is_flipped": True})
                            if card["role"] == "assassin": room["winner"] = "blue" if curr_team_code == "red" else "red"
                            elif card["role"] != curr_team_code: room["current_team"] = "blue" if curr_team_code == "red" else "red"; room["phase"] = "giving_clue"; room["hint"] = {"word": "", "count": 0}
                            if sum(1 for c in room["board"] if c["role"] == "red" and not c["is_flipped"]) == 0: room["winner"] = "red"
                            if sum(1 for c in room["board"] if c["role"] == "blue" and not c["is_flipped"]) == 0: room["winner"] = "blue"
                            st.rerun()
                    else: st.markdown(f'<div class="flipped-card" style="border:1px solid #ddd; background-color:white; color:black;">{card["word"]}</div>', unsafe_allow_html=True)