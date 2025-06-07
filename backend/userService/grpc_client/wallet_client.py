import grpc
from grpc_client import wallet_pb2, wallet_pb2_grpc

def get_wallet_balance(user_id):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = wallet_pb2_grpc.WalletServiceStub(channel)
        request = wallet_pb2.WalletRequest(user_id=user_id)
        response = stub.GetWalletBalance(request)
        return response.balance
