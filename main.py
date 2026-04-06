from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# បើកសិទ្ធិឱ្យ HTML អាចទាញទិន្នន័យបាន (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
def get_video(url: str):
    try:
        # បន្ថែមបន្តិចដើម្បីឱ្យទាញយកបានលឿន និងច្បាស់
        ydl_opts = {
            'format': 'best',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        } 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # បងត្រូវកែត្រង់ចំណុច return នេះ
            return {
                "title": info.get('title', 'Video Download'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": info.get('url')
            }
    except Exception as e:
        return {"error": str(e)}