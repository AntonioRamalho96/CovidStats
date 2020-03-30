import urllib.request




class Fetch:
	@classmethod
	def __fetchFromFile(cls, filename, countryName):
		#csv to a table of elements
		elements = [(line.rstrip('\n')).split(',') for line in open(filename).readlines()]

		#find line corresponding to country
		countries=[lineList[1] for lineList in elements]
		countryIndex=countries.index(countryName)

		#return values over days
		return [int(value) for value in (elements[countryIndex])[4:]]

	@staticmethod
	def updateData():
		#update confirmed cases
		url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
		urllib.request.urlretrieve(url, filename="confirmed.csv")

		#update deaths
		url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
		urllib.request.urlretrieve(url, filename="deaths.csv")

		#update recovered
		url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
		urllib.request.urlretrieve(url, filename="recovered.csv")

	@classmethod
	def confirmed(cls, countryName):
		return cls.__fetchFromFile("confirmed.csv", countryName)

	@classmethod
	def deaths(cls, countryName):
		return cls.__fetchFromFile("deaths.csv", countryName)

	@classmethod
	def recovered(cls, countryName):
		return cls.__fetchFromFile("recovered.csv", countryName)


