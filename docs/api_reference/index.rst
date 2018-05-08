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

There are currently 3 tiers of support for various services:

======= ===========
Tier 0  No functionality, but planned for the future.
Tier 1  Can read messages, conversations, and users.
Tier 2  Can read attachments, edits, or threaded conversations.
======= ===========

========= ======== =========
Service   Status   Notes
--------- -------- ---------
GroupMe   Tier 1
Slack     Tier 1   May also add support for reading from file archives.
Discord   Tier 0   Similar API to slack, shouldn't take long.
========= ======== =========


General Information
==============================

Here is some general information that applies to the API:

* **IDs**: IDs are always alphanumeric strings. Assumptions should not be made
  about the ID size - currently all IDs are fewer than 20 characters, but this
  may change in the future.
* **Tokens**: Authentication tokens are required for every request. For an
  authentication tutorial, see :ref:`authentication`. Every token is an
  alphanummeric string.
* **Page**: This alphanumeric string should be passed in to iterate through
  pages of content. For more information on how Unichat handles pagination, see
  :ref:`pagination`.


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
