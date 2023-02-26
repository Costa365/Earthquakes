## Earthquake Monitor ##

* Earthquake Monitor Service - Get earthquakes via API (Producer)
* Email Notification Service - Send emails (Consumer)
* Push Notification Service - webpushr (Consumer) _(Not implemented yet)_
* Earthquake HistoryService - Gets reports and stores in db. Returns info (Consumer) _(Not implemented yet)_
* Frontend - Shows earthquake info. Periodically

Create a _.env_ file in the root folder with the following settings:

    EMAIL_USER=<email of sender>
    EMAIL_PASSWORD=<password of sender>
    SMTP_SERVER=smtp.mail.yahoo.com
    SMTP_PORT=587
    EMAIL_TEST_RECIPIENT=<email that will receive alerts>

Uses Redis with pub/sub. Example: https://blog.devgenius.io/how-to-use-redis-pub-sub-in-your-python-application-b6d5e11fc8de

It has the following issues:
1) Earthquakes reports are lost while frontend is offline
2) Server Sent Events are sent twice for some reason (workaround implemented)