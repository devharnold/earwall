import grpc
from concurrent import futures
from backend.userService.grpc_protos import user_pb2_grpc
from backend.userService.grpc_server.userServiceimpl import UserService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_Server(UserService(), server)
    server.add_insercure_port('[::]:50051')
    print("User service running on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()