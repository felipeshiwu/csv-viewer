import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import altair as alt
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


def new_hist(col, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.Color('count()',
                  scale=alt.Scale(scheme='yelloworangered'),
                  legend=alt.Legend(title='Total Records')
                  ),
        alt.X(col, bin=True),
        y='count()', tooltip=[col, 'count()']
    ).interactive()
    return chart


def datasciencepage(file):
    if file is not None:
        df = pd.read_csv(file)
        na_values = pd.DataFrame({'columns': df.columns,
                                  'types': df.dtypes,
                                  'perceptual_na': df.isna().sum() / df.shape[0]})

        if False:
            st.markdown('**File is to big**')
        else:
            radio = st.sidebar.radio('Select a option', (
                'Univariate analysis', 'N/A values', 'Correlation',
                'Dangerous area'))
            if radio == 'Univariate analysis':
                st.markdown('**Number of lines:**')
                st.markdown(df.shape[0])
                st.markdown('**Number of columns:**')
                st.markdown(df.shape[1])
                st.markdown('**Count of data types:**')
                st.table(na_values.types.value_counts())

                slider = st.slider('Range', 1, df.shape[0])
                st.dataframe(df.head(slider))

                f = st.text_input('Write the column that you want to groupby', df.columns[0])
                g = st.text_input('Write the feature valuate with groupby', df.columns[-1])
                h = st.selectbox('...use: ', ('mean', 'median', 'sum', 'max', 'min', 'mode', 'count', 'standard deviation'))
                if h:
                    try:
                        if h == 'mean':
                            st.table(df.groupby(f)[g].mean().reset_index().sort_values(g, ascending=False))
                        if h == 'median':
                            st.table(df.groupby(f)[g].median().reset_index().sort_values(g, ascending=False))
                        if h == 'mode':
                            st.table(df.groupby(f)[g].agg(lambda x:x.value_counts().index[0]))
                        if h == 'sum':
                            st.table(df.groupby(f)[g].sum().reset_index().sort_values(g, ascending=False))
                        if h == 'count':
                            st.table(df.groupby(f)[g].count().reset_index().sort_values(g, ascending=False))
                        if h == 'max':
                            st.table(df.groupby(f)[g].max().reset_index().sort_values(g, ascending=False))
                        if h == 'min':
                            st.table(df.groupby(f)[g].min().reset_index().sort_values(g, ascending=False))
                        if h == 'standard deviation':
                            st.table(df.groupby(f)[g].std().reset_index().sort_values(g, ascending=False))
                    except:
                        st.markdown('I failed....')
            if radio == 'N/A values':
                st.table(na_values[na_values['perceptual_na'] != 0][['types', 'perceptual_na']])

                perceptual = st.slider(
                    'Columns with % N/A that will be filled with...', 0, 100)
                list_column = list(na_values[na_values['perceptual_na'] > (perceptual / 100)]['columns'])
                select_method = st.radio('...fill number features with: ', ('Mean', 'Median', 'Zero'))
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
                multi = st.multiselect('Select the columns that you want to see the correlation of...',
                                       list(df.select_dtypes(np.number).columns))
                corr_type = st.radio('', ('pearson', 'spearman',))
                if multi:
                    st.write(df[multi].corr(method=corr_type))
                    st.write(df.describe()[list(multi)])
                else:
                    st.write(df.corr(method=corr_type), height=1000)

                y = st.text_input('Write the name of the feature that you want to see the distribution', df.columns[-1])

                try:
                    sns.distplot(df[y], color='red')
                    st.pyplot()
                    alt_chart = st.checkbox('See more...')
                    if alt_chart:
                        st.write(new_hist(y, df))

                except:
                    st.markdown('I didn\'t find the distribution....')

            if radio == 'Dangerous area':
                st.markdown(
                    'To avoid problems with the integrity of the dataframe, the creations are only valid inside '
                    'the **Dangerous area** section, if you want to add the column permanently, download the '
                    'updated csv file.')
                st.write(list(df))
                f = st.text_input('I want to create a new columns call...(you can change an existing column...)', '')
                g = st.text_input('If value of...', '')
                if g:
                    try:
                        h = st.text_input('is bigger then...', df[g].mean())
                        i = st.text_input('call him...', 'big')
                        j = st.text_input('the opposite call him...', 'small')
                        df[f] = [i if x > int(h) else j for x in df[g]]

                        creation = st.button('Create!')
                        if creation:
                            st.table(df[[g, f]].head(5))

                        st.markdown(get_table_download_link(df, False, []), unsafe_allow_html=True)
                    except:
                        st.markdown('I can\'t recognize this column is the dataframe....')


def main():
    mode = st.sidebar.selectbox("Felipe Wu", ["Home", "Data Science"])

    if mode == 'Home':
        st.title('Data Science pre process')
        st.header('Project guided by Codenation and powered by Articfox')
        st.subheader('Week 2')
        st.markdown('My name is [Felipe](http://thefelipes.site/) and let\'s go')
        st.image('background3.jpg', width=700)
        st.markdown('[![Linkedin](https://github.com/felipeshiwu/Mypage/blob/master/img/stuff/linkedin.png?raw=true)](https://www.linkedin.com/in/felipeshiwu/)\
                     [![Github](https://github.com/felipeshiwu/Mypage/blob/master/img/stuff/github.png?raw=true)](https://github.com/felipeshiwu)\
                     [![Webpage](https://github.com/felipeshiwu/Mypage/blob/master/img/stuff/logo.png?raw=true)](https://thefelipes.site/)\
                     [![Articfox](https://github.com/felipeshiwu/Mypage/blob/master/img/stuff/articfox.png?raw=true)](http://articfox.com.br/)')

    if mode == 'Data Science':
        st.subheader('File upload')
        file = st.file_uploader('Upload file', type='csv')
        datasciencepage(file)


if __name__ == '__main__':
    main()
