from catch_table import CatchTable

class User:
    def __init__(self, system):
        self.system = system
        self.username = None  # 로그인 후 저장할 사용자 정보

    def login(self):
        """로그인 처리"""
        if self.username and self.system.is_logged_in(self.username):
            print(f"{self.username}님, 이미 로그인되어 있습니다.")
        else:
            self.username = self.system.authenticate()
            print(f"{self.username} 로그인 성공" if self.username else "로그인 실패")

    def request_service(self, request_type):
        """사용자가 특정 요청을 수행"""
        if not self.system.is_logged_in(self.username):
            return "로그인 필요"

        actions = {
            "search": lambda: self.system.process_request(self.username, "search", input("검색할 레스토랑 이름을 입력하세요: ")),
            "reservation": lambda: self.system.process_request(self.username, "reservation", 
                            (input("예약할 레스토랑 이름을 입력하세요: "), input("예약할 날짜를 입력하세요 (YYYY-MM-DD): "))),
            "cancel": lambda: self.system.process_request(self.username, "cancel", 
                       (input("취소할 예약 레스토랑 이름을 입력하세요: "), input("취소할 예약 날짜를 입력하세요 (YYYY-MM-DD): "))),
            "list_restaurants": lambda: self.system.process_request(self.username, "list_restaurants"),
        }

        print(actions.get(request_type, lambda: "잘못된 요청")())

    def logout(self):
        """사용자 로그아웃"""
        if input("로그아웃하시겠습니까? (예/아니요): ").strip().lower() == "예":
            print(self.system.logout(self.username))
            self.username = None
        else:
            print("초기 화면으로 돌아갑니다.")
            self.run()
