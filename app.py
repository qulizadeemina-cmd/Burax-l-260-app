import streamlit as st
import json
import os
import random
from datetime import datetime

# 1. Səhifə Konfiqurasiyası
st.set_page_config(
    page_title="Buraxılış Aurası & Müəllim", 
    page_icon="✨", 
    layout="wide"
)

# 2. Xüsusi Soft Bənövşəyi / Glassmorphism Dizayn (CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #F8F5FF 0%, #EEDFFD 100%);
        font-family: 'Poppins', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #EDE9FE;
        border-right: 1px solid #DDD6FE;
    }
    h1, h2, h3 {
        color: #4C1D95 !important;
        font-weight: 700;
    }
    div.stExpander, [data-testid="stMetricContainer"] {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(10px);
        border-radius: 16px !important;
        border: 1px solid #DDD6FE !important;
        box-shadow: 0 6px 20px rgba(109, 40, 217, 0.05) !important;
        padding: 12px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.25);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "my_study_aura_pro.json"

# 3. Yaddaş Mexanizmi
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user_name": "Tələbə", 
        "completed": [], 
        "delayed": {}, 
        "notes": [], 
        "scores": [],
        "rewards": []
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# 4. Profil və Menyu
st.sidebar.title("✨ Şəxsi Auran")
user_name = st.sidebar.text_input("Adın:", value=data.get("user_name", "Tələbə"))
if user_name != data.get("user_name"):
    data["user_name"] = user_name
    save_data(data)

st.sidebar.divider()
menu = st.sidebar.radio(
    "Menyu:", 
    [
        "🏠 Əsas Səhifə", 
        "📚 Müəllim Otağı", 
        "🔥 Günün Çətin Sualı", 
        "📅 Plan & Xəbərdarlıqlar", 
        "📊 Sınaq İzləyicisi", 
        "⏱️ Taymer & Fokus", 
        "📝 Səhv Qutusu"
    ]
)

# 5. DİM Modellərinə Uyğun Xırdalıqlar İlə Dərs İzahları
lessons_db = {
    "Riyaziyyat: Triqonometriya (Tələkəli Yerlər)": {
        "izah": "Nicat Baxışzadə üslubunda: Triqonometriyada ən çox bal aparan yer gətirmə düsturlarında işarə səhvidir. Unutma: rübə görə işarə müəyyən edilərkən İLKİN funksiyanın işarəsinə baxılır! Məsələn, cos(3π/2 - α) ifadəsində 3-cü rübdə kosinus mənfi olduğu üçün nəticə -sinα olur. Həmçinin sinx = a tənliyində |a| > 1 olduqda həllin olmadığını yaddan çıxarma.",
        "sual": "Hesablayın: sin(150°) * cos(120°)",
        "cavab": "-0.25"
    },
    "Azərbaycan Dili: Mətn & Açıq Suallar": {
        "izah": "DİM qiymətləndirmə meyarı: Mətndən cümləni olduğu kimi köçürmək 0 BAL deməkdir. Mütləq sinonimlərdən istifadə edərək öz sözlərinlə yazmalısan. Səbəb-nəticə cədvəlində səbəb xanasına hadisəni yaradan amili, nəticə xanasına isə yekun durumu yaz.",
        "sual": "Mətndəki 'əhali su çatışmazlığından əziyyət çəkirdi' fikrini öz sözlərinlə yaz:",
        "cavab": "sakinlər su qıtlığı ilə üzləşmişdi"
    },
    "İngilis Dili: Passive Voice & Tenses": {
        "izah": "Məchul növün qızıl qaydası: Zaman ƏSLA dəyişmir! Sadəcə cümləyə müvafiq zamanda 'To be' əlavə olunur və əsas feil Participle II (V3) formasına düşür. Məsələn: 'They build houses' -> 'Houses are built'.",
        "sual": "Çevir: 'They build houses every year.' -> Passive Voice:",
        "cavab": "Houses are built every year."
    }
}

# --- MENU BÖLMƏLƏRİ ---

# 1. Əsas Səhifə
if menu == "🏠 Əsas Səhifə":
    st.title(f"Xoş gəldin, {data['user_name']}! ✨")
    st.info("💡 **Günün Sİ Müəllim Mesajı:** Saatın və ya vaxtın önəmi yokdur. Nə vaxt daxil olursansa ol, əsas odur ki, hər gün buraya bir addım qatasan!")
    
    exam_date = datetime(2027, 6, 1)
    remaining_days = (exam_date - datetime.now()).days
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Tamamlananlar", len(data["completed"]))
    c2.metric("Təxirə Salınanlar", len(data["delayed"]))
    c3.metric("Mükafatların", len(data.get("rewards", [])))

    st.divider()
    st.subheader("🏆 Qazandığın Xüsusi Mükafatlar")
    if data.get("rewards"):
        for rw in data["rewards"]:
            st.success(f"🎁 {rw}")
    else:
        st.write("Hələ ki mükafat qazanmamısan. Günün çətin sualını həll et və şansını sına! 😉")

# 2. Müəllim Otağı
elif menu == "📚 Müəllim Otağı":
    st.title("📚 DİM İmtahan Modeli Dərs İzahları")
    sel = st.selectbox("Mövzu seç:", list(lessons_db.keys()))
    st.markdown(f"### 🎯 Mövzu İzahı: {sel}")
    st.write(lessons_db[sel]["izah"])

