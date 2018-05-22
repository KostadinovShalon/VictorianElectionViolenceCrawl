import requests
import paramiko

payload = {'Username': "nick.vivyan@durham.ac.uk", "Password": "EV19@Nick",
           "RememberMe": "false", "NestPage": ""}

headers = {
    "Accept"            :"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding"   :"gzip, deflate, br",
    "Accept-Language"   :"zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control"     :"max-age=0",
    "Connection"        :"keep-alive",
    "Host"              :"www.britishnewspaperarchive.co.uk",
    "User-Agent"        :"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "Origin"            :"https://www.britishnewspaperarchive.co.uk",
    "Link"              :"<https://www.britishnewspaperarchive.co.uk/account/login>; rel=\"canonical\"",
    "X-Frame-Options"   :"SAMEORIGIN",
    }

s = requests.Session()
s.post("https://www.britishnewspaperarchive.co.uk/account/login", data=payload, headers=headers)
#https://www.britishnewspaperarchive.co.uk/viewer/items/bl/0000430/18650701/015/0003
f = s.get("https://www.britishnewspaperarchive.co.uk/viewer/download/bl/0000430/18650701/015/0003")

transport = paramiko.Transport(("coders.victorianelectionviolence.uk", 22))
transport.connect(username="data_feeder", password="Arp48dEx")

sftp = paramiko.SFTPClient.from_transport(transport)
sftp.chdir("documents")
try:
    sftp.chdir("2")  # Test if remote_path exists
except IOError:
    sftp.mkdir("2")  # Create remote_path
    sftp.chdir("2")
sftp.putfo("./test.pdf", './test.pdf')    # At this point, you are in remote_path in either case
sftp.close()