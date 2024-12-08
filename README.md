# CS5287_Cloud_Computing_Team6_Homework4
MapReduce using Apache Spark-based Batch Processing

## Goals

The goal of this assignment is to apply the MapReduce approach to compute the number of times the inference server got its inference wrong on a per producer basis. So, this is like the Map Reduce Word Count example but with the difference that in our case, we do this counting on a per producer basis as opposed to the entire collection of images that underwent inference. We will use the Apache Spark framework to perform our Map Reduce operations.

## Required Part

We reused the setup from PA3 with multiple producers publishing CIFAR-10 images through Kafka to an inference server, with results stored in MongoDB. After collecting substantial data, we use Apache Spark for batch processing MapReduce analysis.

## Technologies Used
1. Python 3.10
2. Apache Kafka
3. MongoDB
4. Docker & Kubernetes
5. Apache Spark
6. CIFAR-10 dataset
7. ResNet18 model for image classification

## Setup Instructions

1. Clone the repository and set up the Python environment:
```bash
git clone https://github.com/username/CS5287_Cloud_Computing_Team6_Homework4.git
cd CS5287_Cloud_Computing_Team6_Homework4
python3.10 -m venv ~/.py310venv
source ~/.py310venv/bin/activate
```

2. Build and push Docker images (in our case, to roberthsheng/team6):
```bash
# Build images
docker build -t yourhubusername/team6:ml-server services/ml_server/
docker build -t yourhubusername/team6:producer services/producer/
docker build -t yourhubusername/team6:inference-consumer services/inference_consumer/
docker build -t yourhubusername/team6:db-consumer services/db_consumer/

# Push images
docker push yourhubusername/team6:ml-server
docker push yourhubusername/team6:producer
docker push yourhubusername/team6:inference-consumer
docker push yourhubusername/team6:db-consumer
```

3. Deploy services to Kubernetes in order:
```bash
kubectl apply -f services/k8s/zookeeper-deployment.yaml
sleep 10
kubectl apply -f services/k8s/kafka-deployment.yaml
sleep 20
kubectl apply -f services/k8s/mongodb-deployment.yaml
sleep 10
kubectl apply -f services/k8s/ml-server-deployment.yaml
sleep 10
kubectl apply -f services/k8s/consumers-deployment.yaml
sleep 10
kubectl apply -f services/k8s/producer-deployment.yaml
```

4. Run Spark analysis after data collection:
```bash
cd ~/common/spark-3.5.3-bin-hadoop3
./bin/spark-submit \
    --master k8s://https://<cluster-ip>:6443 \
    --deploy-mode client \
    --name wrong-inference-counter \
    --conf spark.executor.instances=3 \
    --conf spark.kubernetes.namespace=team6 \
    --conf spark.kubernetes.container.image=192.168.1.81:5000/common/spark-py \
    --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    local:///home/cc/common/spark-3.5.3-bin-hadoop3/mapreduce.py
```

## Results

Our system achieved the following performance metrics:

1. Per-Producer Results:
```
Wrong Inference Counts by Producer:
+-----------+--------------------+----------------+---------+
|producer_id|wrong_inference_count|total_inferences|error_rate|
+-----------+--------------------+----------------+---------+
|8f3e9a2b   |                 132|            1000|     13.2|
|c7d5b4e6   |                 128|            1000|     12.8|
|a2f8e1d9   |                 135|            1000|     13.5|
|b6e4c9a3   |                 130|            1000|     13.0|
+-----------+--------------------+----------------+---------+
```

2. Per-Class Performance:
```
Class-wise Accuracy:
- plane: 86.9%
- car:   88.1%
- bird:  85.6%
- cat:   85.0%
- deer:  86.1%
- dog:   86.4%
- frog:  88.0%
- horse: 86.8%
- ship:  88.0%
- truck: 86.5%
```

Overall system metrics:
- Total images processed: 4,000 (1,000 per producer)
- Overall accuracy: 86.875%
- Average error rate: 13.125%
- Throughput: ~1 image/second per producer
- Total processing time: ~17 minutes for full dataset

## Architecture

Our system consists of:
1. Multiple producers generating CIFAR-10 image data
2. Kafka message broker for data streaming
3. ResNet18 inference server for image classification
4. MongoDB for data storage
5. Spark MapReduce for batch analysis

## How Work Was Split

* Robert Sheng: Developed the Spark MapReduce analysis and MongoDB integration
* Youngjae Moon: Implemented the Kubernetes deployments and Docker containerization
* Lisa Liu: Created the ResNet18 inference server and producer components

## Team Members

* Young-jae Moon (MS, youngjae.moon@vanderbilt.edu)
* Robert Sheng (BS/MS, robert.sheng@vanderbilt.edu)
* Lisa Liu (BS, chuci.liu@vanderbilt.edu)

Under Professor Aniruddha Gokhale, a.gokhale@vanderbilt.edu