import os
import sys
import time
import urllib.request


try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    USE_REQUESTS = False

def download_file(url, save_path, max_retries=3, wait_seconds:int=5):
    """
    下载文件（带重试机制）
    :param url: 下载文件的URL
    :param save_path: 保存文件的路径
    :param max_retries: 最大重试次数
    :param wait_seconds: 每次重试之间的等待时间（秒）
    :return: True 表示下载成功，False 表示下载失败
    """
    for attempt in range(max_retries):
        try:
            print(f"尝试下载 {os.path.basename(save_path)} (尝试 {attempt+1}/{max_retries})...")
            print(f"使用 {'requests' if USE_REQUESTS else 'urllib'} 库进行下载")
            if USE_REQUESTS:
                download_with_requests(url, save_path)
            else:
                download_with_urllib(url, save_path)
            return True
        except Exception as e:
            print(f"下载失败: {str(e)}")
            if attempt < max_retries - 1:
                print("等待5秒后重试...")
                time.sleep(wait_seconds)
    return False

def download_with_urllib(download_url:str, save_path:str):
    """下载文件并显示进度"""
    def show_progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\r下载进度: {percent}%")
        sys.stdout.flush()

    print(f"正在从 [{download_url}] 下载 {os.path.basename(save_path)}...")
    urllib.request.urlretrieve(download_url, save_path, show_progress)
    print("\n下载完成!")


def download_with_requests(download_url, save_path):
    """使用requests库下载文件"""
    try:
        import requests
    except ImportError:
        print("请先安装requests库: pip install requests")
        sys.exit(1)
    print(f"正在从 [{download_url}] 下载 {os.path.basename(save_path)}...")
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                progress = downloaded * 100 / total_size if total_size > 0 else 0
                sys.stdout.write(f"\r下载进度: {int(progress)}%")
                sys.stdout.flush()


if __name__ == '__main__':
    test_url = 'https://example.com/file.zip'
    save_path = 'file.zip'
    download_file(test_url, save_path)