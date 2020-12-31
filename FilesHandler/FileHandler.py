from paramiko import Transport, SFTPClient
from repositories import configuration


def upload_file(document_id, file_to_upload, filename):
    # noinspection PyTypeChecker
    server = configuration.server_variables()
    transport = Transport((server["host"], 22))
    transport.connect(username=server["user"], password=server["password"])
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
