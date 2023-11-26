#!/bin/bash
cd /root/trade_assistant/
/root/anaconda3/envs/trade/bin/python -m trade_assistant.stock_crawlers.jobs.stock_crawl_coin_cronjob --type eod