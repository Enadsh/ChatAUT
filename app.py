import re
from datetime import datetime
import streamlit as st
from groq import Groq

st.set_page_config(page_title="ChatAUT", page_icon="🎓", layout="wide")

LOGO_B64 = "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"

# ── CSS: AUT Logo-Inspired Theme (Navy + Gold + Light Blue) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── RESET & BASE ── */
html, body, .stApp, [class*="st-"], * {
    font-family: 'Noto Kufi Arabic', 'Inter', sans-serif !important;
}
.stApp {
    background: #111d32 !important;
}
#MainMenu, footer, header, .stDeployButton { display: none !important; visibility: hidden !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111d32; }
::-webkit-scrollbar-thumb { background: #2c3e5a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #d4a843; }

/* ── HIDE DEFAULT CHAT AVATARS ── */
[data-testid="stChatMessageContainer"],
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"],
.stChatMessage { display: none !important; }

/* ── ANIMATIONS ── */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #0e1a2e !important;
    border-right: 1px solid #2c3e5a !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown label {
    color: #e8ecf1 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #e8ecf1 !important;
    border: 1px solid #2c3e5a !important;
    border-radius: 8px !important;
    width: 100%;
    transition: all 0.3s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #d4a843 !important;
    background: #1a2744 !important;
    color: #d4a843 !important;
}
/* Sidebar delete button - small and subtle */
section[data-testid="stSidebar"] button[kind="secondary"]:has(+ div) {
    font-size: 0.65rem !important;
}
/* Target delete buttons specifically by key pattern */
section[data-testid="stSidebar"] .stButton > button {
    font-size: 0.85rem !important;
}

/* Sidebar new-chat button override */
.sidebar-new-chat > button {
    background: transparent !important;
    color: #d4a843 !important;
    font-weight: 600 !important;
    border: 2px solid #d4a843 !important;
    padding: 10px 0 !important;
    font-size: 0.95rem !important;
}
.sidebar-new-chat > button:hover {
    background: #d4a84318 !important;
}

/* Active conversation button */
.conv-active > button {
    border-color: #d4a843 !important;
    border-left: 3px solid #d4a843 !important;
    background: #1a2744 !important;
    color: #d4a843 !important;
}

