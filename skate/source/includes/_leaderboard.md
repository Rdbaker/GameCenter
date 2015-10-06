# Leaderboards

## Get the top scores

> Fetching the data:

```java
import gamecenter
client = GameCenterClient("myAPIKey");
ArrayList<Score> scores = client.getScores();
```

```shell
curl "https://tmwild.com/api/leaderboards"
  -X GET
  -H "Authorization: myAPIKey"
```

> Example Response:

```json
[
  {
    "id": 1,
    "user_id": 10,
    "score": 400,
    "tag": "level_3",
    "created_at": "2015-07-12T12:16:22"
  },
  {
    "id": 2,
    "user_id": 8,
    "score": 120,
    "tag": "level_3",
    "created_at": "2015-07-12T12:16:22"
  }
]
```

This retrieves the top or bottom scores of your leaderbaord.

### Query Parameters

Parameter | Required | Type | Default | Description
--------- | -------- | ---- | ------- | -----------
`sort`    | no       | String | `"descending"` | The order the results will be returned, either `"ascending"` or `"descending"`.
`tag`     | no       | String |       | A leaderboard tag to filter the results with.
`start_date` | no    | Date String | The beginning of time. | The start date for a date range filter.
`end_date` | no      | Date String | Now | The end date for a date range filter.  Must be after `start_date`.




## Get a user's scores

> Fetching the data:

```java
import gamecenter
client = GameCenterClient("myAPIKey");
int userId = 1;
ArrayList<Score> scores = client.getUserScores(userId);
```

```shell
curl "https://tmwild.com/api/leaderboards?user_id=1"
  -X GET
  -H "Authorization: myAPIKey"
```

> Example Response:

```json
[
  {
    "id": 3,
    "user_id": 1,
    "score": 450,
    "tag": "full_armor",
    "created_at": "2015-07-12T12:16:22"
  },
  {
    "id": 2,
    "user_id": 1,
    "score": 400,
    "tag": "bonus_level",
    "created_at": "2015-07-12T12:16:22"
  },
  {
    "id": 1,
    "user_id": 1,
    "score": 430,
    "tag": "full_armor",
    "created_at": "2015-07-12T12:16:22"
  }
]
```

This retrieves a list of a user's scores in descending order of time created.

### Query Parameters

Parameter | Required | Type | Default | Description
--------- | -------- | ---- | ------- | -----------
`user_id` | yes      | Integer |      | The ID for the user to query. To query multiple users at once, comma separate `user_id`s.
`tag`     | no       | String |       | A leaderboard tag to filter on.
`start_date` | no    | Date String | The beginning of time. | The start date for a date range filter.
`end_date` | no      | Date String | Now | The end date for a date range filter.  Must be after `start_date`.




## Create a new score

> Creating the score:

```java
import gamecenter
client = GameCenterClient("myAPIKey");

int user_id = 1;
int score = 220;
String tag = "level two";

Score s = client.newScore(user_id, score, tag);
```

```shell
curl "https://tmwild.com/api/leaderboards?user_id=1&score=220&tag=level two"
  -X POST
  -H "Authorization: myAPIKey"
```

> Example Response:

```json
{
  "id": 5,
  "user_id": 1,
  "score": 220,
  "tag": "level two",
  "created_at": "2015-07-12T12:16:22"
}
```

This endpoint creates a new score in the leaderboard and returns the score object back upon success.

### Query Parameters

Parameter | Required | Type | Description
--------- | -------- | ---- | -----------
`user_id` | yes      | Integer | The ID of the user to create a leaderboard entry for.
`score`   | yes      | Integer | The score for the entry in the leaderboard.
`tag`     | no       | String | An identification tag for a leaderboard entry.




## Create a new score and list nearby scores

> Creating the score:

```java
import gamecenter
client = GameCenterClient("myAPIKey");

int user_id = 1;
int score = 220;
String tag = "level two";
int radius = 2;

ArrayList<Score> scores = client.newScoreAndList(user_id, score, tag, radius);
```

```shell
curl "https://tmwild.com/api/leaderboards?user_id=1&score=220&tag=level two&radius=1"
  -X POST
  -H "Authorization: myAPIKey"
```

> Example Response:

```json
[
  {
    "id": 53,
    "user_id": 1,
    "score": 222,
    "tag": "level two",
    "created_at": "2015-03-12T17:12:22"
  }, {
    "id": 5,
    "user_id": 1,
    "score": 220,
    "tag": "level two",
    "created_at": "2015-03-14T18:26:22"
  }, {
    "id": 5,
    "user_id": 1,
    "score": 219,
    "tag": "level two",
    "created_at": "2015-07-11T17:46:22"
  }
]
```

Add a new score and receive the scores above and below the new score.

### Query Parameters

Parameter | Required | Type | Default | Description
--------- | -------- | ---- | ------- | -----------
`user_id`   | yes    | Integer |      | The ID of the user to create a leaderboard entry for.
`score`     | yes    | Integer |      | The score value for the entry in the leaderboard.
`tag`       | no     | String |       | An identification tag for a leaderboard entry.
`radius`    | yes    | Integer |      | The number of scores to return above and below the user's score.
`sort`    | no       | String | `"descending"` | The order the results will be returned, either `"ascending"` or `"descending"`.
`filter_tag` | no    | String |       | A leaderboard tag to filter on. Must be either empty or the same as `tag`.
