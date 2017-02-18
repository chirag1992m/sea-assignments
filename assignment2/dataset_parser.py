# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

DatasetParser
Helps in parsing the dataset given
'''
'''
'''
import xml.etree.ElementTree as et
import text_utility as tu

class DatasetParser:

	def __init__(self, filepath):
		self.__root = et.parse(filepath).getroot()

		self.__base_URL = self.get_base_url()
		self.__text_util = tu.StringCleaner()

	def get_base_url(self):
		base_url = ""

		for child in self.__root:
			if child.tag.endswith('siteinfo'):
				siteinfo = child
				for info in siteinfo:
					if info.tag.endswith('base'):
						base_url = info.text
						break
				break

		if base_url:
			index = base_url.rfind('/')
			base_url = base_url[:index+1]

		return base_url

	def __get_page_url(self, title):
		return self.__base_URL + title.replace(" ", "_")

	def get_page_generator(self):
		for child in self.__root:
			if child.tag.endswith('page'):
				yield child

	def __parse_text(self, text):
		return self.__text_util.process_string(text)

	def get_title_url_textvector(self, pageElement):
		title = ""
		url = ""
		text_vector = []
		title_vector = []
		text = ""

		for child in pageElement.iter(None):
			if child.tag.endswith('title'):
				url = self.__get_page_url(child.text)
				title_vector = self.__parse_text(child.text)
				title = child.text

			if child.tag.endswith('text'):
			 	text_vector = self.__parse_text(child.text)
			 	text = child.text

		return {'title_vector': title_vector, 
			'title': title, 
			'URL': url, 
			'text_vector': text_vector,
			'text': text}

	def parsed_documents_iterator(self):
		for page in self.get_page_generator():
			yield self.get_title_url_textvector(page)