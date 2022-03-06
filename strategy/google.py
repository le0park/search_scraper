from datetime import datetime
from .core import AbstractScrapStrategy

from selenium.webdriver.common.by import By

class GoogleScrapStrategy(AbstractScrapStrategy):
	platform = 'google'
	target_url = 'https://www.google.com/search?q={}&tbm=nws'

	def scraps(self, query, page_count):
		"""Get scraps with Google

		Args:
			driver (WebDriver): Driver that helps to work with web browser
			query (str, optional): Query words to search. Defaults to ''.
			nextCount (int, optional): Count to go next pages. Defaults to 0.

		Returns:
			list: list that has scrap dict
		"""
		self.driver.get(self.target_url.format(query))

		scraps = []

		# iterate X times
		for order in range(page_count):
			# 뉴스 리스트 (#main_pack div.group_news > ul.list_news)
			report_elements = self.driver.find_elements(
				By.CSS_SELECTOR, '#search div > g-card > div > div')
			for reportIndex, report in enumerate(report_elements):
				data_element = None

				# select 2nd element if has thumbnail
				if len(report.find_elements(By.CSS_SELECTOR, ':root a > div > div')) > 1:
					data_element = report.find_element(
						By.CSS_SELECTOR, ':root a > div > div:nth-child(2)')
				else:
					# select 1st element else
					data_element = report.find_element(
						By.CSS_SELECTOR, ':root a > div > div:nth-child(1)')

				title = data_element.find_element(By.CSS_SELECTOR, ':root div:nth-child(2)')
				content = data_element.find_element(
					By.CSS_SELECTOR, ':root div:nth-child(3)')
				press = data_element.find_element(By.CSS_SELECTOR, ':root div:nth-child(1)')
				date = data_element.find_element(By.CSS_SELECTOR, ':root div:nth-child(5)')

				# stores news reports
				parsed_report = {
					'title': title.text,
					'short_text': content.text,
					'press': press.text,
					'date': date.text,
					'scrap_date': datetime.now(),
					'link': title.get_attribute('href'),
					'order': reportIndex + order * 10,
					'sub_reports': [],
					'sub_reports_count': 0,
				}

				scraps.append(parsed_report)

			# go next
			if order < page_count - 1:
				next_btn = self.driver.find_element(By.CSS_SELECTOR, '#pnnext')
				next_btn.click()

		return scraps
