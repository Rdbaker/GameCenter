#Introduction

##Introduction

Welcome to the GameCenter API documentation.

We have a Java client library, or you can use direct HTTP requests (with
cURL or some other tool). You can view code examples in the dark area to
the right, and you can switch between Java and cURL.

This API allows you to manage a leaderboard, adding scores and listing them with
powerful filters. You can list your leaderboard filtering by date and tag. You
can get the top scores, the scores for a particular user, and the scores nearby
another score.


##Requests
Any tool that can make HTTP requests can use the API by requesting the correct
URI. Requests should be made HTTPS so the traffic is encrypted, though the API
will accept HTTP if you cannot use HTTPS for some reason. Alternatively, you can
use our Java client library. You can chose the cURL examples or the Java
client examples on the right.

##Responses

> Example response object:

```json
{
  "data": [
    {
      "id": 5,
      "user_id": 1,
      "score": 220,
      "tag": "level two",
      "created_at": "2015-07-12T12:16:22.018"
    }
  ],
  "meta": {
    "total": 55,
    "links": {
      "prev": "https://tmwild.com/api/leaderboards?offset=1&page_size=1",
      "next": "https://tmwild.com/api/leaderboards?offset=35&page_size=1"
    }
  }
}
```

Each response will be JSON formatted. The object will contain `data` and `meta`.
Data will contain the data requested, or information about the action performed.
Meta is information about the response itself. See the meta section for more
info. TODO link. All example responses in the rest of this document will show
the `data` object and not the full response object.

##Meta

> Example meta object:

```json
{
  "total": 55,
  "links": {
    "prev": "https://tmwild.com/api/leaderboards?offset=5&page_size=5",
    "next": "https://tmwild.com/api/leaderboards?offset=15&page_size=5"
  }
}
```

Each response will include a `meta` object, which contains info about the response
itself. For requests returning lists the `meta` object will contain a `total`
key which is set to the total number of objects the request describes. If this
number is large, it will be different than the number of objects returned, as
the results are paginated. In this case, the `meta` object will also contain
a `links` object. This object will contain `next` and/or `previous`, which are
links that point to the next and previous page of responses, respectively. If
there are no more results or if it is the first response the `next` or `previous`
keys will not exist, respectively.

##Pagination
With requests that ask for lists in response, there are two url parameters you
can pass: `page_size`, which indicates how many elements should be returned per
page, and `offset`, which indicates which element to start at. The default
`page_size` is 5, and the maximum is 25. The default `offset` is `1`, which
refers to the first element.

<aside class="warning">
Note that
<code class="prettyprint">page_size</code>
 is not necessarily the number of objects returned. For
example, if there are 10 total objects, and you request with
<code class="prettyprint">page_size</code> =
<code class="prettyprint">5</code>
and
<code class="prettyprint">offset</code> =
<code class="prettyprint">8</code>
, only three elements will be in the response.
</aside>

These parameters will not be shown in the example requests for brevity.


##Rate Limit
The number of requests that can be made through the API is currently limited to
(TODO) per (TODO) per OAuth token. If you exceed the rate limit, you will get
a `429` error response. For all the errors that can be returned, see the error
section below. TODO link.


##Date Format
All of the dates in requests and responses are to be interpretted as UTC. They
must be in the ISO format `YYYY-MM-DDTHH:mm:ss` for example: `"1994-03-06T23:45:11"`.
