# Frontend Documentation (React & Vite)

This document provides a basic overview of the frontend application, designed for those who may not be familiar with React.

## What is this?

This is the user interface for the Restaurant GACHA project. It's a **Single Page Application (SPA)** built using modern web technologies:

-   **React:** A JavaScript library for building user interfaces. Instead of writing one giant HTML file, we build the UI out of small, reusable pieces called **components**.
-   **Vite:** A very fast and modern tool for building and running the React application during development.

## How It Works: A Simple Overview

1.  When you visit the website, your browser loads a single, mostly empty `index.html` file.
2.  That HTML file then loads the JavaScript code.
3.  React takes over and "renders" the user interface, creating the search form, buttons, and result area dynamically with JavaScript.
4.  When you type in the search form, React keeps track of the input.
5.  When you click "Find Restaurant", React sends a request to the backend API.
6.  When the backend responds with a restaurant, React updates the page to display the result.

This approach makes the user interface feel fast and responsive because the page doesn't need to fully reload from the server every time you do something.

## Key Files Explained

Here are the most important files in this `frontend` directory:

-   `index.html`
    -   This is the **only HTML file**. It's the entry point for the application. Its main job is to provide a `<div id="root"></div>` element where our React application will be rendered.

-   `src/main.jsx`
    -   This is the **starting point for our React code**. It finds the `<div id="root"></div>` from `index.html` and tells React to render our main application component (`<App />`) inside of it.

-   `src/App.jsx`
    -   This is the **main application component**. It contains all the logic and HTML-like code (called JSX) for the entire user interface: the title, the search form, the input boxes, and the area where the result is displayed.
    -   **State (`useState`):** You'll see lines like `const [station, setStation] = useState('');`. This is how React "remembers" things. `station` holds the current value of the station input box, and `setStation` is the function we use to update it. We do this for the search inputs, the final restaurant result, and any errors.
    -   **Event Handling (`onSubmit`):** The `handleSubmit` function is an event handler. It's the code that runs when the user submits the form (by clicking the button). This function is responsible for sending the search request to the backend.
    -   **API Calls (`fetch`):** Inside `handleSubmit`, we use the `fetch` function to make a `POST` request to our backend's `/search` endpoint.

-   `vite.config.js`
    -   This is the configuration file for Vite. The most important part is the `proxy` configuration.
    -   **Why do we need a proxy?** Our React app runs on one address (`http://localhost:5173`) and our backend runs on another (`http://localhost:8081`). For security reasons, browsers block requests between different addresses (this is called CORS). The proxy in Vite acts as a middleman, forwarding our API requests from `/search` to the backend server, which avoids this security issue during development.

-   `package.json`
    -   This file lists the project's dependencies (like React itself) and defines the scripts we can run (like `npm run dev` to start the development server).

## How to Run It

The entire application, including this frontend, is designed to be run with Docker.

```bash
# From the root of the project (restaurantGACHA/)
docker-compose up --build
```

This command will start the Vite development server, and you can view the application at `http://localhost:5173`.