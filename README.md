### UdaConnect
#### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

#### Architecture


![](/docs/architecture_design.png)

In this architecture, there are a total of 6 microservices. The idea behind this architecture is that each service can be owned by a different team providing full flexibility of rolling out their own changes.

1. Kafka - Kafka on Kubernetes uses Strimzi. Here, Strimzi operator is deployed first which takes care of deploying Zookeeper and Kafka brokers. Strimzi also provides Kubernetes services for Kafka to connect to it internally and externally.

2. Person Service - The Person Service is split into two - a REST service which is available to Frontend in Person.js component, and an internal gRPC service which is used by Connection service.

3. Connection Service - The Connection service has REST endpoint which is called by the Frontend from Connection.js component.

4. Location Service - The location service is split into two separate services. The Location Process service provides a REST endpoint for any clients to change their location. It then writes that message to Kafka. The Location Consume service consumes the messages from Kafka and stores in the database.

5. Frontend - The React app is containerized into its own service. It makes REST calls to PersonService to retrieve persons from DB and it also makes REST calls to ConnectionService to lookup person.

6. Database service - The Postgres database is its own internal service and is used by various services.

#### Deploying microservices

To deploy Kafka Cluster, follow the steps in `/modules/00-kafka-service/kafka-on-kubernetes.txt` file which will first deploy a Strimzi Operator in Kafka namespace on Kubernetes and launch Kafka Cluster and create a Kafka Topic.

The rest of the services can be deployed as -

```
kubectl apply -f modules/01-person-service/deployments/
kubectl apply -f modules/02a-location-process-service/deployments/
kubectl apply -f modules/02b-location-consume-service/deployments/
kubectl apply -f modules/03-connection-service/deployments/
kubectl apply -f modules/04-frontend/deployments/
kubectl apply -f modules/05-db-service/deployments/
```

View the app on `localhost:30001`.

