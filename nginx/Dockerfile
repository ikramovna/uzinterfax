FROM nginx:1.21-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx.conf into the container
COPY nginx.conf /etc/nginx/conf.d
