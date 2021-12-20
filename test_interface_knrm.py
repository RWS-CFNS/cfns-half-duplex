import unittest
import socket
import json
from unittest import result
from unittest.case import expectedFailure
from InterfaceOnboardSystems import ClientClosedConnectionError, InterfaceOnboardSystems

class OnBoardInterfaceTester(unittest.TestCase):
    def setUp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("192.168.178.21", 8001))
        self.server.listen()
        self.conn, _ = self.server.accept()
        self.test_interface = InterfaceOnboardSystems("")

    def tearDown(self):
        self.conn.close()
        self.server.close()

    def test_receive_message(self):
        expected_result = json.dumps({"test": True})
        result = self.test_interface.receive_message(self.conn)
        self.assertEqual(result, expected_result)
    
    def test_failed_receive_message(self):
        with self.assertRaises(ClientClosedConnectionError):
            _ = self.test_interface.receive_message(self.conn)
        
unittest.main()