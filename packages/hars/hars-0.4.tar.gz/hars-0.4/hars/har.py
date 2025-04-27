import json
from datetime import datetime
from pathlib import Path

from jsproto import *
import requests


class Har:
    def __init__(self, har_file: Dict | Path | str):
        if isinstance(har_file, Path| str):
            with open(har_file, 'r', encoding='utf-8-sig') as file:
                self.har = var(json.load(file))
            self.entries = self.har.log.entries
        elif isinstance(har_file, Dict):
            self.har = var(har_file)
            self.entries = self.har.log.entries
        else:
            raise TypeError("har_file_path must be a Path or Dict")

class Entry:
    def __init__(self, entry: Dict|var):
        if isinstance(entry, Dict):
            self.entry = var(entry)
        elif isinstance(entry, var):
            self.entry = entry
        self.response = self.entry.response
        self.request = self.entry.request
        self.method = self.request.method
        self.url = self.request.url
        self.headers = var({header["name"]: header["value"] for header in self.request.headers([])})
        for header in self.headers():
            if header.lower() == "accept-encoding":
                self.headers()[header] = "gzip"
        self.cookies = var({cookie["name"]: cookie["value"] for cookie in self.request.cookies([])})
        self.params = var({param["name"]: param["value"] for param in self.request.queryString([])})

        if self.request.postData:
            mimeType = self.request.postData.mimeType
            if mimeType() == "application/json":
                if self.request.postData.text and self.request.postData.text() != "":
                    self.data = var(json.loads(self.request.postData.text()))
                else:
                    self.data = var(None)
            elif mimeType() == "application/x-www-form-urlencoded":
                self.data = var({param["name"]: param["value"] for param in self.request.postData.params([])})

            else:
                if self.request.postData.text:
                    self.data = self.request.postData.text
                else:
                    self.data = var(None)
        else:
            self.data = var(None)

    def setURL(self, url: str):
        self.url = var(url)
        return self
    def setHeaders(self, headers: Dict):
        self.headers = var(headers)
        return self
    def setParams(self, params: Dict):
        self.params = var(params)
        return self
    def setData(self, data: Dict):
        self.data = var(data)
        return self
    def setMethod(self, method: str):
        self.method = var(method)
        return self
    def setCookies(self, cookies: Dict):
        self.cookies = var(cookies)

    def replay(self,**kwargs):
        self.response = var(requests.request(self.method(),self.url(),  **kwargs,headers=self.headers(),cookies=self.cookies(), params=self.params(), data=self.data() if self.data() else None),)
        return self.response

    def save(self):
        self.entry.startedDateTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.entry.time = 0

        self.entry.response.status = self.response.status_code
        self.entry.response.statusText = self.response.reason
        self.entry.response.headers = var([{"name": header, "value": self.response.headers[header]} for header in self.response.headers])
        self.entry.response.content.mimeType = self.response.headers.get("Content-Type", "")
        self.entry.response.content.text = self.response.text
        self.entry.response.content.size = len(self.response.content)
        self.entry.response.content.encoding = self.response.encoding
        self.entry.response.content.compressed = len(self.response.raw.read())

        self.entry.request.method = self.method
        self.entry.request.url = self.url
        self.entry.request.headers = var([{"name": header, "value": self.headers()[header]} for header in self.headers()])
        self.entry.request.cookies = var([{"name": cookie, "value": self.cookies()[cookie]} for cookie in self.cookies()])
        self.entry.request.queryString = var([{"name": param, "value": self.params()[param]} for param in self.params()])
        self.entry.request.postData = var({"mimeType": self.response.headers.get("Content-Type", ""), "text": self.data() if self.data() else None})
        self.entry.request.postData.params = var([{"name": param, "value": self.data()[param]} for param in self.data() if self.data()]) if self.data() else var([])
        self.entry.request.headers = var([{"name": header, "value": self.headers()[header]} for header in self.headers()])
        self.entry.request.cookies = var([{"name": cookie, "value": self.cookies()[cookie]} for cookie in self.cookies()])

        return self.entry




class RequestParser(Entry):
    def __init__(self, entry: Dict | var):
        super().__init__(entry)


class ResponseParser(Entry):
    def __init__(self, entry: Dict | var):
        super().__init__(entry)

