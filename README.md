# Streaming Data Pipeline on AWS

## 0. Introduction
###### This is a sample architecture to process streaming data with below points in mind:
	A. Realtime analysis, as realtime as possible
	B. Offline analysis of streamed data
	C. Serverless, as much as possible

![Alt text](images/streaming_data_pipeline.png?raw=true "Streaming Data Pipeline on AWS")

## 1. Streaming Data Source

We are using wiki change streaming as data source. Details can be found in the below links: 
	https://stream.wikimedia.org/v2/stream/recentchange
	https://wikitech.wikimedia.org/wiki/RCStream

Idea is to create a kinesis producer at the source. To test purpose we can run the producer from local laptop or on a EC2 instance.
In the sample code, we are keeping only 4 fields timestamp, id, type & wiki.

##### Code 
	kinesis producer for wiki change: ./stream_producer/producer.py
	sample wiki change schema: ./stream_producer/wiki_change_stream_sample.json
	
## 2. In Memory Queue
Generic memory queue to hold incoming data as it is. From this generic queue different consumer will consume differently. We are using "kinesis data streams" for this.

##### Code
	No code needed. Just create the "kinesis data streams" with a name "wikiedits".
	
## 3. Delivery Stream for Data Lake
It is a kinesis firehose with S3 as end point. It will also transform JSON input to csv using lambda function. This stream will be for offline analysis.

##### Code 
	lambda function: ./lambda_functions/data-stream-wiki-jsontocsv.zip
	
## 4. Data Lake Storage
We are using S3 a data lake storage.

## 5. Metadata Storage
Glue is the metadata storage for the data lake. Using glue crawler, we will create an external table pointing to the S3 location where firehose storing data (it needs manual edit to fix column names). 
As data lake is for offline analysis, we will run glue crawler everyday to explore new data partitions.

##### Code
	Crawler configuration: ./glue/crawler_config.txt

## 6. SQL Engine
As external table definition is already in glue, we can access data using athena as hive table.

## 6.1 Data Processing
If needed we can utilize transient EMR to process and create transformed tables (with metastore in glue)

## 7. Visualization
We can use quick sight for visualization. Data source will be athena. We can can data in spice and load everyday (as this is offline analysis, it will be fine).

## 8. Delivery Stream for Realtime Analysis
It is a kinesis firehose with Elastic Search as end point. It will also utilize firehose inmemory transformation option (with lambda function) to make it consumable by elastic search schema.  

##### Code
	lambda function: ./lambda_functions/data-stream-wiki-es.zip

##### Note
Even we can use some machine learning model to do prediction and/or do external action here.
	
## 9. Realtime Data Store
AWS Elastic Search service is a good option for real time analytical platform. Data from firehose will be inserted to the index in micro batch. 

##### Code
	Index schema creation commands: ./ES/create_es_index.txt

##### Note
It is realtime analysis not CEP, so 1-5 seconds delay due to micro batch will not be an issue for most of the use cases.

## 10. Realtime Visualization
Kibana is tightly integrated with elastic search (and comes free!). Just visualize and create dashboard.

##### Note
In the overall architecture, only elastic search is not serverless. However, AWS Elastic Search service is a fully managed service and we just need to worry about capacity, I would say, it is semi serverless :)


 


