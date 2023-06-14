
### STAGE 1: Build ###
FROM node:16-slim as build
WORKDIR /app
COPY . .
RUN npm install

### STAGE 2: Run ###
FROM nginx:1.23.3-alpine-slim as production
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/ /usr/share/nginx/html
ENTRYPOINT nginx -g 'daemon off;'