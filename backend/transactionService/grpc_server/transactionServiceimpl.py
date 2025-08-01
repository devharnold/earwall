import grpc
from backend.transactionService.models.transaction import Transaction
from backend.transactionService.grpc_protos import transaction_pb2, transaction_pb2_grpc
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
        
    
    def make__transaction(self, request, context):
        transaction_id = request.transaction_id

        try:
            transaction = Transaction.process_p2p_transaction()

            if not transaction:
                context.set_details("Cannot process transaction")
                context.set_code()
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
        
    def get_transaction_history(self, request, context):
        transaction_id = request.transaction_id

        try:
            transaction = Transaction.fetch_transation_history()

            if not transaction:
                context.set_details("")
                context.set_code()
                return transaction_pb2.TransactionResponse()
            
            return transaction_pb2.TransactionResponse(
                transaction_id=transaction.transaction_id,
                sender_email=transaction.sender_email,
                receiver_email=transaction.receiver_email,
                from_currency=transaction.from_currency,
                to_currency=transaction.to_currency,
                amount=transaction.amount
            )
        
        except grpc.RpcError as e:
            context.set_details(str(e))
            context.set_code(13)
            return transaction_pb2.TransactionResponse()