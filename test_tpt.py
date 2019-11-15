from unittest import TestCase

from tpt_utils import Tpt



class TestTpt(TestCase):
    def setUp(self):
        self.tpt = Tpt('some_user', 'some_password', 'some_host')



class TestTpt(TestTpt):
    def test_teradata_to_file(self):
        query = """
                    SELECT * FROM DBC.DBCInfoV
                """
        assert self.test_teradata_to_file(query, 'out.txt') == 0
