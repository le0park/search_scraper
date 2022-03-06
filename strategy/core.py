from abc import *

class AbstractScrapStrategy(metaclass=ABCMeta):
	platform = 'etc'
	driver = None

	def __init__(self, driver):
		self.driver = driver

	@abstractmethod
	def scraps(self, query, page_count):
		return []
