import paramiko

transport = paramiko.Transport(("coders.victorianelectionviolence.uk", 22))
transport.connect(username="data_feeder", password="Arp48dEx")

sftp = paramiko.SFTPClient.from_transport(transport)
sftp.chdir("documents")
try:
    sftp.chdir("1")  # Test if remote_path exists
except IOError:
    sftp.mkdir("1")  # Create remote_path
    sftp.chdir("1")
sftp.put("./test.pdf", './test.pdf')    # At this point, you are in remote_path in either case
sftp.close()
