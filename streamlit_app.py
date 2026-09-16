import streamlit as st
from openai import OpenAI

# OpenAI API interfeysi (API açarınızı daxil edin)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

st.set_page_config(page_title="A1 Eng-Rus Tutor", page_icon="🔤")
st.title("🔤 A1 İngilis-Rus Tərcümə Yoxlayıcısı")

# Tərcümə rejiminin seçilməsi
direction = st.radio("Tərcümə istiqamətini seçin:", ["İngilis ➔ Rus", "Rus ➔ İngilis"])

# Sessiya yaddaşının sıfırlanması
if "current_sentence" not in st.session_state:
    st.session_state.current_sentence = ""

# A1 cümləsi yaradan funksiya
def generate_sentence():
    source_lang = "English" if direction == "İngilis ➔ Rus" else "Russian"
    prompt = f"Provide one short, extremely simple A1 level sentence in {source_lang}. Do NOT include translation or explanations, just the sentence."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    st.session_state.current_sentence = response.choices[0].message.content.strip()

# Yeni cümlə düyməsi
if st.button("🎯 Yeni Cümlə Ver") or not st.session_state.current_sentence:
    generate_sentence()

st.info(f"**Tərcümə edin:** {st.session_state.current_sentence}")

# İstifadəçi daxil etmə sahəsi
user_input = st.text_input("Tərcümənizi bura yazın:")

if st.button("✅ Cavabı Yoxla"):
    if user_input:
        target_lang = "Russian" if direction == "İngilis ➔ Rus" else "English"
        check_prompt = f"""
        Source sentence: {st.session_state.current_sentence}
        User translation: {user_input}
        Target language: {target_lang}
        
        Evaluate the user's translation strictly for A1 level grammar and vocabulary.
        Provide response in Azerbaijani with these sections:
        1. **Nəticə:** (Düzgün / Hissəvi düzgün / Səhv)
        2. **İdeal Tərcümə:**
        3. **İzah:** (Səhvlər varsa sadə dildə izah edin).
        """
        
        with st.spinner("AI tərcüməni yoxlayır..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": check_prompt}]
            )
            st.success("Yoxlama Yekunlaşdı:")
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("Lütfən, əvvəlcə tərcümənizi yazın.")
