FROM redis/redis-stack-server

COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh
CMD ["sh", "-c", "/usr/local/bin/init.sh"]
