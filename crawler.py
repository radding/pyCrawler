###############################################################################
# This is a script to check the CSS used in a page vs the CSS in the style    # 
# sheets. This is for better maintence. This will slim down a stylesheet and  #
# speed up page load. Created by Yoseph Radding. 							  #
###############################################################################
# Script overview:															  #
#	class webPage: 															  #
###############################################################################

# class Website(object):
# 	def __init__(self,url):

import bs4
import urllib
from collections import deque

class CrawlerManager(object):
	def __init__(self,baseURL):
		self.baseURL = baseURL
		self.next = deque([])
		self.done = []
		self.classAndIDs = []

	def getNext(self):
		if(self.hasNext()):
			nextLink = self.next.popleft()
			self.done.append(nextLink)
			# if (self.baseURL not in nextLink):
			# 	nextLink = self.baseURL + nextLink
			# else:
			# 	nextLink = clean(nextLink)
			return nextLink

	def hasNext(self):
		try:
			x = self.next.popleft()
			self.next.appendleft(x)
			return True
		except IndexError:
			return False

def clean(link):
	while link[0:2] == '..' or link[0:3] == '/..':
		if  link[0:3] == '/..':
			link = link[3:]
		else:
			link = link[2:]
	return link

def extractLinks(soup, manager):
	for i in soup.findAll('a'):
		link = i["href"]
		link = clean(link)
		# print link
		# print manager.done
		if("mp4" in link or "pdf" in link):
			continue
		if(('https' in link or 'http' in link)):
			continue
		if(link[0] == '#'):
			continue
		elif (manager.baseURL  not in link): #and (link[0] == '/' or link[0:2] == '..')):
			link = manager.baseURL + link
			# print link
		else:
			pass 
		if(link not in manager.done and link not in manager.next):
			# print link
			# print manager.done
			# # raw_input()
			manager.next.append(link)

def extractClass(soupTag):
	try:
		return soupTag["class"]
	except:
		return None

def extractID(soupTag):
	try:
		return soupTag["id"]
	except:
		return None

def getIDorClass(soupTag, manager):
	tempList = []
	x = extractClass(soupTag)
	y = extractID(soupTag)
	if(bool(x) and x not in manager.classAndIDs):
		tempList.append(x)
	if(bool(y) and y not in manager.classAndIDs):
		tempList.append(y)
	return tempList

def crawlPage(manager):
	thing = manager.getNext()
	page = urllib.urlopen(thing)
	# print(page)
	soup = bs4.BeautifulSoup(page)
	extractLinks(soup, manager)
	for i in soup.findAll(True):
		print type(i)
		if(type(i) == bs4.element.Tag):
			tempList = getIDorClass(i,manager)
			if(tempList):
				
				if(type(tempList[0]) == type(list())):
					tempList = tempList[0]
				# print(type(tempList[0]))
				manager.classAndIDs = manager.classAndIDs + tempList
	if(manager.next):
		crawlPage(manager)

def crawl(url):
	manager = CrawlerManager(url)
	manager.next.append(url)
	crawlPage(manager)
	return manager


def main(argc,argv):
	webSite = raw_input("Enter Website url: ")
	stylesheet = raw_input("Enter CSS location: ")
	m = crawl(webSite)
	tempList = list(m.classAndIDs)
	print list(set([str(x) for x in tempList]))
	return m

main(None, None)