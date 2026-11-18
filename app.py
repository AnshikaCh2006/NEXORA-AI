import html
import json
import os
import uuid
import requests
import streamlit as st

# ==================================================
# 1. APP CONFIGURATION
# ==================================================

APP_NAME = "NEXORA"
BRAND_ICON = "✦"
AI_AVATAR = ":material/auto_awesome:"
USER_AVATAR = ":material/person:"

MODEL = "openai/gpt-oss-120b"
MODEL_DISPLAY = "gpt-oss-120b"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are NEXORA, a smart, friendly and helpful AI assistant.

Instructions:
- Give accurate and useful answers.
- Explain complex topics in simple language.
- Help with programming, debugging and technical subjects.
- Use Markdown for headings, lists and formatting.
- Use code blocks for programming examples.
- Use $...$ for inline mathematical formulas.
- Use $$...$$ for block mathematical formulas.
- Never use \\( \\) or \\[ \\] delimiters.
- Be natural, professional and conversational.
"""

SUGGESTIONS = [
    {
        "title": "Deep Learning",
        "prompt": "Explain how a transformer works",
        "icon": ":material/psychology:",
    },
    {
        "title": "Python Code",
        "prompt": "Write a Python function to reverse a string",
        "icon": ":material/code:",
    },
    {
        "title": "Career Prep",
        "prompt": "Give me tips for a technical interview",
        "icon": ":material/tips_and_updates:",
    },
    {
        "title": "Automation",
        "prompt": "Explain the basics of PLC programming",
        "icon": ":material/memory:",
    },
]

# ==================================================
# 2. PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# 3. CUSTOM CSS — OBSIDIAN GLASS & LUMINOUS VIOLET
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --bg-canvas: #0B0D14;
    --bg-sidebar: #0F111A;
    --bg-surface: rgba(255, 255, 255, 0.032);
    --bg-surface-hover: rgba(139, 92, 246, 0.09);
    --bg-elevated: #151824;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-accent: rgba(139, 92, 246, 0.42);
    --text-primary: #F3F4F6;
    --text-secondary: #9CA3AF;
    --text-muted: #6B7280;
    --accent: #8B5CF6;
    --accent-soft: #C4B5FD;
    --accent-indigo: #6366F1;
    --online: #10B981;
}

/* GLOBAL TYPOGRAPHY & CANVAS */

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-canvas);
    background-image:
        radial-gradient(ellipse 75% 45% at 50% -8%, rgba(139, 92, 246, 0.16), transparent 65%),
        radial-gradient(ellipse 45% 35% at 85% 12%, rgba(99, 102, 241, 0.08), transparent 60%);
    background-attachment: fixed;
    color: var(--text-primary);
}

.block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 860px !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 1.5rem !important;
    padding-bottom: 8.5rem !important;
}

/* CLEAN CHROME WHILE KEEPING SIDEBAR TOGGLE ACCESSIBLE */

#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}

[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {
    color: var(--text-secondary) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="collapsedControl"] button:hover {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #FFFFFF !important;
}

/* =========================================
   SIDEBAR
   ========================================= */

[data-testid="stSidebar"] {
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border-subtle);
}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-top: 1.1rem;
    padding-bottom: 1.25rem;
}

.brand-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 4px 2px 18px 2px;
}

.brand-orb {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #FFFFFF;
    box-shadow: 0 0 22px rgba(139, 92, 246, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.35);
    flex-shrink: 0;
}

.brand-meta {
    display: flex;
    flex-direction: column;
    line-height: 1.15;
}

.brand-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1.6px;
    color: #FFFFFF;
}

.brand-title span {
    color: var(--accent-soft);
}

.brand-sub {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 2px;
}

/* SIDEBAR PRIMARY NEW CHAT BUTTON */

.st-key-new_chat_btn button {
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.28) !important;
    transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

.st-key-new_chat_btn button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 26px rgba(139, 92, 246, 0.42) !important;
    filter: brightness(1.06) !important;
}

/* SIDEBAR SECTION HEADER */

.sidebar-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 18px 2px 10px 2px;
}

.sidebar-section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--text-muted);
}

.sidebar-count-pill {
    font-size: 11px;
    font-weight: 600;
    color: var(--accent-soft);
    background: rgba(139, 92, 246, 0.14);
    border: 1px solid rgba(139, 92, 246, 0.25);
    padding: 1px 8px;
    border-radius: 999px;
}

/* SIDEBAR CONVERSATION ITEMS */

[class*="st-key-open_"] button,
[class*="st-key-active_chat_"] button {
    justify-content: flex-start !important;
    text-align: left !important;
    min-height: 38px !important;
    padding: 6px 11px !important;
    border-radius: 10px !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
}

[class*="st-key-open_"] button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--text-secondary) !important;
}

[class*="st-key-open_"] button:hover {
    background: rgba(255, 255, 255, 0.045) !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.06) !important;
}

[class*="st-key-active_chat_"] button {
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.18) 0%, rgba(99, 102, 241, 0.08) 100%) !important;
    border: 1px solid rgba(139, 92, 246, 0.35) !important;
    border-left: 3px solid #A78BFA !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

[class*="st-key-delete_"] button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--text-muted) !important;
    min-height: 38px !important;
    padding: 4px 6px !important;
    border-radius: 10px !important;
    transition: all 0.18s ease !important;
}

[class*="st-key-delete_"] button:hover {
    background: rgba(239, 68, 68, 0.14) !important;
    border-color: rgba(239, 68, 68, 0.3) !important;
    color: #FCA5A5 !important;
}

/* SIDEBAR DIVIDER, EXPANDER & DOWNLOAD */

.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent);
    margin: 16px 0;
}

[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] [data-testid="stDownloadButton"] button {
    background: rgba(255, 255, 255, 0.035) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 11px !important;
    min-height: 40px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] [data-testid="stDownloadButton"] button:hover {
    background: rgba(139, 92, 246, 0.14) !important;
    border-color: var(--border-accent) !important;
    color: #FFFFFF !important;
}

.sidebar-footer-card {
    margin-top: 12px;
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.status-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 7px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--online);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    animation: pulseDot 2.2s infinite;
}

.model-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    color: var(--accent-soft);
    background: rgba(139, 92, 246, 0.14);
    border: 1px solid rgba(139, 92, 246, 0.25);
    padding: 2px 7px;
    border-radius: 6px;
}

.powered-by {
    font-size: 11.5px;
    color: var(--text-muted);
}

/* =========================================
   TOP CHAT CONTEXT BAR
   ========================================= */

.chat-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 10px 16px;
    margin-bottom: 18px;
    border-radius: 14px;
    background: rgba(21, 24, 36, 0.72);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
}

.chat-topbar-left {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.chat-topbar-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14.5px;
    font-weight: 700;
    color: #FFFFFF;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.chat-topbar-right {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}

.meta-pill {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border-subtle);
    padding: 3px 10px;
    border-radius: 999px;
}

.meta-pill-accent {
    color: var(--accent-soft);
    background: rgba(139, 92, 246, 0.14);
    border-color: rgba(139, 92, 246, 0.28);
}

/* =========================================
   HERO / EMPTY STATE
   ========================================= */

.hero-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    padding: 6vh 16px 24px 16px;
    animation: fadeInUp 0.45s ease-out;
}

.hero-emblem {
    width: 60px;
    height: 60px;
    margin: 0 auto 20px auto;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.24) 0%, rgba(99, 102, 241, 0.14) 100%);
    border: 1px solid rgba(167, 139, 250, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    color: #DDD6FE;
    box-shadow: 0 0 40px rgba(139, 92, 246, 0.26), inset 0 1px 0 rgba(255, 255, 255, 0.22);
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(32px, 4.2vw, 44px);
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -1.1px;
    text-align: center !important;
    width: 100%;
    margin: 0 auto 12px auto !important;
    padding: 0 !important;
    background: linear-gradient(180deg, #FFFFFF 20%, #C4B5FD 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: var(--text-secondary);
    font-size: 15.5px;
    line-height: 1.65;
    max-width: 540px;
    width: 100%;
    text-align: center !important;
    margin: 0 auto 22px auto !important;
    padding: 0 !important;
}

.hero-subtitle strong {
    color: #E5E7EB;
    font-weight: 600;
}

.hero-chips {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 8px;
    width: 100%;
    margin: 0 auto 10px auto;
}

.hero-chip {
    font-size: 12px;
    font-weight: 500;
    color: #D1D5DB;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid var(--border-subtle);
    padding: 5px 12px;
    border-radius: 999px;
}

.hero-chip span {
    color: var(--accent-soft);
    margin-right: 4px;
}

.suggestions-label {
    width: 100%;
    text-align: center !important;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 12px auto 14px auto;
}

/* SUGGESTION CARDS */

[class*="st-key-suggestion_"] button {
    background: rgba(21, 24, 36, 0.85) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    min-height: 78px !important;
    padding: 15px 18px !important;
    justify-content: flex-start !important;
    text-align: left !important;
    align-items: flex-start !important;
    gap: 10px !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.22) !important;
    transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

[class*="st-key-suggestion_"] button [data-testid="stIconMaterial"] {
    color: #A78BFA !important;
    margin-top: 2px !important;
}

[class*="st-key-suggestion_"] button p {
    font-size: 14px !important;
    line-height: 1.45 !important;
    text-align: left !important;
    white-space: normal !important;
}

[class*="st-key-suggestion_"] button:hover {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.14) 0%, rgba(21, 24, 36, 0.95) 100%) !important;
    border-color: rgba(167, 139, 250, 0.48) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(139, 92, 246, 0.16) !important;
    color: #FFFFFF !important;
}

/* =========================================
   CHAT MESSAGES
   ========================================= */

[data-testid="stChatMessage"] {
    padding: 16px 20px !important;
    border-radius: 18px !important;
    margin-bottom: 14px !important;
    gap: 14px !important;
    animation: fadeInUp 0.28s ease-out;
}

/* USER MESSAGE CARD */

[class*="st-key-msg_user_"] [data-testid="stChatMessage"] {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(99, 102, 241, 0.07) 100%) !important;
    border: 1px solid rgba(139, 92, 246, 0.24) !important;
}

[class*="st-key-msg_user_"] [data-testid="stChatMessageAvatarCustom"],
[class*="st-key-msg_user_"] [data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #2B3044 0%, #1E2233 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    color: #E5E7EB !important;
    border-radius: 11px !important;
}

/* ASSISTANT MESSAGE CARD */

[class*="st-key-msg_ai_"] [data-testid="stChatMessage"] {
    background: rgba(21, 24, 36, 0.72) !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.16) !important;
}

[class*="st-key-msg_ai_"] [data-testid="stChatMessageAvatarCustom"],
[class*="st-key-msg_ai_"] [data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    color: #FFFFFF !important;
    border-radius: 11px !important;
    box-shadow: 0 0 16px rgba(139, 92, 246, 0.35) !important;
}

/* MESSAGE TYPOGRAPHY & MARKDOWN */

[data-testid="stChatMessageContent"] {
    font-size: 15px !important;
    line-height: 1.72 !important;
    color: #EDF0F7 !important;
}

[data-testid="stChatMessageContent"] p {
    margin-bottom: 0.7rem;
}

[data-testid="stChatMessageContent"] p:last-child {
    margin-bottom: 0;
}

[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    margin-top: 1.1rem;
    margin-bottom: 0.5rem;
}

[data-testid="stChatMessageContent"] code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.86em !important;
    background: rgba(139, 92, 246, 0.16) !important;
    color: #DDD6FE !important;
    padding: 0.15em 0.45em !important;
    border-radius: 6px !important;
}

[data-testid="stChatMessageContent"] pre {
    background: #0B0E16 !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
}

[data-testid="stChatMessageContent"] pre code {
    background: transparent !important;
    color: #E5E7EB !important;
    padding: 0 !important;
}

[data-testid="stChatMessageContent"] blockquote {
    border-left: 3px solid var(--accent) !important;
    background: rgba(139, 92, 246, 0.07) !important;
    padding: 10px 14px !important;
    border-radius: 0 10px 10px 0 !important;
    color: #D1D5DB !important;
}

[data-testid="stChatMessageContent"] table {
    border-collapse: collapse;
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}

[data-testid="stChatMessageContent"] th {
    background: rgba(139, 92, 246, 0.12);
    color: #FFFFFF;
    font-weight: 600;
}

[data-testid="stChatMessageContent"] td,
[data-testid="stChatMessageContent"] th {
    border: 1px solid var(--border-subtle);
    padding: 8px 12px;
}

/* THINKING INDICATOR */

.thinking-indicator {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--accent-soft);
    font-size: 14px;
    font-weight: 500;
    padding: 4px 0;
}

.thinking-dots {
    display: inline-flex;
    gap: 4px;
}

.thinking-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #A78BFA;
    animation: bounceDot 1.2s infinite ease-in-out;
}

.thinking-dots span:nth-child(2) {
    animation-delay: 0.16s;
}

.thinking-dots span:nth-child(3) {
    animation-delay: 0.32s;
}

/* ACTION BAR BELOW LATEST RESPONSE */

.st-key-regen_btn button,
.st-key-clear_main_btn button {
    background: rgba(255, 255, 255, 0.03) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 999px !important;
    min-height: 34px !important;
    padding: 4px 14px !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.st-key-regen_btn button:hover {
    background: rgba(139, 92, 246, 0.14) !important;
    border-color: var(--border-accent) !important;
    color: #FFFFFF !important;
}

.st-key-clear_main_btn button:hover {
    background: rgba(239, 68, 68, 0.12) !important;
    border-color: rgba(239, 68, 68, 0.35) !important;
    color: #FCA5A5 !important;
}

/* =========================================
   FLOATING GLASSMORPHIC CHAT INPUT
   ========================================= */

[data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(11, 13, 20, 0) 0%, rgba(11, 13, 20, 0.92) 32%, #0B0D14 100%) !important;
    padding-top: 18px !important;
    padding-bottom: 12px !important;
}

[data-testid="stBottomBlockContainer"] {
    max-width: 860px !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 0 !important;
}

[data-testid="stChatInput"] {
    background: rgba(21, 24, 36, 0.92) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 22px !important;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(139, 92, 246, 0.65) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.18), 0 14px 40px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stChatInput"] textarea {
    color: #F9FAFB !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
    color: #FFFFFF !important;
    border-radius: 14px !important;
    transition: all 0.18s ease !important;
}

[data-testid="stChatInputSubmitButton"]:hover:not(:disabled) {
    filter: brightness(1.12) !important;
    transform: scale(1.03) !important;
}

/* LINKS & SCROLLBAR */

a {
    color: #C4B5FD !important;
    text-decoration-color: rgba(196, 181, 253, 0.4) !important;
}

a:hover {
    color: #DDD6FE !important;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.14);
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(139, 92, 246, 0.45);
}

/* ANIMATIONS */

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulseDot {
    0%, 100% {
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
    }
    50% {
        box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.05);
    }
}

@keyframes bounceDot {
    0%, 80%, 100% {
        transform: scale(0.65);
        opacity: 0.45;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. API KEY CONFIGURATION
# ==================================================

def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


API_KEY = get_api_key()

if not API_KEY:
    st.error(
        "Groq API key not found. "
        "Please configure GROQ_API_KEY in Streamlit secrets."
    )
    st.stop()


# ==================================================
# 5. SESSION STATE
# ==================================================

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {
        "title": "New chat",
        "messages": [],
    }
    st.session_state.current = cid

if "pending" not in st.session_state:
    st.session_state.pending = None

if "regen" not in st.session_state:
    st.session_state.regen = False

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7


# ==================================================
# 6. CHAT FUNCTIONS
# ==================================================

def new_chat():
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {
        "title": "New chat",
        "messages": [],
    }
    st.session_state.current = cid


def delete_chat(cid):
    if cid in st.session_state.chats:
        del st.session_state.chats[cid]

    if not st.session_state.chats:
        new_chat()
    elif st.session_state.current == cid:
        st.session_state.current = next(iter(st.session_state.chats))


def clear_current_chat():
    chat = st.session_state.chats[st.session_state.current]
    chat["messages"] = []
    chat["title"] = "New chat"


def regenerate():
    chat = st.session_state.chats[st.session_state.current]
    if chat["messages"] and chat["messages"][-1]["role"] == "assistant":
        chat["messages"].pop()
    st.session_state.regen = True


def build_transcript(chat_item):
    lines = [f"# {chat_item['title']}\n"]
    for msg in chat_item["messages"]:
        role_label = "NEXORA" if msg["role"] == "assistant" else "YOU"
        lines.append(f"## {role_label}\n{msg['content']}")
    return "\n\n---\n\n".join(lines)


# ==================================================
# 7. GROQ STREAMING API
# ==================================================

def stream_chat(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ] + messages,
        "temperature": st.session_state.temperature,
        "stream": True,
    }

    with requests.post(
        API_URL,
        headers=headers,
        json=payload,
        stream=True,
        timeout=(15, 180),
    ) as response:

        if response.status_code != 200:
            raise RuntimeError(
                f"Groq API Error {response.status_code}: "
                f"{response.text[:1000]}"
            )

        for line in response.iter_lines():
            if not line:
                continue

            if isinstance(line, bytes):
                line = line.decode("utf-8", errors="ignore")

            if not line.startswith("data:"):
                continue

            data = line[5:].strip()

            if data == "[DONE]":
                break

            try:
                event = json.loads(data)
                choices = event.get("choices", [])
                if not choices:
                    continue

                content = choices[0].get("delta", {}).get("content")
                if isinstance(content, str) and content:
                    yield content

            except (json.JSONDecodeError, KeyError, IndexError):
                continue


# ==================================================
# 8. AI RESPONSE
# ==================================================

def respond(chat_id):
    chat = st.session_state.chats[chat_id]

    with st.container(key="msg_ai_live"):
        with st.chat_message("assistant", avatar=AI_AVATAR):
            placeholder = st.empty()
            full_response = ""

            try:
                placeholder.markdown(
                    """
                    <div class="thinking-indicator">
                        <span>✦ NEXORA is thinking</span>
                        <span class="thinking-dots">
                            <span></span><span></span><span></span>
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                for token in stream_chat(chat["messages"]):
                    full_response += token
                    placeholder.markdown(full_response + " ▍")

                placeholder.markdown(full_response)

                if full_response:
                    chat["messages"].append({
                        "role": "assistant",
                        "content": full_response,
                    })

            except Exception as error:
                placeholder.empty()
                st.error(f"API Error: {error}")


