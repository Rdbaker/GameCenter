from mock import patch

from gamecenter.api import views
from gamecenter.api.models import Score
from gamecenter.core.utils_test import BaseTestCase
from gamecenter.core.models import DB


class APIViewsTest(BaseTestCase):
    def setUp(self):
        app = self.create_app()
        self.client = app.test_client()
        DB.create_all()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()

    @patch("gamecenter.api.views.scores_from_query")
    def test_list_of_user_scores(self, sfq):
        """It should filter in the user_id attribute"""
        score1 = Score(user_id=1, score=20)
        score2 = Score(user_id=2, score=21)
        DB.session.add_all([score1, score2])
        DB.session.commit()

        views.list_of_user_scores(1)

        sfq.assert_called_with([score1])
