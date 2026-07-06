## Prerequisites

Before running the project, ensure the following are installed:

* Python 3.x
* Docker Desktop
* Postman (for API testing)

---

## Installation

### 1. Clone the repository

```bash
cd <project-folder>
```

### 2. Install the required Python libraries

```bash
pip install -r requirements.txt
```

---

## RabbitMQ Setup

RabbitMQ was run using **Docker** instead of a local installation.

During development, I encountered compatibility issues while installing Erlang locally. To avoid these issues and maintain a consistent environment, I used the official RabbitMQ Docker image.

### Pull the RabbitMQ image

```bash
docker pull rabbitmq:3.13-management
```

### Create and start the RabbitMQ container

```bash
docker run -d --hostname rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

If the container already exists but is stopped, start it using:

```bash
docker start rabbitmq
```

To verify that the container is running:

```bash
docker ps
```

### RabbitMQ Management Console

Open the following URL in your browser:

```
http://localhost:15672
```

Default credentials:

* Username: `guest`
* Password: `guest`

---

## Running the Project

Open two terminals.

### Terminal 1 – Start the Flask Producer

```bash
python app.py
```

### Terminal 2 – Start the RabbitMQ Consumer

```bash
python celery_worker.py
```

---

## Testing the APIs

### POST API

**URL**

```
POST http://localhost:5000/
```

**Request Body**

```json
{
    "item": "book"
}
```

Expected Response:

* HTTP Status: **202 Accepted**

---

### GET API

**URL**

```
GET http://127.0.0.1:5000/delay?delay_value=2
```

Expected Response:

* HTTP Status: **200 OK**

Example:

```json
{
    "time_taken": 2.15,
    "delay_value": 2,
    "requests_made": 5
}
```
