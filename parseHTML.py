'''
Module for getting Polish words from specific URLs.
Allows to create files with words of given size, separated with a ';'.
URL used: http://www.kupwyraz.pl
'''
from lxml import etree, html, cssselect

def test_the_word(word, wanted_lenght):
	"""
	Naive checking of the correctness of the word.
	Returned word is lower case.
	"""
	if len(word)==wanted_lenght and word.isalpha():
		return word.lower()

def save_words_in_file(filename, words_list):
	"""
	Save words in a file with given filename, separated with a ;
	"""
	input = ";".join(words_list) + ";"
	try:
		fh = open(filename,"a")
		fh.writelines(input)
	except:
		pass
	finally:
		fh.close()

def get_many_word_lists(url, how_many_words):
	"""
	Get words segregated by lenghts from url, where words are between <a> tags.
	"""
	words = [ [] for i in range(how_many_words) ]
	doc = html.parse(url)
	html_tag = doc.getroot()
	for x in html_tag.iter('a'):
		text = x.text
		if text is not None and len(text) <= how_many_words:
			word_len = len(text)
			test_result = test_the_word(text, word_len)
			if test_result is not None:
				words[word_len - 1].append(test_result)
	return words

def generate_urls(basic_url, values):
	'''
	Generate URL in form: basic_url/value
	Values - iterable
	'''
	result = []
	if basic_url.endswith('/') is False:
		basic_url += "/"
	for i in values:
		result.append(basic_url + str(i))
	return result

def upload_words(filename):
	'''
	Get words from a file, separated with a ;
	'''
	fh = open(filename, "r")
	content = fh.read()
	fh.close()
	return content.split(";")

def delete_duplicates(words):
	'''
	deletes duplicates from a list or a file
	'''
	filename = ""
	if isinstance(words, str):
		result = upload_words(words)
		filename = words
		words = result	
	if isinstance(words, (tuple, list)):
		words = list(set(words))	
	if filename is not "":
		open(filename, 'w').close()
		save_words_in_file(filename, words)
	return words

if __name__ == '__main__':
	#generate all url from kupwyraz
	all_urls = generate_urls("http://www.kupwyraz.pl/znak", "abcdefghijklmnoprstuwz")
	pages = []
	for i in all_urls:
		a = generate_urls(i, ("p-", ))
		pages.append(a[0])
	ranges = (36, 42, 44, 65, 18, 23, 30, 17, 17, 15, 85, 30, 52, 68, 101, 269, 70, 116, 43, 44, 117, 115)
	for (page, nr_of_pages) in zip(pages, ranges):
		all_urls.extend(generate_urls(page, [i for i in range(2, nr_of_pages)]))


	#parse urls and save words in files
	for x in all_urls:
		try:
			list_multiple = get_many_word_lists(x, 12)
			for l in range(5, 13):
				try:
					filename = str(l) + ".txt"
					if len(list_multiple[l-5]) >= 1:
						save_words_in_file(filename, list_multiple[l-5])
				except Exception as inst:
					print(type(inst))
					print("url = " + x + " page = " + str(l)  )
		except Exception as inst:
			print(type(inst))
			print("url = " + x)

	#delete duplicates
	for i in range(3, 13):
		delete_duplicates(str(i) + ".txt")


