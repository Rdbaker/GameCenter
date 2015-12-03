#Introduction

##Introduction

Welcome to the Rank API documentation.

We have a Java client library, or you can use direct HTTP requests (with
cURL or some other tool). You can view code examples in the dark area to
the right, and you can switch between Java and cURL.

This API allows you to manage a leaderboard, adding scores and listing them with
powerful filters. You can list your leaderboard filtering by date and tag. You
can get the top scores, the scores for a particular user, and the scores nearby
another score.


##Requests
Any tool that can make HTTP requests can use the API by requesting the correct
URI. Requests should be made HTTPS so the traffic is encrypted Alternatively, you can
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

##API Key
```shell
curl -H "Authorization: Bearer $TOKEN" "https://tmwild.com/api/leaderboards"
```
Each request must be made with a valid API Key. You must send a bearer
authorization header with your request. The Java client handles this for you.

To get your API key, sign up on the homepage of this website, then sign in to the dashboard.
Once in the dashboard, click on the "settings" tab and you will be taken to a page where you can
see your API key.


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
3600 per 24 hours per Auth token, refreshing at midnight. If you exceed the
rate limit, you will get a `429` error response. For all the errors that can be
returned, see [the error section](/static/docs/index.html?#errors) below.


##Date Format
All of the dates in requests and responses are to be interpretted as UTC. They
must be in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format `YYYY-MM-DDTHH:mm:ss` for example: `"1994-03-06T23:45:11"`.

##Java Client
To use the Java client, the setup includes importing the library and
instantiating a client using your API key. We'll assume these steps
have been taken for all of the example code.

```java
import rank.*;
RankClient client = RankClient("myAPIKey");
```

Further, every function saving or listing will throw an `IOException`, which
can be inspected (ioe.getMessage()) to see what the problem was. They map to
the Rank API Error Codes.

The Java Client library uses pagination in a similar way to the raw HTTP API.
A ScoreList represents one page of responses (and can be iterated over), and
to get other pages, use scoreList.next() and scoreList.previous(). They return
null if there are no such pages.

###Installation - Eclipse
* First [download the
dependencies](https://developers.google.com/api-client-library/java/google-http-java-client/setup),
the .zip file.
* Then unzip it somewhere reasonable.
* Then go to eclipse and right click on your project in the Package Explorer
* Select "Build Path" > "Configure Build Path" > "Add External Jars..."
* Navigate to the directory where you unzipped the dependencies, then
  google-http-java-client/libs/ and select:
    1. google-http-client-<version number>.jar
    2. google-http-client-jackson<version number>.jar
    3. jackson-core-<version number>.jar
* Click "open"
* Hit "okay"
* Dance

<aside class="warning">
Make sure that, when initially creating the project, the execution environment JRE
you select for use is version 1.8.
</aside>


