#!/bin/sh


for i in {1..15}
do
    python create_accounts.py
    echo {i}
done