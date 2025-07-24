from flask import Flask, render_template, request, jsonify
import subprocess, threading, time

app = Flask(__name__)
ffmpeg_process = None
stream_log = []

def run_ffmpeg(url, key, duration):
    global ffmpeg_process, stream_log
    full_url = f"{url}/{key}"
    stream_log = []
    cmd = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-re",
        "-i", "video.mp4",  # sementara, nanti kita pasang dynamic
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "160k",
        "-f", "flv",
        full_url
    ]
    def target():
        start_time = time.time()
        ffmpeg_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in ffmpeg_process.stdout:
            stream_log.append(line.strip())
            if time.time() - start_time > duration * 3600:
                ffmpeg_process.terminate()
                break
    threading.Thread(target=target).start()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    run_ffmpeg(data["url"], data["key"], int(data["duration"]))
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.terminate()
        return jsonify({"status": "stopped"})
    return jsonify({"status": "no_process"})

@app.route("/log")
def log():
    return jsonify(log=stream_log[-20:])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
