from catch_table import CatchTable

class User:
    def __init__(self, system):
        self.system = system
        self.username = None  # 로그인 후 저장할 사용자 정보

    def login(self):
        if self.username and self.system.is_logged_in(self.username):
            print(f"{self.username}님, 이미 로그인되어 있습니다.")
        else:
            self.username = self.system.authenticate()
            print(f"{self.username} 로그인 성공" if self.username else "로그인 실패")

    def request_service(self, request_type):
        if not self.system.is_logged_in(self.username):
            return "로그인 필요"

        actions = {
            "search": lambda: self.system.process_request(self.username, "search", input("검색할 레스토랑 이름을 입력하세요: ")),
            "reservation": lambda: self.system.process_request(self.username, "reservation", 
                            (input("예약할 레스토랑 이름을 입력하세요: "), input("예약할 날짜를 입력하세요 (YYYY-MM-DD): "))),
            "cancel": lambda: self.system.process_request(self.username, "cancel", 
                       (input("취소할 예약 레스토랑 이름을 입력하세요: "), input("취소할 예약 날짜를 입력하세요 (YYYY-MM-DD): "))),
            "check_reservation": lambda: self.system.process_request(self.username, "check_reservation", input("확인할 예약 날짜를 입력하세요 (YYYY-MM-DD): ")),
            "notification": lambda: "푸시 알림 설정 완료" if input("푸시 알림을 설정하시겠습니까? (예/아니요): ").strip().lower() == "예" else "알림 설정을 건너뜁니다.",
            "list_restaurants": lambda: self.system.process_request(self.username, "list_restaurants"),
        }

        print(actions.get(request_type, lambda: "잘못된 요청")())

    def logout(self):
        if input("로그아웃하시겠습니까? (예/아니요): ").strip().lower() == "예":
            print(self.system.logout(self.username))
            self.username = None
        else:
            print("초기 화면으로 돌아갑니다.")
            self.run()

    def run(self):
        self.login()
        for service in ["search", "reservation", "check_reservation", "notification", "cancel", "list_restaurants"]:
            self.request_service(service)
        self.logout()
