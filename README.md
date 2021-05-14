# web-to-anki
This is a webscraper written in Python to fetch data from particular pages of "www.chesstactics.org" and parse them into the required fields for an anki deck card. 
It uses beautifulsoup.

##Required fields and output
The anki deck card requires the images it displays to be on local memory so the script downloads images from each page. 
Other required fields from each page are formatted and added to a list.
The data is then written into a csv file.
