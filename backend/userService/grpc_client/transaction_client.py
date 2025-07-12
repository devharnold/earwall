import grpc
from backend.transactionService import transaction_pb2, transaction_pb2_grpc

def get_transaction_history(user_id):
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = transaction_pb2.TransactionServiceStub(channel)
        request = transaction_pb2.TransactionRequest(user_id=user_id)
        response = stub.GetTransactionHistory(request)
        return response.history
    