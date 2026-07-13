#                                                                       ABOUT PROJECT 
#                                                             CSV FILE ANALYZER AND CLEANING TOOLS
# 1: READ CSV FILE
# 2: PREVIEW THE DATA (rows , columns)
# 3: DATA SUMMARY 
# 4: COLUMNS INFORMATION (TYPE , NAME)
# 5: DATA HEALTH REPORT (NULL , DUPLICATE , STRING , NUMERIC)
# 6: SIDEBAR HEADER
# 7: DATA CLEANING FUNCTION ON SIDEBAR
# 8: REMOVE MISSING VALUES
# 9: VISUALIZATION OF DATA (HISTOGRAM , SCATTER PLOT , LINE CHART , BAR CHART , BOX PLOT , PIE CHART)
# 10: SEARCH THE DATA ( BY USER )
# 11: FILTER THE DATA ( GIVE OPTION TO USER )
# 12: GET BACK ORIGINAL DATA IF WE CLEAN IT
# 13: CORRELATION MATRIX
# 14: DOWNLOAD THE CLEAN DATA
# 15: GREETING

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 CSV Data Analyzer & Cleaning Tool")
st.caption(
    "Upload a CSV file, clean the data, visualize it, search, filter, "
    "and download the cleaned dataset."
)
file = st.file_uploader("Uploade your csv file",type=["csv"])
#=====================================
# READ DATA
#=====================================
if file:
    st.success("CSV FILE UPLOADED SUCESSFULLY ✅")
    if( "file_name" not in st.session_state
       or st.session_state.file_name!=file.name
       ):
        st.session_state.file_name = file.name
        st.session_state.df = pd.read_csv(file)
        st.session_state.original_df = st.session_state.df.copy()
    df = st.session_state.df
#=====================================
# PREVIEW DATA
#=====================================
    st.subheader("Data preview 📰 :")
    st.dataframe(df)

    row , coloum = df.shape
    col1 , col2 = st.columns(2)
    with col1:
        st.metric("Rows :",row)
        st.caption("TOTAL NUMBER OF ROWS.")
    with col2:
        st.metric("Columns :",coloum)
        st.caption("TOTAL NUMBER OF COLOUMS.")

#=====================================
#DATA SUMMARY
#=====================================
    st.subheader("DATA SUMMARY 📑")
    if st.checkbox("SHOW DATA SUMMARY :"):
        st.write(df.describe())

#=====================================
# COLUMNS INFORMATION
#=====================================
    st.subheader("COLOUMS INFO :")
    with st.expander("Dataset Info ℹ"):
        if st.checkbox("SHOW COLOUMS NAME"):
            st.write(df.columns)
        if st.checkbox("SHOW DATA TYPE "):
            st.write(df.dtypes)

#=====================================
# DATA REPORTS
#=====================================
    st.subheader("DATASET HEALTH REPORT 🩺")
    missing = df.isnull().sum().sum()
    duplicate = df.duplicated().sum()
    numeric = len(df.select_dtypes(include="number").columns)
    string = len(df.select_dtypes(include="object").columns)

    col1 , col2 , col3 , col4 = st.columns(4)
    with col1:
        st.metric("MISSING VALUES :",missing)
        st.caption("Total Missing values")
    with col2:
        st.metric("DUPLICATED VALUES :",duplicate)
        st.caption("Total Duplicate values")
    with col3:
        st.metric("NUMERIC COLUMNS :",numeric)
        st.caption("Total Numeric columns")
    with col4:
        st.metric("STRING COLUMNS :",string)
        st.caption("Total String columns")
    col1,col2 = st.columns(2)
    with col1:
        if missing == 0:
            st.success("✅ NO MISSING VALUE FOUND.")
        else:
            st.warning(f"⚠ {missing} MISSING VALUE FOUND")
    with col2:
        if duplicate == 0:
            st.success("✅ NO DUPLICATE VALUE FOUND.")
        else:
            st.warning(f"⚠ {duplicate} DUPLICATE VALUE FOUND")
    health = 100
    if missing>0:
        health-=20
    if duplicate>0:
        health-=20
    st.progress(health)
    st.caption(f"Dataset Health : {health}%")

