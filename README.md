# malaysia-weather-data-pipeline

This repository contains an end-to-end data engineering project that ingests, processes, and visualizes weather data using a variety of AWS services and Snowflake. The data pipeline is designed to update hourly and provides a seamless flow from data ingestion to visualization.

## Project Overview

1. **Data Ingestion**:
   - Weather data is ingested using the OpenWeatherAPI.
   - The data is stored in DynamoDB, with 'city' as the partition key and 'time' as the sort key, both of type string.

2. **Data Transfer**:
   - Data from DynamoDB is transferred to S3 for further processing.
   - An AWS Lambda function is used to automate the data transfer process.

3. **Data Processing**:
   - Data stored in S3 is ingested into Snowflake for advanced processing and analytics.

4. **Data Visualization**:
   - Processed data in Snowflake is visualized using Power BI, providing insights and trends in weather data.

The flowchart of the pipeline can be seen below

<p align="center">
  <img src="https://github.com/user-attachments/assets/5fbd7c1a-f446-4674-be6f-f5b9eec66634" alt="Data Pipeline Diagram"/>
</p>

The displayed graph on PowerBI can be seen below

<p align="center">
  <img src="https://github.com/user-attachments/assets/b30ce08e-7938-4142-a860-c4d94f9590e9" alt="Display"/>
</p>

## Key Components

- **DynamoDB**: NoSQL database for initial data storage.
- **AWS Lambda**: Serverless compute service for automating data transfer.
- **Amazon S3**: Scalable object storage for intermediate data storage.
- **Snowflake**: Cloud data warehouse for data processing and analytics.
- **Power BI**: Data visualization tool for creating interactive dashboards.

## Features

- Automated hourly updates from data ingestion to visualization.
- Scalable and robust architecture leveraging cloud services.
- Comprehensive insights and trends in weather data.

## Getting Started

### Prerequisites

- AWS Account
- Snowflake Account
- Power BI
