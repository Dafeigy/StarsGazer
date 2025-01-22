from utils import getStarsRepo

if __name__ == "__main__":
    start_url = "https://github.com/dafeigy?tab=stars"
    all_urls = getStarsRepo.find_next(start_url)
    print("收集到的所有URL:")
    for url in all_urls:
        print(url)