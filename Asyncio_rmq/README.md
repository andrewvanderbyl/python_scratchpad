# AsyncioRabbitMQ
Info:
-----
This code will demonstrate the use of asyncio and RabbitMQ

Requirements: 
-------------
Two instances. One needs to be a "Start" and the other a "Listen". An instance of rabbitmq exchange is also required.
A Docker container is easy to setup and use. 

Pre-requisite: Docker
--------------
To Run: sudo docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management


AsyncioRabbitMQ:
----------------
Input: Initial role to play. This is a string and is either "Start" or "Listen"

Output: A series of messages passed between two 

