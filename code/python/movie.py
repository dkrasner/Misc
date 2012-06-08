import urllib
import BeautifulSoup
import re
from unidecode import unidecode


url = 'http://learn.ikigomu.com/blog_api/?user=ubuntuincident&site=wordpress'

         

def getURLWords(u, check_prop = 1):
	html = urllib.urlopen(u).read()
    	try:
		soup = BeautifulSoup.BeautifulSoup(html)
    	except:
		return ""
	texts = soup.findAll(text=True)
	words = []
	
	if check_prop:  #### this skips propositions listed below
    		for text in texts:
			temp = re.split(' ', text)
			for word in temp:
				if word not in propositions: 
					words.append(word)
	else:
		for text in texts:
			temp = re.split(' ', text)
			[words.append(word) for word in temp]

			
	return words;






propositions = ['about',
 'above',
 'across',
 'after',
 'against',
 'along',
 'amid',
 'among',
 'around',
 'at',
 'atop',
 'before',
 'behind',
 'below',
 'beneath',
 'beside',
 'between',
 'beyond',
 'but ',
 'by',
 'concerning',
 'down',
 'during',
 'except',
 'for',
 'from',
 'in',
 'inside',
 'into',
 'like',
 'near',
 'of',
 'off',
 'on',
 'onto',
 'out',
 'outside',
 'over',
 'past',
 'regarding',
 'since',
 'through',
 'throughout',
 'to',
 'toward',
 'under',
 'underneath',
 'until',
 'up',
 'upon',
 'with',
 'within',
 'without']
