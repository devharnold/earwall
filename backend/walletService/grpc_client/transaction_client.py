import grpc
from grpc_client import transaction_pb2, transaction_pb2_grpc

def get_transactions(wallet_id):
    with grpc.insecure_channel('loacalhost:50053') as channel:
        stub = transaction_pb2_grpc.TransactionServiceStub(channel)
        request = transaction_pb2.TransactionRequest(wallet_id=wallet_id)
        response = stub.GetTransaction(request)
        return response.balance