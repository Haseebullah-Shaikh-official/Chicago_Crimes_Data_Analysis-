import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

@st.cache_data(persist=True)
def get_data():
    chicago_crimes_df = pd.read_csv("preprocessed_crimes.csv")
    chicago_crimes_df['Date'] = pd.to_datetime(chicago_crimes_df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    return chicago_crimes_df

chicago_crimes_df = get_data()

def textual_definitions():
    st.write("<h3>Dataset Description</h3>", unsafe_allow_html=True)
    st.write('''
        <p style="text-align: justify;">
        This dataset reflects reported incidents of crime (with the exception of murders where
        data exists for each victim) that occurred in the City of Chicago from 2001 to present,
        minus the most recent seven days. Data is extracted from the Chicago Police Department's
        CLEAR (Citizen Law Enforcement Analysis and Reporting) system.</p>
        
        <h5>In order to protect the privacy of crime victims, addresses are shown at the block level only and specific
        locations are not identified.</h5>
        
        <p style="text-align: justify;">
        Should you have questions about this dataset, you may contact the Data Fulfillment and Analysis Division of the
        Chicago Police Department at DFA@ChicagoPolice.org.</p>
        
        <p style="text-align: justify;">
        Disclaimer: These crimes may be based upon preliminary information supplied to the Police Department by the
        reporting parties that have not been verified. The preliminary crime classifications may be changed at a later
        date based upon additional investigation and there is always the possibility of mechanical or human error.
        Therefore, the Chicago Police Department does not guarantee (either expressed or implied) the accuracy,
        completeness, timeliness, or correct sequencing of the information and the information should not be used for
        comparison purposes over time. The Chicago Police Department will not be responsible for any error or omission,
        or for the use of, or the results obtained from the use of this information.</p>
        
        <h5>All data visualizations on maps should be considered approximate and attempts to derive specific addresses
        are strictly prohibited.</h5>
        
        <p style="text-align: justify;">
        The Chicago Police Department is not responsible for the content of any off-site pages that are referenced by or
        that reference this web page other than an official City of Chicago or Chicago Police Department web page. The
        user specifically acknowledges that the Chicago Police Department is not responsible for any defamatory,
        offensive, misleading, or illegal conduct of other users, links, or third parties and that the risk of injury
        from the foregoing rests entirely with the user. The unauthorized use of the words "Chicago Police Department,"
        "Chicago Police," or any colorable imitation of these words or the unauthorized use of the Chicago Police
        Department logo is unlawful. This web page does not, in any way, authorize such use. Data are updated daily.</p>
        ''', unsafe_allow_html=True)

    st.write("<h3>Major Columns Understanding</h3>", unsafe_allow_html=True)
    st.write('''
        <p><b>ID:</b> Unique identifier to a crime</p>
        <p><b>Primary type:</b> Type of the crime</p>
        <p><b>Block:</b> Specific area or street near the incident location</p>
        <p><b>Ward:</b> The City of Chicago is divided into fifty wards. Each Ward is represented by an
        alderman who is elected by their constituency to serve a four-year term.</p>
        <p><b>Districts:</b> The City of Chicago is divided into 25 police districts.</p>
        <p><b>Beat:</b> Beat is teams of 8-10 people fully equipped, motorized police unit. They work under
        the districts officers.</p>
        <p><b>Community Area:</b> Chicago is divided into seventy-seven (77) Community Areas. These
        boundaries do not change over time (as political boundaries do).</p>
        <p><b>Domestic:</b> Information about the criminal to check if the criminal is a family member or a stranger.</p>
        ''', unsafe_allow_html=True)

    st.write("<h3>Consideration in Preprocessing </h3>", unsafe_allow_html=True)
    st.write('''
        <p>Based on the given instructions in the dataset description, the following preprocessing steps were taken to
        avoid inaccurate results:</p>
        
        <p>Null values in location-related columns are replaced with the keyword "not specified" since specific
        locations of incidents are not provided in the dataset.</p>
        
        <p>Null values in the 'ward' and 'community area' columns (float data type columns) are replaced using the
        following techniques:</p>
        
        <p>Mapping technique: The already specified blocks within the given community area and ward are used to
        identify the respective ward and community area for rows with null values in those columns. If a block is
        identified, it replaces the null ward and community area.</p>
        
        <p>For remaining null values in 'community area' and 'ward' columns, which contain unidentified or new
        blocks, the value 100 is used to represent "not specified."</p>
        
        <p>As suggested, visualizations on locations should be considered approximate, and any attempts to derive
        specific locations are prohibited. Therefore, the data was analyzed ward, community, district, and beat-wise
        and within the ward and community, block-wise to maintain privacy.</p>
    
        ''', unsafe_allow_html=True)
        

def crime_types_pie_chart(chicago_crimes_df):
    primary_type_counts = chicago_crimes_df['Primary Type'].value_counts().iloc[:10]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(primary_type_counts, labels=primary_type_counts.index, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    ax.set_title('Top 10 Crime Distributions')
    fig.patch.set_facecolor('lightgrey')
    st.pyplot(fig)

def crimes_with_arrest_or_domestic(chicago_crimes_df, count_rate):
    crime_counts = chicago_crimes_df.groupby(['Primary Type', count_rate]).size().reset_index(name='Count')
    true_crimes = crime_counts[crime_counts[count_rate] == True]
    false_crimes = crime_counts[crime_counts[count_rate] == False]
    merged_crimes = true_crimes.merge(false_crimes, on='Primary Type', suffixes=(f'_{count_rate}', f'_Non-{count_rate}'))
    fig_count_rate_type = px.bar(merged_crimes, 
                x='Primary Type', y=f'Count_{count_rate}', 
                title=f'Major Numbers of {count_rate} Crimes by types',
                labels={'Primary Type': 'Crime Type', f'Count_{count_rate}': 'Number of Crimes'},
                color_discrete_map={f'Count_{count_rate}': 'blue'},   
                width=1000, height=600)

    fig_count_rate_type.add_bar(x=merged_crimes['Primary Type'], y=merged_crimes[f'Count_Non-{count_rate}'], 
                name=f'Non-{count_rate}', marker_color='red')

    fig_count_rate_type.update_layout(barmode='stack', xaxis_tickangle=-45)
    st.plotly_chart(fig_count_rate_type)

def crime_by_area_type(chicago_crimes_df, area_type):
    crime_by_area = chicago_crimes_df.groupby(area_type).size().reset_index(name='Count')
    crime_by_area_sorted = crime_by_area.sort_values(by='Count', ascending=False)
    fig_by_area_type = px.bar(
    crime_by_area_sorted,
    x=area_type,
    y='Count',
    title=f'Crime Frequency by {area_type}',
    width=1000,
    height=600
    )
    fig_by_area_type.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_by_area_type)

def crimes_by_area_with_type(chicago_crimes_df, area,type):
    crime_counts = chicago_crimes_df.groupby([area, type]).size().reset_index(name='Count')
    grouped_df = crime_counts.groupby(area)['Count'].sum().reset_index(name='Count')
    sorted_df = grouped_df.sort_values(by='Count', ascending=False)
    sorted_df

    selected_area = st.selectbox(f'Select an {area} no.', tuple(sorted_df[area].tolist()),key=f"select_box_{area}_{type}")

    fig_name = f'fig_{selected_area}'
    area_number = crime_counts[crime_counts[area] == selected_area]
    temp = (area_number[area].iloc[0])
    fig_name = px.bar(area_number, x=type, y='Count', title=f'{area} "{temp}" by {type}', width=1000, height=600)
    fig_name.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_name)


