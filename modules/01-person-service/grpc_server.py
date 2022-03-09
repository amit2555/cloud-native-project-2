import concurrent.futures
import logging
import grpc
import person_pb2
import person_pb2_grpc
import requests
import json


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):
        persons = requests.get("http://person-service-rest:5000/api/persons")
        persons = persons.json()
        result = person_pb2.PersonMessageList(person=persons)
        return result


server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=1))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

print("Starting grpc server on localhost port 5005")
server.add_insecure_port("0.0.0.0:5005")
server.start()
server.wait_for_termination()
