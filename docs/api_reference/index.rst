.. _api reference:

API Reference
******************************

Terminology
==============================
* `HTTP <https://en.wikipedia.org/wiki/HTTP>`_: Application-layer web protocol
  browsers and most Web APIs use.
* `Proxy Server <https://en.wikipedia.org/wiki/Proxy_Server>`_: A “middleman”
  that fetches pages on the client’s behalf
* `JSON <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON>`_:
  Data format used to pass data objects between client and server
* Service: A messaging API we might want to interact with
* Conversation: Any series of messages between two or more participants

Services
==============================

.. NOTE. What the heck is "Full Support"? I think you need to first define a
   "Tier 1" level of support, where there is read access to the elementary
   messages (because, for instance, Slack's extension misses a lot of content
   that is submitted as a reply or as an edited message). We can then advertise
   progress on a "Tier 2" of support that has more stringent requirements.

========= =============== =========
Service   Status          Notes
--------- --------------- ---------
GroupMe   Full Support
Slack     Full Support    May also add support for reading from file archives.
Discord   Support planned Similar API to slack, shouldn't take long.
========= =============== =========

.. NOTE. This below seems like a typo?

:: _endpoints:

Endpoints
==============================

Conversations List
------------------------------
::

	GET /:service/conversations

Returns a paginated list of conversations. May return up to 1,000 conversations,
but can return less. An empty conversations list indicates there are no more
conversations to retrieve.

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
page       params      string      Pass this in to return the next segment of
                                   conversations
========== =========== =========== ===========

Example query: ``/groupme/conversations``:

Example response::

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


Conversation Details
------------------------------
::

	GET /:service/conversations/:id

Required parameters:

========== =========== =========== ===========
Name       Location    Type        Description
---------- ----------- ----------- -----------
service    url         string      Service to query for conversations
token      params      string      Authentication token for the specified service
id         params      string      ID of the conversation to get details about
========== =========== =========== ===========

Example query: ``/groupme/conversations/G12345678?token=yourtokenhere``:

Example response:::

	{
		"id": "G12345678",
		"last_updated": 1525494321.0,
		"name": "The Friendly Friends"
	}

.. NOTE. It'd be nice to have some details such as whether one can always
   expect the timestamp to be in this format, or present, or what we know
   about "id" if anything at all. In other calls, same question if about
   different outputs (i.e., if it is the same type of output, don't
   copy paste explanations)

Users
------------------------------
::

	GET /:service/conversations/:id/users

Required parameters:

========== =========== =========== ===========
Name       Location    Type        Description
---------- ----------- ----------- -----------
service    url         string      Service to query for conversations
token      params      string      Authentication token for the specified service
id         params      string      ID of the conversation to get details about
========== =========== =========== ===========

Example query: ``/groupme/conversations/G42056789/users?token=yourtokenhere``:

Example response:::

    [
        {
            "id": "678967896",
            "name": "Alice Allison"
        },
        {
            "id": "986545678",
            "name": "Bob Bobertson"
        },
        {
            "id": "102w9ejq0",
            "name": "Cedric Cedricson"
        },
        {
            "id": "999999998",
            "name": "Diana Dianasdaughter"
        },
        ...
    ]


Messages
------------------------------
::

	GET /:service/conversations/:id/messages

Required parameters:

========== =========== =========== ===========
Name       Location    Type        Description
---------- ----------- ----------- -----------
service    url         string      Service to query for conversations
token      params      string      Authentication token for the specified service
id         params      string      ID of the conversation to get details about
========== =========== =========== ===========

Optional parameters:

========== =========== =========== ===========
Name       Location    Type        Description
---------- ----------- ----------- -----------
page       params      string      Pass this in to return the next segment of
                                   conversations
========== =========== =========== ===========


Example query: ``/groupme/conversations/D12345678/messages?token=yourtokenhere``:

Example response:::

	{
		"messages": [
			{
				"attachments": [],
				"id": "152549593918124022",
				"text": "Hmm ok.",
				"time": 1525495939,
				"userId": "678967896",
				"userName": "Alice Allison"
			},
			{
				"attachments": [],
				"id": "152549505028052649",
				"text": "Yeah you should definitely do IW before you leave",
				"time": 1525495050,
				"userId": "986545678",
				"userName": "Bob bobertson"
			},
			{
				"attachments": [],
				"id": "152549503011329681",
				"text": "Are you sure?",
				"time": 1525495030,
				"userId": "678967896",
				"userName": "Alice Allison"
			},
		],
		"nextPage": "152548984539247302"
	}
