class Restaurant:
    def __init__(self, name, location, menu, 운영중=True):
        self.name = name
        self.location = location
        self.menu = menu
        self.운영중 = 운영중
        self.reservations = {}

    def get_info(self):
        status = "운영 중" if self.운영중 else "운영 종료"
        return f"이름: {self.name}, 위치: {self.location}, 메뉴: {', '.join(self.menu)}, 상태: {status}"

    def reserve(self, username, date):
        if not self.운영중:
            return f"{self.name}은 현재 운영 중이 아닙니다."
        if date not in self.reservations:
            self.reservations[date] = username
            return f"{self.name} {date} 예약 성공"
        return f"{self.name} {date}은 이미 예약됨"

    def cancel_reservation(self, username, date):
        if date in self.reservations and self.reservations[date] == username:
            del self.reservations[date]
            return f"{self.name} {date} 예약 취소 완료"
        return "예약 정보를 찾을 수 없음"

    def has_reservation(self, username, date):
        return self.reservations.get(date) == username

    def toggle_status(self):
        self.운영중 = not self.운영중