def crimes_depatments_aresst_rate(chicago_crimes_df, team):
    crime_counts_by_District = chicago_crimes_df.groupby(team).size().reset_index(name='Crime_Count')
    crime_counts_by_District = crime_counts_by_District.sort_values(by='Crime_Count', ascending=False)
    top_10_Districts = crime_counts_by_District.head(10)
    arrest_counts_by_District_top_10 = chicago_crimes_df[chicago_crimes_df[team].isin(top_10_Districts[team])]
    arrest_counts_by_District = arrest_counts_by_District_top_10.groupby([team, 'Arrest']).size().reset_index(name='Arrest_Count')
    fig = px.bar(arrest_counts_by_District, x=team, y='Arrest_Count', color='Arrest',
                labels={team: team, 'Arrest_Count': 'Count'},
                title=f'{team} wise Crime Counts with Arrests and Non-Arrests',
                barmode='stack', width=1500, height=600,
                color_discrete_map={'True': 'blue', 'False': 'red'})
    fig.update_traces(marker_line_width=0)
    fig.update_layout(xaxis_title=team, yaxis_title='Count', legend_title='Arrest')
    st.plotly_chart(fig)


def crimes_by_year(chicago_crimes_df):
    df_year_wise = chicago_crimes_df['Date'].dt.year
    year_counts = df_year_wise .value_counts().sort_index()
    fig_name = px.bar(
        x=year_counts.index,
        y=year_counts.values,
        text=year_counts.values,
        title='Occurrences of Crimes by Year',
        labels={'x': 'Year', 'y': 'Count'},
        width=1000,
        height=800
    )
    fig_name.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig_name)

