import grpc
from concurrent import futures
from backend.walletService.grpc_protos import wallet_pb2_grpc
from backend.walletService.grpc_server.walletServiceimpl import WalletService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wallet_pb2_grpc.add_WalletServiceServicer_to_Server(WalletService(), server)
    server.add_insecure_port('[::]:50052')
    print("Wallet service running on port 50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()