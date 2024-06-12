import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="Consumer Behavior Insights", layout="wide")

# Load customer journey data using the full path
data = pd.read_csv('customer_journey_data.csv')

# Define custom colors
custom_colors = {
    'Awareness': '#636EFA',  # Blue
    'Consideration': '#EF553B',  # Red
    'Decision': '#00CC96',  # Green
    'frequent': '#636EFA',  # Blue
    'one_time': '#AB63FA'  # Purple
}

# App title and logo
st.image("Pattern_Logo.png", width=600)
st.title("Consumer Behavior Insights Generator")

# About This App section
st.markdown("""
# About This App
Welcome to the Consumer Behavior Insights Generator! This application was developed as part of my application for the Market Research Summer Internship Opportunity. It showcases my technical skills in data analysis, interactive visualization, and my understanding of consumer behavior analytics. This app provides a comprehensive analysis of customer journey data, including customer journey mapping, segmentation analysis, conversion funnel analysis, and more. Each section below contains insights and recommendations based on the visualizations.

## Key Points
- **Metrics Selection:** The key metrics chosen to evaluate consumer behavior include Conversion Rate, Click-through Rate, Engagement Score, Bounce Rate, and Page Views.
- **Weighted Analysis:** The insights are computed using a comprehensive analysis of these metrics. The weights can be adjusted dynamically to explore different scenarios.
- **Interactive Visualizations:** The app features interactive bar charts, line charts, and heatmaps to help visualize consumer behavior across different stages of the customer journey.

## Skills Demonstrated
- **Technical Proficiency:** Expertise in Python, data analysis with pandas, and creating interactive visualizations with Plotly.
- **Clear Communication:** Ability to explain complex concepts in a clear and concise manner.
- **Passion for Technology:** A strong interest in how data analytics and technology are reshaping consumer behavior and driving business growth.

*Note: The data used in this application was randomized and generated for the purpose of demonstrating my data analysis skills.*

### Date Built: June 12, 2024
""")




# Sidebar
st.sidebar.header("Filter Options")
segmentation_criteria = st.sidebar.selectbox("Select Segmentation Criteria", options=["Frequent Buyers", "One-time Visitors"])
ab_test_metric = st.sidebar.selectbox("Select Metric to Analyze", options=["Conversion Rate", "Click-through Rate"])

# Customer Journey Mapping
st.header("Customer Journey Mapping")
st.markdown("### Visualize the flow of customers through different stages of the journey.")
journey_counts = data['stage'].value_counts().sort_index()
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=["Awareness", "Consideration", "Decision"],
        color=[custom_colors['Awareness'], custom_colors['Consideration'], custom_colors['Decision']]
    ),
    link=dict(
        source=[0, 1],  # indices correspond to labels
        target=[1, 2],
        value=journey_counts.values[:2]
    )
))
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Most customers start at the Awareness stage, with a significant drop as they progress to the Consideration stage.
- The highest drop-off is observed between Awareness and Consideration stages.
- A relatively smaller drop-off is seen between Consideration and Decision stages.

**Recommendations:**
- Enhance strategies to retain customers transitioning from Awareness to Consideration.
- Focus on personalized marketing efforts to keep customers engaged.
""")

# Customer Journey Timeline
st.header("Customer Journey Timeline")
st.markdown("### Track customer interactions over time.")
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.sort_values(by='timestamp', inplace=True)
timeline_data = data.groupby([data['timestamp'].dt.to_period("M"), 'stage']).size().unstack().fillna(0)
timeline_data = timeline_data.resample('M').sum()

fig = make_subplots(specs=[[{"secondary_y": True}]])
for stage in timeline_data.columns:
    fig.add_trace(
        go.Scatter(x=timeline_data.index.to_timestamp(), y=timeline_data[stage], mode='lines', name=stage,
                   line=dict(color=custom_colors[stage])),
        secondary_y=False,
    )
fig.update_layout(title_text="Customer Journey Timeline")
fig.update_xaxes(title_text="Timestamp")
fig.update_yaxes(title_text="Count")
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Customer interactions at the Awareness stage show higher fluctuation compared to other stages.
- Consideration and Decision stages have more stable interactions over time.
- Peaks in interactions could indicate successful marketing campaigns or product launches.

**Recommendations:**
- Analyze peaks in the Awareness stage to understand what drives customer interest.
- Maintain consistent engagement strategies across all stages to stabilize interactions.
""")

