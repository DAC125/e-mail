from twisted.internet import reactor

from twisted.news import database, news, nntp



GROUPS = ['Inbox']

SMTP_SERVER = '127.0.0.1'

STORAGE_DIR = 'mailStorage'



newsStorage = database.NewsShelf(SMTP_SERVER, STORAGE_DIR)

for group in GROUPS:

    newsStorage.addGroup(group, [])

    factory = news.NNTPFactory(newsStorage)

    reactor.listenTCP(1199, factory)

    reactor.run()