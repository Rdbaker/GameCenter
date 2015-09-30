## Create a new score

```java
import gamecenter

gamecenter.setKey("myAPIKey");

int user_id = 1;
int score = 220;
String tag = "level two";

ArrayList scores = gamecenter.newScore(user_id, score, tag);
```

```shell
curl "https://tmwild.com/api/leaderboards"
  -d '{"user_id": 1, "score": 220, "tag": "level two"}'
  -H "Authorization: myAPIKey"
```

> The above command returns JSON structured like this:

```json
{
  "id": 5,
  "user_id": 1,
  "score": 220,
  "tag": "level two",
  "created_at": "2015-07-12T12:16:22.018Z"
}
```

This endpoint creates a new score in the leaderboard and returns the structured JSON representation of the score.


### HTTP Request

`POST https://tmwild.com/api/leaderboards`

### Payload Parameters

Parameter | Required | Type | Description
--------- | -------- | ---- | -----------
user_id | yes | Integer | The ID of the user to create a leaderboard entry for.
score | yes | Integer | The score for the entry in the leaderboard.
tag | no | String | An identification tag for a leaderboard entry.
