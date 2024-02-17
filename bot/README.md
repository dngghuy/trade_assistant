# Bot 

- Telegram

- Binance

- Vnstock


Webhooks are generally recommended over polling for most Telegram bot use cases, because polling requires your bot to constantly make requests to Telegram’s servers, which can consume significant resources. On the other hand, webhooks offer extended functionality, update faster, and scale better.

---

Flask, a WSGI (Web Server Gateway Interface), is synchronous and can handle only one request at a time. But you can still run async functions in Flask using asyncio.run(), as in the custom webhook bot example provided by the python-telegram-bot dev team.

asyncio.run() starts an event loop and executes the given coroutine until it completes. If there are any asynchronous tasks running before or after the request is handled, those tasks will be executed in a separate event loop.

