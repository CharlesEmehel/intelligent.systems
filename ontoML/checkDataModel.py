import urllib.request, urllib.response, urllib.parse, urllib.error

urlHandler = urllib.request.urlopen('https://sargon-n5geh.netlify.app/ontologies/Sargon.ttl')
for line in urlHandler:
    print(line.decode().strip())
