import streamlit as st
from rag_with_palm import RAGPaLMQuery
import time 
import random
# Instantiate the class
rag_palm_query_instance = RAGPaLMQuery()

st.set_page_config(page_title="TrustBank")
st.session_state.token = None
st.title(f"**TrustBank Assistant**")  # Add emojis and colors to the title
st.markdown("Hello welcome to TrustBank support service.🙂")

# Custom CSS for styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f1f1f1;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .css-1d391kg {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar content
st.sidebar.title("Welcome to TrustBank!")
st.sidebar.write("How can we assist you today?")

# Sidebar navigation
st.sidebar.markdown("### Easy Navigation")
# st.sidebar.button("Home", key="home")
if st.sidebar.button("I need to know what are the available Investment Options", key="investment"):
    st.chat_message("assistant").markdown("I need to know what are the available Investment Options")
    # Display user message in chat message container
    st.chat_message("user").markdown(
        """
        **Investment Options at TrustBank:**
        - **Stocks and Bonds**: Invest in a variety of stocks and government or corporate bonds.
        - **Mutual Funds**: Diversify your portfolio with our range of mutual funds.
        - **Retirement Accounts**: Secure your future with our IRA and 401(k) plans.
        - **Savings Accounts**: High-interest savings accounts for risk-free savings.
        - **Certificates of Deposit (CDs)**: Fixed-term CDs with competitive interest rates.
        
        For more detailed information, please visit our Investment Services section or contact our financial advisors.
    """
    )
    # # Displaying a hardcoded answer
    # st.write("""
    #     **Investment Options at TrustBank:**
    #     - **Stocks and Bonds**: Invest in a variety of stocks and government or corporate bonds.
    #     - **Mutual Funds**: Diversify your portfolio with our range of mutual funds.
    #     - **Retirement Accounts**: Secure your future with our IRA and 401(k) plans.
    #     - **Savings Accounts**: High-interest savings accounts for risk-free savings.
    #     - **Certificates of Deposit (CDs)**: Fixed-term CDs with competitive interest rates.
        
    #     For more detailed information, please visit our Investment Services section or contact our financial advisors.
    # """)

st.sidebar.button("Loan Services", key="loans")
st.sidebar.button("Credit Cards", key="credit_cards")
st.sidebar.button("Account Management", key="account")
st.sidebar.button("Support", key="support")
st.sidebar.button("About Us", key="about")

st.sidebar.markdown("---")
st.sidebar.write("Need assistance? Feel free to reach out to our support team at any time.")


# with st.chat_message("assistant"):
#     st.markdown("Hello")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def llm_output(prompt):
    msg = rag_palm_query_instance.query_response(prompt)
    # return msg
    # else:
    return msg

def generate_greeting():
    greetings = ["How can I assist you today?", 
                 "What can I help you with?", 
                 "How may I assist you with your banking queries today?"]
    return random.choice(greetings)

# Your query function
def run_query(prompt):
    
    # Detecting if the input is a greeting
    # if any(greet in prompt.lower() for greet in ['hello', 'hi', 'greetings', 'hey']) and not any(keyword in prompt.lower() for keyword in ['bank', 'loan', 'credit', 'investment']):
    #     # time.sleep(2)
    #     # Check if it also includes banking-related keywords
    #     # if any(keyword in prompt.lower() for keyword in ['bank', 'loan', 'credit', 'investment']):
    #     #     with st.spinner("Thinking..."):
    #     #         time.sleep(2)
    #     #         result = llm_output(prompt)
    #     # else:
    #     with st.spinner("Opps somthing not related to banking domain! Let me see..."):
    #         time.sleep(2)
    #         return "Hello! Sorry, we are a banking app."
    #     # return generate_greeting()
    if any(greet in prompt.lower() for greet in ['hello', 'hi', 'greetings', 'hey']):
        time.sleep(2)
        result =  generate_greeting()
    
    # Check if question is in scope
    elif not any(keyword in prompt.lower() for keyword in ['bank', 'loan', 'credit', 'investment']):
        with st.spinner("Opps somthing not related to banking domain! Let me see..."):
            time.sleep(2)
            result = "Sorry, we are a banking app."
    else:
        with st.spinner("Thinking..."):
            # Generate RAG output
            time.sleep(2)
            result = llm_output(prompt)

    return result

# React to user input
if prompt := st.chat_input("Need info? Drop your question here!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # response = rag_palm_query_instance.query_response(prompt)
    response = run_query(prompt)


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


pop_up_html = """
<style>
@keyframes fadeIn {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 1; }}
}}

.pop-up {{
    animation: fadeIn 1s ease-in-out;
    position: fixed; /* or absolute */
    top: 20px;
    right: 20px;
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 1000;
}}
</style>

<div class="pop-up" id="chatPopUp">
    <p>{}</p>
</div>
"""
