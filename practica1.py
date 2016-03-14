#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import urllib



#cblancoc
class acortarUrl(webapp.webApp):

	content = {}
	content_inv = {}
	num = -1
	def parse(self, request):
		metodo = request.split(" ", 2)[0]
		recurso = request.split(" ", 2)[1]
		try:
			cuerpo = request.split("\r\n\r\n")[1]
		except IndexError:
			cuerpo = ""
		return (metodo, recurso, cuerpo)

	def process(self, resourceName):

		(metodo, recurso , cuerpo) = resourceName

		if metodo == "GET":
			if recurso == "/":
				httpCode = "200 OK"
				htmlBody = "<html><body><h1>ACORTADOR DE URLs</h1>"
				htmlBody += '<form action="" method="POST"'
				htmlBody += 'accept-charset="utf-8">'
				htmlBody += "<h2>Introduce la URL:</h3>"
				htmlBody += '<input type="text" name="long_url"/>'
				htmlBody += '<input type="submit" value="Acortar">'
				htmlBody += "</form>"
				htmlBody += "<table align='left' border='5'>"
				htmlBody += "<tr>"
				htmlBody += "<td bgcolor='#FFFFFF'>URL</td>"
				htmlBody += "<td bgcolor='#FFFFFF'>URL ACORTADA</td>"
				htmlBody += "</tr>"
				try:
				    for key in self.content_inv.keys():
				        htmlBody += "<tr>"
				        htmlBody += "<td>"+str(self.content_inv[key])+"</td>"
				        htmlBody += '<td><a href="'
				        htmlBody += str(self.content_inv[key])
				        htmlBody += '">http://localhost:1234/'
				        htmlBody += str(key)+'</td>'
				        htmlBody += "</tr>"
				except KeyError:
						htmlBody += "<td>No entries</td>"
				htmlBody += "</table>"
				htmlBody += "</body></html>"
			else:       #si es /algo
				try:
					recurso = int(recurso.split("/")[1])
					if recurso not in self.content_inv.keys():  #el caso de lo que pones no esta
						httpCode = "404 Not Found"
						htmlBody = ("<html><body>"
									+ "Error no se encuentra el recurso"
									+"</body></html>")
					else:      #si exite el /algo
						htmlCode = ("300 Multiple choices\nLocation: "
									+ self.content_inv[recurso])
						htmlBody =("<html><body>" + "<a href="
									+ "http://localhost:1234"
									+ self.content_inv[recurso]
									+ "</href></body></html>")
				except ValueError:
						httpCode = "404 Not Found"
						htmlBody = ("<html><body>" + "Error 404: Not Found"
									+ "</href></body></html>")
		elif metodo == "POST":
			url = cuerpo.split("url=", 1)[1]
			url = urllib.unquote(url)
			if not url.startswith("https://") and not url.startswith("https://"):
				url = "http://" + url
			else:
				url = url.split("%3A%2F%2F")[0]
			if url in self.content:
				self.num = self.content[url]
			else:
				self.num = len(self.content)
				self.content[url] = self.num
				self.content_inv[self.num] = url

			httpCode = "200 OK"
			htmlBody = ("<html><body><h2>" + "URL buscada: " + "</html></body></h2>"
						+"<html><body>"
						+"<a href=" + url + ">" + url + "</a></href></br>"
						+"</html></body>"
						+ "<html><body><h2>" "URL acortada: " + "</html></body></h2>"
						+"<html><body>"
						+ "<a href=" + url + ">" + str(self.num) + "</href></br>"
						+ "</html></body>")
		return (httpCode, htmlBody)
if __name__ == "__main__":
    testWebApp = acortarUrl("localhost", 1234)
