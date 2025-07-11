# Stage 1: Build the Go application
FROM golang:1.24.1-alpine AS builder

WORKDIR /app

# Copy Go modules and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the application
# -o /server creates the binary at the root
# CGO_ENABLED=0 and -ldflags '-s -w' create a small, static binary
RUN CGO_ENABLED=0 go build -ldflags '-s -w' -o /server .

# Stage 2: Create the final, minimal image
FROM alpine:latest

# Import the compiled binary from the builder stage
COPY --from=builder /server /server

# Copy the .env file for runtime configuration
# Note: In a real production environment like Railway, you will use their secret management system instead of a .env file.
COPY .env .env

# Expose the port the server runs on
EXPOSE 8080

# The command to run the application
# The server will source the .env file for configuration
CMD ["/server"]
