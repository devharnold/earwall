import grpc
from walletService.grpc_protos import wallet_pb2, wallet_pb2_grpc
from walletService import Wall

def get_wallet(wallet_id):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = wallet_pb2_grpc.WalletServiceStub(channel)
        request = wallet_pb2.WalletRequest(wallet_id=wallet_id)
        response = stub.GetWallet(request)
        return response.wallet_details
    
def transfer_funds(sender_wallet, receiver_wallet, from_currency, to_currency, amount, transaction_id):
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = wallet_pb2_grpc.WalletServiceStub(channel)

        try:
            response = stub.TransferFunds(wallet_pb2.TransferRequest(
                from_wallet=sender_wallet,
                to_wallet=receiver_wallet,
                amount=amount,
                transaction_id=transaction_id
            ), timeout=3.0)

            if response.success:
                return { "transaction_id": transaction_id, "status": response.message }
            
        except grpc.RpcError as e:
            return { "transaction_id": transaction_id, "status": f"Wallet Service Error: {e.details()}"}