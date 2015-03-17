#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import urllib

class acortar (webapp.webApp):
	nUrl = 0
	dicUrl = {}
	dicNewUrl = {}

	def  htmlFormat(self, body):
		return '<html><body>' + body + '</p></body></html>'

	def anadirUrl(self, url):
		if url not in self.dicUrl.keys():
			newUrl = "http://localhost:1234/" + str(self.nUrl)
 			self.nUrl += 1
			self.dicUrl[url] = newUrl   #lo meto en el diccionario 
			self.dicNewUrl[newUrl] = url
		else:
			newUrl = self.dicUrl[newUrl]
		return newUrl

	def getHtmlListUrls(self):
		urlshtml = ""
		for url in self.dicUrl.keys():
			urlshtml += "<p><a href=" +url + ">" + url + "</a>"+ \
							" --->    " + "<a href=" + self.dicUrl[url] + ">" + \
							self.dicUrl[url] + "</a></p>"

	def parse(self, request):
		verb = request.split(" ")[0]
		resource = request.split(" ")[1]
		body = request.split("\r\n\r\n", 1)[1]
		return (verb, resource, body)

	def process(self, parsedRequest):
		(verb, resource, body) = parsedRequest
		
		formulario = '<form action="" method="POST" accept-charset="UTF-8">' + \
								'URL para acortar: <input type="text" name="url">' + \
								'<input type="submit" value="Acorta!"></form>'

		if verb == "GET":
			if resource == "/":
				httpCode = "200 OK"
				urlshtml = self.getHtmlListUrls()
				httpBody = self.htmlFormat(formulario + urlshtml)
			else:
				url = "http://localhost:1234" + resource
				if url in self.dicNewUrl.keys():
					urlsRedirect = self.dicNewUrl[url]
					httpCode = "301 Redirect\nLocation: " + urlRedirect
					httpBody = self.htmlFormat( "<a href=" + urlRedirect
														+ ">Pincha si no teredirige</a>")
				else:
					httpCode= "404 Recurso no encontrado"
					httpBody = self.htmlFormat("404 Recurso no disponible")
		elif  verb == "POST" and resource == "/":
			url = body.split("url=", 1)[1]
			url = urllib.unquote(url)
			if not url.startswith("https://") and not url.startswith("https://"):
				url = "http://" + url
			newUrl = self.addUrl(url)
			httpCode = "200 OK"
			body =  "<p><a href=" + url + ">" + url + "</a>" + \
							" --> <a href=" + newURL + ">" + newURL + "</a></p>"
			httpBody = self.htmlFormat(body)
		else:
			httpCode = "404 Not Found"
			httpBody = self.htmlFormat("No disponible")
		return (httpCode, httpBody)
			
if __name__ == '__main__':
	try:
		urlcortar = acorta("localhost", 1234)
	except KeyboardInterrupt:
		print "Cerrado"



















