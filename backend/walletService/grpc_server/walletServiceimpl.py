import grpc
from backend.walletService.models.wallet import Wallet
from backend.walletService.grpc_protos import wallet_pb2, wallet_pb2_grpc
from backend.engine.db_storage import DatabaseManager

class WalletService(wallet_pb2_grpc.WalletServiceServicer):
    def get_wallet_balance(self, request, context):
        wallet_id = request.wallet_id
        try:
            wallet = Wallet.fetch_wallet_balance(wallet_id)

            if not wallet:
                context.set_details("Wallet balance not found")
                context.set_code(5)
                return wallet_pb2.WalletResponse()
            
            return wallet_pb2.WalletResponse(
                wallet_id=wallet.id,
                balance=wallet.balance
            )
        except grpc.RPCError as e:
            context.set_details(str(e))
            context.set_code(13)
            context.wallet_pb2.WalletResponse()

    def transfer_funds(self, request, context):
        try:
            connection = DatabaseManager.get_db_connection()
            cursor = connection.cursor()

            # locking sender row
            cursor.execute("SELECT balance FROM wallets WHERE wallet_id = %s FOR UPDATE", (request.from_wallet,))
            sender_data = cursor.fetchone()

            if not sender_data or sender_data[0] < request.amount:
                return wallet_pb2.TransferResponse(success=False, message="Insufficient Funds")
            
            # locking reciever's row
            cursor.execute("SELECT balance FROM wallets WHERE wallet_id = %s FOR UPDATE", (request.to_wallet,))
            receiver_data = cursor.fetchone()

            if not receiver_data:
                return wallet_pb2.TransferResponse(success=False, message="Receiver wallet not found")
            
            cursor.execute("UPDATE wallets SET balance = balance - %s WHERE wallet_id = %s",
                           (request.amount, request.from_wallet))
            cursor.execute("UPDATE wallets SET balance = balance + %s WHERE wallet_id = %s",
                           (request.amount, request.to_wallet))
            
            return wallet_pb2.TransferResponse(success=True, message="Funds successfully transferred")
        except grpc.RpcError as e:
            return wallet_pb2.TransferResponse(success=False, message=str(e))