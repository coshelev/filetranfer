from flask import Flask
from smb.SMBConnection import *
import whisper
from whisper.utils import get_writer

# Define the SMB connection parameters for "\\fs-srv-01\d$\1C_DOC\SysAgr_txt" i.e. \\192.168.0.14\SysAgr_txt 
server_name1 = '192.168.0.14'  # Replace this with your server IP
share_name1 = 'SysAgr_txt'  # Replace this with your share name
username1 = 'b...'  # Replace this with your username under which 1c-server is running
password1 = 'P...'  # Replace this with your password  of user under which 1c-server is running

app = Flask(__name__)

@app.route('/whisper', methods=['POST'])
def json_example():

    #connect to \\192.168.0.14\SysAgr_txt 
    conn1 = SMBConnection(username1, password1, '',server_name1, 'main', use_ntlm_v2=True, is_direct_tcp=True)
    conn1.connect(server_name1, 445)
    #file_list1 = conn1.listPath(share_name1, '/')
    #for file_info in file_list1:
    #   print(file_info.filename)

    output_file = open("calls_to_transcribe.txt", 'wb')
    conn1.retrieveFile(service_name = share_name1, path = "/lst/calls_to_transcribe.txt", file_obj = output_file)
    output_file.close()

    model = whisper.load_model("base")

    #Read file from 2-nd line, because in 1-st line appears excess symbols
    output_file = open("calls_to_transcribe.txt", 'r')
    lines = output_file.readlines()
    for i in lines:
        print("*******************************************************************************")
        path = i.strip()
        print("path="+path)
        wav_file_name = "1.wav"
        wav_file_obj = open(wav_file_name, 'wb')
        try:
            #for debugging
            #conn1.retrieveFile(service_name = share_name1, path ="/wav/700981432.2673.wav", file_obj = wav_file_obj)
            conn1.retrieveFile(service_name = share_name1, path ="/wav/"+path, file_obj = wav_file_obj)
        except:
            continue
        wav_file_obj.close()
        result = model.transcribe(wav_file_name)
        transcription = result["text"]
        print(transcription)
        txt_file_name = i.replace("wav", "txt").rstrip("'$'\n'")
        txt_file = open(("./txt/"+txt_file_name), 'w+');
        txt_file.write(transcription)
        txt_file.close()

    output_file.close()

    conn1.close()


    return 'JSON Object Example'



app.run(host='0.0.0.0', port=8082, debug=True)
