# Chicago Crimes Analytics

## Dataset Description
This dataset reflects reported incidents of crime (with the exception of murders where data exists for each victim) that occurred in the City of Chicago from 2001 to present, minus the most recent seven days. Data is extracted from the Chicago Police Department's CLEAR (Citizen Law Enforcement Analysis and Reporting) system.

In order to protect the privacy of crime victims, addresses are shown at the block level only and specific locations are not identified.
Should you have questions about this dataset, you may contact the Data Fulfillment and Analysis Division of the Chicago Police Department at DFA@ChicagoPolice.org.

**Disclaimer**: These crimes may be based upon preliminary information supplied to the Police Department by the reporting parties that have not been verified. The preliminary crime classifications may be changed at a later date based upon additional investigation and there is always the possibility of mechanical or human error. Therefore, the Chicago Police Department does not guarantee (either expressed or implied) the accuracy, completeness, timeliness, or correct sequencing of the information and the information should not be used for comparison purposes over time. The Chicago Police Department will not be responsible for any error or omission, or for the use of, or the results obtained from the use of this information.

All data visualizations on maps should be considered approximate and attempts to derive specific addresses are strictly prohibited.
The Chicago Police Department is not responsible for the content of any off-site pages that are referenced by or that reference this web page other than an official City of Chicago or Chicago Police Department web page. The user specifically acknowledges that the Chicago Police Department is not responsible for any defamatory, offensive, misleading, or illegal conduct of other users, links, or third parties and that the risk of injury from the foregoing rests entirely with the user. The unauthorized use of the words "Chicago Police Department," "Chicago Police," or any colorable imitation of these words or the unauthorized use of the Chicago Police Department logo is unlawful. This web page does not, in any way, authorize such use. Data are updated daily.

## Major Columns Understanding
**ID:** Unique identifier to a crime
**Primary type:** Type of the crime
**Block:** Specific area or street near the incident location
**Ward:** The City of Chicago is divided into fifty wards. Each Ward is represented by an alderman who is elected by their constituency to serve a four-year term.
**Districts:** The City of Chicago is divided into 25 police districts.
**Beat:** Beat is teams of 8-10 people fully equipped, motorized police unit. They work under the districts officers.
**Community Area:** Chicago is divided into seventy-seven (77) Community Areas. These boundaries do not change over time (as political boundaries do).
**Domestic:** Information about the criminal to check if the criminal is a family member or a stranger.

## Consideration in Preprocessing
Based on the given instructions in the dataset description, the following preprocessing steps were taken to avoid inaccurate results:

- Null values in location-related columns are replaced with the keyword "not specified" since specific locations of incidents are not provided in the dataset.

- Null values in the 'ward' and 'community area' columns (float data type columns) are replaced using the following techniques:

- Mapping technique: The already specified blocks within the given community area and ward are used to identify the respective ward and community area for rows with null values in those columns. If a block is identified, it replaces the null ward and community area.

- For remaining null values in 'community area' and 'ward' columns, which contain unidentified or new blocks, the value 100 is used to represent "not specified."

- As suggested, visualizations on locations should be considered approximate, and any attempts to derive specific locations are prohibited. Therefore, the data was analyzed ward, community, district, and beat-wise and within the ward and community, block-wise to maintain privacy.

## Anlytics Implementaions 

### 1. Crimes Analytics by police departments
#### Analytics Use Cases:
**a. Identifying Districts and Their Beats with Major Crimes:** The analytics can help the Chicago Police Department identify districts and their beats (areas under the beat team) with high incidences of major crimes.

**b. Districts with Major Crimes but Low Arrest Rates:** By analyzing the data, it's possible to identify districts and beat teams that have a high occurrence of major crimes but a low rate of successful arrests.

**c. Evaluating District Officers and Beat Teams Performance:** The analytics can evaluate the performance of district officers and beat teams in different aspects:

- **Successful Arrests:** Identify which districts and beat teams have a high success rate in arresting criminals.
- **Performance Gaps:** Determine which districts and beat teams are not performing well, for example, having a high number of major crimes but a low arrest rate.

### 2. Crimes Analytics by areas
#### Analytics Use Cases
The analytics can help the Chicago Police Department to identify:

**1. Wards and Community Areas with Major Crimes:** The analysis can pinpoint wards and community areas experiencing high incidences of major crimes, which may require an increase in police teams within the respective districts to address the issues effectively.

**2. Blocks with Major Crimes in Each Ward and Community Area:** By examining the data, it is possible to identify specific blocks within each ward and community area that are hotspots for major crimes. This can help in targeting resources for crime prevention and enforcement efforts.

**3. Vulnerable Community Members:** The analytics can highlight communities where people are more likely to become victims of criminal activities. This information can be used to implement targeted outreach and support programs for the vulnerable population.

### Crimes Analytics by time
#### Analytics Use Cases
The analytics can help the Chicago Police Department to identify:

**1. Performance Analysis Over Time:** The analysis can track the performance of the police department, districts, and their respective beats over the years. This includes monitoring the trends of crime, such as increases or decreases in crime rates over time.

**2. Major Crime Occurrences by Year:** By examining the data, it is possible to determine in which year major crimes predominantly occurred. This can provide insights into the overall crime patterns and help focus resources on specific time periods.

**3. Crime Trends by Month:** The analytics can reveal the months during which crime incidents are most prevalent. This information can aid in planning and implementing targeted crime prevention strategies for specific months.

**4. Crime Patterns by Day and Time:** The analysis can identify the days of the week and time periods when crimes are most frequently happening. This can help beat teams to proactively monitor incident-prone areas during those specific periods to enhance law enforcement efforts.


## Getting Started with Project
- Download the dataset from: https://www.kaggle.com/datasets/chicago/chicago-crime
- Install the requirements 
```bash
pip install -r requirements.txt
```
- Data preprocessing run
```bash
python3 crimes_preprocessed.py
```
- To run analysis app
```bash
streamlit run crime_analysis_app.py
```