import grpc
from backend.transactionService.grpc_protos import transaction_pb2, transaction_pb2_grpc

def process_transaction(wallet_id):
    with grpc.insecure_channel('localhost:50033') as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        request = transaction_pb2.TransactionRequest(wallet_id=wallet_id)
        response = stub.ProcessTransaction(request)
        return response.message

