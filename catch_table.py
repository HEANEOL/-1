from restaurant import Restaurant

class CatchTable:
    def __init__(self):
        self.user_credentials = {"user1": "password123", "user2": "securepass", "admin": "adminpass"}
        self.logged_in_users = set()
        self.restaurant_system = Restaurant()

    def authenticate(self):
        username = input("사용자 아이디를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        if username in self.user_credentials and self.user_credentials[username] == password:
            self.logged_in_users.add(username)
            return username
        return None

    def is_logged_in(self, username):
        return username in self.logged_in_users

    def process_request(self, username, request_type, data):
        if not self.is_logged_in(username):
            return "로그인 필요"

        requests = {
            "search": lambda: self.restaurant_system.search(data),
            "reservation": lambda: self.restaurant_system.reserve(username, *data),
            "cancel": lambda: self.restaurant_system.cancel_reservation(username, *data),
            "check_reservation": lambda: self.restaurant_system.check_reservation(username, data),
            "notification": lambda: "푸시 알림 설정 완료"
        }

        return requests.get(request_type, lambda: "잘못된 요청")()

    def logout(self, username):
        if username in self.logged_in_users:
            self.logged_in_users.remove(username)
            return f"{username} 로그아웃 완료"
        return "로그아웃 실패"
