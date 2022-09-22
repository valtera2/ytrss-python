from asyncore import read
import configparser, urllib.parse, xml.etree.ElementTree

fileName = 'index.html'
config = configparser.ConfigParser()
config.read('extract.ini')
#baseUrl = 'https://www.youtube.com/feeds/videos.xml?channel_id='
embedBase = 'https://www.youtube.com/embed/'

def genHeader():
	out ='<html><head><link rel="stylesheet" href="t.css" type="text/css"/></head><body>'
	return out
	
def openXml(filename):
	try:
		xmlF = xml.etree.ElementTree.parse(filename)
		return xmlF
	except:
		print("cannot find " + filename)

def stripYurl(url):
	strip_url = urllib.parse.urlparse(url)
	strip_url = strip_url.query[2:]
	return strip_url

def genOut(tree, title):
	out = ("<div class='title'>" + title + "</div>")
	out +=("<table>")
	if isinstance(tree, xml.etree.ElementTree.ElementTree):
		root = tree.getroot()
		for child in root:
			for child2 in child:
				if (child2.tag == '{http://www.w3.org/2005/Atom}title'):
					out +=("<td>" + child2.text + "</td>")
				if (child2.tag == '{http://www.w3.org/2005/Atom}link'):
					out +=("<td>")
					href = child2.get('href')
					out +=(href)
					out +=("</td>")
					out +=("<td>")
					out +=("<a href=" + embedBase + stripYurl(href) + ">" + "embed link" + "</a>")
					out +=("<tr>")
		out +=("</table>")
	else:
		out +=("<div class='error'>" + "missing xml - run refresh to download" + "</div>")
	return out

def getIniFilename(section):
	fileName = config.get(section, 'filename')
	return fileName

def getIniId(section):
	id = config.get(section, 'id')
	return id

def genFooter():
	out = '<div class="toolbar"></div></body></html>'
	return out

def main():
	out = genHeader()
	for sect in config.sections():
		title = config.get(sect, 'title')
		tree = openXml(config.get(sect, 'path'))
		out += genOut(tree, title)
		out += genFooter()
	with open(fileName, 'w') as f:
		f.write(out)
		print("webpage generated")

main()