def crimes_by_month(chicago_crimes_df):
    df_month_wise = chicago_crimes_df['Date'].dt.month
    month_counts = df_month_wise .value_counts().sort_index()
    fig_name = px.bar(
    x=month_counts.index,
    y=month_counts.values,
    text=month_counts.values,
    title='Occurrences of Crimes by month',
    labels={'x': 'Month', 'y': 'Count'},
    width=1000,
    height=800
    )
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    fig_name.update_xaxes(type='category', tickmode='array', tickvals=month_counts.index, ticktext=month_names, tickangle=-45)

    st.plotly_chart(fig_name)
    

def crimes_by_day(chicago_crimes_df):
    crime_in_chicago_df_day_name = chicago_crimes_df['Date'].dt.strftime('%A')
    day_counts = crime_in_chicago_df_day_name.value_counts()
    fig_name = px.bar(
        x=day_counts.index,
        y=day_counts.values,
        text=day_counts.values, 
        title='Occurrences of Crimes by Day',
        labels={'x': 'Day', 'y': 'Count'},
        width=1000,
        height=800
    )
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    fig_name.update_xaxes(type='category', tickmode='array', tickvals=day_names, ticktext=day_names, tickangle=-45)
    fig_name.update_yaxes(range=[1000000, 1200000])
    st.plotly_chart(fig_name)
    

def crimes_by_hour(chicago_crimes_df):
    chicago_crimes_df_time = chicago_crimes_df['Date'].dt.strftime('%H')
    time_counts = chicago_crimes_df_time.value_counts()
    time_counts = time_counts.sort_index()
    fig = px.bar(
        x=time_counts.index,
        y=time_counts.values,
        text=time_counts.values,  
        title='Occurrences of Crimes by Hour',
        labels={'x': 'Hour', 'y': 'Count'},
        width=1000,
        height=800
    )
    st.plotly_chart(fig)
    
def basics():

    textual_definitions()

    st.write('<h3>Crime types distributions</h3>',  unsafe_allow_html=True)
    crime_types_pie_chart(chicago_crimes_df)

    st.write('<h3>Crime Counts by Domestic vs Non-Domestic</h3>',  unsafe_allow_html=True)
    crimes_with_arrest_or_domestic(chicago_crimes_df,"Domestic")

    st.write('<h3>Crime Counts by Arrest vs Non-Arrest</h3>',  unsafe_allow_html=True)
    crimes_with_arrest_or_domestic(chicago_crimes_df,"Arrest")


def crimes_by_police_deparements():
    st.write("<h3>Crimes Analytics by police departments</h3>", unsafe_allow_html=True)

    st.write('''          
        <h4>Analytics Use Cases:</h4>
        <p><b>a. Identifying Districts and Their Beats with Major Crimes:</b> The analytics can help the Chicago Police 
        Department identify districts and their beats (areas under the beat team) with high incidences of major crimes.</p>
        
        <p><b>b. Districts with Major Crimes but Low Arrest Rates:</b> By analyzing the data, it's possible to identify 
        districts and beat teams that have a high occurrence of major crimes but a low rate of successful arrests.</p>
        
        <p><b>c. Evaluating District Officers and Beat Teams Performance:</b> The analytics can evaluate the performance 
        of district officers and beat teams in different aspects:</p>
        
        <ul>
            <li><b>Successful Arrests:</b> Identify which districts and beat teams have a high success rate in arresting 
            criminals.</li>
            <li><b>Performance Gaps:</b> Determine which districts and beat teams are not performing well, for example, 
            having a high number of major crimes but a low arrest rate.</li>
        </ul>
        ''', unsafe_allow_html=True)

    st.write("<h3>Police Districts having major crimes with their type</h3>", unsafe_allow_html=True)
    crimes_by_area_with_type(chicago_crimes_df, "District", "Primary Type")

    st.write("<h3>Police Districts having major crimes beat wise</h3>", unsafe_allow_html=True)
    crimes_by_area_with_type(chicago_crimes_df, "District", "Beat")

    st.write("<h3>Police Districts arrest rate</h3>", unsafe_allow_html=True)
    crimes_depatments_aresst_rate(chicago_crimes_df, "District")

    st.write("<h3>Police Beat arrest rate</h3>", unsafe_allow_html=True)
    crimes_depatments_aresst_rate(chicago_crimes_df, "Beat")