/* ── HEADER ── */
.aut-header {
    background: linear-gradient(135deg, #0e1a2e 0%, #1a2744 100%);
    border-radius: 0;
    padding: 14px 22px;
    margin-bottom: 4px;
    border-bottom: 2px solid #d4a843;
    display: flex;
    align-items: center;
    gap: 16px;
}
.aut-header img {
    width: 60px; height: 60px;
    border-radius: 50%;
    border: 2px solid #d4a843;
    flex-shrink: 0;
}
.aut-header-text { flex: 1; text-align: right; }
.aut-header-text h1 { font-size: 1.15rem; font-weight: 700; color: #ffffff; margin: 0 0 3px; }
.aut-header-text p { font-size: 0.78rem; color: #4a8fb8; margin: 0 0 5px; }
.aut-badge {
    background: #1a2744; color: #d4a843;
    font-size: 0.68rem; padding: 2px 10px;
    border-radius: 20px; display: inline-block;
    border: 1px solid #d4a84355;
}

/* ── DIVIDER ── */
.aut-divider {
    height: 2px;
    background: linear-gradient(90deg, #d4a843, #4a8fb8, #d4a843);
    margin: 0 0 16px; border: none;
}

/* ── CHAT CONTAINER ── */
#chat-box {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-bottom: 16px;
    padding: 8px 4px;
}

/* ── MESSAGE WRAPPERS ── */
.msg-wrapper-assistant {
    display: flex;
    justify-content: flex-end;
    animation: fadeSlideIn 0.4s ease-out;
}
.msg-wrapper-user {
    display: flex;
    justify-content: flex-start;
    animation: fadeSlideIn 0.4s ease-out;
}
.msg-inner {
    max-width: 85%;
}
.msg-inner-user {
    max-width: 75%;
}

/* ── ASSISTANT BUBBLE ── */
.msg-assistant {
    background: #1a2744;
    border: 1px solid #2c3e5a;
    border-right: 3px solid #d4a843;
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    color: #e8ecf1;
    font-size: 0.95rem;
    line-height: 1.8;
    direction: rtl;
    text-align: right;
}

/* ── USER BUBBLE ── */
.msg-user {
    background: #152236;
    border: 1px solid #2c3e5a;
    border-left: 3px solid #4a8fb8;
    border-radius: 16px 16px 16px 4px;
    padding: 14px 18px;
    color: #e8ecf1;
    font-size: 0.95rem;
    line-height: 1.8;
    direction: rtl;
    text-align: right;
}

/* ── MESSAGE LABELS ── */
.msg-label {
    font-size: 0.7rem;
    color: #d4a843;
    margin-bottom: 4px;
    text-align: right;
    direction: rtl;
    font-family: 'Inter', sans-serif !important;
}
.msg-label-user {
    font-size: 0.7rem;
    color: #4a8fb8;
    margin-bottom: 4px;
    text-align: right;
    direction: rtl;
    font-family: 'Inter', sans-serif !important;
}

/* ── TIMESTAMP ── */
.msg-time {
    font-size: 0.65rem;
    color: #6b7f99;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace !important;
}
.msg-time-right { text-align: right; }
.msg-time-left { text-align: left; }

/* ── WELCOME CARD ── */
.welcome-card {
    background: #1a2744;
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 14px;
    border: 1px solid #2c3e5a;
    border-right: 3px solid #d4a843;
    direction: rtl;
    text-align: right;
    transition: all 0.3s ease;
}
.welcome-card:hover {
    border-color: #d4a84388;
}
.welcome-card h3 {
    font-size: 0.95rem; font-weight: 700;
    color: #d4a843; margin: 0 0 10px;
}
.welcome-card ul {
    margin: 0; padding-right: 20px;
    color: #b0bfd0; font-size: 0.88rem; line-height: 2.2;
    list-style: none;
}
.welcome-card ul li {
    padding: 2px 0;
    transition: all 0.2s ease;
    cursor: default;
}
.welcome-card ul li:hover {
    color: #d4a843;
    padding-right: 6px;
}
.welcome-card ul li::before {
    content: "‣ ";
    color: #4a8fb8;
}

/* ── INPUT AREA ── */
.stChatInputContainer {
    background: #1a2744 !important;
    border: 1.5px solid #2c3e5a !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    transition: all 0.3s ease !important;
}
.stChatInputContainer:focus-within {
    border-color: #d4a843 !important;
    box-shadow: 0 0 8px #d4a84322 !important;
}
[data-testid="stChatInput"] {
    direction: rtl !important;
    text-align: right !important;
    color: #e8ecf1 !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"]::placeholder {
    color: #6b7f99 !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: #d4a843 !important;
    border-radius: 8px !important;
}

/* ── FOOTER ── */
.aut-footer {
    text-align: center;
    margin-top: 24px;
    padding: 14px 0 16px;
    border-top: 1px solid #2c3e5a;
}
.aut-footer p {
    font-size: 0.74rem; color: #6b7f99; margin: 0 0 3px; direction: ltr;
    font-family: 'Inter', sans-serif !important;
}
.aut-footer .dev-name {
    font-size: 0.75rem; font-weight: 600; direction: ltr;
    color: #d4a843;
}

/* ── SPINNER (hidden, replaced by typing indicator) ── */
.stSpinner { display: none !important; }

/* ── TYPING INDICATOR ── */
.typing-indicator {
    display: flex;
    justify-content: flex-end;
    padding: 0 4px;
    animation: fadeSlideIn 0.4s ease-out;
}
.typing-dots {
    background: #1a2744;
    border: 1px solid #2c3e5a;
    border-right: 3px solid #d4a843;
    border-radius: 16px 16px 4px 16px;
    padding: 14px 22px;
    display: flex;
    align-items: center;
    gap: 6px;
    direction: rtl;
}
.typing-dots span {
    width: 8px; height: 8px;
    background: #d4a843;
    border-radius: 50%;
    display: inline-block;
    animation: bounce 1.4s infinite ease-in-out both;
}
.typing-dots span:nth-child(1) { animation-delay: 0s; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
.typing-dots .typing-text {
    color: #6b7f99;
    font-size: 0.78rem;
    margin-right: 8px;
}
@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.4); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
}

/* ── HOVER EFFECTS ON BUBBLES ── */
.msg-assistant, .msg-user {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.msg-assistant:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(212, 168, 67, 0.15);
}
.msg-user:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(74, 143, 184, 0.15);
}

/* ── ONLINE STATUS ── */
.online-status {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.7rem;
    color: #4ade80;
    margin-right: 8px;
}
.online-dot {
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* ── MESSAGE COUNT BADGE ── */
.msg-count-badge {
    background: #d4a843;
    color: #0e1a2e;
    font-size: 0.6rem;
    font-weight: 700;
    padding: 1px 7px;
    border-radius: 10px;
    margin-right: 6px;
    display: inline-block;
    font-family: 'Inter', sans-serif !important;
}

/* ── DELETE CONVERSATION BUTTON ── */
.conv-delete-btn {
    background: transparent;
    border: none;
    color: #6b7f99;
    font-size: 1rem;
    cursor: pointer;
    padding: 2px 6px;
    border-radius: 4px;
    transition: all 0.2s ease;
    line-height: 1;
}
.conv-delete-btn:hover {
    color: #ef4444;
    background: #ef444418;
}
.conv-row {
    display: flex;
    align-items: center;
    gap: 4px;
}
.conv-row > div:first-child { flex: 1; }

/* ── CLICKABLE SUGGESTIONS ── */
.suggestion-btn {
    background: transparent;
    border: 1px solid #2c3e5a;
    color: #b0bfd0;
    padding: 8px 16px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 0.88rem;
    text-align: right;
    direction: rtl;
    width: 100%;
    transition: all 0.25s ease;
    font-family: 'Noto Kufi Arabic', sans-serif;
    margin-bottom: 6px;
    display: block;
}
.suggestion-btn:hover {
    border-color: #d4a843;
    color: #d4a843;
    background: #d4a84312;
    padding-right: 22px;
}
.suggestion-btn::before {
    content: "‣ ";
    color: #4a8fb8;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    st.session_state.active_conv = None
    st.session_state.conv_counter = 0

# Initialize first conversation if needed
if st.session_state.active_conv is None:
    st.session_state.conv_counter += 1
    conv_id = st.session_state.conv_counter
    st.session_state.active_conv = conv_id
    st.session_state.conversations[conv_id] = [
        {
            "role": "assistant",
            "content": "أهلاً بك في نظام المساعد الأكاديمي لجامعة العقبة للتكنولوجيا.\n\nيمكنني مساعدتك في:\n- معلومات المواد الدراسية والتخصصات\n- متطلبات التسجيل والقبول\n- الجداول الدراسية والأنظمة الأكاديمية\n- أي استفسار يتعلق بدراستك في الجامعة\n\nكيف أقدر أساعدك؟",
            "time": datetime.now().strftime("%H:%M"),
        }
    ]

messages = st.session_state.conversations[st.session_state.active_conv]

# ── SIDEBAR ──
with st.sidebar:
    # Logo section
    st.markdown(f"""
    <div style="text-align:center; padding: 16px 0 8px;">
        <img src="data:image/webp;base64,{LOGO_B64}" alt="AUT"
             style="width:72px; height:72px; border-radius:50%;
                    border: 2px solid #d4a843;" />
        <h2 style="color:#ffffff; font-size:1.1rem; margin:10px 0 2px;
                   font-family:'Noto Kufi Arabic',sans-serif !important;">ChatAUT</h2>
        <p style="color:#4a8fb8; font-size:0.72rem; margin:0;
                 font-family:'Noto Kufi Arabic',sans-serif !important;">Academic AI Assistant</p>
    </div>
    <hr style="border:none; height:1px; background: #2c3e5a; margin:8px 0 16px;" />
    """, unsafe_allow_html=True)

    # New Chat button
    st.markdown('<div class="sidebar-new-chat">', unsafe_allow_html=True)
    if st.button("محادثة جديدة   +", key="new_chat", use_container_width=True):
        st.session_state.conv_counter += 1
        conv_id = st.session_state.conv_counter
        st.session_state.active_conv = conv_id
        st.session_state.conversations[conv_id] = [
            {
                "role": "assistant",
                "content": "أهلاً بك في نظام المساعد الأكاديمي لجامعة العقبة للتكنولوجيا.\n\nيمكنني مساعدتك في:\n- معلومات المواد الدراسية والتخصصات\n- متطلبات التسجيل والقبول\n- الجداول الدراسية والأنظمة الأكاديمية\n- أي استفسار يتعلق بدراستك في الجامعة\n\nكيف أقدر أساعدك؟",
                "time": datetime.now().strftime("%H:%M"),
            }
        ]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Conversation history
    st.markdown("""
    <p style="color:#d4a843; font-size:0.75rem; margin:16px 0 8px; padding:0 4px;
              font-family:'Noto Kufi Arabic',sans-serif !important;">المحادثات السابقة</p>
    """, unsafe_allow_html=True)

    for cid in sorted(st.session_state.conversations.keys(), reverse=True):
        conv_msgs = st.session_state.conversations[cid]
        # Find first user message for label
        label = "محادثة جديدة"
        for m in conv_msgs:
            if m["role"] == "user":
                label = m["content"][:30] + ("..." if len(m["content"]) > 30 else "")
                break

        msg_count = len(conv_msgs)
        is_active = cid == st.session_state.active_conv
        wrapper_class = "conv-active" if is_active else ""

        # Conversation button with badge
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        btn_label = f"{label}  ({msg_count})"
        if st.button(btn_label, key=f"conv_{cid}", use_container_width=True):
            st.session_state.active_conv = cid
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Delete button right under, small and aligned
        if st.button("🗑 حذف", key=f"del_{cid}"):
            del st.session_state.conversations[cid]
            if st.session_state.active_conv == cid:
                remaining = sorted(st.session_state.conversations.keys())
                if remaining:
                    st.session_state.active_conv = remaining[-1]
                else:
                    st.session_state.conv_counter += 1
                    new_id = st.session_state.conv_counter
                    st.session_state.active_conv = new_id
                    st.session_state.conversations[new_id] = [
                        {
                            "role": "assistant",
                            "content": "أهلاً بك في نظام المساعد الأكاديمي لجامعة العقبة للتكنولوجيا.\n\nيمكنني مساعدتك في:\n- معلومات المواد الدراسية والتخصصات\n- متطلبات التسجيل والقبول\n- الجداول الدراسية والأنظمة الأكاديمية\n- أي استفسار يتعلق بدراستك في الجامعة\n\nكيف أقدر أساعدك؟",
                            "time": datetime.now().strftime("%H:%M"),
                        }
                    ]
            st.rerun()

    # Clear conversation (no temperature slider)
    st.markdown("""
    <hr style="border:none; height:1px; background: #2c3e5a; margin:20px 0 12px;" />
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:12px;">', unsafe_allow_html=True)
    if st.button("مسح المحادثة الحالية", key="clear_conv", use_container_width=True):
        st.session_state.conversations[st.session_state.active_conv] = [
            {
                "role": "assistant",
                "content": "أهلاً بك في نظام المساعد الأكاديمي لجامعة العقبة للتكنولوجيا.\n\nيمكنني مساعدتك في:\n- معلومات المواد الدراسية والتخصصات\n- متطلبات التسجيل والقبول\n- الجداول الدراسية والأنظمة الأكاديمية\n- أي استفسار يتعلق بدراستك في الجامعة\n\nكيف أقدر أساعدك؟",
                "time": datetime.now().strftime("%H:%M"),
            }
        ]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── HEADER ──
st.markdown(f"""
<div class="aut-header">
    <img src="data:image/webp;base64,{LOGO_B64}" alt="AUT"/>
    <div class="aut-header-text">
        <h1>جامعة العقبة للتكنولوجيا</h1>
        <p>Aqaba University of Technology</p>
        <span class="aut-badge">Academic AI Assistant — مركز الحاسوب</span>
        <span class="online-status"><span class="online-dot"></span> متصل</span>
    </div>
</div>
<hr class="aut-divider"/>
""", unsafe_allow_html=True)

# ── GROQ CLIENT ──
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Re-read messages for active conversation
messages = st.session_state.conversations[st.session_state.active_conv]

# ── WELCOME CARD WITH CLICKABLE SUGGESTIONS ──
SUGGESTIONS = [
    "ما تخصصات قسم الحاسوب المتاحة؟",
    "ما متطلبات التسجيل في الجامعة؟",
    "كيف أتواصل مع الإرشاد الأكاديمي؟",
    "ما نظام الساعات المعتمدة في الجامعة؟",
]
if len(messages) == 1:
    st.markdown("""
    <div class="welcome-card">
        <h3>أسئلة يمكنك البدء بها:</h3>
    </div>
    """, unsafe_allow_html=True)
    for i, suggestion in enumerate(SUGGESTIONS):
        if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            now = datetime.now().strftime("%H:%M")
            messages.append({"role": "user", "content": suggestion, "time": now})
            st.session_state._pending_question = suggestion
            st.rerun()


# ── RENDER CONTENT ──
def render_content(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.replace('\n', '<br>')
    return text


# ── RENDER CHAT ──
chat_html = '<div id="chat-box">'
for msg in messages:
    content = render_content(msg["content"])
    timestamp = msg.get("time", "")
    if msg["role"] == "assistant":
        chat_html += f'''
        <div class="msg-wrapper-assistant">
            <div class="msg-inner">
                <div class="msg-label">المساعد الأكاديمي</div>
                <div class="msg-assistant">{content}</div>
                <div class="msg-time msg-time-right">{timestamp}</div>
            </div>
        </div>'''
    else:
        chat_html += f'''
        <div class="msg-wrapper-user">
            <div class="msg-inner-user">
                <div class="msg-label-user">أنت</div>
                <div class="msg-user">{content}</div>
                <div class="msg-time msg-time-left">{timestamp}</div>
            </div>
        </div>'''
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── PROCESS QUESTION (from chat input or suggestion click) ──
def process_question(question_text):
    """Send question to Groq and append the answer."""
    # Show typing indicator
    typing_html = '''
    <div class="typing-indicator">
        <div class="typing-dots">
            <span class="typing-text">يكتب...</span>
            <span></span><span></span><span></span>
        </div>
    </div>
    '''
    typing_placeholder = st.empty()
    typing_placeholder.markdown(typing_html, unsafe_allow_html=True)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "أنت مساعد أكاديمي رسمي لجامعة العقبة للتكنولوجيا في محافظة العقبة، الأردن.\n\nقواعد صارمة يجب اتباعها دائماً:\n1. جميع ردودك يجب أن تكون باللغة العربية فقط.\n2. ممنوع منعاً باتاً استخدام أي لغة أخرى: لا صينية، لا إنجليزية، لا فرنسية، لا أي لغة غير العربية.\n3. لا تكتب أي حرف غير عربي إطلاقاً (لا Latin، لا Chinese، لا Japanese، لا Korean، لا أي رموز أجنبية).\n4. إذا طلب المستخدم الرد بلغة أخرى، ارفض بأدب وأجب بالعربية فقط.\n5. أجب بأسلوب أكاديمي واضح ومختصر.\n6. إذا لم تعرف إجابة دقيقة، وجّه الطالب للتواصل مع الجهة المختصة في الجامعة.\n\nتذكر: العربية فقط في كل كلمة وكل حرف."
            },
            *[{"role": m["role"], "content": m["content"]} for m in messages]
        ]
    )
    answer = response.choices[0].message.content
    answer = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u0660-\u0669\s\d\.\,\:\;\!\?\-\(\)\*\#\n\r]', '', answer)
    answer = re.sub(r'\n{3,}', '\n\n', answer).strip()
    messages.append({"role": "assistant", "content": answer, "time": datetime.now().strftime("%H:%M")})
    typing_placeholder.empty()

# Handle pending suggestion question
if hasattr(st.session_state, '_pending_question') and st.session_state._pending_question:
    pending_q = st.session_state._pending_question
    st.session_state._pending_question = None
    process_question(pending_q)
    st.rerun()

# ── CHAT INPUT ──
if question := st.chat_input("اكتب سؤالك هنا..."):
    now = datetime.now().strftime("%H:%M")
    messages.append({"role": "user", "content": question, "time": now})
    process_question(question)
    st.rerun()

# ── AUTO-SCROLL TO LATEST MESSAGE ──
st.markdown("""
<script>
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
        chatBox.scrollIntoView({behavior: 'smooth', block: 'end'});
    }
    // Fallback: scroll the main container
    window.setTimeout(function() {
        const main = window.parent.document.querySelector('section.main');
        if (main) main.scrollTop = main.scrollHeight;
    }, 300);
</script>
""", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="aut-footer">
    <p>Aqaba University of Technology — Computer Center | All Rights Reserved © 2026</p>
    <span class="dev-name">Developed by Enad Alshoubaki</span>
</div>
""", unsafe_allow_html=True)
