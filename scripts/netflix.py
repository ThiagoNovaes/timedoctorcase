import requests
import json

payload={}
headers = {
  'authority': 'www.netflix.com',
  'accept': '*/*',
  'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8',
  'cookie': 'netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; hasSeenCookieDisclosure=true; dsca=customer; nfvdid=BQFmAAEBENNoeQ8s2ArYcQhSUQJiN6ZgGYkmPWTl3Vnis8Fm6AJjhINQp3nWXucB5wFULYOw-3VnkTrbNO9IXHOBecbckbzam4sGP5DJdKvdn_Fx349_VnqW5xhUOlbVMvrSwa210SzrCDUOPwZhJQu3EL9bchly; flwssn=c9849055-f056-4f83-a69d-1c87317921b4; SecureNetflixId=v%3D2%26mac%3DAQEAEQABABTpBHdLlu0cw7kg79N1zJFzjjb27XNqo_c.%26dt%3D1687124511374; NetflixId=v%3D2%26ct%3DBQAOAAEBEN4Q-F6-vfEXtqlToGlzrKiBwNYlXiMuy054o-crugA4Shsgsg54tUQtpok98JxEF3HYtyQk4y_abE09JMuPT3Zg16dz1Dfsk4vTi1t-Rj1H6-IoPi3Tjk_SIzt906akPKMH4Ic-H5H2fKfLw3vSOfSDuMCEYtaTGQ9rEDazetuEuyKScdxZiwaoERaX8aTYx_e5IOKvhJq9c1_wIFoooz32tV9PMxgR7zilzPlDHPrPaS3ll6XCFpIVaKjH4xWHDuAQ6b2cvFllaEfY4-gdJnYnWNls84z8pYMHLMsOU5vpxCZvlRpvtFtPTxQBi6FbWSmeJWXdeZKLUrFV29HjhZ0Zxl2BUo5DOOStnGNEtI5iSR5MxUH7BjydrFOgTPf8DyfOFJgMhwhONc3v-fPI4-efMDCFJM6bN9f0meUrHWp1aFEz0uzH7huaXgiWkOEXYuIc3DTYn_Gix1f-PohxAVXohC_pjm0pXgNmZwUL94SHnHXQoxBggw9tdDh_BsfaUYAFTkLccAhKKuovOHMY-dFBjYHJ1j-2uVHGCwIf0vQb1jghrdwLCf4_i5aGEhC_1BeBiKbOn2vpVligtuQhknS5y77E8bXkUjTLPgEaPt58QtY.%26bt%3Ddbl%26ch%3DAQEAEAABABSlS_4o6-4hKboueZO-DKFXbOlrSSBoxVA.%26mac%3DAQEAEAABABQYXgRNAaGa44uwjjMCYQxJMupc-JHod9g.; profilesNewSession=0; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jun+18+2023+18%3A42%3A18+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=af7b30df-e27b-4b11-80a3-f3379d48c6ba&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
  'referer': 'https://www.netflix.com/settings/viewed/GG65WWL2YNFOBGGRD7CX4OKHUM',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'x-netflix.browsername': 'Chrome',
  'x-netflix.browserversion': '114',
  'x-netflix.client.request.name': 'ui/xhrUnclassified',
  'x-netflix.clienttype': 'akira',
  'x-netflix.esn': 'NFCDCH-02-J46ZDQM8LL81XLLJY1HJFL11W6U21P',
  'x-netflix.esnprefix': 'NFCDCH-02-',
  'x-netflix.osfullname': 'Windows 10',
  'x-netflix.osname': 'Windows',
  'x-netflix.osversion': '10.0',
  'x-netflix.uiversion': 'v7462cb0c'
}

def make_request(url):
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data

def iterate_pagination(base_url, page_param, start_page, end_page):
    result = {
        "viewedItems": []
    }

    for page in range(start_page, end_page + 1):
        url = f"{base_url}?{page_param}={page}&pgSize=20&guid=GG65WWL2YNFOBGGRD7CX4OKHUM&_=1687124552312&authURL=1687124542359.N660%2BieXwuAvLeoNnPfCF1xk7GE%3D"
        data = make_request(url)
        result["viewedItems"].extend(data["viewedItems"])

    return result

# Example usage
base_url = "https://www.netflix.com/api/shakti/mre/viewingactivity"
page_param = "pg"
start_page = 0
end_page = 99

result = iterate_pagination(base_url, page_param, start_page, end_page)

# Write the result to a JSON file
with open("netflix.json", "w") as file:
    json.dump(result, file, indent=4)