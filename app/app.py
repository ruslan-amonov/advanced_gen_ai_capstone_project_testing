# app/app.py

import streamlit as st
from chatbot import answer_query
from config import COMPANY_INFO
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.github_issues import create_github_issue


st.set_page_config(page_title="Ask me anything about Silk Road Samarkand EPC project", page_icon="🤖")
st.header("📚 Geodesist. Oracle of lands and local conditions")
st.markdown("early version of agent, which will eventually be added into 'Dream Team of Experts' to answer queries and replicate entire Silk Road Samarkand touristic center EPC project")


# Sidebar with company info
with st.sidebar:
    st.image("static/sexy_advanced_intelligence.webp", width=160)  # adjust width as needed
    st.header("Advanced Intelligence you've been craving for")
    st.markdown(f"**Company**: {COMPANY_INFO['name']}")
    st.markdown(f"📧 Email: {COMPANY_INFO['email']}")
    st.markdown(f"📞 Phone: {COMPANY_INFO['phone']}")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "message_consumed" not in st.session_state:
    st.session_state.message_consumed = True


# Show support ticket form early in the render
if st.session_state.get("creating_ticket", False):
    st.subheader("📮 Create Support Ticket")

    with st.form("ticket_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        summary = st.text_input("Issue Summary (Title)")
        description = st.text_area("Describe your issue in detail", value=st.session_state.get("last_question", ""))

        submitted = st.form_submit_button("Submit Ticket")

        if submitted:
            success = create_github_issue(name, email, summary, description)

            if success:
                st.success("🐙 GitHub issue created successfully!")
            else:
                st.error("❌ Failed to create GitHub issue.")

            st.markdown(f"**Name**: {name}")
            st.markdown(f"**Email**: {email}")
            st.markdown(f"**Summary**: {summary}")
            st.markdown(f"**Description**: {description}")

            # Reset state
            st.session_state.creating_ticket = False
            st.session_state.offer_ticket = False
            st.session_state.message_consumed = True

    st.info("📮 Please complete the support ticket form above before continuing the conversation.")


# ✅ Capture new user input (only when not creating a ticket)
if not st.session_state.get("creating_ticket", False):
    user_input = st.chat_input("Ask a question about your documents...")
    if user_input:
        st.session_state.last_user_input = user_input
        st.session_state.message_consumed = False
else:
    user_input = st.session_state.get("last_user_input", None)

# ✅ Handle message once only
if user_input and not st.session_state.get("message_consumed", True):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.last_user_input = None
    st.session_state.message_consumed = True  # ✅ prevent reuse

    # Detect manual intent to raise ticket
    is_ticket_request = (
        "ticket" in user_input.lower() and
        any(word in user_input.lower() for word in ["yes", "create", "open", "raise"])
    )

    if is_ticket_request:
        st.session_state.last_question = user_input  # ✅ Save for ticket description
        st.session_state.creating_ticket = True
        st.session_state.offer_ticket = False
        bot_reply = "📝 Great! Let's fill in the support ticket form below."
        st.session_state.messages.append({"role": "ai", "content": bot_reply})
        st.rerun()  # 🔁 Trigger next render cycle to show the form
    else:
        with st.spinner("Thinking..."):
            result = answer_query(user_input)
            bot_reply = result["response"]
            st.session_state.messages.append({"role": "ai", "content": bot_reply})
            st.session_state.offer_ticket = result["offer_ticket"]



# Offer ticket creation if needed
if st.session_state.get("offer_ticket", False):
    st.warning("Looks like we couldn't help this time. Want to create a support ticket?")
    if st.button("📝 Create Support Ticket"):
        st.session_state.creating_ticket = True
        st.session_state.last_question = st.session_state.messages[-1]["content"]
        st.rerun()  # ← re-render to show form immediately

# Render chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])




