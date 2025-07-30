import grpc
from concurrent import futures
from backend.transactionService.grpc_protos import transaction_pb2_grpc
from backend.transactionService.grpc_server.transactionServiceimpl import TransactionService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_pb2_grpc.add_TransactionServiceServicer_to_Server(TransactionService(), server)
    server.add_insecure_port('[::]:50053')
    print("Transaction server running on port 50053")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    