FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /usr/src/app

# Install runtime deps directly (no package.json)
RUN npm install --omit=dev express@4.19.2 mysql2@3.10.0

# Copy source
COPY app ./app

EXPOSE 8000
CMD ["node", "app/index.js"]
