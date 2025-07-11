import grpc
from walletService.grpc_protos import wallet_pb2, wallet_pb2_grpc

def get_wallet(wallet_id):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = wallet_pb2_grpc.WalletServiceStub(channel)
        request = wallet_pb2.WalletRequest(wallet_id=wallet_id)
        response = stub.GetWallet(request)
        return response.wallet_details
    
