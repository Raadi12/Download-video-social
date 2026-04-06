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
            'quiet': True,
            'no_warnings': True,
            # បន្ថែមជួរខាងក្រោមនេះ
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'addheader': [
                'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language: en-US,en;q=0.9',
                ],
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
        print(f"Error details: {str(e)}") # វានឹងបង្ហាញក្នុង Render Logs
        return {"error": "Server ជាប់រវល់ ឬ Link មិនត្រឹមត្រូវ។ សូមព្យាយាមម្តងទៀត!"}