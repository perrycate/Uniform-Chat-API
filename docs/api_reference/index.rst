.. _introduction:
API Reference
******************************

Terminology
==============================
* `HTTP <https://en.wikipedia.org/wiki/HTTP>`_: Application-layer web protocol browsers and most Web APIs use.
* `Proxy Server <https://en.wikipedia.org/wiki/Proxy_Server>`_: A “middleman” that fetches pages on the client’s behalf
* `JSON <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON>`_: Data format used to pass data objects between client and server
* Service: A messaging API we might want to interact with
* Conversation: Any series of messages between two or more participants

Services
==============================

Endpoints
==============================

Conversations
------------------------------
::

	GET /:service/conversations

Required parameters:

========== =========== =========== ===========
Name       Location    Type        Description
---------- ----------- ----------- -----------
service    url         string      Service to query for conversations
token      params      string      Authentication token for the specified service
========== =========== =========== ===========

Optional parameters:

========== =========== =========== ===========
Name       Location    Type        Description
---------- ----------- ----------- -----------
page       params      string      Pass this in to return the next segment of conversations
========== =========== =========== ===========


::

	{
		"conversations": [
			{
				"id": "G3435721",
				"last_updated": 1525346945.0,
				"name": "Group of people in class A"
			},
			{
				"id": "G16492586",
				"last_updated": 1525346901.0,
				"name": "Some other group"
			},
			{
				"id": "D19220606",
				"last_updated": 1525327554.0,
				"name": "John Smith"
			},
			...
		],
		"nextPage": "1:10-2:0"
	}

