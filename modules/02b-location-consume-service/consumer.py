import json

from app.udaconnect.services import LocationService

from kafka import KafkaConsumer


topic_location = "locations"

kafka_consumer = KafkaConsumer(
    topic_location,
    bootstrap_servers=['my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'],
)

for message in kafka_consumer:
    message = json.loads(message.value.decode())
    print('Received message:', message)
    LocationService.create(message)        
