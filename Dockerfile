# Stage 1: build the React client
FROM node:22-alpine AS client-build
WORKDIR /build
COPY client/package.json client/package-lock.json ./
RUN npm ci
COPY client/ ./
RUN npm run build

# Stage 2: Python backend serving the built client
FROM python:3.12-slim
WORKDIR /app
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server/app ./server/app
COPY --from=client-build /build/dist ./client/dist
ENV PORT=8000
EXPOSE 8000
CMD uvicorn app.main:app --app-dir server --host 0.0.0.0 --port "$PORT"
