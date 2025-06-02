from grpc_protos import user_pb2, user_pb2_grpc
from backend.engine.db_storage import get_db_connection

class UserService(user_pb2_grpc.UserServiceServicer):
    def getUser(self, request, context):
        user_id = request.user_id
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT *  FROM users WHERE user_id = %s", (user_id))
            row = cursor.fetchone()

            if not row:
                context.set_details("User not found")
                context.set_code(5)
                return user_pb2.UserResponse()
            
            return user_pb2.UserResponse(
                user_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3]
            )
        
        except Exception as e:
            context.set_details(str(e))
            context.set_code(13)
            return user_pb2.UserResponse()
        finally:
            cursor.close()
            connection.close()