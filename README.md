# Uber streaming Data for backend

## create python virtual environment
```bash
python3 venv my_env
```

## Activate the virtual environment using 
```bash
source my_env/bin/activate
```
Make Sure the Python 3 and Docker installed in your system
## Install Requirements
```bash
pip3 install -r requirements.txt
```
## Run the container
```bash
docker-compose up -d
```

## create the topic 'uber_events'
```bash
docker exec -it $(docker ps -q -f name=kafka) kafka-topics.sh --create --topic uber_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

## Run the Kafka Producer File
```bash
python producer.py
```

## Run the Kafka Consumer File
```bash
python consumer.py
```
## Visualise the top 5 zones through streamlit dashboard
```bash
streamlit run dashboard.py
```
## Note : Stop the scripts with Ctrl+C

## Stop the containers after finished
```bash
docker-compose down
```

