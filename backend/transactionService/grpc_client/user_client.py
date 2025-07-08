import grpc
from userService.grpc_protos import user_pb2_grpc, user_pb2

def get_authenticate_user(user_id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.UserRequest(user_id=user_id)
        response = stub.GetUserAuthDetails(request)
        return response.details
    
