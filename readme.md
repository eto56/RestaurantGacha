# Restaurant GACHA

This project is a restaurant search application that allows users to find restaurants based on their location and desired genre. It provides a simple web interface and a Discord bot for searching. The application is powered by a Go backend, a PostgreSQL database, and data from the HotPepper Gourmet Web Service.

## Features

- **Web Interface:** A user-friendly web interface to search for restaurants by station and genre.
- **Discord Bot:** A Discord bot that allows users to search for restaurants directly from their Discord server.
- **Random Restaurant Selection:** The application returns a randomly selected restaurant that matches the user's search criteria, like a "GACHA" game.
- **Data from HotPepper:** The restaurant data is sourced from the HotPepper Gourmet Web Service, ensuring a wide variety of options.
- **Containerized with Docker:** The entire application is containerized using Docker, making it easy to set up and run.

## Technologies Used

- **Backend:** Go
- **Frontend:** HTML, JavaScript
- **Database:** PostgreSQL
- **Data Fetching:** Python (for interacting with the HotPepper API)
- **Discord Bot:** Node.js, discord.js
- **Containerization:** Docker, Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A HotPepper Gourmet Web Service API key.
- A Discord bot token.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/restaurantGACHA.git
    cd restaurantGACHA
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root of the project and add the following environment variables:

    ```
    DB_USER=your_db_user
    DB_PASS=your_db_password
    DB_NAME=restaurant
    DB_PORT=5432
    DB_HOST=db
    DB_SSLMODE=disable
    HOTPEPPER_API_KEY=your_hotpepper_api_key
    DISCORD_TOKEN=your_discord_bot_token
    ```

3.  **Fetch Restaurant Data:**
    Run the following command to fetch restaurant data from the HotPepper API and create a `hotpepper_data.csv` file in the `data` directory.

    ```bash
    docker-compose run --rm init_db python scripts/hotpepperAPI.py
    ```

4.  **Build and run the application:**
    Use Docker Compose to build and start all the services:

    ```bash
    docker-compose up --build
    ```

### Usage

-   **Web Interface:** Open your web browser and navigate to `http://localhost:8081`. You can then enter a station and genre to search for restaurants.
-   **Discord Bot:** Invite the Discord bot to your server. You can then use the `!` command to search for restaurants. For example:
    `!新宿 居酒屋`

## Project Structure

```
.
├── backend         # Go backend service
├── database        # Database initialization and management scripts
├── discord         # Discord bot service
├── frontend        # Frontend static files
├── scripts         # Scripts for data fetching, etc.
├── .env            # Environment variables
├── docker-compose.yml # Docker Compose configuration
└── readme.md       # This file
```

## How It Works

1.  The `scripts/hotpepperAPI.py` script fetches restaurant data from the HotPepper Gourmet Web Service and saves it as a CSV file.
2.  The `database/init_db.py` script initializes the PostgreSQL database, creates a `restaurant` table, and populates it with the data from the CSV file.
3.  The Go backend provides a `/search` API endpoint that queries the database for restaurants based on the provided station and genre.
4.  The frontend sends requests to the backend's `/search` endpoint and displays the results.
5.  The Discord bot also communicates with the backend's `/search` endpoint to provide restaurant suggestions in a Discord channel.
