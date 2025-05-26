import re
import requests
import os

def download_images_from_string(input_string, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 提取所有图片网址
    img_urls = re.findall(r'(https?://[^\s]+?\.(?:jpg|png|gif))', input_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    # 下载并重命名图片
    for idx, url in enumerate(img_urls):
        try:
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                _, extension = os.path.splitext(url)
                filename = f"{idx+1}{extension}"
                filepath = os.path.join(output_folder, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {url} as {filename}")
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")


def download_mp4_urls_from_string(input_string, output_directory):
    # 使用正则表达式来匹配.mp4链接
    mp4_urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          input_string)
    mp4_urls = [url for url in mp4_urls if url.endswith('.mp4')]

    if not mp4_urls:
        print("未找到任何.mp4链接。")
        return

    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 逐个下载并重命名.mp4链接
    for index, mp4_url in enumerate(mp4_urls):
        try:
            response = requests.get(mp4_url)
            if response.status_code == 200:
                filename = f"video_{index + 1}.mp4"
                output_path = os.path.join(output_directory, filename)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"已下载并保存: {output_path}")
            else:
                print(f"无法下载: {mp4_url}")
        except Exception as e:
            print(f"下载时发生错误: {e}")



# 示例用法
output_folder = "downloaded_images"
output_MP4 = "downloaded_mp4"




total_path = "https://img.alicdn.com/imgextra/i3/2209864271836/O1CN01z9UEU41PQvwhTUrxr_!!2209864271836.jpghttps://img.alicdn.com/imgextra/i1/2209864271836/O1CN01FJBIdU1PQvwsE5xg0_!!2209864271836.jpghttps://img.alicdn.com/imgextra/i4/2209864271836/O1CN01bSq5en1PQvwuPUiin_!!2209864271836.jpghttps://img.alicdn.com/imgextra/i4/2209864271836/O1CN01i5NWse1PQvwxBfpt9_!!2209864271836.jpg"
# download_mp4_urls_from_string(total_path,output_MP4)
download_images_from_string(total_path, output_folder)
