import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Thiết lập tiêu đề cho ứng dụng
st.title("Netflix Content Analysis")

# Tải dữ liệu CSV
uploaded_file = st.file_uploader("Upload Netflix Titles CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Xử lý dữ liệu thiếu
    df['director'].fillna('Unknown', inplace=True)
    df['cast'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df.dropna(subset=['date_added', 'rating', 'duration'], inplace=True)

    # Chuyển đổi cột 'duration' sang định dạng số phút nhất quán
    df['duration_minutes'] = df['duration'].str.extract('(\d+)').astype(float)
    df['duration_minutes'] = np.where(df['duration'].str.contains('Season'), np.nan, df['duration_minutes'])

    # Hiển thị một vài hàng dữ liệu
    st.write("Data Preview:")
    st.write(df.head())

    # Biểu đồ đường: Xu hướng phát hành nội dung của Netflix qua các năm
    st.subheader("Xu hướng phát hành nội dung của Netflix qua các năm")
    release_trend = df['release_year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.plot(release_trend.index, release_trend.values, marker='o', linestyle='-', color='b')
    ax.set_title("Xu hướng phát hành nội dung của Netflix qua các năm")
    ax.set_xlabel("Năm phát hành")
    ax.set_ylabel("Số lượng phát hành")
    ax.grid(True)
    st.pyplot(fig)

    # Biểu đồ tròn: Phân phối loại nội dung và top 10 thể loại
    st.subheader("Phân phối các loại nội dung (Phim và Chương trình TV)")
    type_distribution = df['type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(type_distribution, labels=type_distribution.index, autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightgreen'])
    ax.set_title("Phân phối các loại nội dung")
    st.pyplot(fig)

    st.subheader("Phân phối 10 thể loại hàng đầu")
    genres = df['listed_in'].str.split(', ').explode()
    genre_distribution = genres.value_counts().head(10)
    fig, ax = plt.subplots()
    colors = plt.cm.Paired(np.arange(10))
    ax.pie(genre_distribution, labels=genre_distribution.index, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title("Phân phối 10 thể loại hàng đầu")
    st.pyplot(fig)

    # Biểu đồ phân tán: Mối quan hệ giữa Năm phát hành và Thời lượng
    st.subheader("Mối quan hệ giữa Năm phát hành và Thời lượng")
    filtered_data = df.dropna(subset=['release_year', 'duration_minutes'])
    fig, ax = plt.subplots()
    ax.scatter(filtered_data['release_year'], filtered_data['duration_minutes'], alpha=0.5, color='purple')
    ax.set_title("Mối quan hệ giữa Năm phát hành và Thời lượng")
    ax.set_xlabel("Năm phát hành")
    ax.set_ylabel("Thời lượng (phút)")
    ax.grid(True)
    st.pyplot(fig)

    # Biểu đồ cột: Số lượng Phim và Chương trình TV theo Quốc gia (Top 10 Quốc gia)
    st.subheader("Số lượng Phim và Chương trình TV theo Quốc gia (Top 10 Quốc gia)")
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
    st.subheader("Số lượng nội dung theo loại xếp hạng (Top 10 xếp hạng)")
    rating_counts = df['rating'].value_counts().head(10)
    fig, ax = plt.subplots()
    rating_counts.plot(kind='bar', color='coral', ax=ax)
    ax.set_title("Số lượng nội dung theo loại xếp hạng")
    ax.set_xlabel("Xếp hạng")
    ax.set_ylabel("Số lượng nội dung")
    ax.tick_params(axis='x', rotation=0)
    st.pyplot(fig)