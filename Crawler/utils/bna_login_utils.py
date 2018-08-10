import bna_login_details as details

username = details.username
password = details.password
remember_me = 'false'
next_page = ''

login_url = "https://www.britishnewspaperarchive.co.uk/account/login"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.britishnewspaperarchive.co.uk",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/64.0.3282.167 Safari/537.36",
    "Origin": "https://www.britishnewspaperarchive.co.uk",
    "Link": "<https://www.britishnewspaperarchive.co.uk/account/login>; rel=\"canonical\"",
    "X-Frame-Options": "SAMEORIGIN",
}

