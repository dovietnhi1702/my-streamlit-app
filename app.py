import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

# Thiết lập tiêu đề cho ứng dụng
st.title("📺 Netflix Content Analysis")
st.markdown("### Welcome to the Netflix Analysis Dashboard 🎬")
st.markdown("""
This app provides an analysis of Netflix content by release year, type, country, and rating.
Explore the data, filter by various attributes, and gain insights into Netflix's content library!
""")

# Đọc dữ liệu
url = "https://raw.githubusercontent.com/dovietnhi1702/my-streamlit-app/572ffd3f7ae70143ff8e9f94392ec4d5e9796b1d/netflix_titles.csv"
df_raw = pd.read_csv(url)

# Tạo bản sao của dữ liệu thô sơ để hiển thị trước khi xử lý
df_before = df_raw.copy()

# Xử lý dữ liệu
df = df_raw.copy()
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('No Data', inplace=True)
df['country'].fillna(df['country'].mode()[0], inplace=True)
df['date_added'] = df['date_added'].fillna('No')
df['rating'] = df['rating'].fillna('Unknown')
df['duration'] = df['duration'].apply(lambda x: int(x.split(' ')[0]) if isinstance(x, str) else x)
df.drop_duplicates(inplace=True)

# Thêm cột năm và tháng cho 'date_added'
df['year_added'] = df['date_added'].apply(lambda x: x[-4:] if x != 'No' else np.nan)
df['month_added'] = df['date_added'].apply(lambda x: x.split(' ')[0] if x != 'No' else '')

# Chuyển đổi xếp hạng theo nhóm tuổi
MR_age = {'TV-MA': 'Adults', 'R': 'Adults', 'PG-13': 'Teens', 'TV-14': 'Young Adults', 'TV-PG': 'Older Kids',
          'NR': 'Adults', 'TV-G': 'Kids', 'TV-Y': 'Kids', 'TV-Y7': 'Older Kids', 'PG': 'Older Kids', 'G': 'Kids',
          'NC-17': 'Adults', 'TV-Y7-FV': 'Older Kids', 'UR': 'Adults'}
df['age_group'] = df['rating'].map(MR_age)

# Tabs hiển thị dữ liệu trước và sau khi xử lý
tab_raw, tab_processed = st.tabs(["Dữ liệu thô sơ", "Dữ liệu đã xử lý"])

# Thêm checkbox để hiển thị toàn bộ dữ liệu hoặc chỉ một phần
show_full_data_raw = st.checkbox("Hiển thị toàn bộ dữ liệu thô sơ")
show_full_data_processed = st.checkbox("Hiển thị toàn bộ dữ liệu đã xử lý")

with tab_raw:
    st.subheader("📋 Dữ liệu Thô Sơ")
    st.write("### Dữ liệu trước khi xử lý")
    if show_full_data_raw:
        st.write(df_before)  # Hiển thị toàn bộ dữ liệu nếu được chọn
    else:
        st.write(df_before.head())  # Chỉ hiển thị 5 hàng đầu tiên nếu không chọn
    st.write("### Thống kê các giá trị null ban đầu")
    st.write(df_before.isnull().sum())
    st.write("### Tùy chọn xem dữ liệu")

with tab_processed:
    st.subheader("📋 Dữ liệu Đã Xử Lý")
    st.write("### Dữ liệu sau khi xử lý")
    if show_full_data_processed:
        st.write(df)  # Hiển thị toàn bộ dữ liệu nếu được chọn
    else:
        st.write(df.head())  # Chỉ hiển thị 5 hàng đầu tiên nếu không chọn
    st.write("### Thống kê các giá trị null sau xử lý")
    st.write(df.isnull().sum())
    st.write("### Tùy chọn xem dữ liệu")
    st.write(df.info())
st.title("📊 Biểu đồ trực quan hóa")
# Tabs hiển thị biểu đồ
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Xu hướng thời gian", "Phân phối nội dung", "Phân tích quốc gia",
    "Xếp hạng", "Đám mây từ khóa"
])

# Biểu đồ đường: Xu hướng phát hành nội dung qua các năm
with tab1:
    st.subheader("📈 Xu hướng phát hành nội dung qua các năm")
    release_trend = df['release_year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.plot(release_trend.index, release_trend.values, marker='o', linestyle='-', color='b')
    ax.set_title("Xu hướng phát hành nội dung qua các năm")
    ax.set_xlabel("Năm phát hành")
    ax.set_ylabel("Số lượng phát hành")
    ax.grid(True)
    st.pyplot(fig)

# Biểu đồ tròn: Phân phối loại nội dung và top 10 thể loại
with tab2:
    st.subheader("🎬 Phân phối các loại nội dung (Phim và Chương trình TV)")
    type_distribution = df['type'].value_counts()
    fig = px.pie(type_distribution, values=type_distribution, names=type_distribution.index, title="Phân phối các loại nội dung", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)

    st.subheader("🎬 Phân phối 10 thể loại hàng đầu")
    genres = df['listed_in'].str.split(', ').explode()
    genre_distribution = genres.value_counts().head(10)
    fig = px.pie(genre_distribution, values=genre_distribution, names=genre_distribution.index, title="Phân phối 10 thể loại hàng đầu", color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig)

# Biểu đồ phân tán: Mối quan hệ giữa Năm phát hành và Thời lượng
with tab3:
    st.subheader("⏱️ Mối quan hệ giữa Năm phát hành và Thời lượng")
    filtered_data = df.dropna(subset=['release_year', 'duration'])
    fig = px.scatter(filtered_data, x="release_year", y="duration", title="Mối quan hệ giữa Năm phát hành và Thời lượng", color_discrete_sequence=["purple"])
    st.plotly_chart(fig)

    # Heatmap phân bố nội dung theo nhóm tuổi tại 10 quốc gia hàng đầu
    st.subheader("🌍 Heatmap phân bố nội dung theo nhóm tuổi tại 10 quốc gia hàng đầu")
    top_countries = df['country'].value_counts().nlargest(10).index
    filtered_data = df[df['country'].isin(top_countries)]
    age_group_country_data = filtered_data.pivot_table(index='country', columns='age_group', aggfunc='size', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(age_group_country_data, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5)
    plt.title("Mức độ nội dung theo nhóm tuổi tại các quốc gia")
    st.pyplot(plt)

# Biểu đồ cột: Số lượng nội dung theo loại xếp hạng
with tab4:
    st.subheader("📊 Số lượng nội dung theo loại xếp hạng (Top 10 xếp hạng)")
    rating_counts = df['rating'].value_counts().head(10)
    fig, ax = plt.subplots()
    rating_counts.plot(kind='bar', color='coral', ax=ax)
    ax.set_title("Số lượng nội dung theo loại xếp hạng")
    ax.set_xlabel("Xếp hạng")
    ax.set_ylabel("Số lượng nội dung")
    ax.tick_params(axis='x', rotation=0)
    st.pyplot(fig)

# Đám mây từ khóa từ các mô tả
with tab5:
    st.subheader("🔍 Đám mây từ khóa trong mô tả của các nội dung")
    text = ' '.join(df['description'].astype(str))
    stopwords = set(STOPWORDS)
    mask = np.array(Image.open("Netflix-Logo-2014-present.jpg"))
    wordcloud = WordCloud(stopwords=stopwords, background_color='white', mask=mask, max_words=150, colormap='OrRd').generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Footer
st.markdown("---")
st.markdown("Made by [donhi](https://github.com/dovietnhi1702) - For questions, please do not contact")