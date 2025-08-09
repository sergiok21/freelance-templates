#!/bin/bash

redis-stack-server --appendonly yes &

while ! redis-cli ping; do
  sleep 1
done

users_exists=$(redis-cli EXISTS users)
if [ "$users_exists" -eq 0 ]; then
  redis-cli JSON.SET users . '{}';
fi

admins_exists=$(redis-cli EXISTS admins)
if [ "$admins_exists" -eq 0 ]; then
  redis-cli JSON.SET admins . '{}';
  redis-cli JSON.SET admins .tokens '{}';
  redis-cli JSON.SET admins .tasks '{}';
fi

wait
