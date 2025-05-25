from restaurant import Restaurant

class CatchTable:
    def __init__(self):
        self.user_credentials = {"user1": "password123", "user2": "securepass", "admin": "adminpass"}
        self.logged_in_users = set()
        self.restaurants = []  # 여러 개의 독립적인 Restaurant 인스턴스를 리스트로 관리

        # 샘플 레스토랑 추가
        self.add_sample_restaurants()

    def add_sample_restaurants(self):
        """초기 샘플 레스토랑을 추가"""
        sample_data = [
            ("맛있는 식당", "서울 강남구", "스테이크, 파스타"),
            ("고급 레스토랑", "서울 종로구", "랍스터, 와인"),
            ("가성비 좋은 식당", "서울 신촌", "볶음밥, 라면"),
        ]
        for name, location, menu in sample_data:
            self.restaurants.append(Restaurant(name, location, menu.split(","), 운영중=True))

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
        """특정 레스토랑을 검색"""
        return [restaurant.get_info() for restaurant in self.restaurants if query in restaurant.name] or "검색 결과 없음"

    def reserve(self, username, restaurant_name, date):
        """레스토랑에 예약 요청"""
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                return restaurant.reserve(username, date)
        return "레스토랑을 찾을 수 없음"

    def cancel_reservation(self, username, restaurant_name, date):
        """예약 취소 요청"""
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                return restaurant.cancel_reservation(username, date)
        return "레스토랑을 찾을 수 없음"

    def check_reservation(self, username, date):
        """사용자의 예약 확인"""
        return [restaurant.name for restaurant in self.restaurants if restaurant.has_reservation(username, date)] or "예약된 레스토랑이 없습니다."

    def add_restaurant(self, name, location, menu):
        """새로운 레스토랑 추가"""
        new_restaurant = Restaurant(name, location, menu.split(","), 운영중=True)
        self.restaurants.append(new_restaurant)
        return f"{name} 레스토랑이 시스템에 등록되었습니다."

    def remove_restaurant(self, name):
        """레스토랑 삭제"""
        for restaurant in self.restaurants:
            if restaurant.name == name:
                self.restaurants.remove(restaurant)
                return f"{name} 레스토랑 삭제 완료"
        return "레스토랑을 찾을 수 없음"

    def list_restaurants(self):
        """현재 등록된 레스토랑 목록 조회"""
        return [restaurant.get_info() for restaurant in self.restaurants] or "등록된 레스토랑이 없습니다."

    def toggle_restaurant_status(self, name):
        """레스토랑 운영 상태 변경"""
        for restaurant in self.restaurants:
            if restaurant.name == name:
                restaurant.toggle_status()
                return f"{name}의 운영 상태 변경 완료"
        return "레스토랑을 찾을 수 없음"
