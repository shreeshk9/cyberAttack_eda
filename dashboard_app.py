import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('cybersecurity_attacks.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Hour'] = df['Timestamp'].dt.hour
    df['Weekday'] = df['Timestamp'].dt.day_name()

    def extract_geo_info(geo_string):
        if pd.isna(geo_string):
            return None, None
        parts = geo_string.split(',')
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        return None, None

    df['City'] = df['Geo-location Data'].apply(lambda x: extract_geo_info(x)[0])
    df['State'] = df['Geo-location Data'].apply(lambda x: extract_geo_info(x)[1])

    # ONLY CITIES FROM YOUR DATASET
    cities_coords = {
        'Jamshedpur': (22.8046, 86.2029), 'Bilaspur': (22.0797, 82.1409),
        'Bokaro': (23.6693, 86.1511), 'Jaunpur': (25.7327, 82.6837),
        'Anantapur': (14.6819, 77.6006), 'Raipur': (21.2514, 81.6296),
        'Ranchi': (23.3441, 85.3096), 'Jodhpur': (26.2389, 73.0243),
        'Kota': (25.2138, 75.8648), 'Gwalior': (26.2183, 78.1828),
        'Vijayawada': (16.5062, 80.6480), 'Madurai': (9.9252, 78.1198),
        'Varanasi': (25.3176, 82.9739), 'Meerut': (28.9845, 77.7064),
        'Amritsar': (31.6340, 74.8723), 'Allahabad': (25.4358, 81.8463),
        'Jabalpur': (23.1815, 79.9864), 'Aurangabad': (19.8762, 75.3433),
        'Dhanbad': (23.7957, 86.4304), 'Srinagar': (34.0837, 74.7973),
        'Thiruvananthapuram': (8.5241, 76.9366), 'Mysore': (12.2958, 76.6394),
        'Tiruchirappalli': (10.7905, 78.7047), 'Bareilly': (28.3670, 79.4304),
        'Aligarh': (27.8974, 78.0880), 'Moradabad': (28.8389, 78.7378),
        'Gorakhpur': (26.7606, 83.3732), 'Jalandhar': (31.3260, 75.5762),
        'Gurgaon': (28.4595, 77.0266), 'Noida': (28.5355, 77.3910),
        'Faridabad': (28.4089, 77.3178), 'Ghaziabad': (28.6692, 77.4538),
        'Udaipur': (24.5854, 73.7125), 'Ajmer': (26.4499, 74.6399),
        'Bikaner': (28.0229, 73.3119), 'Jhansi': (25.4484, 78.5685),
        'Rourkela': (22.2604, 84.8536), 'Cuttack': (20.4625, 85.8828),
        'Bhubaneswar': (20.2961, 85.8245), 'Siliguri': (26.7271, 88.3953),
        'Adoni': (15.6281, 77.2750), 'Durg': (21.1905, 81.2849),
        'Bhilai': (21.2094, 81.3793), 'Guntur': (16.3067, 80.4365),
        'Nellore': (14.4426, 79.9865), 'Warangal': (17.9689, 79.5941),
        'Tirupati': (13.6288, 79.4192), 'Rajahmundry': (17.0005, 81.8040),
        'Kakinada': (16.9891, 82.2475), 'Mangalore': (12.9141, 74.8560),
        'Belgaum': (15.8497, 74.4977), 'Hubli': (15.3647, 75.1240),
        'Shimoga': (13.9299, 75.5681), 'Tumkur': (13.3392, 77.1006),
        'Salem': (11.6643, 78.1460), 'Vellore': (12.9165, 79.1325),
        'Erode': (11.3410, 77.7172), 'Thanjavur': (10.7870, 79.1378),
        'Dehradun': (30.3165, 78.0322), 'Haridwar': (29.9457, 78.1642),
        'Muzaffarpur': (26.1225, 85.3906), 'Purnia': (25.7771, 87.4753),
        'Bhagalpur': (25.2425, 86.9842), 'Darbhanga': (26.1542, 85.8918),
        'Asansol': (23.6739, 86.9524), 'Durgapur': (23.5204, 87.3119),
        'Imphal': (24.8170, 93.9368), 'Agartala': (23.8315, 91.2868),
        'Shillong': (25.5788, 91.8933), 'Aizawl': (23.7271, 92.7176),
        'Kohima': (25.6751, 94.1086), 'Itanagar': (27.1004, 93.6966),
    }

    df['Lat'] = df['City'].map(lambda x: cities_coords.get(x, (None, None))[0])
    df['Long'] = df['City'].map(lambda x: cities_coords.get(x, (None, None))[1])

    df_full = df.copy()


    df = df.dropna(subset=['Lat', 'Long'])

    return df, df_full

df, df_full = load_data()

# Header
st.title("🛡️ Cybersecurity Attack Dashboard")
st.markdown("Real-time Network Threat Intelligence & Analysis")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    attack_filter = st.selectbox("🎯 Attack Type", ['All'] + list(df['Attack Type'].unique()))
with col2:
    severity_filter = st.selectbox("⚠️ Severity", ['All'] + list(df['Severity Level'].unique()))
with col3:
    date_range = st.date_input("📅 Date Range", [df['Timestamp'].min(), df['Timestamp'].max()])

# Filter data
filtered = df.copy()
if attack_filter != 'All':
    filtered = filtered[filtered['Attack Type'] == attack_filter]
if severity_filter != 'All':
    filtered = filtered[filtered['Severity Level'] == severity_filter]

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Attacks", f"{len(filtered):,}")
with col2:
    high = len(filtered[filtered['Severity Level'] == 'High'])
    st.metric("High Severity", f"{high:,}", f"{high/len(filtered)*100:.1f}%")
