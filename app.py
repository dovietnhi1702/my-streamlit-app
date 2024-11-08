import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Thiết lập tiêu đề cho ứng dụng
st.markdown("# 📊 Netflix Content Analysis")
st.markdown("### Welcome to the Netflix Analysis Dashboard 🎬")
st.markdown("""
This app provides an analysis of Netflix content by release year, type, country, and rating.
Explore the data, filter by various attributes, and gain insights into Netflix's content library!
""")

# Đọc tệp CSV từ GitHub
url = "https://raw.githubusercontent.com/dovietnhi1702/my-streamlit-app/572ffd3f7ae70143ff8e9f94392ec4d5e9796b1d/netflix_titles.csv"
df = pd.read_csv(url)

# Xử lý dữ liệu thiếu
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df.dropna(subset=['date_added', 'rating', 'duration'], inplace=True)

# Chuyển đổi cột 'duration' sang định dạng số phút nhất quán
df['duration_minutes'] = df['duration'].str.extract('(\d+)').astype(float)
df['duration_minutes'] = np.where(df['duration'].str.contains('Season'), np.nan, df['duration_minutes'])

# Sidebar
st.sidebar.title("📊 Lọc dữ liệu")
year_selected = st.sidebar.slider("Chọn năm phát hành", min_value=int(df['release_year'].min()), max_value=int(df['release_year'].max()))
type_selected = st.sidebar.selectbox("Chọn loại nội dung", options=df['type'].unique())
filtered_df = df[(df['release_year'] == year_selected) & (df['type'] == type_selected)]

# Hiển thị dữ liệu đã lọc
st.write("### Dữ liệu đã lọc:")
st.write(filtered_df)

# Phân chia nội dung bằng Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Xu hướng thời gian", "Phân phối nội dung", "Phân tích quốc gia", "Xếp hạng"])

# Biểu đồ đường: Xu hướng phát hành nội dung của Netflix qua các năm
with tab1:
    st.subheader("📈 Xu hướng phát hành nội dung của Netflix qua các năm")
    release_trend = df['release_year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.plot(release_trend.index, release_trend.values, marker='o', linestyle='-', color='b')
    ax.set_title("Xu hướng phát hành nội dung của Netflix qua các năm")
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
    filtered_data = df.dropna(subset=['release_year', 'duration_minutes'])
    fig = px.scatter(filtered_data, x="release_year", y="duration_minutes", title="Mối quan hệ giữa Năm phát hành và Thời lượng", color_discrete_sequence=["purple"])
    st.plotly_chart(fig)

# Biểu đồ cột: Số lượng Phim và Chương trình TV theo Quốc gia (Top 10 Quốc gia)
with tab4:
    st.subheader("🌍 Số lượng Phim và Chương trình TV theo Quốc gia (Top 10 Quốc gia)")
    type_by_country = df.groupby(['country', 'type']).size().unstack().fillna(0)
    top_countries = type_by_country.sum(axis=1).nlargest(10).index
    type_by_country_top = type_by_country.loc[top_countries]
    fig, ax = plt.subplots()
    type_by_country_top.plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'lightgreen'])
    ax.set_title("Số lượng Phim và Chương trình TV theo Quốc gia")
    ax.set_xlabel("Quốc gia")
    ax.set_ylabel("Số lượng nội dung")
    ax.legend(title="Loại")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Biểu đồ cột: Số lượng nội dung theo loại xếp hạng
with st.expander("📊 Xem chi tiết biểu đồ xếp hạng"):
    st.subheader("Số lượng nội dung theo loại xếp hạng (Top 10 xếp hạng)")
    rating_counts = df['rating'].value_counts().head(10)
    fig, ax = plt.subplots()
    rating_counts.plot(kind='bar', color='coral', ax=ax)
    ax.set_title("Số lượng nội dung theo loại xếp hạng")
    ax.set_xlabel("Xếp hạng")
    ax.set_ylabel("Số lượng nội dung")
    ax.tick_params(axis='x', rotation=0)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Made by [donhi](https://github.com/dovietnhi1702) - For questions, please do not contact")
