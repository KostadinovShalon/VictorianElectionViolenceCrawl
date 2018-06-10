import paramiko


def upload_file(document_id, file_to_upload, filename):
    transport = paramiko.Transport(("coders.victorianelectionviolence.uk", 22))
    transport.connect(username="data_feeder", password="Arp48dEx")
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.chdir("documents")  # Test if remote_path exists
    except IOError:
        sftp.mkdir("documents")  # Create remote_path
        sftp.chdir("documents")
    try:
        sftp.chdir(str(document_id))  # Test if remote_path exists
    except IOError:
        sftp.mkdir(str(document_id))  # Create remote_path
        sftp.chdir(str(document_id))
    sftp.putfo(file_to_upload, filename)  # At this point, you are in remote_path in either case
    sftp.close()
    #this is a comment