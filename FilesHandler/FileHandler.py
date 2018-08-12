import paramiko
from paramiko import Transport, SFTPClient
from Crawler.utils import server_variables as server


def upload_file(document_id, file_to_upload, filename):
    # noinspection PyTypeChecker
    transport = Transport((server.host, 22))
    transport.connect(username=server.ftp_user, password=server.ftp_password)
    sftp = SFTPClient.from_transport(transport)
    paramiko.util.log_to_file("filename.log")
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
