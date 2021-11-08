import re
import paramiko


def get_gscn_from_rrh_config(hostname: str, username: str, password: str) -> int:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
        command = r"cat /home/RRH.xml | grep -i GSCN | grep -o '[[:digit:]]*'"
        _, stdout, stderr = client.exec_command(command)
        error_message = stderr.read().decode()
        print(error_message if error_message else "")
        return int(stdout.read().decode())
    except Exception:
        print("[!] Cannot connect to the Remote Radio Head")
        raise SystemExit
    finally:
        client.close()


def get_gscn_from_bs_config(configuration_file_path: str) -> int:
    with open(configuration_file_path) as cfg:
        lines = cfg.readlines()

    pattern = '<p name="gscn">(.*)</p>'

    for line in lines:
        matched_expression = re.search(pattern, line)
        if matched_expression:
            return int(matched_expression.group(1))
