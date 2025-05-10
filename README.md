# ZypherAI

## Overview
ZypherAI is an innovative platform for Machine Learning 
model deployment and inference.

## Architecture

### Consumer Service
This component is acting as a background task running on a separate thread. It is being used to process all asynchronous request.

### Prediction Service
The core component is the `PredictionService` which implements a singleton pattern to ensure consistent state across multiple threads. This design was chosen to address the challenge of maintaining consistent state between publisher and consumer threads.

### Queue Service
The Queue Service Component holds implementation of RabbitMQ. It contains two essential methods for producing and subscribing or publishing and consuming messages.

### State Management
Instead of using Database, we are currently using temporary memories which holds data until the application is up & running.

- `async_prediction_map`: Stores completed prediction results
- `currently_processing`: Tracks predictions in progress

## Setup and Running

### Prerequisites
- Docker and Docker Compose
- RabbitMQ
- Python 3.x

### Running the Application
1. Start the services:
   ```bash
   docker-compose up
   ```
2. The application will be available at:
   - Main service: `http://localhost:8080`
   - Debug port: `5678`