import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Analysis Project", layout="wide")

st.title("📊 Data Analysis Dashboard")

st.sidebar.title("Project Info")

st.sidebar.write("""

Project: Data Cleaning and Analysis

Tools Used:
Python
Pandas
Matplotlib
Seaborn
Streamlit

""")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:

    df = pd.read_csv(file, encoding="latin1")

    df_original = df.copy()

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.write("Shape:", df.shape)

    st.write("Columns:", list(df.columns))

    # cleaning if columns exist
    required_cols = [

    'InvoiceNo',
    'Description',
    'Quantity',
    'UnitPrice',
    'CustomerID',
    'Country',
    'InvoiceDate'

    ]

    if all(col in df.columns for col in required_cols):

        df.dropna(subset=['CustomerID','Description'], inplace=True)

        df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

        df.drop_duplicates(inplace=True)

        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

        df['Month'] = df['InvoiceDate'].dt.month

        df['Day'] = df['InvoiceDate'].dt.day_name()

        st.success("Data Cleaned Successfully")

        # KPIs

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Sales", round(df['TotalPrice'].sum(),2))

        col2.metric("Orders", df['InvoiceNo'].nunique())

        col3.metric("Customers", df['CustomerID'].nunique())

        col4.metric("Products", df['Description'].nunique())

        # summary

        if st.checkbox("Show Statistical Summary"):

            st.write(df.describe())

        if st.checkbox("Show Data Types"):

            st.write(df.dtypes)

        # filter

        st.sidebar.header("Filters")

        country = st.sidebar.selectbox(

        "Select Country",

        ["All"] + list(df['Country'].unique())

        )

        if country != "All":

            df = df[df['Country'] == country]

        top_n = st.sidebar.slider("Select Top N", 5, 20, 10)

        # search product

        st.subheader("Search Product")

        search = st.text_input("Enter product name")

        if search:

            st.write(

            df[df['Description'].str.contains(search, case=False)]

            )

        # graph select

        graph = st.selectbox(

        "Select Graph",

        [

        "Top Selling Products",

        "Monthly Sales",

        "Country Sales",

        "Top Customers",

        "Sales by Day",

        "Expensive Products",

        "Scatter Plot",

        "Histogram",

        "Boxplot",

        "Correlation Heatmap",

        "Missing Values Heatmap"

        ]

        )

        # graphs

        if graph == "Top Selling Products":

            data = df.groupby('Description')['Quantity'].sum(

            ).sort_values(ascending=False).head(top_n)

            fig = plt.figure()

            data.plot(kind='bar')

            st.pyplot(fig)

        elif graph == "Monthly Sales":

            data = df.groupby('Month')['TotalPrice'].sum()

            fig = plt.figure()

            data.plot()

            st.pyplot(fig)

        elif graph == "Country Sales":

            data = df.groupby('Country')['TotalPrice'].sum(

            ).sort_values(ascending=False).head(top_n)

            fig = plt.figure()

            data.plot(kind='bar')

            st.pyplot(fig)

        elif graph == "Top Customers":

            data = df.groupby('CustomerID')['TotalPrice'].sum(

            ).sort_values(ascending=False).head(top_n)

            fig = plt.figure()

            data.plot(kind='bar')

            st.pyplot(fig)

        elif graph == "Sales by Day":

            data = df.groupby('Day')['TotalPrice'].sum()

            fig = plt.figure()

            data.plot(kind='bar')

            st.pyplot(fig)

        elif graph == "Expensive Products":

            data = df.sort_values(

            by="UnitPrice", ascending=False

            ).head(top_n)

            st.write(

            data[['Description','UnitPrice']]

            )

        elif graph == "Scatter Plot":

            fig = plt.figure()

            plt.scatter(

            df['Quantity'],

            df['TotalPrice']

            )

            st.pyplot(fig)

        elif graph == "Histogram":

            fig = plt.figure()

            plt.hist(df['Quantity'], bins=20)

            st.pyplot(fig)

        elif graph == "Boxplot":

            fig = plt.figure()

            plt.boxplot(df['UnitPrice'])

            st.pyplot(fig)

        elif graph == "Correlation Heatmap":

            fig = plt.figure()

            sns.heatmap(

            df.corr(),

            annot=True

            )

            st.pyplot(fig)

        elif graph == "Missing Values Heatmap":

            fig = plt.figure()

            sns.heatmap(

            df.isnull(),

            yticklabels=False,

            cbar=False

            )

            st.pyplot(fig)

        # interactive table

        if st.checkbox("Show Full Table"):

            st.dataframe(df)

        # download

        csv = df.to_csv(index=False)

        st.download_button(

        "Download Clean Data",

        csv,

        "clean_data.csv"

        )

        # raw data

        if st.checkbox("Show Raw Data"):

            st.dataframe(df_original)

    else:

        st.error(

        "Dataset columns not matching expected format"

        )