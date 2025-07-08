import grpc
from userService.models.user import User
from grpc_protos import user_pb2, user_pb2_grpc
from backend.engine.db_storage import get_db_connection

class UserService(user_pb2_grpc.UserServiceServicer):
    def getUser(self, request, context):
        email = request.email

        try:
            user = User.find_user_by_email(email)

            if not user:
                context.set_details("User not found")
                context.set_code(5)
                return user_pb2.UserResponse()
            
            return user_pb2.UserResponse(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
        
        except grpc.RpcError as e:
            context.set_details(str(e))
            context.set_code(13)
            return user_pb2.UserResponse()