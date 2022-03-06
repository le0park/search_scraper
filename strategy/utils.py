from strategy.google import GoogleScrapStrategy
from strategy.naver import NaverScrapStrategy

def set_strategy(driver, platform):
	if platform == 'naver':
		return NaverScrapStrategy(driver)
	elif platform == 'google':
		return GoogleScrapStrategy(driver)
	else:
		# default search on naver
		raise ValueError('Invalid site `{}` '.format(platform))
