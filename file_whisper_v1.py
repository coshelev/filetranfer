from flask import Flask
from smb.SMBConnection import SMBConnection

# Define the SMB connection parameters
server_name = '192.168.0.14'  # Replace this with your server IP
share_name = 'SysAgr_txt'  # Replace this with your share name
username = 'beuser'  # Replace this with your username
password = 'P@ssw0rd'  # Replace this with your password

app = Flask(__name__)

@app.route('/whisper', methods=['POST'])
def json_example():

    #file_path = '//192.168.0.14/SysAgr_txt/1700208178.30741.txt'
    
    conn = SMBConnection(username, password, '',server_name, 'main.luidorauto.ru', use_ntlm_v2=True, is_direct_tcp=True)
    conn.connect(server_name, 445)
    file_list = conn.listPath(share_name, '/')  # Replace '/' with the path to the directory you want to list
    for file_info in file_list:
       print(file_info.filename)
    conn.close()

    return 'JSON Object Example'





app.run(host='0.0.0.0', port=8081, debug=True)
