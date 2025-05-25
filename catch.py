class User:
    def __init__(self, system):
        self.system = system
        self.username = None  # 로그인 후 저장할 사용자 정보

    def login(self):
        # 이미 로그인된 경우 로그인 과정을 생략
        if self.username and self.system.is_logged_in(self.username):
            print(f"{self.username}님, 이미 로그인되어 있습니다.")
        else:
            self.username = self.system.authenticate()
            print(f"{self.username} 로그인 성공" if self.username else "로그인 실패")

    def request_service(self, request_type):
        if not self.system.is_logged_in(self.username):
            return "로그인 필요"

        if request_type == "search":
            query = input("검색할 레스토랑 이름을 입력하세요: ")
            result = self.system.process_request(self.username, "search", query)
            print(result)
        elif request_type == "reservation":
            restaurant_name = input("예약할 레스토랑 이름을 입력하세요: ")
            reservation_date = input("예약할 날짜를 입력하세요 (YYYY-MM-DD): ")
            result = self.system.process_request(self.username, "reservation", (restaurant_name, reservation_date))
            print(result)
        elif request_type == "cancel":
            cancel_name = input("취소할 예약 레스토랑 이름을 입력하세요: ")
            cancel_date = input("취소할 예약 날짜를 입력하세요 (YYYY-MM-DD): ")
            result = self.system.process_request(self.username, "cancel", (cancel_name, cancel_date))
            print(result)
        elif request_type == "check_reservation":
            check_date = input("확인할 예약 날짜를 입력하세요 (YYYY-MM-DD): ")
            result = self.system.process_request(self.username, "check_reservation", check_date)
            print(result)
        elif request_type == "notification":
            response = input("푸시 알림을 설정하시겠습니까? (예/아니요): ").strip().lower()
            if response == "예":
                result = self.system.process_request(self.username, "notification", None)
                print(result)
            else:
                print("알림 설정을 건너뜁니다.")

    def logout(self):
        response = input("로그아웃하시겠습니까? (예/아니요): ").strip().lower()
        if response == "예":
            print(self.system.logout(self.username))
            self.username = None  # 로그아웃 시 사용자 정보 제거
        elif response == "아니요":
            print("초기 화면으로 돌아갑니다.")
            self.run()  # 처음부터 다시 실행

    def run(self):
        self.login()  # 로그인 과정 실행 (이미 로그인된 경우 생략)
        self.request_service("search")
        self.request_service("reservation")
        self.request_service("check_reservation")
        self.request_service("notification")
        self.request_service("cancel")
        self.logout()


class CatchTable:
    def __init__(self):
        self.user_credentials = {
            "user1": "password123",
            "user2": "securepass",
            "admin": "adminpass"
        }
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

        if request_type == "search":
            return self.restaurant_system.search(data)
        elif request_type == "reservation":
            return self.restaurant_system.reserve(username, *data)
        elif request_type == "cancel":
            return self.restaurant_system.cancel_reservation(username, *data)
        elif request_type == "check_reservation":
            return self.restaurant_system.check_reservation(username, data)
        elif request_type == "notification":
            return "푸시 알림 설정 완료"

    def logout(self, username):
        if username in self.logged_in_users:
            self.logged_in_users.remove(username)
            return f"{username} 로그아웃 완료"
        return "로그아웃 실패"


class Restaurant:
    def __init__(self):
        self.restaurants = {
            "맛있는 식당": {"location": "서울 강남구", "menu": ["스테이크", "파스타"], "reservations": {}},
            "고급 레스토랑": {"location": "서울 종로구", "menu": ["랍스터", "와인"], "reservations": {}},
            "가성비 좋은 식당": {"location": "서울 신촌", "menu": ["볶음밥", "라면"], "reservations": {}}
        }

    def search(self, query):
        result = [f"이름: {name}, 위치: {data['location']}, 메뉴: {', '.join(data['menu'])}"
                  for name, data in self.restaurants.items() if query in name]
        return result if result else "검색 결과 없음"

    def reserve(self, username, restaurant_name, date):
        if restaurant_name in self.restaurants:
            if date not in self.restaurants[restaurant_name]["reservations"]:
                self.restaurants[restaurant_name]["reservations"][date] = username
                return f"{restaurant_name} {date} 예약 성공"
            return f"{restaurant_name} {date}은 이미 예약됨"
        return "레스토랑을 찾을 수 없음"

    def cancel_reservation(self, username, restaurant_name, date):
        if restaurant_name in self.restaurants:
            if self.restaurants[restaurant_name]["reservations"].get(date) == username:
                del self.restaurants[restaurant_name]["reservations"][date]
                return f"{restaurant_name} {date} 예약 취소 완료"
            return f"{restaurant_name} {date}은 예약되지 않았거나 다른 사용자가 예약함"
        return "레스토랑을 찾을 수 없음"

    def check_reservation(self, username, date):
        reservations = [f"{name} - {date}" for name, data in self.restaurants.items()
                        if data["reservations"].get(date) == username]
        return reservations if reservations else "예약된 레스토랑이 없습니다."


# 실행 부분 (프로그램 시작 역할만 담당)
def main():
    system = CatchTable()
    user = User(system)

    user.run()


if __name__ == "__main__":
    main()
