import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
data = pd.read_csv("Scorecards 2023-2024 - Sheet1.csv")

# Preprocess the data
data['Submitted'] = pd.to_datetime(data['Submitted'], errors='coerce')
data['Month'] = data['Submitted'].dt.to_period('M')  # Extract month-year for grouping


# Title
st.title("Interview Dashboard Talent Adquisition GFM/Classy")

# Sidebar Filters
st.sidebar.header("Filters")
filter_q = st.sidebar.selectbox("Select Q:", sorted(data['Q'].unique()), index=0)
filter_year = st.sidebar.selectbox("Select Year:", sorted(data['Year'].unique()), index=0)

# Column filters, including Outcome
st.sidebar.header("Column Filters")
column_filters = {}
for column in ['Interviewer', 'Stage', 'Job', 'Outcome']:
    unique_values = sorted(data[column].dropna().unique())
    selected_values = st.sidebar.multiselect(f"Filter by {column}:", unique_values)
    if selected_values:
        column_filters[column] = selected_values

# Apply filters
filtered_data = data.copy()
if filter_q:
    filtered_data = filtered_data[filtered_data['Q'] == filter_q]
if filter_year:
    filtered_data = filtered_data[filtered_data['Year'] == filter_year]
for column, values in column_filters.items():
    filtered_data = filtered_data[filtered_data[column].isin(values)]

# Metrics
st.header("General Metrics")

# Total interviews by Q and Year
st.subheader("Total Interviews by Q and Year")
total_by_q_year = data.groupby(['Q', 'Year']).size().reset_index(name='Total Interviews')
st.dataframe(total_by_q_year)
fig_q_year = px.bar(total_by_q_year, x='Q', y='Total Interviews', color='Year', title="Total Interviews by Q and Year")
st.plotly_chart(fig_q_year, use_container_width=True)

# Total interviews by interviewer
st.subheader("Total Interviews by Interviewer")
total_by_interviewer = filtered_data.groupby('Interviewer').size().reset_index(name='Total Interviews')
st.dataframe(total_by_interviewer)
fig_interviewer = px.bar(total_by_interviewer, x='Interviewer', y='Total Interviews', title="Total Interviews by Interviewer", text='Total Interviews')
fig_interviewer.update_traces(textposition='outside')
st.plotly_chart(fig_interviewer, use_container_width=True)

# Total interviews by stage
st.subheader("Total Interviews by Stage")
total_by_stage = filtered_data.groupby('Stage').size().reset_index(name='Total Interviews')
st.dataframe(total_by_stage)
fig_stage = px.bar(total_by_stage, x='Stage', y='Total Interviews', title="Total Interviews by Stage", text='Total Interviews')
fig_stage.update_traces(textposition='outside')
st.plotly_chart(fig_stage, use_container_width=True)

# Negative responses by interviewer
st.subheader("Negative Responses by Interviewer")
negative_by_interviewer = filtered_data[filtered_data['Outcome'].str.contains("No", na=False)].groupby('Interviewer').size().reset_index(name='Negative Responses')
st.dataframe(negative_by_interviewer)
fig_negative_interviewer = px.bar(negative_by_interviewer, x='Interviewer', y='Negative Responses', title="Negative Responses by Interviewer", text='Negative Responses')
fig_negative_interviewer.update_traces(textposition='outside')
st.plotly_chart(fig_negative_interviewer, use_container_width=True)

# Negative responses by interviewer and stage
st.subheader("Negative Responses by Interviewer and Stage")
negative_by_interviewer_stage = filtered_data[filtered_data['Outcome'].str.contains("No", na=False)].groupby(['Interviewer', 'Stage']).size().reset_index(name='Negative Responses')
st.dataframe(negative_by_interviewer_stage)
fig_negative_stage = px.bar(negative_by_interviewer_stage, x='Stage', y='Negative Responses', color='Interviewer', title="Negative Responses by Interviewer and Stage")
st.plotly_chart(fig_negative_stage, use_container_width=True)