#=====================================
# SIDEBAR 
#=====================================
    st.sidebar.title("⚙️ Dashboard")
    st.sidebar.caption("CSV Data Analyzer")
    st.sidebar.divider()

#=====================================
# CLEANING DATA SIDEBAR
#=====================================
    st.sidebar.header("🧹 DATA CLEANING")
# DUPLICATE REMOVE
    if duplicate > 0:
        if st.sidebar.button("Remove Duplicate Values 🗑"):
            st.session_state.df=df.drop_duplicates()
            st.rerun()

#=====================================
# MISSING REMOVE
#=====================================
    if missing>0:
        action = st.sidebar.selectbox(
            "Choose Action",
            ["~~Select an option~~","Drop missing values 🗑","Fill missing values ✍"]
        )
        if action == "Drop missing values 🗑":
            if st.sidebar.button("Drop Values"):
                # df = df.dropna()
                # st.sidebar.success("Missing values removed successfully ✅")
                # st.dataframe(df)
                st.session_state.df=df.dropna()
                st.rerun()

        elif action == "Fill missing values ✍":
            method = st.sidebar.selectbox(
                "Select Method",
                ["~~Select an option~~","Mean","Mode","Median"]
            )
            num_col = df.select_dtypes(include="number").columns
            if method != "~~Select an option~~":
                if st.sidebar.button("Apply Cleaning"):
                    if method == "Mean":
                        for col in num_col:
                            df[col]=df[col].fillna(df[col].mean())
                    elif method == "Median":
                        for col in num_col:
                            df[col]=df[col].fillna(df[col].median())
                    elif method == "Mode":
                        for col in df.columns:
                            df[col]=df[col].fillna(df[col].mode()[0])
                    st.session_state.df=df
                    st.rerun()

                    remain_miss = df.isnull().sum().sum()

                    if remain_miss == 0:
                        st.sidebar.success("Missing values fill successfully ✅")
                    else :
                        st.warning(f"Cleaning data ! but {remain_miss} missing values still remain ")
    st.sidebar.divider()
    st.divider()

#=====================================
# DATA VISUALIZATION
#=====================================
    st.sidebar.subheader("📊 Visualization")
    chart = st.sidebar.selectbox(
        "Select Chart type",
        [ "~~Select an option~~", "Histogram","Bar Chart","Scatter Plot","Line Chart","Box Plot","Pie Chart"]
    )

    num_col = df.select_dtypes(include="number").columns
    str_col = df.select_dtypes(include="object").columns

#=====================================
# HISTOGRAM
#=====================================
    st.header("📊 VISUALIZATION")
    if chart == "Histogram":
        column = st.sidebar.selectbox(
            "Select Coloumn",
            ["~~Select column name~~"]+list(num_col)
        )
        if column!="~~Select column name~~":
            fig,ax = plt.subplots(figsize=(8,5))
            ax.hist(df[column],bins=10)
            ax.grid(alpha=0.3)
            ax.set_title(f'Histogram of {column}')
            ax.set_xlabel(column)
            ax.set_ylabel("ferequency")
            st.pyplot(fig)

#=====================================
# SCATTER PLOT
#=====================================
    elif chart == "Scatter Plot":
        x = st.sidebar.selectbox(
        "Select X Axis",
        ["~~Select X Axis~~"] + list(num_col)
    )
        y = st.sidebar.selectbox(
        "Select Y Axis",
        ["~~Select Y Axis~~"] + list(num_col)
    )
        if x!="~~Select X Axis~~" and y!="~~Select Y Axis~~":
            fig,ax = plt.subplots(figsize=(8,5))
            ax.scatter(df[x],df[y])
            ax.grid(alpha=0.3)
            ax.set_title(f'{x} vs {y}')
            ax.set_xlabel(f'{x}')
            ax.set_ylabel(f'{y}')
            st.pyplot(fig)

#=====================================
# LINE CHART
#=====================================
    elif chart == "Line Chart":
        x = st.sidebar.selectbox(
        "Select X Axis",
        ["~~Select X Axis~~"] + list(num_col)
    )
        y = st.sidebar.selectbox(
        "Select Y Axis",
        ["~~Select Y Axis~~"] + list(num_col)
    )
        if x!="~~Select X Axis~~" and y!="~~Select Y Axis~~":
            fig,ax = plt.subplots(figsize=(8,5))
            ax.plot(df[x],df[y])
            ax.grid(alpha=0.3)
            ax.set_title(f'{x} vs {y}')
            ax.set_xlabel(f'{x}')
            ax.set_ylabel(f'{y}')
            st.pyplot(fig)

