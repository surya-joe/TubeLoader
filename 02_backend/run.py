from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json

    url = data.get('url')
    preference = data.get('preference')
    output_path = data.get('output_path', '')
    cookies_file = data.get('cookies_file', '')
    cookies_data = data.get('cookies_data', '')  # Accept cookies as raw data

    if not url:
        return jsonify({"error": "Invalid URL"}), 400

    ydl_opts = {
        'outtmpl': f'./outputs/{output_path}/%(title)s.%(ext)s',
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
        return jsonify({'error': 'Invalid preference'}), 400

    # Handle cookies file or raw cookies data
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file
    elif cookies_data:
        # Save cookies_data to a temporary file
        temp_cookie_file = './cookies.txt'
        with open(temp_cookie_file, 'w') as f:
            f.write(cookies_data)
        ydl_opts['cookiefile'] = temp_cookie_file

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Cleanup temporary cookie file if used
        if cookies_data and os.path.exists(temp_cookie_file):
            os.remove(temp_cookie_file)
        return jsonify({'message': 'Download successful.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
