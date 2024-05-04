## Earthquake Monitor ##

This is an Earthquake monitoring and reporting application. It originally used the [EMSC](https://emsc-csem.org) RSS Feed and when that became unavailable, the [USGS API](https://earthquake.usgs.gov/fdsnws/event/1/) was used instead.

Can be accessed at [earthquakes.costa365.site](https://earthquakes.costa365.site).

* Earthquake Monitor Service - Get earthquakes via API (Producer)
* Email Notification Service - Send emails (Consumer) _(Sends to one email address only)_
* Push Notification Service - webpushr (Consumer) _(Not implemented yet)_
* Earthquake HistoryService - Gets reports and stores in db. Returns info (Consumer) _(Not implemented yet)_
* Frontend - Shows earthquake information. Is dynamically update via Server Sent Events (SSE)

Create a _.env_ file in the root folder with the following settings:

    EMAIL_USER=<email of sender>
    EMAIL_PASSWORD=<password of sender>
    SMTP_SERVER=smtp.mail.yahoo.com
    SMTP_PORT=587
    EMAIL_TEST_RECIPIENT=<email that will receive alerts>

Run local dev environment using Docker: ``Docker compose up``.

Uses Redis with pub/sub. Example: https://blog.devgenius.io/how-to-use-redis-pub-sub-in-your-python-application-b6d5e11fc8de

It has the following issues:
1) Earthquakes reports are lost while frontend is offline (page needs to be refreshed)
2) Server Sent Events are sent twice for some reason (workaround implemented)
