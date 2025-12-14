# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Build-Argument für API URL
ARG VITE_API_URL=http://localhost:5000/api
ENV VITE_API_URL=$VITE_API_URL

# Dependencies installieren
COPY package*.json ./
RUN npm ci

# App bauen
COPY . .
RUN npm run build

# Production stage mit Nginx
FROM nginx:alpine

# Nginx Config kopieren
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Build-Output kopieren
COPY --from=builder /app/dist /usr/share/nginx/html

# Port freigeben
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

