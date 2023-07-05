from dash import html, dcc
import base64

sound_filename = 'app/static/warning.mp3'  # replace with your own .mp3 file
encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())



def check_values(value, alert):
    print(value)
    if value>44:
        if not alert:
            return (True, 'red', 'red', 'red', 'red')
        else:
            return (False, 'red', 'red', 'red', 'red')
    return (False, 'black', 'black', 'black', 'black')

def getAudio(play):
    
    if play:
        return html.Audio(src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()),
            controls=False,
            autoPlay=True,
            )
    return ""
     