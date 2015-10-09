from datetime import datetime
import json

from gamecenter.api.models import Score
from gamecenter.core.utils_test import BaseTestCase
from gamecenter.core.models import DB


URL_PREFIX = "https://tmwild.com/api"


class APIViewsTest(BaseTestCase):
    starting_data = [  # don't modify this list
        Score(created_at=datetime(2015, 4, 19), user_id=1, score=21),
        Score(created_at=datetime(2015, 4, 20), user_id=1, score=31, tag="fun"),
        Score(created_at=datetime(2015, 4, 21), user_id=1, score=41, tag="fun"),
        Score(created_at=datetime(2015, 4, 21), user_id=2, score=12),
        Score(created_at=datetime(2015, 4, 21), user_id=2, score=22),
        Score(created_at=datetime(2015, 4, 22), user_id=2, score=32),
        Score(created_at=datetime(2015, 4, 22), user_id=3, score=33, tag="level1"),
        Score(created_at=datetime(2015, 4, 22), user_id=4, score=44, tag="level1"),
        Score(created_at=datetime(2015, 5, 10), user_id=5, score=55),
        Score(created_at=datetime(2015, 6, 10), user_id=6, score=66),
    ]

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        DB.create_all()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()

    # **********  meta  *********
    def test_meta(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()

        r = self.client.get("/api/top")
        self.assertEqual(json.loads(r.data)["meta"], {
            "total": 10,
            "links": {
                "next": URL_PREFIX + "/top?offset=6&page_size=5",
            }
        })

    def test_prev(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"offset": 7, "page_size": 4})
        self.assertEqual(
            json.loads(r.data)["meta"]["links"]["prev"],
            URL_PREFIX + "/top?offset=3&page_size=4",
        )

    def test_prev_boundary(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"offset": 3, "page_size": 5})
        self.assertEqual(
            json.loads(r.data)["meta"]["links"]["prev"],
            URL_PREFIX + "/top?offset=1&page_size=5",
        )

    def test_next_boundary(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"offset": 7, "page_size": 5})
        self.assertFalse("next" in json.loads(r.data)["meta"]["links"])

    def test_paging_limit(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"offset": 10, "page_size": 5})
        self.assertEqual(len(json.loads(r.data)["data"]), 1)

    # **********  top  *********

    def test_top_basic(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"page_size": 2})
        self.assertEqual(json.loads(r.data)["meta"]["total"], 10)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 6)
        self.assertEqual(o1["score"], 66)
        self.assertEqual(o2["user_id"], 5)
        self.assertEqual(o2["score"], 55)

    def test_top_tag_filter(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"page_size": 2, "tag": "level1"})
        self.assertEqual(json.loads(r.data)["meta"]["total"], 2)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 4)
        self.assertEqual(o1["score"], 44)
        self.assertEqual(o2["user_id"], 3)
        self.assertEqual(o2["score"], 33)

    def test_top_ascending(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={"page_size": 2, "sort": "ascending"})
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 2)
        self.assertEqual(o1["score"], 12)
        self.assertEqual(o2["user_id"], 1)
        self.assertEqual(o2["score"], 21)

    def test_top_date_filter(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/top", data={
            "page_size": 2,
            "sort": "ascending",
            "start_date": "2015-05-01T12:34:56",
            "end_date": "2015-05-20T00:16:00",
        })
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)
        o1 = json.loads(r.data)["data"][0]
        self.assertEqual(o1["user_id"], 5)

    def test_top_dates_misordered(self):
        r = self.client.get("/api/top", data={
            "start_date": "2015-05-20T00:16:00",
            "end_date": "2015-05-01T12:34:56",
        })
        self.assertEqual(r.status_code, 400)

    # **********  user_id  *********

    def test_user_id_basic(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/user_id", data={
            "page_size": 2,
            "user_id": 5,
        })
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)
        o1 = json.loads(r.data)["data"][0]
        self.assertEqual(o1["user_id"], 5)
        self.assertEqual(o1["score"], 55)

    def test_user_id_many_users(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/user_id", data={
            "page_size": 2,
            "user_id": "4,5,6",
        })
        self.assertEqual(json.loads(r.data)["meta"]["total"], 3)
        o1, o2, o3 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1], json.loads(r.data)["data"][2]
        self.assertEqual(o1["user_id"], 6)
        self.assertEqual(o2["user_id"], 5)
        self.assertEqual(o3["user_id"], 4)

    def test_user_id_no_user_id(self):
        r = self.client.get("/api/user_id")
        self.assertEqual(r.status_code, 400)

    def test_user_id_dates_misordered(self):
        r = self.client.get("/api/user_id", data={
            "user_id": 5,
            "start_date": "2015-05-20T00:16:00",
            "end_date": "2015-05-01T12:34:56",
        })
        self.assertEqual(r.status_code, 400)

    def test_user_id_tag_filter(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/user_id", data={
            "user_id": 1,
        })
        self.assertEqual(json.loads(r.data)["meta"]["total"], 2)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 1)
        self.assertEqual(o1["score"], 41)
        self.assertEqual(o2["user_id"], 1)
        self.assertEqual(o2["score"], 31)

    def test_user_id_date_filter(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/user_id", data={
            "user_id": 4,
            "start_date": "2015-04-01T12:34:56",
            "end_date": "2015-04-21T23:59:59",
        })
        self.assertEqual(json.loads(r.data)["meta"]["total"], 2)
        o1, o2 = json.loads(r.data)["data"][0], json.loads(r.data)["data"][1]
        self.assertEqual(o1["user_id"], 4)
        self.assertEqual(o1["score"], 32)
        self.assertEqual(o2["user_id"], 4)
        self.assertEqual(o2["score"], 22)

    def test_user_id_dates_descending(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.get("/api/user_id", data={
            "user_id": 1,
        })
        self.assertEqual(json.loads(r.data)["meta"]["total"], 2)
        data = json.loads(r.data)["data"]
        sorted_data = sorted(data, key=lambda x: x["created_at"], reverse=True)
        self.assertEqual(data, sorted_data)

    # **********  add_score  *********

    def test_add_score_no_user_id(self):
        r = self.client.post("/api/add_score", data={
            "score": 99,
        })
        self.assertEqual(r.status_code, 400)

    def test_add_score_no_score(self):
        r = self.client.post("/api/add_score", data={
            "user_id": 5,
        })
        self.assertEqual(r.status_code, 400)

    def test_add_score_basic(self):
        r = self.client.post("/api/add_score", data={
            "user_id": 11,
            "score": 11,
        })
        self.assertEqual(json.loads(r.data)["data"]["user_id"], 11)
        self.assertEqual(json.loads(r.data)["data"]["score"], 11)

        r = self.client.get("/api/top")
        self.assertEqual(json.loads(r.data)["meta"]["total"], 1)
        score = json.loads(r.data)["data"][0]
        self.assertEqual(score["user_id"], 11)
        self.assertEqual(score["score"], 11)

    # **********  add_score_and_list  *********
    def test_add_and_list_basic(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.post("/api/add_score_and_list", data={
            "user_id": 11,
            "score": 25,
            "radius": 1,
        })

        scores = json.loads(r.data)["data"]
        s1, s2, s3 = scores[0], scores[1], scores[2]

        self.assertEqual(s1["user_id"], 1)
        self.assertEqual(s1["score"], 31)

        self.assertEqual(s2["user_id"], 11)
        self.assertEqual(s2["score"], 25)

        self.assertEqual(s3["user_id"], 21)
        self.assertEqual(s3["score"], 22)

    def test_add_and_list_no_user_id(self):
        r = self.client.post("/api/add_score_and_list", data={
            "score": 11,
            "radius": 1,
        })
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_no_score(self):
        r = self.client.post("/api/add_score_and_list", data={
            "user_id": 11,
            "radius": 1,
        })
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_no_radius(self):
        r = self.client.post("/api/add_score_and_list", data={
            "user_id": 11,
            "score": 11,
        })
        self.assertEqual(r.status_code, 400)

    def test_add_and_list_ascending(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.post("/api/add_score_and_list", data={
            "user_id": 11,
            "score": 25,
            "radius": 1,
            "sort": "ascending",
        })

        scores = json.loads(r.data)["data"]
        s1, s2, s3 = scores[0], scores[1], scores[2]

        self.assertEqual(s1["user_id"], 21)
        self.assertEqual(s1["score"], 22)

        self.assertEqual(s2["user_id"], 11)
        self.assertEqual(s2["score"], 25)

        self.assertEqual(s3["user_id"], 1)
        self.assertEqual(s3["score"], 31)

    def test_add_and_list_tag_filter(self):
        DB.session.add_all(self.starting_data)
        DB.session.commit()
        r = self.client.post("/api/add_score_and_list", data={
            "user_id": 11,
            "score": 37,
            "radius": 1,
            "filter_tag": "level1",
        })
        Score(created_at=datetime(2015, 4, 22), user_id=3, score=33, tag="level1"),
        Score(created_at=datetime(2015, 4, 22), user_id=4, score=44, tag="level1"),

        scores = json.loads(r.data)["data"]
        s1, s2, s3 = scores[0], scores[1], scores[2]

        self.assertEqual(s1["user_id"], 4)
        self.assertEqual(s1["score"], 44)

        self.assertEqual(s2["user_id"], 11)
        self.assertEqual(s2["score"], 37)

        self.assertEqual(s3["user_id"], 3)
        self.assertEqual(s3["score"], 33)

    # TODO: with every test that doesn't error, verify the json schema is full
