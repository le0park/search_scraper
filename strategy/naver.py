from datetime import datetime
from .core import AbstractScrapStrategy

from selenium.webdriver.common.by import By

class NaverScrapStrategy(AbstractScrapStrategy):
	platform = 'naver'
	target_url = 'https://search.naver.com/search.naver?where=news&query={}'

	def scraps(self, query, page_count):
		"""Get scraps with Naver

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
			report_elements = self.driver.find_elements(By.CSS_SELECTOR, '#main_pack div.group_news > ul.list_news > li')
			for reportIndex, report in enumerate(report_elements):
				title = report.find_element(By.CSS_SELECTOR, 'div.news_wrap a.news_tit')
				content = report.find_element(By.CSS_SELECTOR, 'div.news_wrap div.news_dsc .dsc_txt_wrap')
				press = report.find_element(By.CSS_SELECTOR, 'div.news_info div.info_group > a.press')
				date = report.find_element(By.CSS_SELECTOR, 'div.news_info div.info_group > span.info')

				sub_reports = []
				sub_reports_elements = report.find_elements(By.CSS_SELECTOR, 'div.news_cluster ul.list_cluster > li')
				for sub_report in sub_reports_elements:
					sub_title = sub_report.find_element(By.CSS_SELECTOR, 'a.sub_tit')
					sub_press = sub_report.find_element(By.CSS_SELECTOR, 'span.sub_area > cite.press')
					sub_date = sub_report.find_element(By.CSS_SELECTOR, 'span.sub_area > span.sub_txt')

					sub_reports.append({
						'title': sub_title.text,
						'press': sub_press.text,
						'date': sub_date.text,
						'url': sub_title.get_attribute('href')
					})

				# stores news reports
				parsed_report = {
					'title': title.text,
					'short_text': content.text,
					'press': press.text,
					'date': date.text,
					'scrap_date': datetime.now(),
					'link': title.get_attribute('href'),
					'order': reportIndex + order * 10,
					'sub_reports': sub_reports,
					'sub_reports_count': len(sub_reports),
				}

				scraps.append(parsed_report)

			# go next
			if order < page_count - 1:
				next_btn = self.driver.find_element(By.CSS_SELECTOR, '#main_pack > div.api_sc_page_wrap > div > a.btn_next')
				next_btn.click()

		return scraps
