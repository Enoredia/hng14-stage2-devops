FROM node:18-alpine

WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy app
COPY . .

# Create non-root user
RUN addgroup appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

# Healthcheck
HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["npm", "start"]
