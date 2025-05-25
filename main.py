from catch_table import CatchTable
from user import User

def main():
    system = CatchTable()
    user = User(system)
    user.run()

if __name__ == "__main__":
    main()

#실행용 메인 파일(현재 기능으론 샘플 가게만 이용중 수정 시 임의로 가게 추가가 가능하나 사용자 시점이 적절하다고 생각해 기능 일부를 살린 체 작동중. )
