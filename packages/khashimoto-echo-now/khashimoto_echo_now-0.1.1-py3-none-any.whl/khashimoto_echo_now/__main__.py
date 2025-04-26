from datetime import datetime


def echo_now():
    print(f"今日は {datetime.now(): %Y 年 %m 月 %d 日 %H 時 %M 分 %S 秒です}")


if __name__ == "__main__":
    echo_now()
