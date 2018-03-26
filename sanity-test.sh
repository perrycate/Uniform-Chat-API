#!/usr/bin/env sh

# Quick and dirty sanity checks looking for anything but HTTP 200s on endpoints
total=0
pipenv run http localhost:8000/dummy/conversations?token=AUTH --check-status
if [ $? -ne 0 ]; then
    echo "Conversations list sanity check FAILED!"
else
    echo "Conversations list sanity check passed :)"
    total=$((total+1))
fi

pipenv run http localhost:8000/dummy/conversations/42?token=AUTH --check-status
if [ $? -ne 0 ]; then
    echo "Conversations sanity check FAILED!"
else
    echo "Conversations sanity check passed :)"
    total=$((total+1))
fi

pipenv run http localhost:8000/dummy/conversations/42/users?token=AUTH --check-status
if [ $? -ne 0 ]; then
    echo "Users sanity check FAILED!"
else
    echo "Conversations sanity check passed :)"
    total=$((total+1))
fi

pipenv run http localhost:8000/dummy/conversations/42/messages?token=AUTH --check-status
if [ $? -ne 0 ]; then
    echo "Messages sanity check FAILED!"
else
    echo "Messages sanity check passed :)"
    total=$((total+1))
fi
echo $total/4
