class Restaurant:
    def __init__(self, name, location, menu, 운영중=True):
        self.name = name
        self.location = location
        self.menu = menu
        self.운영중 = 운영중
        self.reservations = {}

    def self_reference(self):
        """자신을 식별할 수 있도록 표현"""
        return f"나는 '{self.name}'입니다."

    def get_info(self):
        """레스토랑의 운영 상태 및 기본 정보를 반환"""
        return {
            "name": self.name,
            "location": self.location,
            "menu": self.menu,
            "status": "운영 중" if self.운영중 else "🚫 운영 중지",
            "reservations": self.reservations
        }

    def reserve(self, username, date):
        """예약 처리"""
        if not self.운영중:
            return f"{self.name}은 현재 운영 중이 아닙니다."
        if date not in self.reservations:
            self.reservations[date] = username
            return f"{self.name} {date} 예약 성공"
        return f"{self.name} {date}은 이미 예약됨"

    def cancel_reservation(self, username, date):
        """예약 취소 처리"""
        if date in self.reservations and self.reservations[date] == username:
            del self.reservations[date]
            return f"{self.name} {date} 예약 취소 완료"
        return "예약 정보를 찾을 수 없음"

    def has_reservation(self, username, date):
        """해당 사용자가 예약했는지 확인"""
        return self.reservations.get(date) == username

    def toggle_status(self):
        """운영 상태 변경"""
        self.운영중 = not self.운영중

    def is_operating(self):
        """현재 운영 상태 반환"""
        return self.운영중
