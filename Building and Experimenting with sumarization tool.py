import requests
from colorama import Fore, Style, init
from config import API_key

init(autoreset=True)

DEFAULT_MODEL = "facebook/bart-large-cnn"

def build_api_url(model_name):
    return f"https://router.huggingface.co/{model_name}"

def query(payload, model_name=DEFAULT_MODEL):
    api_url = build_api_url(model_name)
    headers = {"Authorization": f"Bearer {API_key}"}
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
            }
        }
    
    print(Fore.YELLOW + f"\n🔄 Performing AI summarization using model: {model_name}")

    result = query(payload, model_name=model_name)

    if isinstance(result, list) and result and 'summary_text' in result[0]:
        return result[0]['summary_text']
    else:
        print(Fore.RED + "!!! Error: in summarization response.", result)
        return None

if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "\n=== Text Summarization Tool ===\n")
    print(Fore.YELLOW + Style.BRIGHT + "----Hi there! What's your name?----")
    user_name = input("Enter your name: ").strip()
    if not user_name:
        user_name = "User"
    print(Fore.GREEN + f"\nWelcome, {user_name}! Let's give your text some AI-Magic!\n")

    print(Fore.YELLOW + "\nPlease enter the text you want to summarize:")
    user_text = input("> " ).strip()

    if not user_text:
        print(Fore.RED + "!!! Error: No text provided. Exiting.")
    else:
        model_choice = input("Model name (leave blank for default): ").strip()
        if not model_choice:
            model_choice = DEFAULT_MODEL    
        
        print(Fore.YELLOW + "\nChoose your summarization style:")
        print("1. Standard (Quick and concise)")
        print("2. Detailed (More comprehensive summary)")
        style_choice = input("Enter 1 or 2: ").strip()

        if style_choice == '2':
            min_len, max_len = 80, 200
            print(Fore.GREEN + "\nUsing Detailed summarization style.\n")
        else:
            min_len, max_len = 50, 150
            print(Fore.GREEN + "\nUsing Standard summarization style.\n")

        summary = summarize_text(user_text, min_length=min_len, max_length=max_len, model_name=model_choice)
        if summary:
            print(Fore.CYAN + Style.BRIGHT + f"\n📝 AI Summarizer Output for {user_name}:\n")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + "!!! Error: Summarization failed.")