# Negative responses by interviewer and job
st.subheader("Negative Responses by Interviewer and Job")
negative_by_interviewer_job = filtered_data[filtered_data['Outcome'].str.contains("No", na=False)].groupby(['Interviewer', 'Job']).size().reset_index(name='Negative Responses')
st.dataframe(negative_by_interviewer_job)
fig_negative_job = px.bar(negative_by_interviewer_job, x='Job', y='Negative Responses', color='Interviewer', title="Negative Responses by Interviewer and Job")
st.plotly_chart(fig_negative_job, use_container_width=True)

# Total interviews by month
st.subheader("Total Interviews by Month")
total_by_month = filtered_data.groupby(filtered_data['Submitted'].dt.to_period('M')).size().reset_index(name='Total Interviews')
total_by_month['Submitted'] = total_by_month['Submitted'].astype(str)  # Convert Period to string
st.dataframe(total_by_month)
fig_month = px.bar(total_by_month, x='Submitted', y='Total Interviews', title="Total Interviews by Month", text='Total Interviews')
fig_month.update_traces(textposition='outside')
st.plotly_chart(fig_month, use_container_width=True)

# Total Outcome counts
st.subheader("Total Outcomes")
total_outcomes = filtered_data['Outcome'].value_counts().reset_index()
total_outcomes.columns = ['Outcome', 'Total']
st.dataframe(total_outcomes)
fig_outcome = px.bar(total_outcomes, x='Outcome', y='Total', title="Total Outcomes", text='Total')
fig_outcome.update_traces(textposition='outside')
st.plotly_chart(fig_outcome, use_container_width=True)

# Advanced filtering section
st.header("Filtered Data Viewer")
st.subheader("Explore the data with applied filters")
st.dataframe(filtered_data)


# Comparison Dashboard: Q and Year
st.header("Comparison Dashboard")

# Total interviews by Q and Year
st.subheader("Total Interviews by Q and Year")
total_by_q_year = data.groupby(['Q', 'Year']).size().reset_index(name='Total Interviews')
st.dataframe(total_by_q_year)

# Graph: Total interviews by Q and Year
fig_comparison = px.bar(total_by_q_year, x='Q', y='Total Interviews', color='Year',
                        title="Total Interviews by Q and Year", barmode='group', text='Total Interviews')
fig_comparison.update_traces(textposition='outside')
st.plotly_chart(fig_comparison, use_container_width=True)

# Total interviews by interviewer and Q-Year
st.subheader("Total Interviews by Interviewer, Q and Year")
interviewer_by_q_year = data.groupby(['Interviewer', 'Q', 'Year']).size().reset_index(name='Total Interviews')
st.dataframe(interviewer_by_q_year)

# Graph: Total interviews by Interviewer and Q-Year
fig_interviewer_q_year = px.bar(interviewer_by_q_year, x='Interviewer', y='Total Interviews', color='Year',
                                facet_col='Q', title="Total Interviews by Interviewer, Q and Year")
st.plotly_chart(fig_interviewer_q_year, use_container_width=True)

# Total outcomes by Q and Year
st.subheader("Outcomes by Q and Year")
outcomes_by_q_year = data.groupby(['Outcome', 'Q', 'Year']).size().reset_index(name='Total')
st.dataframe(outcomes_by_q_year)

custom_color = '#02A95C'
color_discrete_map = {year: custom_color for year in outcomes_by_q_year['Year'].unique()}

# Graph: Outcomes by Q and Year with custom color
fig_outcomes_q_year = px.bar(outcomes_by_q_year, x='Outcome', y='Total', color='Year',
                             facet_col='Q', title="Outcomes by Q and Year",
                             color_discrete_map=color_discrete_map)
st.plotly_chart(fig_outcomes_q_year, use_container_width=True)

# Total interviews by stage and Q-Year
st.subheader("Total Interviews by Stage, Q and Year")
stage_by_q_year = data.groupby(['Stage', 'Q', 'Year']).size().reset_index(name='Total Interviews')
st.dataframe(stage_by_q_year)

# Graph: Total interviews by Stage and Q-Year
fig_stage_q_year = px.bar(stage_by_q_year, x='Stage', y='Total Interviews', color='Year',
                          facet_col='Q', title="Total Interviews by Stage, Q and Year")
st.plotly_chart(fig_stage_q_year, use_container_width=True)