import socket
import threading
import json
from Error import Error
from Request import CategoryRequest, LatestRequest, TestRequest
from Interface.Ethernet import pad_msg_length

class ClientClosedConnectionError(Exception):
    """This error is raised when the client closes the connection without the disconnect message."""

class InterfaceOnboardSystems(threading.Thread):
    def __init__(self, folder, max_msg_length = 10) -> None:
        threading.Thread.__init__(self)
        self.folder = folder
        self.max_msg_length = max_msg_length
    
    def receive_message(self, conn):
        # Receive the length of the request
        message_length = conn.recv(self.max_msg_length).decode()
        
        # Check if they closed the connection the wrong way. If so raise an custom error
        if len(message_length) == 0:
            raise (ClientClosedConnectionError)

        # Now you know that they sent a message and not an conn.close(), so convert the message_length to an int.
        message_length = int(message_length)
        message = conn.recv(message_length).decode()

        return message

    def extract_request(self, message):
        try:
            request = json.loads(message)
        except json.JSONDecodeError:
            return Error.INCORRECT_JSON_DECODER
        
        # Check if the request is a dict, because the interface works with the request as a dict.
        if not isinstance(request, dict): 
            return Error.NO_DICT

        required_key = "request_type"
        request_keys = request.keys()

        """
            This checks if the request contains request_type. If not return an Error.
            When request_type is by_category it checks if the request also contains the key category. When that key is not available it will return an Error. 
            When valid is in the request and the type is not a bool return an Error otherwise return the request 
            If there is a request_type present and it is not by_category return the request.
        """
        if required_key in request_keys:
            if request[required_key] == "by_category" and not "category" in request_keys:
                return Error.INCORRECT_FORMAT
            elif "valid" in request_keys and not type(request["valid"]) == bool:
                return Error.INCORRECT_FORMAT
            else: 
                return request
        else:
            return Error.INCORRECT_FORMAT
      
    
    def send_error(self, conn, error):
        error_message = json.dumps({"reply": False, "error_message": error.value})

        self.send_response(conn, error_message)
    
    def send_response(self, conn, response):
        response_length = pad_msg_length(self.max_msg_length, len(response))

        conn.send(response_length)
        conn.send(response.encode())

    def choose_request(self, request_type, category = [], valid = True, **kwargs):
        if request_type == "latest":
            return LatestRequest(self.folder, valid)
        elif request_type == "by_category":
            return CategoryRequest(self.folder, category, valid)
        elif request_type == "test":
            return TestRequest(self.folder)
        else:
            return Error.UNKOWN_REQUEST_TYPE

    def handle_client(self, conn):
        try:
            message = self.receive_message(conn)
            print("[Client handler] received message properly!")
        except ClientClosedConnectionError:
            print("[Client handler] client closed connection before sending the complete message")
            conn.close()
            return
        
        # Validates the request. If the request would be invalid it could cause the interface to crash.
        dict_request = self.extract_request(message)

        if isinstance(dict_request, Error):
            print("[Client handler] sent message invalid")

            # Send an error message as reply
            self.send_error(conn, dict_request)
            conn.close()
            return
        print("[Client handler] message is validated properly")

        request = self.choose_request(**dict_request)

        if isinstance(request, Error):
            print("[Client handler] request_type not found!")

            # Send an error message as reply
            self.send_error(conn, request)
            conn.close()
            return
        print("[Client handler] found request_type")
        
        information = request.parse()
        response = request.build_response(information)
        
        print("[Client handler] request parsed")
        self.send_response(conn, response)
        print("[Client handler] response sent")
        print("[Client handler] closing connection ... ")
        conn.close()
        print("[Client handler] connection closed")
        print()

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("192.168.178.68", 8001))
        server.listen()

        while True:
            conn, _ = server.accept()
            print("[Server] accepted a connection")

            print("[Server] starting client handler")
            client_thread = threading.Thread(target=self.handle_client, args=[conn])
            client_thread.start()