# Aggregated Heatmap of Engagement
st.header("Aggregated Heatmap of Engagement")
st.markdown("### Explore engagement scores by segment and stage.")
agg_heatmap_data = data.pivot_table(index='segment', columns='stage', values='engagement_score', aggfunc='mean')
fig = px.imshow(agg_heatmap_data, aspect='auto', color_continuous_scale='Viridis', title='Aggregated Heatmap of Engagement')

# Adding annotations to the heatmap
for i, segment in enumerate(agg_heatmap_data.index):
    for j, stage in enumerate(agg_heatmap_data.columns):
        fig.add_annotation(dict(
            x=j,
            y=i,
            text=str(round(agg_heatmap_data.loc[segment, stage], 2)),
            showarrow=False,
            font=dict(color="white")
        ))

st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Frequent customers have higher engagement scores across all stages compared to one-time customers.
- Engagement scores are highest during the Consideration stage for both segments.

**Recommendations:**
- Leverage the high engagement during the Consideration stage with targeted offers and incentives.
- Develop loyalty programs to convert one-time customers into frequent customers.
""")

# Segmentation Analysis
st.header("Segmentation Analysis")
st.markdown("### Analyze customer segments based on their behavior patterns.")
if segmentation_criteria == "Frequent Buyers":
    segment_data = data[data['segment'] == 'frequent']
else:
    segment_data = data[data['segment'] == 'one_time']
st.write(segment_data)
st.markdown("""
**Insights:**
- Frequent customers exhibit higher conversion rates and engagement scores compared to one-time customers.
- Bounce rates are lower for frequent customers, indicating better retention.

**Recommendations:**
- Focus on improving the experience for one-time customers to reduce bounce rates.
- Implement personalized marketing strategies to enhance engagement for both segments.
""")

# Pie Chart for Segment Distribution
st.header("Segment Distribution")
st.markdown("### Visualize the distribution of different customer segments.")
segment_distribution = data['segment'].value_counts()
fig = px.pie(values=segment_distribution, names=segment_distribution.index, title='Segment Distribution',
             color=segment_distribution.index, color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- The majority of customers are frequent customers, making up 69.9% of the total customer base.
- One-time customers constitute 30.1% of the customer base.

**Recommendations:**
- Develop retention strategies specifically tailored for one-time customers to increase their lifetime value.
- Continue to nurture frequent customers with exclusive benefits to maintain their loyalty.
""")

# Conversion Funnel Analysis
st.header("Conversion Funnel Analysis")
st.markdown("### Analyze the conversion funnel to understand drop-off rates at each stage.")
funnel_data = pd.DataFrame({
    'stage': journey_counts.index,
    'value': journey_counts.values
})
fig = px.funnel(funnel_data, x='value', y='stage', color='stage',
                color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- The largest drop-off occurs between the Awareness and Consideration stages.
- The Decision stage has the highest conversion rate.

**Recommendations:**
- Improve the nurturing process in the Awareness stage to reduce drop-offs.
- Streamline the transition from Consideration to Decision with clear CTAs and incentives.
""")

# Conversion Rates by Segment
st.header("Conversion Rates by Segment")
st.markdown("### Compare conversion rates between different segments.")
conversion_by_segment = data.groupby('segment')['conversion_rate'].mean().reset_index()
fig = px.bar(conversion_by_segment, x='segment', y='conversion_rate', title='Conversion Rates by Segment',
             color='segment', color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Conversion rates are slightly higher for frequent customers compared to one-time customers.

**Recommendations:**
- Utilize targeted campaigns to increase conversion rates for one-time customers.
- Encourage frequent customers to maintain or increase their conversion rates with loyalty rewards.
""")

