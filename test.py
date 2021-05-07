import requests
from bs4 import BeautifulSoup


baseQuery = 'https://patents.google.com/xhr/result'

params = {'id': 'patent/US10343279B2/en',
          'qs': 'q=Deep+learning+neural+interfaces&oq=Deep+learning+neural+interfaces'}


response = requests.get(baseQuery, params=params)

soup = BeautifulSoup(response.text, 'lxml')

"""
<span itemprop="title">Navigational control of robotic systems and other computer-implemented processes using developmental network with turing machine learning</span>

<dd itemprop="publicationNumber">US10343279B2</dd>

<dd itemprop="countryCode">US</dd>
<dd itemprop="countryName">United States</dd>

<dd itemprop="priorArtKeywords" repeat>area</dd>
<dd itemprop="priorArtKeywords" repeat>developmental</dd>
<dd itemprop="priorArtKeywords" repeat>turing machine</dd>
<dd itemprop="priorArtKeywords" repeat>weights</dd>
<dd itemprop="priorArtKeywords" repeat>emergent</dd>

<dd><time itemprop="priorArtDate" datetime="2015-07-10">2015-07-10</time></dd>

<dd itemprop="inventor" repeat>Juyang Weng</dd>
<dd itemprop="inventor" repeat>Zejia Zheng</dd>
<dd itemprop="inventor" repeat>Xie He</dd>
<dt>Current Assignee (The listed assignees may be inaccurate. Google has not performed a legal analysis and makes no representation or warranty as to the accuracy of the list.)</dt>
<dd itemprop="assigneeCurrent" repeat>
  Michigan State University MSU
</dd>

<dd itemprop="assigneeOriginal" repeat>Michigan State University MSU</dd>

<dd><time itemprop="priorityDate" datetime="2015-07-10">2015-07-10</time></dd>

<dt>Filing date</dt>
<dd><time itemprop="filingDate" datetime="2016-07-08">2016-07-08</time></dd>

<dt>Publication date</dt>
<dd><time itemprop="publicationDate" datetime="2019-07-09">2019-07-09</time></dd>

<div class="abstract">
"""

title = soup.find('span', {'itemprop': "title"})
print(title.text.strip())

publicationNumber = soup.find("dd", {"itemprop": "publicationNumber"})
print(publicationNumber.text)

countryCode = soup.find("dd", {"itemprop": "countryCode"})
print(countryCode.text)

countryName = soup.find("dd", {"itemprop": "countryName"})
print(countryName.text)

priorArtKeywords = soup.find_all("dd", {"itemprop": "priorArtKeywords"})
print(priorArtKeywords)

priorArtDate = soup.find("time", {"itemprop": "priorArtDate"})
print(priorArtDate.text)

inventors = soup.find_all("dd", {"itemprop": "inventor"})
print(inventors)

assigneeCurrent = soup.find("dd", {"itemprop": "assigneeCurrents"})
print(assigneeCurrent.text.strip() if assigneeCurrent is not None else None)

assigneeOriginal = soup.find("dd", {"itemprop": "assigneeOriginal"})
print(assigneeOriginal.text)

priorityDate = soup.find("time", {"itemprop": "priorityDate"})
print(priorityDate.text)

filingDate = soup.find("time", {"itemprop": "filingDate"})
print(filingDate.text)

publicationDate = soup.find("time", {"itemprop": "publicationDate"})
print("publicationDate", publicationDate.text)

abstract = soup.find("div", {"class": "abstract"})
print("abstract", abstract.text)
