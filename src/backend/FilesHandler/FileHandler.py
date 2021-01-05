from paramiko import Transport, SFTPClient


def upload_file(document_id, file_to_upload, filename, server_details):
    # noinspection PyTypeChecker
    transport = Transport((server_details["host"], 22))
    transport.connect(username=server_details["user"], password=server_details["password"])
    sftp = SFTPClient.from_transport(transport)
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
    sftp.put(file_to_upload, filename)  # At this point, you are in remote_path in either case
    sftp.close()
