# --- Build stage for Go backend ---
FROM golang:1.24.1-alpine AS builder
WORKDIR /app

# Install git and bash for env loading
RUN apk add --no-cache git bash

# Copy env for build-time
COPY .env /app/.env

# Copy Go modules manifests and download dependencies
COPY backend/go.mod backend/go.sum ./backend/
WORKDIR /app/backend
RUN go mod download

# Copy backend source
COPY backend/. ./

# Build with build-time environment variables loaded
#   - 1) grep でコメント行を除外
#   - 2) xargs で KEY=VALUE 形式に展開して export
RUN export $(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' /app/.env | xargs) \
    && go build -o server .

# --- Build stage for frontend (static) ---
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/. ./
# If frontend needs build, uncomment:
# RUN npm ci && npm run build

# --- Final runtime stage ---
FROM alpine:3.18
WORKDIR /app

# Install bash and certificates for runtime
RUN apk add --no-cache bash ca-certificates

# Copy env, backend binary, and frontend files
COPY --from=builder /app/.env .env
COPY --from=builder /app/backend/server ./server
COPY --from=frontend-builder /app/frontend ./frontend

# Expose HTTP port
EXPOSE 8080

# Source env and run server
ENTRYPOINT ["bash", "-c", "set -o allexport && source .env && exec ./server"]
