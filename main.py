from app.utils import logger
from app.utils import chat as chat_utils
import streamlit as st


def initialization():
    # SESSION STATE
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_conversation' not in st.session_state:
        st.session_state.current_conversation = ''
    if 'model' not in st.session_state:
        st.session_state.model = 'gpt-3.5-turbo'
    if 'api_key' not in st.session_state:
        st.session_state.api_key = chat_utils.read_key()

    st.set_page_config(
        page_title='Finance Chatbot',
        page_icon='💸',
        # layout='wide'
    )


# TABS 
def tab_conversations(tab):

    tab.button('➕ New conversation',
                on_click=select_conversation,
                args=('', ),
                use_container_width=True)
    tab.markdown('')
    conversations = chat_utils.list_conversations()
    for file_name in conversations:
        message_name = chat_utils.deconvert_message_name(file_name).capitalize()
        if len(message_name) == 30:
            message_name += '...'
        tab.button(message_name,
            on_click=select_conversation,
            args=(file_name, ),
            disabled=file_name == st.session_state['current_conversation'],
            use_container_width=True)

def select_conversation(file_name):
    if file_name == '':
        st.session_state['messages'] = []
    else:
        message = chat_utils.read_message_by_file_name(file_name)
        st.session_state['messages'] = message
    st.session_state['current_conversation'] = file_name

def tab_settings(tab):
    selected_model = tab.selectbox('Select the model',
                                   ['gpt-3.5-turbo', 'gpt-4'])
    st.session_state['model'] = selected_model

    key = tab.text_input('Add your API key', value=st.session_state['api_key'])
    if key != st.session_state['api_key']:
        st.session_state['api_key'] = key
        chat_utils.save_key(key)
        tab.success('Key saved successfully')


def chat_box():
    messages = chat_utils.read_messages(st.session_state['messages'])

    st.header('💸 Finance Chatbot', divider=True)
    
    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])
    
    prompt = st.chat_input('Type your message here...')
    if prompt:
        if st.session_state['api_key'] == '':
            st.error('Add an API key in the settings tab')
        else:
            new_message = {'role': 'user',
                           'content': prompt}
            chat = st.chat_message(new_message['role'])
            chat.markdown(new_message['content'])
            messages.append(new_message)

            chat = st.chat_message('assistant')
            placeholder = chat.empty()
            placeholder.markdown("▌")
            full_response = ''

            try:
                responses = chat_utils.get_model_response(messages,
                                                st.session_state['api_key'],
                                                model=st.session_state['model'],
                                                stream=True)
                if responses is None:
                    raise Exception('No response from OpenAI API')
                
                for response in responses:
                    full_response += response.choices[0].delta.get('content', '')
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                new_message = {'role': 'assistant',
                            'content': full_response}
                messages.append(new_message)

                st.session_state['messages'] = messages
                chat_utils.save_messages(messages)
            except Exception as e:
                msg = 'Error connecting to OpenAI API, check your API key'
                st.error(msg)
                logger.log_error(f"{msg}: {e}")
               

# MAIN
def main():
    logger.clean()
    initialization()
    chat_box()
    tab1, tab2 = st.sidebar.tabs(['Conversations', 'Settings'])
    tab_conversations(tab1)
    tab_settings(tab2)
    

if __name__ == '__main__':
    main()
# streamlit run main.py
