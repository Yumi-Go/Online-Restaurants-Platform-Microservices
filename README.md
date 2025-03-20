# README: Microservices with gRPC, Docker, and Redis Pub/Sub

Welcome! This project is a sample microservices system containing **three** main services:

1. **Order Service**  
2. **Restaurant Service**  
3. **Delivery Service**

They communicate via **gRPC** and are orchestrated using **Docker Compose**. We also added **Redis Pub/Sub** for **asynchronous** (event‐driven) communication between the Restaurant and Delivery services.

Below is a detailed guide explaining how the system works, how to run it, how to test it, and important notes about data storage.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [System Architecture](#system-architecture)  
4. [Prerequisites](#prerequisites)  
5. [Installation & Setup](#installation--setup)  
6. [Running the System](#running-the-system)  
7. [Testing](#testing)  
8. [Why Redis Pub/Sub and Not Storing Data in Redis?](#why-redis-pubsub-and-not-storing-data-in-redis)  
9. [Justification and Benefits](#justification-and-benefits)  
10. [Limitations & Future Improvements](#limitations--future-improvements)  

---

## 1. Overview

The project implements an **Online Food Order/Delivery Platform** for their small restaurants:

- **Order Service** – Handles creating orders and fetching their status.  
- **Restaurant Service** – Handles updating menus, accepting or rejecting orders.  
- **Delivery Service** – Receives assignment requests to deliver orders and updates delivery status.

**Bonus Challenge: Asynchronous Event process**
When the Restaurant Service accepts an order, it **publishes** an event to **Redis**.
The Delivery Service **subscribes** to these events and automatically assigns a driver.
This creates a more decoupled design where the Restaurant Service doesn’t need to call the Delivery Service directly.

---

## 2. Features

- **gRPC** for high‐performance, RPC‐style calls between services.  
- **Docker Compose** to run all services with a single command.  
- **Redis Pub/Sub** for asynchronous notifications:
  - Restaurant publishes an “ORDER_ACCEPTED” event.  
  - Delivery listens and auto‐assigns a driver upon acceptance.  
- **Python** implementation with minimal external dependencies.  
- **Unit Tests** for each microservice (using Python `unittest`).  
- **Testing in Docker Container** (`test_client.py`) calls all three services from local machine.

---

## 3. System Architecture

Here’s a simple diagram of how the pieces fit together:

```
+-----------------+        +-----------------+        +-----------------+
|  Order Service  |        | Restaurant Svc  |        | Delivery Svc    |
| (gRPC on 50051) | <----> | (gRPC on 50052) | <----> | (gRPC on 50053) |
+-----------------+        +-----------------+        +-----------------+
                                 |   ^
                                 v   |
                    (Pub/Sub)  Redis  
                                 
```
![Phase1_Communication_Diagram](https://github.com/user-attachments/assets/e82aaa16-803a-429a-bae9-3e0e417c082a)

1. **Order Service** – No direct involvement with Redis Pub/Sub in this demo.  
2. **Restaurant Service** – Publishes `ORDER_ACCEPTED:<order_id>` messages to the Redis channel `order_events`.  
3. **Delivery Service** – Subscribes to `order_events` and triggers an **auto‐assign** to a driver.

---

## 4. Prerequisites

- **Docker**
- **Docker Compose**
- (Optional) **Python 3.9+** on your local machine if you want to run the `test_client.py`.

---

## 5. Installation & Setup

1. **Clone(https://github.com/Yumi-Go/Online-Restaurants-Platform-Microservices) the repository or Download(./YumiGo_Assignment1/Codes)** this project folder.  
2. **Navigate** to the project root folder (where `docker-compose.yml` is located).  

---

## 6. Running the System

1. **Build** all images:
   ```bash
   docker-compose build
   ```
2. **Start** the containers in the background:
   ```bash
   docker-compose up -d
   ```
   This will launch:  
   - **order_service** listening on port `50051`  
   - **restaurant_service** on `50052`  
   - **delivery_service** on `50053`  
   - **redis** (no external port by default, used internally)  

3. **Check** running containers:
   ```bash
   docker ps
   ```
   You should see all four containers up and running.

4. **Logs** (optional):
   ```bash
   docker-compose logs -f
   ```
   This shows console output from each container.

5. **Stop** everything when done:
   ```bash
   docker-compose down
   ```

---

## 7. Testing

I offer **two** main ways to test:

### 7.1 Using the Python Test Client (`test_client.py`)

From your **host machine** (with Python 3.9+ installed), run:

```bash
python test_client.py
```

This does the following:
1. Connects to **Order Service** (localhost:50051), places an order, and retrieves its status.  
2. Connects to **Restaurant Service** (50052), updates a sample menu, accepts an order (order_1), and rejects order_2.  
3. Connects to **Delivery Service** (50053), assigns a driver to order_1, updates delivery status, and fetches driver assignments.  
4. Prompts you to **interactively** accept an order with custom IDs.

Watch the console output for details. If you see “ACCEPTED,” “ASSIGNED,” etc., it’s working!

### 7.2 Unit Tests for Each Microservice

Each service folder has a **test_*.py** file (e.g. `test_order_service.py`). To run them individually:

1. **Install** test dependencies:  
   ```bash
   pip install grpcio protobuf
   ```
   (`unittest` is built into Python.)
2. **Inside** each microservice folder, run:
   ```bash
   python -m unittest test_order_service.py
   ``` 
   ```bash
   python -m unittest test_restaurant_service.py
   ```
   ```bash
   python -m unittest test_delivery_service.py
   ```

---

## 8. Why Redis Pub/Sub and **Not** Storing Data in Redis?

I am using Redis **only** for **Pub/Sub** in this demo, which is an **in-memory** message passing mechanism. **Pub/Sub does not persist** messages—if a service is offline when an event is published, it misses that event. Also, the messages are not stored long‐term.

I could store data in **Redis** by using **key‐value** or **hash** data structures. However, for **this assignment**, I chose an **in‐memory dictionary** approach for each service to keep the implementation simple. That means data **is lost** if the service or container restarts. This is okay for this project, but not for production.

---

## 9. Justification and Benefits

### 9.1 Why I Added Asynchronous (Pub/Sub)

1. **Loose Coupling**: The Restaurant Service publishes “ORDER_ACCEPTED,” and doesn’t need to call the Delivery Service’s API.  
2. **Scalability**: More services can subscribe without changing the Restaurant Service code.  
3. **Real‐Time Notifications**: The Delivery Service immediately knows when a new order is accepted and can auto‐assign a driver.  

### 9.2 How It Improves the System

- It reduces **blocking calls**: The Restaurant Service is free to move on after publishing.  
- It’s easier to add new features, like sending a confirmation email or push notification, by **subscribing** to the same event channel.  

---

## 10. Limitations & Future Improvements

1. **Data Persistence**: Currently, all order data, menus, and assignments are kept in memory. This means everything resets when containers stop.  
   - **Improvement**: Use a real database (e.g. PostgreSQL, or Redis as a data store) to save data across restarts.  
2. **Pub/Sub** Reliability**: If the Delivery Service is down when an event is published, it misses the event.  
   - **Improvement**: Use a message broker that can store messages (e.g., RabbitMQ or Kafka), or implement Redis streams with persistence.  
3. **Security & Logging**: Minimal logging and no authentication is set up.  
   - **Improvement**: Add proper logs, security, TLS, and so forth.  

---

# Conclusion

This project demonstrates **gRPC** for service‐to‐service calls, **Docker Compose** for multi‐container orchestration, and **Redis Pub/Sub** for asynchronous event handling.
I **do not** store data permanently in Redis for this assignment.
However, the main goal was to highlight **microservice communication** and the **decoupled** approach gained by event‐based messaging.

Thank you!
