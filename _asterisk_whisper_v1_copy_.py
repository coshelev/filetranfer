from flask import Flask
from smb.SMBConnection import *
import tempfile
import whisper

# Define the SMB connection parameters for Asterisk
server_name = '192.168.0.245'  # Replace this with your server IP
share_name = 'call-records'  # Replace this with your share name
username = 'aster-crm'  # Replace this with your username
password = 'Vtuf&65Gfccdjhl'  # Replace this with your password

# Define the SMB connection parameters for "\\fs-srv-01\d$\1C_DOC\SysAgr_txt" i.e. \\192.168.0.14\SysAgr_txt 
server_name1 = '192.168.0.14'  # Replace this with your server IP
share_name1 = 'SysAgr_txt'  # Replace this with your share name
username1 = 'beuser'  # Replace this with your username 
password1 = 'P@ssw0rd'  # Replace this with your password

app = Flask(__name__)

@app.route('/whisper', methods=['POST'])
def json_example():

    #connect to Asterisk
    conn = SMBConnection(username, password, '',server_name, 'main', use_ntlm_v2=True, is_direct_tcp=True)
    conn.connect(server_name, 445)
    #file_list = conn.listPath(share_name, '/')
    #for file_info in file_list:
    #   print(file_info.filename)

    #connect to \\192.168.0.14\SysAgr_txt 
    conn1 = SMBConnection(username1, password1, '',server_name1, 'main', use_ntlm_v2=True, is_direct_tcp=True)
    conn1.connect(server_name1, 445)
    #file_list1 = conn1.listPath(share_name1, '/')
    #for file_info in file_list1:
    #   print(file_info.filename)

    #file_obj = tempfile.NamedTemporaryFile()
    #file_attributes, filesize = conn1.retrieveFile(service_name = share_name1, path = "/lst/calls_to_transcribe.txt", file_obj = file_obj)
    #file_obj.close()

    output_file = open("calls_to_transcribe.txt", 'wb')
    conn1.retrieveFile(service_name = share_name1, path = "/lst/calls_to_transcribe.txt", file_obj = output_file)
    output_file.close()

    #model = whisper.load_model("base")

    output_file = open("calls_to_transcribe.txt", 'r')
    lines = output_file.readlines()
    for i in lines:
        print(i)
        wav_file_obj = open("1.wav", 'wb')
        conn.retrieveFile(service_name = share_name, path = i, file_obj = wav_file_obj)
        result = model.transcribe(wav_file_obj)
        transcription = result["text"]
        wav_file_obj.close()

    output_file.close()
    #file_contents = file_obj.read()
    #decoded_file_contents = file_contents.decode('utf-8')
    #print(decoded_file_contents)

    #model = whisper.load_model("large-v3")
    #model = whisper.load_model("base")

    #output_file = open("calls_to_transcribe.txt", 'wb')
    #output_file.write(decoded_file_contents)
    #output_file.close()
    
    #lines = decoded_file_contents.readlines()
    #for i in lines:
        #print(i)
        #wav_file_obj = conn.retrieveFile(service_name = share_name, path = i, file_obj = wav_file_obj)

        #result = model.transcribe(wav_file_obj)
        #transcription = result["text"]
        #wav_file_obj.close()

    # Close the remote text file  
    #file_obj.close()

    conn.close()
    conn1.close()


    return 'JSON Object Example'



app.run(host='0.0.0.0', port=8082, debug=True)
