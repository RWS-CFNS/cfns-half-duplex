import unittest
import socket
import json
from unittest.case import expectedFailure
from Category import Category
from Error import Error
from File import File
from InterfaceOnboardSystems import ClientClosedConnectionError, InterfaceOnboardSystems
from Request import CategoryRequest, LatestRequest, TestRequest
from Folder import Folder

class OnBoardInterfaceTester(unittest.TestCase):
    """
        Setup method to start the server and create an interface.
    """
    def setUp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("192.168.178.68", 8001))
        self.server.listen()

        test_folder = Folder("")
        self.test_interface = InterfaceOnboardSystems(test_folder)

    """
        Method to propely close the program without having sockets still open.
    """
    def tearDown(self):
        self.server.close()

    """
        The client will send a msg_length followed by a message. This asserts true when the received message matches the expected result.
        The client will send the expected result.
    """
    def test_interface_receive(self):
        conn, _ = self.server.accept()

        expected_result = json.dumps({"test": True})
        result = self.test_interface.receive_message(conn)
        self.assertEqual(result, expected_result)
        conn.close()

    """
        The client will close the conn before sending this test checks if the interface will detect that and raises an error.
    """
    def test_interface_failed_receive(self):
        conn, _ = self.server.accept()

        with self.assertRaises(ClientClosedConnectionError):
            _ = self.test_interface.receive_message(conn)
        conn.close()

    """
        This test checks if the interface can validate input true when send correctly and validate false when send incorrectly.
    """
    def test_interface_validate_input(self):
        # Tests if the interface can validate the input true when a message is a dict and send in json format.
        correct_message = json.dumps({"test": True})
        expected_result = json.loads(correct_message)
        result = self.test_interface.extract_request(correct_message)
        self.assertEqual(result, expected_result)

        # Tests if the interface can validate the input false and return an Error when the message is not send in json format.
        no_json_message = "wrong no json"
        expected_result = Error.INCORRECT_JSON_DECODER
        result = self.test_interface.extract_request(no_json_message)
        self.assertEqual(result, expected_result)

        # Tests if the interface can validate the input false and return an Error when the message is not a dict.
        no_dict_message = json.dumps(["no", "dict"])
        expected_result = Error.NO_DICT
        result = self.test_interface.extract_request(no_dict_message)
        self.assertEqual(result, expected_result)

        # Tests if the interface can validate the input false and return an Error when the message does not contain the required keys in the send dict.
        incorrect_field_message = json.dumps({"random": 0})
        expected_result = Error.INCORRECT_FIELD
        result = self.test_interface.extract_request(incorrect_field_message)
        self.assertEqual(result, expected_result)

    def test_interface_interpret_message(self):
        # This test checks when you pass in a dict as choose_request expects with a valid request_type it will return the request object asked for.
        correct_input = {"request_type": "test"}
        expected_result = TestRequest
        result = self.test_interface.choose_request(**correct_input)
        self.assertTrue(isinstance(result, expected_result))
        
        # This checks if the method will return an Error when the request_type is not known.
        incorrect_input = {"request_type": False}
        expected_result = Error.UNKOWN_REQUEST_TYPE
        result = self.test_interface.choose_request(**incorrect_input)
        self.assertEqual(result, expected_result)

        # This test does the same thing as the test above but also tests if it will ignore unknown keywords.
        incorrect_input = {"request_type": False, "unused random keyword": 0}
        expected_result = Error.UNKOWN_REQUEST_TYPE
        result = self.test_interface.choose_request(**incorrect_input)
        self.assertEqual(result, expected_result)

    def test_parse(self):
        test_file = File("")
        test_file.lines = [90,1,"other"]
        self.test_interface.folder.files = [test_file]

        expected_result = [(test_file.lines[0], test_file.lines[1:])]
        result = LatestRequest(self.test_interface.folder).parse()
        self.assertEqual(result, expected_result)

        # expected restult is the same as above
        result = CategoryRequest(self.test_interface.folder).parse()
        self.assertEqual(result, expected_result)

        expected_result = [[1, 4, "other", [1.1234, 5.6789]]]
        result = TestRequest(self.test_interface.folder).parse()
        self.assertEqual(result, expected_result)

    def test_build_response(self):
        test_information = [1,2,3,4]

        # Tests if build_response returns the expected json string
        expected_result = json.dumps({"reply": True, "information": test_information})
        result = LatestRequest(self.test_interface.folder).build_response(test_information)
        self.assertEqual(result, expected_result)

        # expected_result is the same as above, so not redefined.
        result = TestRequest(self.test_interface.folder).build_response(test_information)
        self.assertEqual(result, expected_result)

        # Tests if the buid_response returns a json string in the format defined in expected_result.
        category = Category.OTHER
        expected_result = json.dumps({"reply": True, "category": category.value, "information": test_information})
        result = CategoryRequest(self.test_interface.folder, category).build_response(test_information)
        self.assertEqual(result, expected_result)

    def test_reply(self):
        conn, _ = self.server.accept()

        test_response = "test_response"
        self.test_interface.send_response(conn, test_response)

        # To get an accurate test result test receive message before this test.
        result = self.test_interface.receive_message(conn)
        self.assertEqual(result, test_response)

        # It does not matter which Error value is used here. NO_DICT is just an example.
        test_error_response = Error.NO_DICT
        self.test_interface.send_error(conn, test_error_response)

        # To get an accurate test result test receive message before this test.
        expected_result = json.dumps({"reply": False, "error_message": test_error_response.value})
        result = self.test_interface.receive_message(conn)
        self.assertEqual(result, expected_result)

        conn.close()

    def test_onboard_interface(self):
        
        
        conn, _ = self.server.accept()

        self.test_interface.handle_client(conn)

        conn.close()

        
