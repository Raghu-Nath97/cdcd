# Data QA Checklist

**Source:** [Confluence - Data QA Checklist](https://jira-pg-ds.atlassian.net/wiki/spaces/HWR/pages/356614535/Data+QA+Checklist)

## Purpose

This checklist shall ensure good understanding of the data and possible use cases - and shall be stored within every DataScience project repository. It is to be owned by the Project/Algorithm Owner who needs to fill this (with the Data Owner) & signed off by the Model Risk Officer. Update with any major data change.

---

## Quick Assessment Questions

As generic questions, starting off a review, the following items can be answered instead of a complete review with the entire table:

1. What methods were used for data validation (e.g., manual, automatic, batch, streaming, single record)?
2. What types of data were validated (e.g., text, image, audio, video)?
3. How was the data accuracy validated? Were any statistical measures used?
4. How was data consistency ensured? Were any standardization methods employed?
5. What steps were taken to ensure data completeness?
6. How was data relevance determined (e.g., VIF, Correlation Coefficient, or Business interest)? Were any features selected or excluded?
7. Were any biases detected in the data? If so, what steps were taken to mitigate them?
8. Were any missing values imputed in the data? If so, how were they handled?
9. Were any outlier values detected in the data? If so, how were they handled?
10. What data privacy and security measures were taken to ensure compliance with regulations?
11. How was the quality of the data verified? Were any metrics used?
12. Were any conflicts or inconsistencies in the data resolved? If so, how?
13. How was the data preprocessed before being used in the model pipeline?
14. What steps were taken to ensure the data was representative of the problem domain?
15. Were any data validation checks performed after the model was trained? If so, what were the results?

---

## Detailed Checklist

### COVID-19 Effects (2020 to end of pandemic)

| Question | Examples & Details | Answers, Links & Notes |
| --- | --- | --- |
| Were data available for the duration of COVID-19 pandemic for your use-case? Did you include data for COVID-19 pandemic? | Enumerate and explain Abnormalities and steps taken | |
| How did COVID-19 pandemic affect changes in Scale, feature size and number, target values in your data set at each stage of the pandemic? | | |
| Do you need to exclude or impute data for the duration of pandemic? If so, how is it managed - at source or via ETL process or alternate method? | | |
| Did COVID-19 lead to inclusion of new features or covariate data in your data universe? | | |
| Do your data follow micro and macro trends happening in regional socio-economic environment? | | |
| Does your data increase or decrease in scale with social restrictions? | | |
| Does your data follow unemployment trends? | | |
| Can your data be bucketed in pandemic time transitions (pre-lockdown, lockdown, post-lockdown)? | | |
| Does your data have regional impacts? If so, do you need to exclude/impute impacted regional data? | Consider travel/tourism/hospitality/auto industry impacts as well as local governmental restrictions | |

---

### Data Universe

| Question | Examples & Details | Answers, Links & Notes |
| --- | --- | --- |
| How is the data collected? Is it collected in one or in parts? | Describe data creation, or link to data source description. Include potential biases, like sampling, collection methodology, sensor placement, etc. | |
| What is the lineage of data / dependencies to other datasets? | Link to data lineage description, or documentation | |
| How often do we receive new data? | Batch update with frequency, stream update with lag | |
| Incremental vs. full re-delivery? If historical data is re-delivered, are they consistent with previous deliveries? How are restatements handled? | | |
| What are the usage limitations and legal restrictions? | PII, Customer Firewalls, Corporate Policy, etc. | |

---

### Bias & Completeness

| Question | Examples & Details | Answers, Links & Notes |
| --- | --- | --- |
| What is the universe covered? | Compared to the ground truth and the business need, how much is the data covering | |
| Is the data sufficient for the model(s)? If not, what is NOT covered? | DTC, Online, Coupons included? Retail Brands masked? | |
| If you need more data, how do you plan to get it? | | |
| If universe is not covered, do you use a sample, and project to get the universe? If yes, what is the projection methodology? | Projection methodology - e.g., complementation | |
| Is there anything masked? | | |
| Is it raw data or derived data (modeled, complementation, or imputed)? | | |
| If derived data, what kind of biases are present in the data? | | |
| Is it a combination of raw and derived data? If so, do biases and variabilities match up? | | |
| Is there a reference dataset, and what/where is it? | Reference dataset: golden dataset, test dataset, ground truth, etc. | |
| Is the data representative / order of magnitude matching up with official datasets? If not, why? Does it comply with common sense? | Compare vs. alternative sources, Nielsen, Shipments, usual coverage | |
| What is the time covered by the dataset? | E.g. rolling 3 years | |
| Are there gaps in the time series? | Also relevant for non-ts datasets | |
| Is there a trend break in key measures & record count over time? Is the world/universe changing - impacting the data/behavior captured in the data? Why - and how does that impact usability of data? | Methodology, scope changes, append vs. restate? | |
| Is there major seasonality or different times/segments behaving significantly different? Why? | | |
| Were there changes to the data structure (new column) and how to handle missing data before is to be handled? What actions need to take place for data restatements? | | |
| Where should you not have any data - and is that the case? | E.g. stores in lakes/sea, mountains; age over 100 or negative; etc. | |

---

### Data Delivery

| Question | Examples & Details | Answers, Links & Notes |
| --- | --- | --- |
| Do you need to ingest a new data source or is it handled by P&G data management? If new data source, who would be the data provider - external or internal? | | |
| Where are the data stored? Is the data from a production database (i.e. with fully built data quality control & test process prior to data load) or user data table? | Cloud, on-prem, 3rd-party server, etc. | |
| What is the expected delivery timing of data (i.e. date, time, week, WD, etc)? | Batch, stream, etc. | |
| What is the delivery medium (i.e. email, SFTP, etc)? | | |
| Is there a format required for the data delivery (i.e. xls, database, hdfs, etc)? | | |
| Is the data delivered complete vs. expected (i.e. # of files, # of brands, etc)? | Do we have a completeness criteria for data delivery, and are we checking. What is it? | |
| Use case vs. data delivery | Streaming vs batch | |
| What are the SLA terms with the data owner/vendor? (timings, trainings, post-delivery support, issue resolution, etc) | | |

---

### Data Structure

| Question | Examples & Details | Answers, Links & Notes |
| --- | --- | --- |
| Is there a defined, documented data structure/dictionary (standard data model, SDM) and where is it? If not, should an SDM be created? Did you work with Data Architects to design a Data Model? | Link to SDM | |
| Are there different data structures by market/brand/etc.? | Reference link to the data model descriptions | |
| Are all fields documented in terms of data type, format, and assumptions? | E.g. usual cases: "Age field an Integer, formatted without decimal places, between 0 and 120, with a poisson distribution." | |
| How are IDs encoded? FPC/UPC/GTIN | With/without leading 0s, check digits, UUID, etc. | |
| What Unit of measures used for the KPIs? What do they represent? What do nulls represent? | M = millions or thousands, FX conversions, Net/gross, volume in SU vs. Units, SU restatement rules? | |
| How are Percent values represented? Which should sum to 100% and which are ok to not do? | 0-1 or 0-100? | |
| What Time/Date representation & calendar is used? What is the Time zone? | 4-4-5 vs 5-4-4? "monthly, weekly, fortnightly"? | |
| Where is hashing applied/required, how is it done? | Define algo used | |
| Geo Location: (ZIP, Lat/Long) What representation/accuracy is it and how is it collected? | | |
| What are the keys in the data? Do you have duplicate records? How are the duplicates handled? Are the keys consecutive, can you validate for missing keys? | | |
| What are the foreign keys? What are the recommended joins between tables? Are there data loss expected? | | |
| What are fact and reference tables? If you have similar tables, what are differences? | | |
| Which columns must never be null? | | |
| How do you know if data is missing? | | |

---

### Data Characteristics

**Key metrics that need to be monitored to ensure data quality:**

| Question | Examples & Details | Answers, Links & Notes |
| --- | --- | --- |
| **Did you work with DM and AIE to deploy data quality sensors and collect data quality metrics? Did you work with AIE to build the data quality solution for the questions below:** | | |
| What data quality checks have been done to ensure data quality? | Link to data quality checks documentation and/or codified implementation | |
| Who will be responsible for the data quality on-going, data producer or data consumer (i.e. modeler)? | | |
| Is the data quality sustainable during the model's expected life cycle? Is there a remediation plan if there was known changes impacting data quality in the future? | | |
| Which columns are really raw/observed, and which are derived, if derived then how? | | |
| Categorical Values: Is harmonization required / applied? | Spelling, upper/lower case, spaces, etc | |
| Categorical Values: Which columns have a dictionary? How do you handle if new values are received? | | |
| Are there any pre-binned values? How is it binned? | Tiers, sizes, etc. | |
| Are there outliers? (extreme value) How do you define & handle them? | Sales per person outrageous (prison), mismatch sales vs. population (airport), Impressions from VPN, etc. | |
| Are there missing values? Are there Zero values? Are Zeros = Nulls? What is the percent of null rows / business kpis - and is there any bias introduced by this? What is the threshold of % nulls we are ok with? How do you handle missing data? | Link to EDA Impute, exclude, missing_value_flag - and is this documented | |
| Are there negative values - and what causes them? How do you handle negative values? | Negative sales, prices, etc. | |
| What are your expected max/mins and distributions & summary statistics? | Link to EDA | |
| How are IDs assigned & what do they represent? Is there a default value and how to handle that? | Random numbers used? Ordered unique values? | |
| What does the ID represent - and is it consistent? | Individual? Family? Household?, etc. | |
| Is there information encoded in the ID? If so, could that be useful? | Parts of the ID indicating gender, state, etc. | |
| Is there collinearity / duplication of information within the data? | E.g. adult females, females 18+, etc. | |
| Are there company / industry codes & encodings used - and are they valid? Can they be used to join the data with other interesting datasets? | 2/3 letter ISO codes for country, P&G country numbers, etc. | |
| Were there any values truncated or rounded - and what is the impact? | | |
| Are there any extreme values? Will they be cap-floored or handled in other ways? Are they any invalid values? such as string in a supposed-to-be numerical column. How are they handled? | | |
| **Summarize: What are the top 5 watchouts?** | | |