with col3:
    blocked = len(filtered[filtered['Action Taken'] == 'Blocked'])
    st.metric("Blocked", f"{blocked:,}", f"{blocked/len(filtered)*100:.1f}%")
with col4:
    st.metric("Cities", filtered['City'].nunique())

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Attack Type Distribution")
    attack_counts = filtered['Attack Type'].value_counts()
    fig1 = px.bar(
        x=attack_counts.index, 
        y=attack_counts.values, 
        color=attack_counts.index,
        labels={'x': 'Attack Type', 'y': 'Count'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎯 Severity Distribution")
    sev_counts = filtered['Severity Level'].value_counts()
    fig2 = px.pie(values=sev_counts.values, names=sev_counts.index, hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# Hourly pattern 
st.subheader("⏰ Attacks by Hour of Day")

hourly = df_full['Hour'].value_counts().sort_index()


fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=hourly.index, 
    y=hourly.values, 
    mode='lines+markers',
    line=dict(color='blue', width=3),
    marker=dict(size=10, color='blue', symbol='circle'),
    name='Attacks'
))


fig3.update_layout(
    title={
        'text': 'Attacks by Hour of Day',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 16, 'color': '#222'}
    },

    xaxis=dict(
        title=dict(
            text='Hour (0-23)',
            font=dict(color='#0077cc', size=16)
        ),
        tickmode='array',
        tickvals=[0, 5, 10, 15, 20],
        range=[0, 23],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        tickfont=dict(color='#00aaff', size=14)
    ),

    yaxis=dict(
        title=dict(
            text='Count',
            font=dict(color='#cc6600', size=16)
        ),
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        tickfont=dict(color='#ff8800', size=14)
    ),

    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    height=500,
    margin=dict(l=80, r=40, t=60, b=60)
)

st.plotly_chart(fig3, use_container_width=True)


# Weekly and Protocol
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Weekly Pattern")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly = filtered['Weekday'].value_counts().reindex(days, fill_value=0)
    fig4 = px.bar(x=weekly.index, y=weekly.values,
                  labels={'x': 'Day', 'y': 'Attacks'})
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("🔌 Protocol Distribution")
    proto = filtered['Protocol'].value_counts()
    fig5 = px.bar(y=proto.index, x=proto.values, orientation='h',
                  labels={'x': 'Count', 'y': 'Protocol'})
    st.plotly_chart(fig5, use_container_width=True)

# Geographic Map - TOP 5 CITIES PER SEVERITY LEVEL
st.subheader("🗺️ Geographic Attack Distribution - Top Cities by Severity")
st.markdown("*Showing top 5 cities for each severity level from your dataset*")

geo_full = filtered.groupby(['City', 'Lat', 'Long', 'Severity Level'], as_index=False).size()
geo_full.rename(columns={'size': 'Count'}, inplace=True)

top_high = geo_full[geo_full['Severity Level'] == 'High'].nlargest(5, 'Count')
top_medium = geo_full[geo_full['Severity Level'] == 'Medium'].nlargest(5, 'Count')
top_low = geo_full[geo_full['Severity Level'] == 'Low'].nlargest(5, 'Count')

geo = pd.concat([top_high, top_medium, top_low], ignore_index=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"🔴 High Severity: {len(top_high)} cities")
with col2:
    st.warning(f"🟡 Medium Severity: {len(top_medium)} cities")
with col3:
    st.success(f"🟢 Low Severity: {len(top_low)} cities")

fig6 = px.scatter_geo(
    geo,
    lat='Lat',
    lon='Long',
    size='Count',
    color='Severity Level',
    hover_name='City',
    hover_data={
        'Lat': ':.2f', 
        'Long': ':.2f',
        'Count': True,
        'Severity Level': True
    },
    size_max=40,
    color_discrete_map={
        'High': '#ef4444',
        'Medium': '#f59e0b',
        'Low': '#10b981'
    }
)

fig6.update_geos(
    center=dict(lat=23, lon=78),
    projection_scale=3.5,
    scope='asia',
    showcountries=True,
    countrycolor="rgb(200, 200, 200)",
    showcoastlines=True,
    coastlinecolor="rgb(100, 100, 100)",
    showland=True,
    landcolor="rgb(240, 248, 255)",
    showocean=True,
    oceancolor="rgb(204, 229, 255)",
    bgcolor="white",
    projection_type="mercator"
)

fig6.update_layout(
    height=700,
    margin={"r":10,"t":40,"l":10,"b":10},
    paper_bgcolor="white",
    title_text="Top 15 Attack Hotspots (5 per Severity Level)"
)

st.plotly_chart(fig6, use_container_width=True)

# Table for mapped cities
st.subheader("📋 Top Cities Details")
geo_sorted = geo.sort_values(['Severity Level', 'Count'], ascending=[True, False])
geo_display = geo_sorted[['City', 'Severity Level', 'Count']].reset_index(drop=True)
geo_display.index = geo_display.index + 1

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔴 High Severity")
    st.dataframe(geo_display[geo_display['Severity Level'] == 'High'][['City', 'Count']], use_container_width=True)

with col2:
    st.markdown("#### 🟡 Medium Severity")
    st.dataframe(geo_display[geo_display['Severity Level'] == 'Medium'][['City', 'Count']], use_container_width=True)

with col3:
    st.markdown("#### 🟢 Low Severity")
    st.dataframe(geo_display[geo_display['Severity Level'] == 'Low'][['City', 'Count']], use_container_width=True)

st.markdown("---")

# Top 20 cities (all severities)
st.subheader("🏙️ Top 20 Most Targeted Cities (All Severities)")
top = filtered['City'].value_counts().head(20).reset_index()
top.columns = ['City', 'Total Attacks']
top.index = top.index + 1
st.dataframe(top, use_container_width=True)
