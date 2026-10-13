
import platform
import time
from datetime import datetime, timedelta

# Xác định đường dẫn file hosts theo hệ điều hành
if platform.system() == "Windows":
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOSTS_PATH = "/etc/hosts"

REDIRECT_IP = "127.0.0.1"
MARKER = "# BLOCKED_BY_PYTHON_SCRIPT"


def block_sites(sites):
    """Thêm các trang web vào danh sách chặn."""
    with open(HOSTS_PATH, "r+", encoding="utf-8") as f:
        content = f.read()
        for site in sites:
            if site in content:
                print(f"[Bỏ qua] {site} đã bị chặn từ trước.")
                continue
            f.write(f"{REDIRECT_IP} {site} {MARKER}\n")
            f.write(f"{REDIRECT_IP} www.{site} {MARKER}\n")
            print(f"[Đã chặn] {site}")


def unblock_sites(sites=None):
    """Bỏ chặn các trang web. Nếu sites=None, bỏ chặn tất cả do script này thêm."""
    with open(HOSTS_PATH, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if MARKER in line:
            if sites is None:
                continue  # bỏ hết
            if any(site in line for site in sites):
                continue  # bỏ site được chỉ định
        new_lines.append(line)

    with open(HOSTS_PATH, "w") as f:
        f.writelines(new_lines)

    print("Đã cập nhật file hosts.")


def block_until(sites, end_time_str):
    """
    Chặn các trang cho đến một thời điểm cụ thể trong ngày, ví dụ '18:00'.
    Script sẽ chạy nền và tự bỏ chặn khi đến giờ.
    """
    now = datetime.now()
    end_time = datetime.strptime(end_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    if end_time < now:
        end_time += timedelta(days=1)

    block_sites(sites)
    print(f"Đã chặn tới {end_time.strftime('%H:%M')}. Đang chờ...")

    try:
        while datetime.now() < end_time:
            time.sleep(30)
    except KeyboardInterrupt:
        print("Đã dừng theo yêu cầu (Ctrl+C).")
    finally:
        unblock_sites(sites)
        print("Đã tự động bỏ chặn.")


if __name__ == "__main__":
    # Ví dụ sử dụng:
    danh_sach_chan = [
        'facebook.com'
        "tiktok.com",
        "instagram.com",
        "threads.com",
    ]

    print("1. Chặn ngay")
    print("2. Bỏ chặn tất cả")
    print("3. Chặn đến một giờ nhất định (vd: tập trung học/làm việc)")
    choice = input("Chọn (1/2/3): ").strip()

    if choice == "1":
        block_sites(danh_sach_chan)
    elif choice == "2": 
         unblock_sites()
    elif choice == "3":
        gio_ket_thuc = input("Chặn đến mấy giờ? (HH:MM, vd 18:00): ").strip()
        block_until(danh_sach_chan, gio_ket_thuc)
    else:
        print("Lựa chọn không hợp lệ.")
