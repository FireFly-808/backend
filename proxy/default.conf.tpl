// config block for server 
server {
    // set from config that is passed to the service LISTEN_PORT is an env var
    listen ${LISTEN_PORT};

    // map urls from /static to /vol/static
    location /static {
        alias /vol/static;
    }

    // map all forward slash requests
    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }
}