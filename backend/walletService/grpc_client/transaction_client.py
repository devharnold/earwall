import grpc
from transactionService.grpc_protos import transaction_pb2, transaction_pb2_grpc

def get_transactions(wallet_id):
    with grpc.insecure_channel('loacalhost:50053') as channel:
        stub = transaction_pb2_grpc.TransactionServiceStub(channel)
        request = transaction_pb2.TransactionRequest(wallet_id=wallet_id)
        response = stub.GetTransaction(request)
        return response.balance
    
def make_transaction(wallet_id):
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = transaction_pb2_grpc.TransactionServiceStub(channel)
        request = transaction_pb2.TranasactionRequest(wallet_id=wallet_id)
        response = stub.MakeTransaction(request)
        return response.balance
    
def get_transaction_history(wallet_id):
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = transaction_pb2_grpc.TransactionServiceStub(channel)
        request = transaction_pb2.TransactionRequest(wallet_id=wallet_id)
        response = stub.GetHistory(request)
        return response.