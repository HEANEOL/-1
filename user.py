from catch_table import CatchTable

class User:
    def __init__(self, system):
        self.system = system
        self.username = None  # 로그인 후 저장할 사용자 정보

    def login(self):
        """사용자 로그인"""
        if self.username and self.system.is_logged_in(self.username):
            print(f"{self.username}님, 이미 로그인되어 있습니다.")
        else:
            self.username = self.system.authenticate()
            print(f"{self.username} 로그인 성공" if self.username else "로그인 실패")

    def request_service(self):
        """순서대로 서비스 요청 (레스토랑 목록 → 검색 → 예약 → 예약 날짜 확인 → 예약 취소 → 로그아웃)"""
        if not self.system.is_logged_in(self.username):
            print("로그인이 필요합니다.")
            return

        # 1️⃣ 레스토랑 목록 확인
        print("\n📌 현재 등록된 레스토랑 목록:")
        print(self.system.process_request(self.username, "list_restaurants", None))

        # 2️⃣ 특정 레스토랑 검색
        search_query = input("\n🔍 검색할 레스토랑 이름을 입력하세요: ")
        print(self.system.process_request(self.username, "search", search_query))

        # 3️⃣ 예약 요청
        restaurant_name = input("\n📅 예약할 레스토랑 이름을 입력하세요: ")
        reservation_date = input("📅 예약할 날짜를 입력하세요 (YYYY-MM-DD): ")
        print(self.system.process_request(self.username, "reservation", (restaurant_name, reservation_date)))

        # 4️⃣ 예약 날짜 확인
        check_date = input("\n📋 확인할 예약 날짜를 입력하세요 (YYYY-MM-DD): ")
        print(self.system.process_request(self.username, "check_reservation", check_date))

        # 5️⃣ 예약 취소 요청
        cancel_name = input("\n❌ 취소할 예약 레스토랑 이름을 입력하세요: ")
        cancel_date = input("❌ 취소할 예약 날짜를 입력하세요 (YYYY-MM-DD): ")
        print(self.system.process_request(self.username, "cancel", (cancel_name, cancel_date)))

        # 6️⃣ 로그아웃 요청
        self.logout()
        #  레스토랑 운영 상태 변경 요청 (사장님이 사용할 기능)
        # 운영 상태 변경은 관리자가 특정 레스토랑을 "운영 중/중지"로 변경할 때 사용됩니다.
        # restaurant_name = input("\n🔄 운영 상태 변경할 레스토랑 이름을 입력하세요: ")
        # print(self.system.process_request(self.username, "toggle_status", restaurant_name))


    def logout(self):
        """사용자 로그아웃"""
        if input("\n🔓 로그아웃하시겠습니까? (예/아니요): ").strip().lower() == "예":
            print(self.system.logout(self.username))
            self.username = None
        else:
            print("초기 화면으로 돌아갑니다.")
            self.request_service()  # 서비스를 처음부터 다시 진행

    def run(self):
        """사용자 서비스 실행"""
        self.login()
        self.request_service()  #  서비스 흐름 실행
