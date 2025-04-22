import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import statsmodels.api as sm
# Load the dataset

data = pd.read_csv('bank_cleaned.csv')

#['int_tgt', 'demog_age', 'demog_ho', 'demog_homeval', 'demog_inc', 'demog_pr', 'rfm1', 'demog_genf', 'demog_genm']

# App Title and Description
st.title("Interactive Data Pattern Exploration App")
st.write("This interactive dashboard presents insights from banking data covering 76573 customers with 20 different variables. The data has been cleaned and includes information like customer age, gender, homeownership, income and behavior metrics like purchase history, sales figures etc.")
st.write("Use the filters on the sidebar to explore and change the visualizations made for different attributes of the data ")


# Sidebar Filters
st.sidebar.header("Filter Options")   #give a title for the sidebar menu


# Sidebar Filters for Numerical Variables

demog_age = st.sidebar.slider("Age", int(data['demog_age'].min()), int(data['demog_age'].max()), (5, 30))
demog_pr = st.sidebar.slider("Retired Percentage", int(data['demog_pr'].min()), int(data['demog_pr'].max()), (20, 50))


# Sidebar Filters for Categorical Variables
demog_ho = st.sidebar.multiselect("HomeOwner", options=data['demog_ho'].unique(), default=data['demog_ho'].unique())
# demog_genf = st.sidebar.multiselect("Female", options=data['demog_genf'].unique(), default=data['demog_genf'].unique())


# Create a dictionary to map binary values to display values
gender_display_map = {1: "Female", 0: "Male"}

# Get unique values from the binary column
unique_values = data['demog_genf'].unique()

# Map these binary values to display values for the sidebar options
display_options = [gender_display_map[value] for value in unique_values]

# Create the multiselect with display values
demog_genf_display = st.sidebar.multiselect(
    "Gender", 
    options=display_options,
    default=display_options
)

# Convert the selected display values back to binary for filtering
demog_genf_selected_binary = [key for key, value in gender_display_map.items() if value in demog_genf_display]

# Filter the dataframe based on the selected binary values
filtered_data = data[data['demog_genf'].isin(demog_genf_selected_binary)]


# Filter data based on selections
filtered_data = data[
    (data['demog_age'].between(*demog_age)) &
    (data['demog_age'].between(*demog_pr)) &
    (data['demog_ho'].isin(demog_ho)) &
    (data['demog_genf'].isin(demog_genf_selected_binary))
]

# .between(*experience_range): checks whether each value in the experience column falls within the range
# experience_range  is a tuple
# * operator unpacks the tuple
# & acts as an AND operator




# Show filtered data if user selects the option
if st.sidebar.checkbox("Show Filtered Data"):
    st.write(filtered_data)

# st.sidebar places the checkbox in the sidebar section of the Streamlit app.
# checkbox("Show Filtered Data") creates a checkbox with the label "Show Filtered Data"
# st.write(filtered_data):



## Add a histogram
# Section: Distribution of Customer Age
st.header("Distribution of Customer Age")
st.write("This histogram shows the distribution of customer age in the filtered data.")

# Plot histogram
fig, ax = plt.subplots()
sns.histplot(filtered_data['demog_age'], bins=20, color='skyblue', kde=False, ax=ax)
ax.set_title("Distribution of Customer Ages")
ax.set_xlabel("Age")
ax.set_ylabel("Frequency")
st.pyplot(fig)


# Adding a Scatter Plot
# Section: Scatter Plot - Home value  vs. Income

st.header("Scatter Plot: Home value  vs. Income")
st.write("Check the box below to add a trendline to the scatter plot.")
show_trendline = st.checkbox("Show Trendline", value=False)

fig = px.scatter(filtered_data, x='demog_inc', y='demog_homeval', title="Home value  vs. Income",
                 labels={"demog_inc": "Income ($)", "demog_homeval": "Home ($)"},
                 trendline="ols" if show_trendline else None)
st.plotly_chart(fig)






## Add a correlation matrix

# Section: Correlation Matrix
st.header("Correlation Matrix")
st.write("Check the box to view the correlation matrix for numerical variables.")

continuous_vars = ['int_tgt', 'demog_age', 'demog_inc', 'demog_pr', 'rfm1', 'demog_homeval', 'demog_ho', 'demog_genf', 'demog_genm']

# Show correlation matrix
if st.checkbox("Show Correlation Matrix"):
    corr_matrix = filtered_data[continuous_vars].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