#=====================================
# BAR CHART
#=====================================
    elif chart == "Bar Chart":
        x = st.sidebar.selectbox(
        "Select X Axis",
        ["~~Select X Axis~~"] + list(num_col)
    )
        y = st.sidebar.selectbox(
        "Select Y Axis",
        ["~~Select Y Axis~~"] + list(num_col)
    )
        if x!="~~Select X Axis~~" and y!="~~Select Y Axis~~":
            fig,ax = plt.subplots(figsize=(8,5))
            ax.bar(df[x],df[y])
            ax.grid(alpha=0.3)
            ax.set_title(f'{x} vs {y}')
            ax.set_xlabel(f'{x}')
            ax.set_ylabel(f'{y}')
            st.pyplot(fig)

#=====================================
# BOX PLOT
#=====================================
    elif chart == "Box Plot":
        x = st.sidebar.selectbox(
            "Select Column",
            ["~~Select Column~~"] + list(num_col)
        )
        if x !="~~Select Column~~":
            fig , ax = plt.subplots(figsize=(6,5))
            ax.boxplot(df[x])
            ax.grid(alpha=0.3)
            ax.set_title(f'{x} box plot')
            ax.set_xlabel(f'{x}')
            ax.set_ylabel(f'Frequency')
            st.pyplot(fig)

#=====================================
# PIE CHART
#=====================================
    elif chart =="Pie Chart":
        x=st.sidebar.selectbox(
            "Select columns",
            ["~~Select columns~~"] + list(str_col)
        )
        if x !="~~Select columns~~":
            value = df[x].value_counts().head(8)
            fig , ax = plt.subplots(figsize=(6,6))
            ax.pie(
                value,
                labels=value.index,
                autopct="%1.1f%%",
                startangle=90
            )
            ax.set_title(f'Pie cahrt of {x}')
            st.pyplot(fig)
    st.divider()

#=====================================
# SEARCHING DATA
#=====================================
    st.subheader("🔎 Search Data")
    column = st.selectbox(
        "Select Column",
        ["~~Select an column~~"] + list(df.columns)
    )
    search = st.text_input("Enter Value")
    if search:
        result = df[
            df[column]
            .astype(str)
            .str.contains(
                search,
                case=False
            )
        ]
        st.dataframe(result)
    st.divider()

#=====================================
# FILTER DATA
#=====================================
    st.subheader("🎯 Filter Data")
    column = st.selectbox(
        "Select column",
        ["~~Select column~~"] + list(df.columns)
    )
    if column!="~~Select column~~":
        value = df[column].unique()
        option = st.selectbox(
            "Select Value",
            ["~~Select Value~~"] + list(value)
        )
        if option!="~~Select Value~~":
            result = df[df[column]==option]
            st.dataframe(result)
    st.sidebar.divider()

#=====================================
# RESET ORIGINAL DATA
#=====================================
    st.sidebar.subheader("♻ Dataset")
    if st.sidebar.button("🔄 Reset Dataset"):
        st.session_state.df=st.session_state.original_df.copy()
        st.rerun()
    st.divider()

#=====================================
# CORRELATION MATRIX
#=====================================
    st.subheader("📈 Correlation Matrix")
    corr = df.corr(numeric_only=True)
    fig,ax= plt.subplots(figsize=(6,4))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=1,
        linecolor="white",
        square=True,
        ax=ax
    )
    ax.set_title("Correlation Matrix",
                 fontsize=15,
                 fontweight="bold" 
                 ),
    st.pyplot(fig)
    st.divider()
#=====================================
# DOWMLOAD CLEANED DATA
#=====================================
    st.subheader("📥 DOWNLOAD CLEANED CSV")
    csv = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 DOWNLOAD CLEANED CSV",
        data=csv,
        file_name="Cleaned_data.csv",
        mime="text/csv"
    )
    st.divider()

#=====================================
# GREETING
#=====================================
    st.caption(
    "Developed by Amit Verma | CSV Data Analyzer v1.0"
    )