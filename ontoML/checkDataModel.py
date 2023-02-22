import urllib.request, urllib.response, urllib.parse, urllib.error

urlHandler = urllib.request.urlopen('https://raw.githubusercontent.com/smart-data-models/dataModel.Consumption/d0de8a34d4cc466ff86434270afb5c2f76845654/context.jsonld')
for line in urlHandler:
    print(line.decode().strip())
