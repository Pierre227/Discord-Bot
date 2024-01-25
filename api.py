import requests

# Replace 'your_api_key' with your actual API key
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()
#{'id': 'v0ya5BUzFY9esnssQlyLsEiCu1_GHPKLlNnT9kS-SpY4gT4', 'accountId': '2eMqCgJXCEuwuyO9CqbQHgFPQcpYZ95jgLnzlWl-6oF6Bg', 
#'puuid': 'By-pbVWjq4fGGiganfN3Nfak92fZlgQBe6vBP9mtLtnUqgUmfD8vs6SRwT9rfsZU4tFRcglo6JPY9A',
#'name': 'Eclow', 'profileIconId': 654, 'revisionDate': 1706043340517, 'summonerLevel': 158}

# api_url = 'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/By-pbVWjq4fGGiganfN3Nfak92fZlgQBe6vBP9mtLtnUqgUmfD8vs6SRwT9rfsZU4tFRcglo6JPY9A'
# api_url = api_url + '?api_key=' + api_key

# req = requests.get(api_url)
# print(req)
# print(req.json())

def get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_puuid(username, tag):
    response = get_request('https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + username + '/' + tag + '?api_key=' + api_key)
    if response:
        return response.json()['puuid']
    return None
def get_summonder_id(puuid):
    response = get_request('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/' + puuid + '?api_key=' + api_key)
    if response:
        return response.json()['id']
    return None

def get_infos(summoner_id):
    response = get_request('https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id + '?api_key=' + api_key)
    if response.json():
        return [response.json()[0]['tier'], response.json()[0]['rank'], response.json()[0]['leaguePoints'], response.json()[0]['wins'], response.json()[0]['losses']]
    return None

def get_rank(username, tag):
    puuid = get_puuid(username, tag)
    if puuid:
        summoner_id = get_summonder_id(puuid)
        if summoner_id:
            response = get_infos(summoner_id)
            return response
    return None


# username = input("Please enter your username: ")
# print("You entered:", username)

# tag = input("Please enter your TAG: ")
# print("You entered:", tag)

# print(get_rank(username, tag))