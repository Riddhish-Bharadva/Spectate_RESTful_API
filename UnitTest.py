from index import app
import unittest

class TestApp(unittest.TestCase):
    # Below test is checking if we are getting response on API call.
    def test1(self):
        response = app.test_client(self).get("/api/match/")
        self.assertEqual(response.status_code,200)

    # Below test is checking if we are getting back response in application/json format or not.
    def test2(self):
        response = app.test_client(self).get("/api/match/")
        self.assertEqual(response.content_type,"application/json")

    # Below test is checking if we are getting response in case we search by id.
    def test3(self):
        response = app.test_client(self).get("/api/match/123")
        self.assertTrue(b'id' in response.data)

    # Below test is checking if we are getting response in case we search data by sport and order.
    def test4(self):
        response = app.test_client(self).get("/api/match/?sport=football&ordering=start_time")
        self.assertTrue(b'Data by Sport and Order' in response.data)

    # Below test is checking if we are getting response in case we search data by match.
    def test5(self):
        response = app.test_client(self).get("/api/match/?name=Real%20Madrid%20vs%20Barcelona")
        self.assertTrue(b'Data by Match' in response.data)

    # Below test is checking if we request for get, we must not be allowed and must also returning 405 response.
    def test6(self):
        response = app.test_client(self).get("/api/createOrUpdate")
        self.assertEqual(response.status_code,405)

    # Below test is checking if we get proper response on POST for adding a new event which must return 200 as response.
    def test7(self):
        JSON_Data = {"id":"123","message_type":"NewEvent"}
        response = app.test_client(self).post("/api/createOrUpdate", json=JSON_Data)
        self.assertEqual(response.status_code,200)
        self.assertTrue(b'message' in response.data)

    # Below test is checking if we get proper response on PUT for adding a new event which must return 200 as response.
    def test8(self):
        JSON_Data = {"id":"123","message_type":"NewEvent"}
        response = app.test_client(self).put("/api/createOrUpdate", json=JSON_Data)
        self.assertEqual(response.status_code,200)
        self.assertTrue(b'message' in response.data)

    # Below test is checking if we get proper response on POST for correct message_type to be added a new event.
    def test9(self):
        JSON_Data = {"id": "123","message_type": "NewEvent","event": {"id": "456","name": "Mumbai vs Delhi","startTime": "2020-11-25 10:30:20","sport": {"id": "1","name": "Cricket"},"markets": [{"id": "789","name": "Winner","selections":[{"id": "101112","name": "Mumbai","odds": "11"},{"id": "131415","name": "Delhi","odds": "11"}]}]}}
        response = app.test_client(self).post("/api/createOrUpdate", json=JSON_Data)
        if b'added successfully' in response.data:
            self.assertTrue(b'added successfully' in response.data)
        elif b'Duplicate record' in response.data:
            self.assertTrue(b'Duplicate record' in response.data)
        else:
            self.assertTrue(b'Please try again' in response.data)

    # Below test is checking if we get proper response on PUT for correct message_type to be added a new event.
    def test10(self):
        JSON_Data = {"id": "123","message_type": "NewEvent","event": {"id": "456","name": "Mumbai vs Delhi","startTime": "2020-11-25 10:30:20","sport": {"id": "1","name": "Cricket"},"markets": [{"id": "789","name": "Winner","selections":[{"id": "101112","name": "Mumbai","odds": "11"},{"id": "131415","name": "Delhi","odds": "11"}]}]}}
        response = app.test_client(self).put("/api/createOrUpdate", json=JSON_Data)
        if b'added successfully' in response.data:
            self.assertTrue(b'added successfully' in response.data)
        elif b'Duplicate record' in response.data:
            self.assertTrue(b'Duplicate record' in response.data)
        else:
            self.assertTrue(b'Please try again' in response.data)

    # Below test is checking if we get proper response on POST for updating odds which must return 200 as response.
    def test11(self):
        JSON_Data = {"id":"123","message_type":"UpdateOdds"}
        response = app.test_client(self).post("/api/createOrUpdate", json=JSON_Data)
        self.assertEqual(response.status_code,200)

    # Below test is checking if we get proper response on PUT for updating odds which must return 200 as response.
    def test12(self):
        JSON_Data = {"id":"123","message_type":"UpdateOdds"}
        response = app.test_client(self).put("/api/createOrUpdate", json=JSON_Data)
        self.assertEqual(response.status_code,200)

    # Below test is checking if we get proper response on POST for correct message_type to be updated.
    def test13(self):
        JSON_Data = {"id": "123","message_type": "UpdateOdds","event": {"id": "456","name": "Mumbai vs Delhi","startTime": "2020-11-25 10:30:20","sport": {"id": "1","name": "Cricket"},"markets": [{"id": "789","name": "Winner","selections":[{"id": "101112","name": "Mumbai","odds": "11"},{"id": "131415","name": "Delhi","odds": "11"}]}]}}
        response = app.test_client(self).post("/api/createOrUpdate", json=JSON_Data)
        if b'updated successfully' in response.data:
            self.assertTrue(b'updated successfully' in response.data)
        else:
            self.assertTrue(b'Please try again' in response.data)

    # Below test is checking if we get proper response on PUT for correct message_type to be updated.
    def test14(self):
        JSON_Data = {"id": "123","message_type": "UpdateOdds","event": {"id": "456","name": "Mumbai vs Delhi","startTime": "2020-11-25 10:30:20","sport": {"id": "1","name": "Cricket"},"markets": [{"id": "789","name": "Winner","selections":[{"id": "101112","name": "Mumbai","odds": "11"},{"id": "131415","name": "Delhi","odds": "11"}]}]}}
        response = app.test_client(self).put("/api/createOrUpdate", json=JSON_Data)
        if b'updated successfully' in response.data:
            self.assertTrue(b'updated successfully' in response.data)
        else:
            self.assertTrue(b'Please try again' in response.data)

    # Below test is checking if we get proper response on POST for any other message_type.
    def test15(self):
        JSON_Data = {"id":"123","message_type":"abc"}
        response = app.test_client(self).post("/api/createOrUpdate", json=JSON_Data)
        self.assertTrue(b'Un-identified message_type' in response.data)

    # Below test is checking if we get proper response on PUT for any other message_type.
    def test16(self):
        JSON_Data = {"id":"123","message_type":"abc"}
        response = app.test_client(self).put("/api/createOrUpdate", json=JSON_Data)
        self.assertTrue(b'Un-identified message_type' in response.data)

if __name__ == "__main__":
    unittest.main()
