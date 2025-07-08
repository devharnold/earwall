import grpc
from transactionService.models.transaction import Transaction
from grpc_protos import transaction_pb2, transaction_pb2_grpc
from backend.engine.db_storage import get_db_connection

class TransactionService(transaction_pb2_grpc.TransactionServiceServicer):
    def get_transaction(self, request, context):
        transaction_id = request.transaction_id

        try:
            transaction = Transaction.fetch_transaction_data()

            if not transaction:
                context.set_details("Transaction not found")
                context.set_code(5)
                return transaction_pb2.TransactionResponse()
            
            return transaction_pb2.TransactionResponse(
                transaction_id=transaction.transaction_id,
                sender_email=transaction.sender_email,
                receiver_email=transaction.receiver_email,
                amount=transaction.amount
            )
        
        except grpc.RpcError as e:
            context.set_details(str(e))
            context.set_code(13)
            return transaction_pb2.TransactionResponse()