# ==================================================
# 9. SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown(
        f"""
        <div class="brand-card">
            <div class="brand-orb">{BRAND_ICON}</div>
            <div class="brand-meta">
                <div class="brand-title">{APP_NAME}<span>.</span></div>
                <div class="brand-sub">AI Workspace</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "New chat",
        key="new_chat_btn",
        icon=":material/add:",
        type="primary",
        use_container_width=True,
    ):
        new_chat()
        st.rerun()

    st.markdown(
        f"""
        <div class="sidebar-section-header">
            <span class="sidebar-section-title">Conversations</span>
            <span class="sidebar-count-pill">{len(st.session_state.chats)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for cid, item in reversed(list(st.session_state.chats.items())):
        col1, col2 = st.columns([5.2, 1], gap="small")
        is_active = cid == st.session_state.current
        btn_key = f"active_chat_{cid}" if is_active else f"open_{cid}"

        if col1.button(
            item["title"],
            key=btn_key,
            icon=":material/chat_bubble_outline:",
            use_container_width=True,
        ):
            st.session_state.current = cid
            st.rerun()

        if col2.button(
            "",
            key=f"delete_{cid}",
            icon=":material/close:",
            help="Delete conversation",
            use_container_width=True,
        ):
            delete_chat(cid)
            st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    with st.expander("Model settings", icon=":material/tune:", expanded=False):
        st.session_state.temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.2,
            value=st.session_state.temperature,
            step=0.1,
            help="Lower values are more focused and deterministic; higher values are more creative.",
        )

    current_chat = st.session_state.chats[st.session_state.current]

    if current_chat["messages"]:
        st.download_button(
            "Export conversation",
            data=build_transcript(current_chat),
            file_name="nexora_chat.md",
            mime="text/markdown",
            icon=":material/download:",
            use_container_width=True,
        )

    st.markdown(
        f"""
        <div class="sidebar-footer-card">
            <div class="status-row">
                <span class="status-indicator">
                    <span class="status-dot"></span>
                    Online
                </span>
                <span class="model-chip">{MODEL_DISPLAY}</span>
            </div>
            <div class="powered-by">✦ {APP_NAME} AI · Powered by Groq</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# 10. MAIN CHAT PAGE
# ==================================================

chat_id = st.session_state.current
chat = st.session_state.chats[chat_id]

# HOME SCREEN (EMPTY STATE)

if not chat["messages"]:
    st.markdown(
        f"""
        <div class="hero-wrapper">
            <div class="hero-emblem">{BRAND_ICON}</div>
            <div class="hero-title" role="heading" aria-level="1">What can I help with?</div>
            <div class="hero-subtitle">
                Welcome to <strong>{APP_NAME}</strong> — your fast, intelligent AI companion for
                code, explanations, math, and technical problem solving.
            </div>
            <div class="hero-chips">
                <span class="hero-chip"><span>✦</span>Code &amp; Debugging</span>
                <span class="hero-chip"><span>✦</span>Math &amp; Reasoning</span>
                <span class="hero-chip"><span>✦</span>Real-time Streaming</span>
            </div>
        </div>
        <div class="suggestions-label">Try asking</div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")

    for i, item in enumerate(SUGGESTIONS):
        target = col1 if i % 2 == 0 else col2
        label = f"**{item['title']}**  \n{item['prompt']}"
        if target.button(
            label,
            key=f"suggestion_{i}",
            icon=item["icon"],
            use_container_width=True,
        ):
            st.session_state.pending = item["prompt"]
            st.rerun()

else:
    safe_title = html.escape(chat["title"])
    msg_count = len(chat["messages"])
    msg_label = "1 message" if msg_count == 1 else f"{msg_count} messages"

    st.markdown(
        f"""
        <div class="chat-topbar">
            <div class="chat-topbar-left">
                <span class="chat-topbar-title">{safe_title}</span>
            </div>
            <div class="chat-topbar-right">
                <span class="meta-pill">{msg_label}</span>
                <span class="meta-pill meta-pill-accent">{BRAND_ICON} {MODEL_DISPLAY}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# 11. DISPLAY CHAT HISTORY
# ==================================================

for idx, message in enumerate(chat["messages"]):
    if message["role"] == "assistant":
        with st.container(key=f"msg_ai_{idx}"):
            with st.chat_message("assistant", avatar=AI_AVATAR):
                st.markdown(message["content"])
    else:
        with st.container(key=f"msg_user_{idx}"):
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(message["content"])


# ==================================================
# 12. USER INPUT
# ==================================================

prompt = st.chat_input("Ask NEXORA anything...")

# Handle suggestion clicks
if not prompt and st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None

# Handle new user message
if prompt:
    if not chat["messages"]:
        chat["title"] = (
            prompt[:28] + "..."
            if len(prompt) > 28
            else prompt
        )

    chat["messages"].append({
        "role": "user",
        "content": prompt,
    })

    with st.container(key="msg_user_live"):
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

    respond(chat_id)
    st.rerun()


# ==================================================
# 13. REGENERATE RESPONSE & ACTION BAR
# ==================================================

if st.session_state.regen:
    st.session_state.regen = False
    respond(chat_id)
    st.rerun()

if chat["messages"] and chat["messages"][-1]["role"] == "assistant":
    act_col1, act_col2, _ = st.columns([1.45, 1.15, 4.4], gap="small")
    with act_col1:
        st.button(
            "Regenerate",
            key="regen_btn",
            icon=":material/refresh:",
            on_click=regenerate,
            use_container_width=True,
        )
    with act_col2:
        st.button(
            "Clear chat",
            key="clear_main_btn",
            icon=":material/cleaning_services:",
            on_click=clear_current_chat,
            use_container_width=True,
        )
