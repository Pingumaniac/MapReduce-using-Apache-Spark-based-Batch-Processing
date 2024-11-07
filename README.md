# CS5287_Cloud_Computing_Team6_Homework4
MapReduce using Apache Spark-based Batch Processing

## Goals

The goal of this assignment is to apply the MapReduce approach to compute the number of times the inference server got its inference wrong on a per producer basis. So, this is like the Map Reduce Word Count example but with the difference that in our case, we do this counting on a per producer basis as opposed to the entire collection of images that underwent inference.  We will use the Apache Spark (https://spark.apache.org/docs/latest/index.html) framework to perform our Map Reduce operations. Spark was developed in a language called Scala but provides a Python binding that we will use.

## Required part

We will reuse the entire setup from PA3. We will collect substantial amount of inference data by running multiple producers that will publish a large number of images that get sent one by one (as we have been doing so far) to the inference server and then the results are saved in the database. We will let the data collection phase end after a substantial amount of data is collected in the database. Then, we will use this large batch of data and send it to Apache Spark to run the batch processing Map Reduce application.

So far, we have been using CH-822922 where each team has 4 VMs. However, that may be too restrictive to run multiple producers with large number of images that undergo inferencing. To overcome these constraints, we will scale our data pipeline to large number of publishers and their image stream using pre-allocated K8s clusters on CH-819381 project. All students will be enrolled in this project also. 
4 independent but interconnected K8s clusters have been already deployed and are functional. You just need to use the cluster. But care must be taken to deploy your pods in your team’s namespace. 4 different private registries, one on each of the 4 cluster masters 

## Optional Part I

Instead of batch mode (you still save results in database) but up to PA3, we were sending inference results into Kafka. Apache Spark streaming can directly ingest streaming data from Kafka. See diagram from their web page where more information is available. See https://spark.apache.org/docs/latest/streaming-programming-guide.html.

<img width="287" alt="image" src="https://github.com/user-attachments/assets/3febede9-74be-4cd0-920e-d73739616fa7">

Behind the scenes, Apache Spark streaming divides data into small batches and processes them as in batch. It uses something known as discretized streams. See figure from their web page:

<img width="276" alt="image" src="https://github.com/user-attachments/assets/abe297e3-3959-4631-92ed-5474613a9de1">

## Optional Part II 5G Emulated UE/gNB sending traffic to our kafka broker for inferencing
We will use the Open5gs (or Free5gc) 5G simulator of user equipment and gNodeB (base station) to act as yet another of our producers sending image data into our Kafka broker. We will set up this Open6gs or Free5gc simulation on our laptop. Since we will need to send information into a Kafka broker running inside a private network, we will be using the ssh -L trick of port forwarding and port mapping. Please see Week10B_K8s_CNI lecture slides, which show a detailed example and explanation of how the ssh -L works.

Open5gs is described at and available from https://open5gs.org/

Free5gc is described at and available from https://free5gc.org/ 

## Technologies Used
1. Python 3
2. Apache Kafka
3. MongoDB
4. Chameleon Cloud with Ubuntu Linux version 22.04 image (CC-Ubuntu22.04 on Chameleon)
5. CIFAR-10 image data set used by the IoT source.
6. Docker
7. Ansible
8. Kubernetes
9. Apache Spark

## Instructions for setting up the technologies used

1. Install the following Python packages through your chosen CLI.

```
pip3 install kafka-python
pip3 install torch torchvision
pip3 install pymongo
```

2. Install Docker Image for Apache Kafka.

```
docker pull apache/kafka
```

3. Download Apache Kafka on your chosen directory using wget or curl -0 command.

```
wget https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
```

```
curl -O https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
```

Then, unzip the file, and move to the kafka directory.

```
tar -xzf kafka_2.13-3.8.0.tgz
cd kafka_2.13-3.8.0
```

## How work was split

* Robert Sheng primarily worked on...
* Youngjae Moon primarily worked on...
* Lisa Liu primarily worked on...

## Team Members

* Young-jae Moon (MS, youngjae.moon@vanderbilt.edu
* Robert Sheng (BS/MS, robert.sheng@vanderbilt.edu
* Lisa Liu (BS, chuci.liu@vanderbilt.edu

under Professor Aniruddha Gokhale, a.gokhale@vanderbilt.edu
