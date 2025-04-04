FROM python:3.11-slim

# =========== // ENVIRONMENT VARIABLES // ===========

ENV APP_ROOT=/eze-finance
ENV ALWAYS_HEALTHY=false

# =========== // ARGS // ===========

ARG DEBIAN_FRONTEND=noninteractive

# =========== // INSTALLATIONS // ===========

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    file \
    git \
    supervisor \
    nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && \
    chmod +x /usr/local/bin/cloudflared


# =========== // WORKING DIRECTORY SETUP // ===========

WORKDIR $APP_ROOT
COPY . .

# COPY AND MAKE DIRS
RUN mkdir -p /var/log/supervisor /etc/cloudflared
COPY cloudflare/ /etc/cloudflared/
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/supervisord.conf /etc/supervisor/supervisord.conf

# =========== // BUILD SCRIPTS // ===========

# Installing
RUN pip install -r requirements.txt

# Building the Sphinx Docs
RUN cd docs && make clean && make html && cd .. 

# Move the built HTML files to the Nginx web root
RUN mkdir -p /var/www/docs
RUN cp -r docs/build/html/* /var/www/docs/

# =========== // ENTRYPOINT AND HEALTHCHECK // ===========

HEALTHCHECK --interval=5m --timeout=3s --start-period=5s --start-interval=5s --retries=3\
  CMD python healthcheck.py || exit 1

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]