# Engagement Score by Segment
st.header("Engagement Score by Segment")
st.markdown("### Compare engagement scores between different segments.")
engagement_by_segment = data.groupby('segment')['engagement_score'].mean().reset_index()
fig = px.bar(engagement_by_segment, x='segment', y='engagement_score', title='Engagement Scores by Segment',
             color='segment', color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Frequent customers have significantly higher engagement scores than one-time customers.

**Recommendations:**
- Focus on engagement strategies for one-time customers to boost their interaction with the brand.
- Continue to engage frequent customers with relevant content and offers.
""")

# Bounce Rate by Stage
st.header("Bounce Rate by Stage")
st.markdown("### Analyze the bounce rate at each stage of the customer journey.")
bounce_rate_by_stage = data.groupby('stage')['bounce_rate'].mean().reset_index()
fig = px.bar(bounce_rate_by_stage, x='stage', y='bounce_rate', title='Bounce Rate by Stage',
             color='stage', color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Bounce rates are highest at the Consideration stage, indicating potential issues in this phase.
- The Decision stage has the lowest bounce rate, suggesting effective engagement strategies.

**Recommendations:**
- Investigate potential barriers or friction points in the Consideration stage to reduce bounce rates.
- Maintain and enhance successful engagement strategies in the Decision stage.
""")

# Page Views by Stage
st.header("Page Views by Stage")
st.markdown("### Compare the average number of page views at each stage.")
page_views_by_stage = data.groupby('stage')['page_views'].mean().reset_index()
fig = px.bar(page_views_by_stage, x='stage', y='page_views', title='Page Views by Stage',
             color='stage', color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- The Decision stage has the highest average number of page views, indicating strong customer interest.
- The Awareness stage has the lowest average number of page views.

**Recommendations:**
- Increase efforts to drive page views during the Awareness stage with engaging content and promotions.
- Continue to optimize the Decision stage to maintain high levels of customer interest.
""")

# A/B Test Results
st.header("A/B Test Results")
st.markdown("### Simulate A/B test scenarios and show how different changes impact key metrics.")
# Map the selected metric to the corresponding column name
metric_column = "conversion_rate" if ab_test_metric == "Conversion Rate" else "click_through_rate"

ab_data = data.groupby('stage')[metric_column].mean().reset_index()
fig = px.bar(ab_data, x='stage', y=metric_column, title=f"{ab_test_metric} Results",
             color='stage', color_discrete_map=custom_colors)
st.plotly_chart(fig)
st.markdown("""
**Insights:**
- Conversion rates are highest at the Decision stage, followed by the Consideration stage.
- Click-through rates show similar trends across different stages.

**Recommendations:**
- Implement changes that positively impact conversion rates in the Awareness stage.
- Test different CTAs and page designs to optimize click-through rates across all stages.
""")

# Customer Retention Analysis
st.header("Customer Retention Analysis")
st.markdown("### Analyze customer retention over time.")
# Assuming retention information is available
if 'retention_period' in data.columns and 'retention_rate' in data.columns:
    retention_data = data.copy()
    retention_data['retention_period'] = pd.to_numeric(retention_data['retention_period'])
    retention_data.sort_values(by='retention_period', inplace=True)
    
    # Aggregate by week and calculate mean retention rate
    retention_data['retention_week'] = retention_data['retention_period'] // 7
    weekly_retention = retention_data.groupby('retention_week')['retention_rate'].mean().reset_index()
    
    fig = px.line(weekly_retention, x='retention_week', y='retention_rate', markers=True, title='Customer Retention Over Time')
    st.plotly_chart(fig)
    st.markdown("""
    **Insights:**
    - Retention rates fluctuate over time, with notable peaks and troughs.
    - The highest retention rates are observed in specific weeks, potentially indicating effective retention strategies during those periods.

    **Recommendations:**
    - Identify factors contributing to high retention rates during peak periods and replicate those strategies.
    - Address issues causing low retention rates to minimize customer churn.
    """)
else:
    st.write("Retention data not available.")

# Additional Insights and Recommendations
st.header("Insights and Recommendations")
st.markdown("""
### Key Takeaways:
1. **Enhance Content in the 'Awareness' Stage:** Focus on providing valuable information to keep users engaged.
2. **Optimize Conversion Strategies:** Use A/B test results to refine strategies and improve conversion rates.
3. **Monitor and Improve Retention:** Regularly analyze retention data to identify and address issues.

Thank you for using the Consumer Behavior Insights Generator! If you have any questions or need further analysis, feel free to reach out.
""")
