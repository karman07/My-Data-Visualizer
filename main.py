import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title='Data Visualizer',
    layout='wide',
    page_icon='📊'
)

# Set Seaborn theme for better aesthetics
sns.set_theme(style="darkgrid")

# Title and description
st.title('📊 Data Visualizer')
st.markdown("""
Welcome to the **Data Visualizer**!  
- Upload your CSV files into the **data** folder.  
- Choose a file, filter data, and visualize various plot types.  
""")

working_dir = os.path.dirname(os.path.abspath(__file__))

# Folder path for CSV files
folder_path = f"{working_dir}/data"

# Ensure the data folder exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Allow users to upload CSV files
st.subheader("📤 Upload a CSV file")
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

if uploaded_file is not None:
    # Save the uploaded file to the data folder
    file_path = os.path.join(folder_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File **{uploaded_file.name}** uploaded successfully!")

# List all CSV files in the folder
try:
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
except FileNotFoundError:
    st.error("Data folder not found. Please make sure it exists.")
    files = []

# Dropdown to select a file
selected_file = st.selectbox('Select a file', files)

if selected_file:
    file_path = os.path.join(folder_path, selected_file)

    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        st.success(f"Loaded **{selected_file}** successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # Display basic info
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # Display statistics
    st.subheader("📊 Data Statistics")
    st.write(df.describe())

    # Filter data
    st.subheader("🔧 Data Filtering")
    columns = df.columns.tolist()
    filter_col = st.selectbox("Select a column to filter", options=columns)
    unique_values = df[filter_col].dropna().unique()
    filter_value = st.selectbox("Select a value to filter by", options=unique_values)
    filtered_df = df[df[filter_col] == filter_value]
    st.write(f"Filtered Data ({filter_col} = {filter_value}):")
    st.write(filtered_df)

    # Plotting section
    st.subheader("📈 Data Visualization")
    col1, col2, col3 = st.columns(3)

    with col1:
        x_axis = st.selectbox('X-axis', options=["None"] + columns)
    with col2:
        y_axis = st.selectbox('Y-axis', options=["None"] + columns)
    with col3:
        plot_type = st.selectbox('Plot Type', [
            'Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Box Plot', 'Heatmap', 'Pie Chart'
        ])

    # Additional options
    if plot_type == 'Heatmap':
        st.subheader("📊 Correlation Heatmap")
        corr_matrix = filtered_df.corr()
        st.write(corr_matrix)
        st.pyplot(sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt='.2f'))

    if st.button('Generate Plot'):
        if x_axis == "None" or y_axis == "None":
            st.warning("Please select both X and Y axes.")
        else:
            fig, ax = plt.subplots(figsize=(8, 5))

            try:
                if plot_type == 'Line Plot':
                    sns.lineplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
                elif plot_type == 'Bar Chart':
                    sns.barplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
                elif plot_type == 'Scatter Plot':
                    sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
                elif plot_type == 'Distribution Plot':
                    sns.histplot(data=filtered_df, x=x_axis, kde=True, ax=ax)
                elif plot_type == 'Count Plot':
                    sns.countplot(data=filtered_df, x=x_axis, ax=ax)
                elif plot_type == 'Box Plot':
                    sns.boxplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
                elif plot_type == 'Pie Chart':
                    pie_data = filtered_df[x_axis].value_counts()
                    fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
                    ax_pie.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                    ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    st.pyplot(fig_pie)

                plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=14)
                plt.xlabel(x_axis, fontsize=12)
                plt.ylabel(y_axis, fontsize=12)
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error generating plot: {e}")
else:
    st.info("Please select a file to begin visualization.")
