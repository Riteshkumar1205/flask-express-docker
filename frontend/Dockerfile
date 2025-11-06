# frontend/Dockerfile
FROM node:20-slim

WORKDIR /app

# Copy package.json and package-lock.json first for caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
