import streamlit as st


def main():
    st.title('Data Science pre process')
    st.header('This is a project guided by Aceleradev DataScience')
    st.subheader('Week 2')
    st.text('My name is Felipe and let\'s go')
    st.image('background3.jpg', width=700)
    #st.audio('')
    #st.video('')

    st.subheader('Button')
    button = st.button('Click here')
    if button:
        st.markdown('Clicked')

    st.subheader('Checkbox')
    check = st.checkbox('Checkbox')
    if check:
        st.markdown('Checked')

    st.subheader('Radio')
    radio = st.radio('Select a option', ('1', '2'))
    if radio == '1':
        st.markdown('Option 1')
    if radio == '2':
        st.markdown('Option 2')

    st.subheader('Selectbox')
    select = st.selectbox('Choose a option', ('1', '2'))
    if select == '1':
        st.markdown('Option 1')
    if select == '2':
        st.markdown('Option 2')

    st.subheader('Multi selection')
    multi = st.multiselect('Choose:', ('1', '2'))
    if multi == '1':
        st.markdown('Option 1')
    if multi == '2':
        st.markdown('Option 2')

    st.subheader('File upload')
    file = st.file_uploader('Upload file', type='csv')
    if file is not None:
        st.markdown('File uploaded')

if __name__ == '__main__':
    main()
