import unittest
import socket
import json
from unittest import result
from Error import Error
from InterfaceOnboardSystems import ClientClosedConnectionError, InterfaceOnboardSystems

class OnBoardInterfaceTester(unittest.TestCase):
    """
        Setup method to start the server and create an interface.
    """
    def setUp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("192.168.178.68", 8001))
        self.server.listen()

        self.test_interface = InterfaceOnboardSystems("")

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
        incorrect_field_message = json.dumps({"afakj": 0})
        expected_result = Error.INCORRECT_FIELD
        result = self.test_interface.extract_request(incorrect_field_message)
        self.assertEqual(result, expected_result)

    def test_interface_interpret_message(self):
        self.test_interface.choose_request()

