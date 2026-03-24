import streamlit as st
import random
import os
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# --- 1. 共有データの設定 ---
@st.cache_resource
def get_global_state():
    return {"rooms": {}}

global_data = get_global_state()

def get_default_words():
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
        "両面テープ", "シュレッダー", "クラフトパンチ", "ラミネーター", "裁断機", "電卓", "ストップウォッチ", "三角定規", "スマートフォン",
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

def load_custom_word_packs():
    packs = {"標準パック": get_default_words()}
    folder = "word_packs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            pack_name = file.replace(".txt", "")
            try:
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    words = [line.strip() for line in f if line.strip()]
                    if len(words) >= 25:
                        packs[pack_name] = words
            except Exception:
                pass
    return packs

def cleanup_rooms():
    rooms = global_data["rooms"]
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
    
    /* カードボタンの基本設定：背景白・文字黒に固定 */
    div.stButton > button {
        width: 100% !important; height: 100px !important;
        background-color: #ffffff !important; 
        color: #111111 !important; 
        border: 2px solid #333 !important; 
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* めくられた後のカード */
    .flipped-card {
        height: 100px; width: 100%; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* スパイマスターが見ている未めくりカード（枠線で正解を表示） */
    .master-view-card {
        height: 100px; width: 100%; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem;
        background-color: #ffffff !important;
        color: #111111 !important;
        box-sizing: border-box;
    }

    /* 一般プレイヤーが見ている未めくりカード */
    .plain-card {
        height: 100px; width: 100%; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem;
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #ddd;
    }

    .player-tag-text {
        padding: 6px 10px; color: white; font-weight: bold; 
        flex-grow: 1; font-size: 0.8rem; border-radius: 4px; margin-bottom: 2px;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .hint-area {
        background-color: #ffffff; padding: 20px; border-radius: 8px;
        text-align: center; border: 3px solid #000; margin-bottom: 25px;
    }
    .chat-msg-container {
        margin-bottom: 8px; padding: 8px; background-color: #ffffff;
        border-bottom: 1px solid #eee; color: #000000 !important;
    }
    .chat-all { border-left: 4px solid #9e9e9e; }
    .chat-team { border-left: 4px solid #2196f3; }
    .chat-role { border-left: 4px solid #ffeb3b; }
    .chat-info { font-size: 0.7rem; color: #888; margin-bottom: 2px; }
    .chat-time { color: #bbb; margin-left: 5px; }
    .chat-text { font-size: 0.9rem; word-wrap: break-word; color: #000 !important; }

    .stSidebar .stButton > button {
        height: 28px !important; padding: 0 !important; font-size: 0.8rem !important;
        background-color: #f0f0f0 !important; color: #333 !important; border: 1px solid #ccc !important;
    }
    .terminate-container button {
        background-color: #ff4b4b !important; color: white !important;
        height: 45px !important; font-size: 0.9rem !important; margin-top: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ログイン画面 ---
if "room_id" not in st.session_state:
    st.title("🕵️ CodeName Online")
    r_id = st.text_input("ルームIDを入力").strip()
    u_name = st.text_input("プレイヤー名を入力").strip()
    
    if st.button("入室する"):
        if r_id and u_name:
            if r_id not in global_data["rooms"]:
                global_data["rooms"][r_id] = {
                    "host": u_name, "status": "setup", "board": [], "players": {}, 
                    "current_team": "red", "phase": "giving_clue", "hint": {"word": "", "count": 0}, 
                    "winner": None, "word_packs": load_custom_word_packs(), "selected_pack": "標準パック",
                    "chat_logs": []
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
            st.success("全てのルームを削除しました")
            st.rerun()
    st.stop()

# 共通データ参照
room_id = st.session_state.room_id
user_name = st.session_state.user_name
room = global_data["rooms"][room_id]
my_info = room["players"].get(user_name, {"side": "赤チーム", "role": "観戦者"})
is_host = (room["host"] == user_name)

# --- 4. サイドバー ---
with st.sidebar:
    st.subheader(f"📍 Room: {room_id}")
    st.write("--- メンバー ---")
    for name, info in list(room["players"].items()):
        p_color = "#d9534f" if info["side"] == "赤チーム" else "#428bca"
        m_col1, m_col2 = st.columns([5, 1]) 
        with m_col1:
            st.markdown(f'<div class="player-tag-text" style="background-color:{p_color}">{info["side"][0]} | {info["role"][:2]} : {name}</div>', unsafe_allow_html=True)
        with m_col2:
            if is_host and name != user_name:
                if st.button("×", key=f"kick_{name}"):
                    del room["players"][name]
                    st.rerun()

    st.write("--- チャット ---")
    chat_type = st.radio("送信先", ["全員", "チーム", "役職のみ"], horizontal=True)
    c_msg = st.text_input("メッセージ", key="chat_input")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("送信", use_container_width=True):
            if c_msg:
                now_str = datetime.now().strftime("%H:%M:%S")
                room["chat_logs"].append({
                    "id": random.randint(0, 999999), "sender": user_name, "team": my_info["side"],
                    "role": my_info["role"], "text": c_msg, "type": chat_type, "time": now_str
                })
                st.rerun()
    with col_c2:
        if is_host:
            if st.button("全消去"): room["chat_logs"] = []; st.rerun()

    for i, log in enumerate(reversed(room["chat_logs"])):
        visible = (log["type"] == "全員") or \
                  (log["type"] == "チーム" and log["team"] == my_info["side"]) or \
                  (log["type"] == "役職のみ" and log["team"] == my_info["side"] and log["role"] == my_info["role"])
        if visible:
            css_type = {"全員": "chat-all", "チーム": "chat-team", "役職のみ": "chat-role"}[log["type"]]
            l_col1, l_col2 = st.columns([5.5, 1])
            with l_col1:
                st.markdown(f'<div class="chat-msg-container {css_type}"><div class="chat-info">[{log["type"]}] <b>{log["sender"]}</b> <span class="chat-time">{log["time"]}</span></div><div class="chat-text">{log["text"]}</div></div>', unsafe_allow_html=True)
            with l_col2:
                if log["sender"] == user_name or is_host:
                    if st.button("×", key=f"del_{log['id']}_{i}"):
                        room["chat_logs"] = [l for l in room["chat_logs"] if l.get("id") != log["id"]]
                        st.rerun()

    st.write("---")
    if is_host and room["status"] == "playing":
        st.markdown('<div class="terminate-container">', unsafe_allow_html=True)
        if st.button("強制終了して再設定"):
            room["status"] = "setup"; room["board"] = []; room["winner"] = None; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("ルームから退出"):
        if user_name in room["players"]: del room["players"][user_name]
        del st.session_state.room_id; st.rerun()

# --- 5. セットアップ画面 ---
if room["status"] == "setup":
    st.title("⚙️ セットアップ")
    
    if is_host:
        with st.expander("📁 単語パック管理"):
            up_file = st.file_uploader("新パック追加 (.txt)", type="txt")
            if up_file:
                with open(os.path.join("word_packs", up_file.name), "wb") as f:
                    f.write(up_file.getbuffer())
                st.success("追加完了！")
                room["word_packs"] = load_custom_word_packs(); st.rerun()
            
            st.divider()
            pack_list = [p for p in room["word_packs"].keys() if p != "標準パック"]
            if pack_list:
                target = st.selectbox("削除するパック", pack_list)
                if st.button("削除実行"):
                    os.remove(os.path.join("word_packs", f"{target}.txt"))
                    room["word_packs"] = load_custom_word_packs(); st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    with c1: my_side = st.radio("チームを選択", ["赤チーム", "青チーム"], index=0 if my_info["side"]=="赤チーム" else 1)
    with c2: my_role = st.radio("役職を選択", ["プレイヤー", "スパイマスター", "観戦者"], index=["プレイヤー", "スパイマスター", "観戦者"].index(my_info["role"]))
    room["players"][user_name] = {"side": my_side, "role": my_role}

    if is_host:
        st.divider()
        room["selected_pack"] = st.selectbox("使用するパック", list(room["word_packs"].keys()))
        if st.button("🎮 試合開始", use_container_width=True):
            source = room["word_packs"][room["selected_pack"]]
            if len(source) >= 25:
                selected = random.sample(source, 25)
                roles = (["red"]*9) + (["blue"]*8) + (["neutral"]*7) + (["assassin"]*1)
                random.shuffle(roles)
                room["board"] = [{"word": s, "role": r, "is_flipped": False} for s, r in zip(selected, roles)]
                room["current_team"] = "red"; room["phase"] = "giving_clue"; room["winner"] = None; room["status"] = "playing"
                st.rerun()
            else: st.error("25単語以上必要です")
    else: st.info("ホストの開始を待機中...")

# --- 6. 試合画面 ---
else:
    curr_t = room["current_team"]
    curr_name = "赤チーム" if curr_t == "red" else "青チーム"
    curr_c = "#d9534f" if curr_t == "red" else "#428bca"

    if room["winner"]:
        w_c = "#d9534f" if room["winner"] == "red" else "#428bca"
        st.markdown(f'<div style="background-color:{w_c}; color:white; font-size:2rem; text-align:center; padding:20px; border-radius:12px; margin-bottom:20px;">{"赤" if room["winner"]=="red" else "青"}チームの勝利！</div>', unsafe_allow_html=True)

    st.title(f"🎭 {my_info['side']} / {my_info['role']}")
    r_n = sum(1 for c in room["board"] if c["role"] == "red" and not c["is_flipped"])
    b_n = sum(1 for c in room["board"] if c["role"] == "blue" and not c["is_flipped"])
    st.write(f"残り: <span style='color:#d9534f; font-weight:bold;'>赤 {r_n}</span> / <span style='color:#428bca; font-weight:bold;'>青 {b_n}</span>", unsafe_allow_html=True)

    if room["hint"]["word"]:
        st.markdown(f'<div class="hint-area">ヒント：<b style="color:{curr_c}; font-size:1.8rem;">{room["hint"]["word"]}</b> ({room["hint"]["count"]}枚)</div>', unsafe_allow_html=True)

    if not room["winner"] and my_info["side"] == curr_name:
        if room["phase"] == "guessing" and my_info["role"] == "プレイヤー":
            if st.button("ターンを終了して交代", use_container_width=True):
                room["current_team"] = "blue" if curr_t=="red" else "red"; room["phase"] = "giving_clue"; room["hint"] = {"word":"", "count":0}; st.rerun()
        elif room["phase"] == "giving_clue" and my_info["role"] == "スパイマスター":
            with st.expander("💡 ヒントを入力する", expanded=True):
                hw = st.text_input("連想ワード"); hc = st.number_input("対象枚数", 1, 9, 1)
                if st.button("ヒントを送信"): room["hint"] = {"word": hw, "count": hc}; room["phase"] = "guessing"; st.rerun()

    # ボード表示
    bg = {"red": "#d9534f", "blue": "#428bca", "neutral": "#CCCCCC", "assassin": "#333333"}
    for i in range(5):
        cols = st.columns(5)
        for j in range(5):
            idx = i * 5 + j
            card = room["board"][idx]
            with cols[j]:
                if card["is_flipped"]:
                    # めくられた後は、背景がチーム色、文字が白（ニュートラルは黒）
                    txt_c = "white" if card["role"] != "neutral" else "black"
                    st.markdown(f'<div class="flipped-card" style="background-color:{bg[card["role"]]}; color:{txt_c};">{card["word"]}</div>', unsafe_allow_html=True)
                elif my_info["role"] in ["スパイマスター", "観戦者"]:
                    # スパイマスター用の透かし：背景白、文字黒、枠線がチーム色
                    st.markdown(f'<div class="master-view-card" style="border:5px solid {bg[card["role"]]};">{card["word"]}</div>', unsafe_allow_html=True)
                elif not room["winner"] and my_info["role"] == "プレイヤー" and room["phase"] == "guessing" and my_info["side"] == curr_name:
                    # 回答中のプレイヤー：ボタン形式（CSSで白背景・黒文字に固定済み）
                    if st.button(card["word"], key=f"c_{idx}"):
                        card["is_flipped"] = True
                        if card["role"] == "assassin": room["winner"] = "blue" if curr_t=="red" else "red"
                        elif card["role"] != curr_t: room["current_team"] = "blue" if curr_t=="red" else "red"; room["phase"] = "giving_clue"; room["hint"] = {"word":"", "count":0}
                        if sum(1 for c in room["board"] if c["role"] == "red" and not c["is_flipped"]) == 0: room["winner"] = "red"
                        if sum(1 for c in room["board"] if c["role"] == "blue" and not c["is_flipped"]) == 0: room["winner"] = "blue"
                        st.rerun()
                else:
                    # 待機中のプレイヤーや観戦者：背景白、文字黒
                    st.markdown(f'<div class="plain-card">{card["word"]}</div>', unsafe_allow_html=True)
