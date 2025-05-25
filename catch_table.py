from restaurant import Restaurant

class CatchTable:
    def __init__(self):
        self.user_credentials = {"user1": "password123", "user2": "securepass", "admin": "adminpass"}
        self.logged_in_users = set()
        self.restaurants = {  # 레스토랑 리스트만 관리
            "맛있는 식당": Restaurant("맛있는 식당", "서울 강남구", ["스테이크", "파스타"], 운영중=True),
            "고급 레스토랑": Restaurant("고급 레스토랑", "서울 종로구", ["랍스터", "와인"], 운영중=True),
            "가성비 좋은 식당": Restaurant("가성비 좋은 식당", "서울 신촌", ["볶음밥", "라면"], 운영중=False)
        }

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
            "search": lambda: self.search_restaurant(data),
            "reservation": lambda: self.reserve(username, *data),
            "cancel": lambda: self.cancel_reservation(username, *data),
            "check_reservation": lambda: self.check_reservation(username, data),
            "notification": lambda: "푸시 알림 설정 완료",
            "add_restaurant": lambda: self.add_restaurant(*data),
            "remove_restaurant": lambda: self.remove_restaurant(data),
            "list_restaurants": lambda: self.list_restaurants(),
            "toggle_status": lambda: self.toggle_restaurant_status(data),
        }

        return requests.get(request_type, lambda: "잘못된 요청")()

    def search_restaurant(self, query):
        return [restaurant.get_info() for name, restaurant in self.restaurants.items() if query in name] or "검색 결과 없음"

    def reserve(self, username, restaurant_name, date):
        if restaurant_name in self.restaurants:
            return self.restaurants[restaurant_name].reserve(username, date)
        return "레스토랑을 찾을 수 없음"

    def cancel_reservation(self, username, restaurant_name, date):
        if restaurant_name in self.restaurants:
            return self.restaurants[restaurant_name].cancel_reservation(username, date)
        return "레스토랑을 찾을 수 없음"

    def check_reservation(self, username, date):
        return [f"{name} - {date}" for name, restaurant in self.restaurants.items() if restaurant.has_reservation(username, date)] or "예약된 레스토랑이 없습니다."

    def add_restaurant(self, name, location, menu):
        if name in self.restaurants:
            return f"{name}은 이미 존재하는 레스토랑입니다."
        self.restaurants[name] = Restaurant(name, location, menu.split(","), 운영중=True)
        return f"{name} 레스토랑 추가 완료"

    def remove_restaurant(self, name):
        if name in self.restaurants:
            del self.restaurants[name]
            return f"{name} 레스토랑 삭제 완료"
        return "레스토랑을 찾을 수 없음"

    def list_restaurants(self):
        return [restaurant.get_info() for restaurant in self.restaurants.values()] or "등록된 레스토랑이 없습니다."

    def toggle_restaurant_status(self, name):
        if name in self.restaurants:
            self.restaurants[name].toggle_status()
            return f"{name}의 운영 상태 변경 완료"
        return "레스토랑을 찾을 수 없음"
