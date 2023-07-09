from dash import html, dcc
import base64

sound_filename = 'app/static/warning.mp3'  # replace with your own .mp3 file
encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())



def check_values(value, alert):
    colors = ('black', 'black', 'black', 'black')
    indicator = False
    if value < 10:
        colors = ('black', 'black', 'black', 'blue')
        indicator = True
    elif value > 42:
        colors =  ('black', 'black', 'black', 'red')
        indicator = True
    elif value > 36:
        colors =  ('black', 'black', 'black', 'orange')
        indicator = False
        
    if not alert and indicator:
        return (1,) + colors
    else:
        return (0,) + colors

def getAudio(play):
    
    if play:
        return html.Audio(src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()),
            controls=False,
            autoPlay=True,
            )
    return ""
     