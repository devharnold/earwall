from walletService.models.wallet import Wallet
from grpc_protos import wallet_pb2, wallet_pb2_grpc
from backend.engine.db_storage import get_db_connection

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
        except Exception as e:
            context.set_details(str(e))
            context.set_code(13)
            context.wallet_pb2.WalletResponse()