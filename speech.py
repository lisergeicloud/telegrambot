import ffmpy
import wit

from mytokens import wit_token

witClient = wit.Wit(wit_token)


def voice_handler(file):
    path = 'voice.ogg'
    file.download(path)
    output = convert_to_mp3(path)
    with open(output, 'rb') as f:
        resp = witClient.speech(f, None, {'Content-Type': 'audio/mpeg3'})
    text = resp['_text'].lower()
    return text


# $ ffmpeg - i voice.ogg - ac 1 voice.mp3
def convert_to_mp3(path):
    output = 'voice.mp3'
    ff = ffmpy.FFmpeg(global_options=['-y'], inputs={path: None}, outputs={output: '-ac 1'})
    print(ff.cmd)
    ff.run()
    return output