# 3. Günün Çətin Sualı & Şanslı Mükafat
elif menu == "🔥 Günün Çətin Sualı":
    st.title("🔥 DİM Səviyyəli Çətin Sual")
    st.write("Suala doğru cavab ver, 25% şansla mükafatı (1 saat telefon/kino) qazan!")

    challenge = lessons_db[list(lessons_db.keys())[0]]
    st.warning(f"📌 **Sual:** {challenge['sual']}")
    
    ans = st.text_input("Cavabınız:")
    if st.button("Cavabı Yoxla 🚀"):
        if challenge["cavab"].lower() in ans.lower():
            st.success("🎉 Təbriklər! Cavab Tamamilə DOĞRUDUR!")
            
            # ARADA BİR MÜKAFAT VERMƏK ÜÇÜN 25% ŞANS
            if random.randint(1, 100) <= 25:
                st.balloons()
                st.success("🎁 BƏXTİN GƏTİRDİ! 1 Saatlıq Telefon Vaxtı və ya Kino Mükafatı Qazandın!")
                rw_text = f"1 Saatlıq Telefon/Kino ({datetime.now().strftime('%d.%m')})"
                if rw_text not in data["rewards"]:
                    data["rewards"].append(rw_text)
                    save_data(data)
            else:
                st.info("⭐ Əla bilik! Bu dəfə mükafat düşmədi, amma bilik bazana bal əlavə olundu. Növbəti dəfə şansını yenidən sına!")
        else:
            st.error("❌ Yanlış cavab. Müəllim otağına keçib izahı yenidən oxu!")

# 4. Plan & Xəbərdarlıqlar
elif menu == "📅 Plan & Xəbərdarlıqlar":
    st.title("📅 Çevik Həftəlik Plan")
    weeks = {
        "1-ci Həftə": ["Riyaziyyat: Ədədlər və Hesab", "Azərbaycan dili: Fonetika", "İngilis dili: Nouns", "Mətn: 1 Bədii + 1 Reading"],
        "2-ci Həftə": ["Riyaziyyat: Tənasüb və Faiz", "Azərbaycan dili: Leksika", "İngilis dili: Articles", "Mətn: 1 Publisistik + 1 Reading"]
    }
    for w, tasks in weeks.items():
        with st.expander(f"📌 {w}", expanded=True):
            for t in tasks:
                col1, col2 = st.columns([0.75, 0.25])
                done = t in data["completed"]
                with col1:
                    if st.checkbox(t, value=done, key=f"c_{t}"):
                        if not done:
                            data["completed"].append(t)
                            data["delayed"].pop(t, None)
                            save_data(data)
                            st.rerun()
                    else:
                        if done:
                            data["completed"].remove(t)
                            save_data(data)
                            st.rerun()
                with col2:
                    if not done and t not in data["delayed"]:
                        if st.button("⏰ Təxirə Sal", key=f"d_{t}"):
                            data["delayed"][t] = datetime.now().strftime("%d.%m")
                            save_data(data)
                            st.rerun()

    if data["delayed"]:
        st.divider()
        st.subheader("⚠️ Xəbərdarlıq Edilən Borc Mövzular:")
        for t_name, t_date in list(data["delayed"].items()):
            c_d1, c_d2 = st.columns([0.8, 0.2])
            c_d1.error(f"Borc: {t_name} ({t_date})")
            if c_d2.button("Tamamla ✔️", key=f"fix_{t_name}"):
                data["delayed"].pop(t_name, None)
                data["completed"].append(t_name)
                save_data(data)
                st.rerun()

# 5. Sınaq İzləyicisi
elif menu == "📊 Sınaq İzləyicisi":
    st.title("📊 Sınaq Balları")
    with st.form("sc_form"):
        name = st.text_input("Sınaq Adı")
        m = st.number_input("Riyaziyyat", 0.0, 100.0)
        a = st.number_input("Azərbaycan Dili", 0.0, 100.0)
        e = st.number_input("İngilis Dili", 0.0, 100.0)
        if st.form_submit_button("Saxla"):
            data["scores"].append({"name": name or "Sınaq", "total": m+a+e, "date": datetime.now().strftime("%d.%m.%Y")})
            save_data(data)
            st.success("Qeyd olundu!")
            st.rerun()
    for sc in reversed(data["scores"]):
        st.info(f"📍 **{sc['name']}** ({sc['date']}) — **Ümumi: {sc['total']} Bal**")

# 6. Taymer
elif menu == "⏱️ Taymer & Fokus":
    st.title("⏱️ Çalışma Vaxtı")
    if st.button("165 Dəqiqəlik İmtahan Taymeri"):
        st.warning("İmtahan simulyasiyası başladı!")

# 7. Səhv Qutusu
elif menu == "📝 Səhv Qutusu":
    st.title("📝 Səhv Qutusu")
    nt = st.text_area("Unutmamaq istədiyin qayda və ya səhv:")
    if st.button("Qeyd Et") and nt:
        data["notes"].append({"text": nt, "date": datetime.now().strftime("%d.%m.%Y")})
        save_data(data)
        st.success("Saxlandı!")
    for n in reversed(data["notes"]):
        st.write(f"🔹 ({n['date']}): {n['text']}")

