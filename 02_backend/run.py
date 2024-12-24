from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL 

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json

    url = data.get('url')
    preference = data.get('preference')
    output_path = data.get('ouput_path','')

    if not url:
        return jsonify({"error": "Invalid URL"}), 400
    
    ydl_opts = {
        'outtmpl' : f'./outputs/{output_path}/%(title)s.%(ext)s',
    }

    if preference == 1:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    elif preference == 2:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        return jsonify({'error':'Invalid preference'}), 400
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download successful.'})
    except Exception as e:
        return jsonify({'error':str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
