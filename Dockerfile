FROM nginx:stable

RUN \
  apt-get update \
  && apt-get -y install python3 python3-pip python3-venv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN \
   pip3 install jinja2 simplejson


ADD ./nginx /etc/nginx
ADD . /habidat

RUN \
  mkdir /habidat/static \
  && chown -R nginx:nginx /habidat

ADD . /habidat

WORKDIR /habidat

COPY docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh 

ENTRYPOINT ["docker-entrypoint.sh"]
CMD /bin/sh -c 'while :; do sleep 1h & wait ${!}; nginx -s reload; done & nginx -g "daemon off;"'

