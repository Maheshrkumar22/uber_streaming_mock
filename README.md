Step 1 :Activate the virtual environment using 

source my_env/bin/activate

step 2 : 

pip install -r requirements.txt

step 3 : 

docker-compose up -d

step 4 : create the topic 'uber_events'

docker exec -it $(docker ps -q -f name=kafka) kafka-topics.sh --create --topic uber_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

step 5 : run ->
python producer.py

step 6 : run ->
python consumer.py

step 7 :run ->
streamlit run dashboard.py

Note : Stop the scripts with Ctrl+C

step 8 :

docker-compose down


