# 네이버 지도 데이터 수집하기
import argparse
import csv
from datetime import datetime
import os

from strategy.utils import set_strategy
from utils import set_chrome_driver

# get input from program argument
parser = argparse.ArgumentParser(description='Search and scrap news reports.')
parser.add_argument('--site', '-s', type=str,
	help='site name to search (option: naver, google)')
parser.add_argument('--query', '-q', required=True,
	help='keyword to query')
parser.add_argument('--page-count', '-p', type=int, default=1, dest='page_count',
	help='page count to navigate (default: 1)')

user_input = parser.parse_args()

scraps = []

# load chrome driver
with set_chrome_driver() as driver:
	# set strategy of site
	strategy = set_strategy(driver, user_input.site)

	# scrap
	scraps = strategy.scraps(user_input.query, user_input.page_count)

# save scrap data to csv
# make output directory if not exist
if not os.path.exists('output'):
    os.makedirs('output')

# save result to csv file
fieldnames = ['title', 'date', 'press', 'short_text', 'order', 'scrap_date', 'link', 'sub_reports_count']
with open('output/검색결과_{}_{}.csv'.format(user_input.query, datetime.now()), 'w', encoding='utf-8-sig', newline='') as csvfile:
	csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
	csvwriter.writeheader()
	csvwriter.writerows(scraps)
