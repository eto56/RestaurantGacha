# Restaurant GACHA 

This project is a demonstration of a modern, containerized, multi-service application. It's a restaurant search tool that allows users to find a random restaurant ("gacha" style) based on their location and genre preferences, accessible via both a web interface and a Discord bot.


## Core Features

-   **Random Restaurant Search:** The core "GACHA" feature returns a single, randomly selected restaurant that matches the user's search criteria.
-   **Dual Interfaces:** Users can interact with the service through either a simple web UI or a Discord bot command.
-   **External API Integration:** Fetches and processes data from the HotPepper Gourmet Web Service.
-   **Containerized Deployment:** The entire application stack is managed and deployed with Docker and Docker Compose.

## System Architecture

The application is designed using a microservices architecture, where each component is a separate, containerized service that handles a specific business concern.

-   **Go Backend (`backend`):** A lightweight API server written in Go that exposes a `/search` endpoint. It receives search requests, queries the database, and returns a random matching restaurant.
-   **Node.js Discord Bot (`bot`):** A simple Discord bot that listens for `!` commands. It calls the Go backend's API and replies with the restaurant information in the Discord channel.
-   **Python Data Pipeline (`init_db` & `scripts`):** A set of Python scripts responsible for the ETL (Extract, Transform, Load) process.
    1.  `hotpepperAPI.py` fetches thousands of restaurant records from the HotPepper API and saves them to a CSV file.
    2.  `init_db.py` creates the database schema and loads the data from the CSV into the PostgreSQL database.
-   **PostgreSQL Database (`db`):** The data store for all restaurant information.
-   **Nginx/Frontend (`frontend`):** A simple, static HTML/JavaScript frontend for the web interface. (In this setup, the Go server is serving the file directly, but in a larger app, Nginx would be a common choice).

All services communicate with each other over a Docker network.

## Technology Stack

This project intentionally uses a variety of technologies to demonstrate versatility:

-   **Backend:** **Go** - Chosen for its performance, simplicity, and low memory footprint, making it ideal for a lightweight API service.
-   **Discord Bot:** **Node.js** & **discord.js** - A popular and robust choice for building Discord bots, with a rich ecosystem.
-   **Data Processing:** **Python**, **Pandas**, & **SQLAlchemy** - The de-facto standard for data scripting and ETL tasks, demonstrating data handling capabilities.
-   **Database:** **PostgreSQL** - A powerful, open-source relational database.
-   **Containerization:** **Docker** & **Docker Compose** - For creating a reproducible, isolated, and easy-to-manage development and deployment environment. The multi-stage `Dockerfile` is used to create a minimal production image.

## How It Works

1.  **Data Ingestion:** The process starts with the `hotpepperAPI.py` script, which is run manually to populate a `hotpepper_data.csv` file.
2.  **Database Initialization:** On the first `docker-compose up`, the `init_db` service runs. It connects to the Postgres database, creates the `restaurant` table, and uses Pandas to efficiently load the data from the CSV into the database.
3.  **Application Runtime:**
    -   The **Go backend** starts, ready to accept API requests on port `8080`.
    -   The **Discord bot** starts, logs into the Discord API, and listens for messages.
4.  **User Interaction:**
    -   A user on the **web frontend** (served on port `8081`) submits a search. The JavaScript makes a `POST` request to the Go backend's `/search` endpoint.
    -   A user in **Discord** types `!新宿 居酒屋`. The bot parses this message and makes a similar `POST` request to the Go backend.
5.  **Response:** The Go backend queries the PostgreSQL database for all restaurants matching the criteria, randomly selects one, and returns it as a JSON response to either the frontend or the bot.
