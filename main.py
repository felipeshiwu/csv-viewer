import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import base64


def get_table_download_link(df, check, list_column):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """

    if check:
        df[list_column] = df[list_column].fillna('None')
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="after_process.csv">Download csv file</a>'
    return href


def datasciencepage(file):
    if file is not None:
        df = pd.read_csv(file)
        na_values = pd.DataFrame({'columns': df.columns,
                                  'types': df.dtypes,
                                  'perceptual_na': df.isna().sum() / df.shape[0]})
        st.subheader('Analyzing the data')
        st.markdown('**Number of lines:**')
        st.markdown(df.shape[0])
        st.markdown('**Number of columns:**')
        st.markdown(df.shape[1])
        st.markdown('**Count of data types:**')
        st.table(na_values.types.value_counts())

        if df.shape[0] + df.shape[1] > 5000:
            st.markdown('**File is to big**')
        else:
            radio = st.sidebar.radio('Select a option', ('Univariate analysis', 'See % of N/A values', 'Show data', 'Complete N/A', 'Correlation'))
            if radio == 'Univariate analysis':
                st.markdown('**Number of lines:**')
                st.markdown(df.shape[0])
                st.markdown('**Number of columns:**')
                st.markdown(df.shape[1])
                st.markdown('**Count of data types:**')
                st.table(na_values.types.value_counts())
            if radio == 'See % of N/A values':
                st.table(na_values[na_values['perceptual_na'] != 0][['types', 'perceptual_na']])
            if radio == 'Show data':
                slider = st.slider('Range', 1, df.shape[0])
                st.dataframe(df.head(slider))
            if radio == 'Complete N/A':
                perceptual = st.slider(
                    'Columns with % N/A that will be filled with...', 0, 100)
                list_column = list(na_values[na_values['perceptual_na'] > (perceptual / 100)]['columns'])
                select_method = st.radio('...fill number features with :', ('Mean', 'Median', 'Zero'))
                st.markdown(
                    'You have selected : ->' + str(select_method) + '<- and the features that will be filled are...')

                df_output = df[list_column]
                output_na = pd.DataFrame(
                    {'names': df_output.columns, 'types': df_output.dtypes, 'NA #': df_output.isna().sum(),
                     'NA %': (df_output.isna().sum() / df_output.shape[0]) * 100})
                check = st.checkbox('Complete the no number NaN features with \'None\'')
                if check:
                    st.table(output_na)
                else:
                    st.table(output_na[output_na['types'] != 'object'])
                st.subheader('Output download below : ')
                if select_method == 'Mean':
                    df[list_column] = df[list_column].fillna(df[list_column].mean())
                    st.markdown(get_table_download_link(df, check, list_column), unsafe_allow_html=True)

                if select_method == 'Median':
                    df[list_column] = df[list_column].fillna(df[list_column].median())
                    st.markdown(get_table_download_link(df, check, list_column), unsafe_allow_html=True)

                if select_method == 'Zero':
                    aux_list = list(output_na[output_na['types'] != 'object']['names'])
                    df[aux_list] = df[aux_list].fillna(0)
                    st.markdown(get_table_download_link(df, check, list_column), unsafe_allow_html=True)
            if radio == 'Correlation':
                st.write(df.corr(), height=1000)
                y = st.text_input('Write the name of the feature that you want to see the distribution', df.columns[-1])
                st.write('The current is', y)
                multi = st.multiselect('Select the columns that you want to see the describe:',
                                       list(df.select_dtypes(np.number).columns))
                if multi:
                    st.write(df.describe()[list(multi)])

                try:
                    sns.distplot(df[y], color='red')
                    st.pyplot()
                except:
                    st.markdown('I didn\'t find the distribution....')


def main():
    mode = st.sidebar.selectbox("Felipe Wu", ["Home", "Data Science"])

    if mode == 'Home':
        st.title('Data Science pre process')
        st.header('Project guided by Aceleradev and powered by Articfox')
        st.subheader('Week 2')
        st.text('My name is Felipe and let\'s go')
        st.image('background3.jpg', width=700)

    if mode == 'Data Science':
        st.subheader('File upload')
        file = st.file_uploader('Upload file', type='csv')
        datasciencepage(file)


if __name__ == '__main__':
    main()