def crimes_by_chicago_areas():

    st.write("<h3>Crimes Analytics by areas</h3>", unsafe_allow_html=True)

    st.write("<h4>Analytics Use Cases</h4>", unsafe_allow_html=True)
    st.write('''
        <p>The analytics can help the Chicago Police Department to identify:</p>
  
        <p><b>1. Wards and Community Areas with Major Crimes:</b> The analysis can pinpoint wards and community areas 
        experiencing high incidences of major crimes, which may require an increase in police teams within the 
        respective districts to address the issues effectively.
        </p>
        
        <p><b>2. Blocks with Major Crimes in Each Ward and Community Area:</b> By examining the data, it is possible to 
        identify specific blocks within each ward and community area that are hotspots for major crimes. This can help 
        in targeting resources for crime prevention and enforcement efforts.
        </p>
        
        <p><b>3. Vulnerable Community Members:</b> The analytics can highlight communities where people are more likely 
        to become victims of criminal activities. This information can be used to implement targeted outreach and 
        support programs for the vulnerable population.
        </p>
       
        ''', unsafe_allow_html=True)

    areas = {
    "Community Area": crime_by_area_type,
    "Ward": crime_by_area_type,
    }

    selected_area = st.selectbox('Select an area:', tuple(areas.keys()), key=f"select_box_crime_area")
    if selected_area == "Ward":
        areas[selected_area](chicago_crimes_df, "Ward")
    else:
        areas[selected_area](chicago_crimes_df, "Community Area")


    st.write("<h3>Community areas having major crimes with their type</h3>", unsafe_allow_html=True)
    crimes_by_area_with_type(chicago_crimes_df, "Community Area", "Primary Type")

    st.write("<h3>Ward areas having major crimes with their type</h3>", unsafe_allow_html=True)
    crimes_by_area_with_type(chicago_crimes_df, "Ward", "Primary Type")

    st.write("<h3>Community areas having major crimes block wise</h3>", unsafe_allow_html=True)
    crimes_by_area_with_type(chicago_crimes_df, "Community Area", "Block")

    st.write("<h3>Ward having major crimes block wise</h3>", unsafe_allow_html=True)
    crimes_by_area_with_type(chicago_crimes_df, "Ward", "Block")

def crimes_by_time():
    st.write("<h3>Crimes Analytics by time</h3>", unsafe_allow_html=True)
    st.write("<h4>Analytics Use Cases</h4>", unsafe_allow_html=True)
    st.write('''
        <p>The analytics can help the Chicago Police Department to identify:</p>
      
        <p><b>1. Performance Analysis Over Time:</b> The analysis can track the performance of the police department, 
        districts, and their respective beats over the years. This includes monitoring the trends of crime, such as 
        increases or decreases in crime rates over time.</p>
        
        <p><b>2. Major Crime Occurrences by Year:</b> By examining the data, it is possible to determine in which 
        year major crimes predominantly occurred. This can provide insights into the overall crime patterns and help 
        focus resources on specific time periods.</p>
        
        <p><b>3. Crime Trends by Month:</b> The analytics can reveal the months during which crime incidents are most 
        prevalent. This information can aid in planning and implementing targeted crime prevention strategies for 
        specific months.</p>
        
        <p><b>4. Crime Patterns by Day and Time:</b> The analysis can identify the days of the week and time periods 
        when crimes are most frequently happening. This can help beat teams to proactively monitor incident-prone 
        areas during those specific periods to enhance law enforcement efforts.</p>
    
        ''', unsafe_allow_html=True)

    crimes_by_year(chicago_crimes_df)
    crimes_by_month(chicago_crimes_df)
    crimes_by_day(chicago_crimes_df)
    crimes_by_hour(chicago_crimes_df)

def main():
    st.title("Chicago Crimes Analytics")

    pages = {
    "Basics": basics,
    "Crimes by Departments": crimes_by_police_deparements,
    "Crimes by Areas": crimes_by_chicago_areas,
    "Crimes by Time": crimes_by_time,
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox("Go to", tuple(pages.keys()), key="select box page switch")
    pages[selected_page]()

if __name__ == "__main__":
    main()
