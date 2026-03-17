import yt_dlp
import os

def download_video(url, quality, download_folder="downloads/"):
    os.makedirs(download_folder, exist_ok=True)

    output = os.path.join(download_folder, "%(title)s.%(ext)s")

    # 🎵 تحميل الصوت فقط (احترافي)
    if quality == "audio":
        ydl_opts = {
            "format": "best",
            "outtmpl": output,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

    # 🎥 تحميل فيديو بجودة معينة
    else:
        ydl_opts = {
            "format": f"bestvideo[height<={quality}]+bestaudio/bestvideo+bestaudio/best",
            "outtmpl": output,
            "merge_output_format": "mp4",
            "quiet": True,
            "noplaylist": True
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # اسم الملف النهائي
            if quality == "audio":
                filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
            else:
                filename = ydl.prepare_filename(info)

        return filename

    except Exception as e:
        print("Download error:", e)
        return None