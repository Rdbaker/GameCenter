from datetime import datetime
import json

from gamecenter.api.models import Score, Game
from gamecenter.core.utils_test import BaseTestCase
from gamecenter.core.models import DB


# URL_PREFIX = "https://tmwild.com/api"
URL_PREFIX = u"http://127.0.0.1:5000/api"


class APIViewsTest(BaseTestCase):
    valid_key = "valid_key"
    auth_header = {"Authorization": "Bearer " + valid_key}
    starting_games = [
        Game(api_key=valid_key),
        Game(api_key="some_other_valid_key"),
    ]
    starting_scores = [  # don't modify this list
        dict(game=starting_games[0], created_at=datetime(2015, 4, 19), user_id=1, score=21),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 20), user_id=1, score=31, tag="fun"),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 21), user_id=1, score=41, tag="fun"),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 21), user_id=2, score=12),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 21), user_id=2, score=22),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 22), user_id=2, score=32),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 22), user_id=3, score=33, tag="level1"),
        dict(game=starting_games[0], created_at=datetime(2015, 4, 22), user_id=4, score=44, tag="level1"),
        dict(game=starting_games[0], created_at=datetime(2015, 5, 10), user_id=5, score=55),
        dict(game=starting_games[0], created_at=datetime(2015, 6, 10), user_id=6, score=66),
        dict(game=starting_games[1], created_at=datetime(2015, 4, 20), user_id=11, score=26),
    ]
    starting_data = starting_games + starting_scores

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        # only run the following few lines once
        DB.drop_all()
        DB.create_all()
        for table in reversed(DB.metadata.sorted_tables):
            DB.session.execute(table.delete())
        DB.session.add_all(self.starting_games)
        DB.session.commit()
        # DB.session.add_all(self.starting_data)
        DB.session.commit()

    def tearDown(self):
        # DB.session.close()
        # DB.drop_all()
        # DB.session.remove()
        for table in reversed(DB.metadata.sorted_tables):
            DB.session.execute(table.delete())
        # DB.session.add_all(self.starting_data)
        DB.session.commit()
        DB.drop_all()
        pass

    # **********  meta  *********
    def test_meta(self):
        """Is the meta object being generated?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header)
        self.assertEqual(json.loads(r.data)["meta"], {
            u"total": 11,
            u"links": {
                u"next": URL_PREFIX + "/leaderboards?offset=6&page_size=5",
            }
        })

    def test_prev(self):
        """Does prev point to the previous page?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={"offset": 7, "page_size": 4}, headers=self.auth_header)
        self.assertEqual(
            json.loads(r.data)["meta"]["links"]["prev"],
            URL_PREFIX + "/leaderboards?offset=3&page_size=4",
        )

    def test_prev_boundary(self):
        """Does prev go below the first object?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={"offset": 3, "page_size": 5}, headers=self.auth_header)
        self.assertEqual(
            json.loads(r.data)["meta"]["links"]["prev"],
            URL_PREFIX + "/leaderboards?offset=1&page_size=5",
        )

    def test_next_boundary(self):
        """Does next go past the last object?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={"offset": 7, "page_size": 5}, headers=self.auth_header)
        self.assertFalse("next" in json.loads(r.data)["meta"]["links"])

    def test_paging_limit(self):
        """Is there one object returned when we ask for 5 items, starting with the last?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={"offset": 11, "page_size": 5}, headers=self.auth_header)
        self.assertEqual(len(json.loads(r.data)["data"]), 1)

    # **********  GET /leaderboards  *********

    def test_leaderboards_basic(self):
        """Test basic usage of /leaderboards"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={'page_size': 2}, headers=self.auth_header)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 6)
        self.assertEqual(o1["score"], 66)
        self.assertEqual(o2["user_id"], 5)
        self.assertEqual(o2["score"], 55)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 11)

    def test_leaderboard_tag_filter(self):
        """Does the tag filter work for /leaderboards?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={"page_size": 2, "tag": "level1"},
                            headers=self.auth_header)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 4)
        self.assertEqual(o1["score"], 44)
        self.assertEqual(o2["user_id"], 3)
        self.assertEqual(o2["score"], 33)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 2)

    def test_leaderboard_ascending(self):
        """Does the sort work for /leaderboards?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", query_string={"page_size": 2, "sort": "ascending"},
                            headers=self.auth_header)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 2)
        self.assertEqual(o1["score"], 12)
        self.assertEqual(o2["user_id"], 1)
        self.assertEqual(o2["score"], 21)

    def test_leaderboard_date_filter(self):
        """Does the date filter work for /leaderboards?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "page_size": 2,
            "sort": "ascending",
            "start_date": "2015-05-01T12:34:56",
            "end_date": "2015-05-20T00:16:00",
        })
        o1 = json.loads(r.data)["data"][0]
        self.assertEqual(o1["user_id"], 5)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)

    def test_leaderboard_dates_misordered(self):
        """Does /leaderboards error when the dates given are out of order?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "start_date": "2015-05-20T00:16:00",
            "end_date": "2015-05-01T12:34:56",
        })
        self.assertEqual(r.status_code, 400)

    # **********  user_id  *********

    def test_user_id_basic(self):
        """Test basic usage of /leaderboards with a user_id"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "page_size": 2,
            "user_id": 5,
        })
        o1 = json.loads(r.data)["data"][0]
        self.assertEqual(o1["user_id"], 5)
        self.assertEqual(o1["score"], 55)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)

    def test_user_id_many_users(self):
        """Test multiple users requested for /leaderboards"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "page_size": 3,
            "user_id": "4,5,6",
        })
        o1, o2, o3 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1], json.loads(r.data)["data"][2]
        self.assertEqual(o1["user_id"], 6)
        self.assertEqual(o2["user_id"], 5)
        self.assertEqual(o3["user_id"], 4)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 3)

    def test_user_id_dates_misordered(self):
        """Does /leaderboards with a user_id error when the dates are out of order?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "user_id": 5,
            "start_date": "2015-05-20T00:16:00",
            "end_date": "2015-05-01T12:34:56",
        })
        self.assertEqual(r.status_code, 400)

    def test_user_id_tag_filter(self):
        """Does the tag filter work on /leaderboards?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "user_id": 1,
            "tag": "fun"
        })
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 1)
        self.assertEqual(o1["score"], 41)
        self.assertEqual(o2["user_id"], 1)
        self.assertEqual(o2["score"], 31)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 2)

    def test_user_id_date_filter(self):
        """Does the date filter work on /leaderboards?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "user_id": 4,
            "start_date": "2015-04-01T12:34:56",
            "end_date": "2015-04-22T23:59:59",
        })
        o = json.loads(r.data)["data"][0]
        self.assertEqual(o["user_id"], 4)
        self.assertEqual(o["score"], 44)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)

    def test_user_id_dates_descending(self):
        """Does sort work on /leaderboards?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.get("/api/leaderboards", headers=self.auth_header, query_string={
            "user_id": 1,
        })
        data = json.loads(r.data)["data"]
        sorted_data = sorted(data, key=lambda x: x["created_at"], reverse=True)
        self.assertEqual(data, sorted_data)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 3)

    # **********  add_score  *********

    def test_add_score_no_user_id(self):
        """Does /add_score error if no user_id is given?"""
        r = self.client.post(
            "/api/add_score",
            data=json.dumps({"score": 99}),
            headers=self.auth_header,
        )
        self.assertEqual(r.status_code, 400)

    def test_add_score_no_score(self):
        """Does /add_score error if no score is given?"""
        r = self.client.post(
            "/api/add_score",
            data=json.dumps({"user_id": 5}),
            headers=self.auth_header,
        )
        self.assertEqual(r.status_code, 400)

    def test_add_score_basic(self):
        """Test basic /add_score usage"""
        r = self.client.post(
            "/api/add_score",
            data=json.dumps({
                "user_id": 11,
                "score": 11,
            }),
            headers=self.auth_header,
        )
        self.assertEqual(json.loads(r.data)["data"]["user_id"], 11)
        self.assertEqual(json.loads(r.data)["data"]["score"], 11)

        r = self.client.get("/api/leaderboards", headers=self.auth_header)
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)
        score = json.loads(r.data)["data"][0]
        self.assertEqual(score["user_id"], 11)
        self.assertEqual(score["score"], 11)

    # **********  add_score_and_list  *********
    def test_add_and_list_basic(self):
        """Test basic /add_score_and_list usage"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "user_id": 11,
                "score": 25,
            }),
            query_string={"radius": 1},
            headers=self.auth_header,
        )

        scores = json.loads(r.data)["data"]
        s1, s2, s3 = scores[0], scores[1], scores[2]
        self.assertEqual(s1["user_id"], 11)
        self.assertEqual(s1["score"], 26)

        self.assertEqual(s2["user_id"], 11)
        self.assertEqual(s2["score"], 25)

        self.assertEqual(s3["user_id"], 2)
        self.assertEqual(s3["score"], 22)

    def test_add_and_list_no_user_id(self):
        """Does /add_score_and_list error if no user_id is given?"""
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "score": 11,
            }),
            query_string={"radius": 1},
            headers=self.auth_header,
        )
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_tags_mismatch(self):
        """Does /add_score_and_list error if tag and filter_tag are different?"""
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "score": 11,
                "user_id": 11,
                "tag": "level99",
            }),
            query_string={"radius": 1, "filter_tag": "level0"},
            headers=self.auth_header,
        )
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_no_score(self):
        """Does /add_score_and_list error if no score is given?"""
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "user_id": 11,
            }),
            query_string={"radius": 1},
            headers=self.auth_header,
        )
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_no_radius(self):
        """Does /add_score_and_list error if no radius is given?"""
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "user_id": 11,
                "score": 11,
            }),
            headers=self.auth_header,
        )
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_ascending(self):
        """Does sort work on /add_score_and_list?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "user_id": 11,
                "score": 25,
            }),
            query_string={
                "radius": 1,
                "sort": "ascending",
            },
            headers=self.auth_header,
        )
        scores = json.loads(r.data)["data"]
        s1, s2, s3 = scores[0], scores[1], scores[2]

        self.assertEqual(s1["user_id"], 2)
        self.assertEqual(s1["score"], 22)

        self.assertEqual(s2["user_id"], 11)
        self.assertEqual(s2["score"], 25)

        self.assertEqual(s3["user_id"], 11)
        self.assertEqual(s3["score"], 26)

    def test_add_and_list_tag_filter(self):
        """Does tag filter work on /add_score_and_list?"""
        DB.session.add_all([Score(**r) for r in self.starting_scores])
        r = self.client.post(
            "/api/add_score_and_list",
            data=json.dumps({
                "user_id": 11,
                "score": 37,
                "tag": "level1",
            }),
            query_string={
                "radius": 1,
                "filter_tag": "level1",
            },
            headers=self.auth_header,
        )
        scores = json.loads(r.data)["data"]
        s1, s2, s3 = scores[0], scores[1], scores[2]

        self.assertEqual(s1["user_id"], 4)
        self.assertEqual(s1["score"], 44)

        self.assertEqual(s2["user_id"], 11)
        self.assertEqual(s2["score"], 37)

        self.assertEqual(s3["user_id"], 3)
        self.assertEqual(s3["score"], 33)

    # TODO: with every test that doesn't error, verify the json schema is full

    # ********** api_key validation **********
    def test_auth_invalid_api_key(self):
        """Is there an error when a bad api key is given?"""
        r = self.client.get("/api/leaderboards", headers={"Authorization": "Bearer lolIAmNotAKey"})
        self.assertEqual(r.status_code, 401)

    def test_auth_no_api_key(self):
        """Is there an error when no api key is given in the header?"""
        r = self.client.get("/api/leaderboards", headers={"Authorization": "Bearer"})
        self.assertEqual(r.status_code, 401)

    def test_no_key(self):
        """Is there an error when no headers are sent?"""
        r = self.client.get("/api/leaderboards")
        self.assertEqual(r.status_code, 401)

    # ********** api_key creation **********
    def test_api_key_create_basic(self):
        """Can you create an api token and get it back?"""
        r = self.client.get("/api/signup")
        key = json.loads(r.data)["data"]["api_key"]
        self.assertIsNotNone(key)
        # self.assertIsNotNone(Game.query.filter(Game.api_key == key).first())
