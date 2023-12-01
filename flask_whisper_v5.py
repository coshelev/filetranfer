from flask import Flask, request
import whisper
from pydub import AudioSegment
from whisper.utils import get_writer
import requests
import os
import soundfile as sf
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.route('/whisper', methods=['POST'])
def whspr():
    
    inputHeaders        = request.headers
    filenameWithoutExt  = inputHeaders.get('filenameWithoutExt')
    filenameWAV = inputHeaders.get('filenameWAV')

    print(filenameWAV)

    binary_data = request.data
    
    file = open(filenameWAV, 'wb')
	   
    try:
        file.write(binary_data)
    finally:
        file.close()

    model = whisper.load_model("large-v3")
    #model = whisper.load_model("base")

    result = model.transcribe(filenameWAV)
    transcription = result["text"]
    
    ## Load the audio data
    #audio, sr = sf.read(filenameWAV)
    ## Extract the left and right audio channels
    #left_channel = audio[:, 0]
    #right_channel = audio[:, 1]
    ##left_channel = left_channel.astype('float32')
    #right_channel = right_channel.astype('float32')
    ## Transcribe the left channel
    #left_transcription = whisper.transcribe(audio = left_channel, model = model)["text"]
    ## Transcribe the right channel
    #right_transcription = whisper.transcribe(audio = right_channel, model = model)["text"]
    ## Combine the transcriptions with timestamps
    #transcription = f"{transcription}\nLeft channel: {left_transcription}\nRight channel: {right_transcription}"

    print(transcription)

    # Convert the transcription to tsv format
    #output_directory = "./"
    #tsv_writer = get_writer("tsv",  output_directory)
    #tsv_output = tsv_writer(result, filenameWAV)
    #tsv_file = open(filenameWithoutExt+".tsv", "w")
    #tsv_file.write(tsv_output)
    #tsv_file.close()

    # Save as a TSV file
    #-------------------
    #output_directory = "./"
    #tsv_writer = whisper.get_writer("tsv", output_directory)
    #tsv_file = filenameWithoutExt+".tsv"
    #tsv_writer(result,  tsv_file)

    #txtfileName = filenameWithoutExt+".tsv"
    #txtfile = open(txtfileName, 'r')
    #file_content = txtfile.read()

    #filecontent = flask.jsonify({"transcription": transcription})
	
    #audio = AudioSegment.from_wav(filenameWAV)
    #channels = audio.split_to_mono()    
    #left_channel = channels[0]
    #filenameLeftWAV = filenameWithoutExt+"_1.WAV"
    #left_channel.export(filenameLeftWAV, format="wav")
    #model = whisper.load_model("large-v3")
    #result = model.transcribe(filenameWAV)
    #print(result["text"])
    #tsv_writer(result, filenameLeftWAV)

    # Delete the file
    #===================	
    try:
        os.remove(filenameWAV)
        print(f"File '{filenameWAV}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{filenameWAV}' not found.")
    except PermissionError:
        print(f"Permission denied to delete '{filenameWAV}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    post_url = 'http://mainappl.main.luidorauto.ru/sys_agr/hs/webhooks/anypost/v1'
    headers = {'Content-Type': 'application/json'}

    signature   = inputHeaders.get('signature')
   
    payload =  '{"type":"transcription","signature":'+'"'+signature+'", "linkedid":'+'"'+filenameWithoutExt+'","transcription":'+ '"'+ transcription+'"}'
    payload1 = payload.encode('utf-8')
    response = requests.post(post_url, headers=headers, data=payload1)

    return 'whisper'


@app.route('/whisper_for_job', methods=['POST'])
async def whspr_job():
    data = await async_whspr()
    return 'whisper_job'

def async_whspr():
    inputHeaders        = request.headers
    filenameWithoutExt  = inputHeaders.get('filenameWithoutExt')
    filenameWAV = inputHeaders.get('filenameWAV')

    print(filenameWAV)

    binary_data = request.data

    file = open(filenameWAV, 'wb')

    try:
        file.write(binary_data)
    finally:
        file.close()

    model = whisper.load_model("large-v3")
    #model = whisper.load_model("base")

    result = model.transcribe(filenameWAV)
    transcription = result["text"]

    # Delete the file
    #===================
    try:
        os.remove(filenameWAV)
        print(f"File '{filenameWAV}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{filenameWAV}' not found.")
    except PermissionError:
        print(f"Permission denied to delete '{filenameWAV}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    post_url = 'http://mainappl.main.luidorauto.ru/sys_agr/hs/webhooks/anypost/v1'
    headers = {'Content-Type': 'application/json'}

    signature   = inputHeaders.get('signature')

    payload =  '{"type":"transcription_job","signature":'+'"'+signature+'", "linkedid":'+'"'+filenameWithoutExt+'","transcription":'+ '"'+ transcription+'"}'
    payload1 = payload.encode('utf-8')
    response = requests.post(post_url, headers=headers, data=payload1)

    return 'whspr_asnk'
	

app.run(host='0.0.0.0', port=8080, debug=False)
