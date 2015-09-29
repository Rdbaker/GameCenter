# Leaderboards

## Get the top N scores

```java
import gamecenter

gamecenter.setKey("myAPIKey");

ArrayList scores = gamecenter.getScores(10);
```

```shell
curl "https://tmwild.com/api/leaderboards?top_n=10"
  -H "Authorization: myAPIKey"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "user_id": 10,
    "score": 400,
    "tag": "level_3",
    "created_at": "2015-07-12T12:16:22.018Z"
  },
  {
    "id": 2,
    "user_id": 8,
    "score": 120,
    "tag": "level_3",
    "created_at": "2015-07-12T12:16:22.018Z"
  }
]
```

This endpoint retrieves the top N scores on a leaderbaord.

### HTTP Request

<a href="/api/leaderboards" style="text-decoration: none;">
`GET https://tmwild.com/api/leaderboards?top_n=<N>&tag=<tag>`
</a>

### Query Parameters

Parameter | Required | Type | Default | Description
--------- | -------- | ---- | ------- | -----------
top_n | yes | Integer | 10 | The number of scores to return. Maximum of 100.
tag | no | String | | An identification tag for a leaderboard entry.
start_date | no | String in YYYY-MM-DDTHH:mm:ss.sssZ (ISO) format | the beginning of time. | The start date for a date range search.
end_date | no | String in YYYY-MM-DDTHH:mm:ss.sssZ (ISO) format | Now | The end date for a date range search.




## Get a user's scores

```java
import gamecenter

gamecenter.setKey("myAPIKey");

int userId = 1;

ArrayList scores = gamecenter.getUserScores(userId, radius);
```

```shell
curl "https://tmwild.com/api/leaderboards?user_id=1"
  -H "Authorization: myAPIKey"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 3,
    "user_id": 1,
    "score": 450,
    "tag": "full_armor",
    "created_at": "2015-07-12T12:16:22.018Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "score": 400,
    "tag": "bonus_level",
    "created_at": "2015-07-12T12:16:22.018Z"
  },
  {
    "id": 1,
    "user_id": 1,
    "score": 430,
    "tag": "full_armor",
    "created_at": "2015-07-12T12:16:22.018Z"
  }
]
```

This endpoint will return a list of a single user's scores based on the user's ID in descending order by most recent score.

### HTTP Request

<a href="/api/leaderboards?user_id=1" style="text-decoration: none;">
`GET https://tmwild.com/api/leaderboards?user_id=<id>&tag=<tag>`
</a>

### Query Parameters

Parameter | Required | Type | Default | Description
--------- | -------- | ---- | ------- | -----------
user_id | yes | Integer | | The ID for the user to query.
tag | no | String | | An identification tag for a leaderboard entry.
start_date | no | String in YYYY-MM-DDTHH:mm:ss.sssZ (ISO) format | the beginning of time. | The start date for a date range search.
end_date | no | String in YYYY-MM-DDTHH:mm:ss.sssZ (ISO) format | Now | The end date for a date range search.




## Get a user's score with a radius

```java
import gamecenter

gamecenter.setKey("myAPIKey");

int userId = 1;
int radius = 1;

ArrayList scores = gamecenter.getScoreRadius(userId, radius);
```

```shell
curl "https://tmwild.com/api/leaderboards?user_id=1&radius=1"
  -H "Authorization: myAPIKey"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 3,
    "user_id": 17,
    "score": 450,
    "tag": "level_1",
    "created_at": "2015-07-12T12:16:22.018Z"
  },
  {
    "id": 1,
    "user_id": 1,
    "score": 400,
    "tag": "level_1",
    "created_at": "2015-07-12T12:16:22.018Z"
  },
  {
    "id": 2,
    "user_id": 8,
    "score": 120,
    "tag": "level_2",
    "created_at": "2015-07-12T12:16:22.018Z"
  }
]
```

This endpoint retrieves a list of leaderboard scores. It will return a list of scores sorted in descending order by score, with the user's most recent score in the middle (if there is a middle value).


### HTTP Request

<a href="/api/leaderboards" style="text-decoration: none;">
`GET https://tmwild.com/api/leaderboards?user_id=<ID>&radius=<radius>`
</a>

### URL Parameters

Parameter | Required | Type | Default | Description
--------- | -------- | ---- | ------- | -----------
ID | yes | Integer | | The ID of the user to retrieve.
radius | yes | Integer | 4 | The number of scores to return above and below the user's score.
tag | no | String | | An identification tag for a leaderboard entry.
start_date | no | String in YYYY-MM-DDTHH:mm:ss.sssZ (ISO) format | the beginning of time. | The start date for a date range search.
end_date | no | String in YYYY-MM-DDTHH:mm:ss.sssZ (ISO) format | Now | The end date for a date range search.
