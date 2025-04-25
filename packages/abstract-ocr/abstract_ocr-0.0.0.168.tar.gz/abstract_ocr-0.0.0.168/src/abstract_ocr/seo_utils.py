from .text_utils import *
from .audio_utils import *
from .functions import (logger,
                        create_key_value,
                        os,
                        timestamp_to_milliseconds,
                        format_timestamp,
                        get_time_now_iso,
                        parse_timestamp,
                        url_join)
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
def generate_info_json(filename: str, prompt: str):
    """
    Build structured info.json for an image, including SEO schema and social metadata.
    """
    file_stem = Path(filename).stem
    ext = Path(filename).suffix.upper().lstrip('.')
    file_path = Path(IMGS_DIR) / filename
    url_path = f"/imgs/{filename}"

    img_meta = get_image_metadata(str(file_path)) if file_path.exists() else {"dimensions": {"width": 0, "height": 0}, "file_size": 0.0}
    gen = generator(prompt, max_length=100, num_return_sequences=1)[0]
    description = gen.get('generated_text', '')[:150]

    info = {
        "alt": file_stem,
        "caption": file_stem,
        "keywords_str": file_stem,
        "filename": file_stem,
        "ext": f".{ext}",
        "title": f"{filename} ({img_meta['dimensions']['width']}×{img_meta['dimensions']['height']})",
        "dimensions": img_meta["dimensions"],
        "file_size": img_meta["file_size"],
        "license": "CC BY-SA 4.0",
        "attribution": "Created by thedailydialectics for educational purposes",
        "longdesc": None,
        "schema": {
            "@context": "https://schema.org",
            "@type": "ImageObject",
            "name": file_stem,
            "description": description,
            "url": f"{DOMAIN}{url_path}",
            "contentUrl": f"{DOMAIN}{url_path}",
            "width": img_meta['dimensions']['width'],
            "height": img_meta['dimensions']['height'],
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
            "creator": {"@type": "Organization", "name": "thedailydialectics"},
            "datePublished": datetime.now().strftime("%Y-%m-%d")
        },
        "social_meta": {
            "og:image": f"{DOMAIN}{url_path}",
            "og:image:alt": None,
            "twitter:card": "summary_large_image",
            "twitter:image": f"{DOMAIN}{url_path}"
        }
    }
    return info

def update_sitemap(video_data,
                   sitemap_path):
    with open(sitemap_path, 'a') as f:
        f.write(f"""
<url>
    <loc>{video_data['canonical_url']}</loc>
    <video:video>
        <video:title>{video_data['seo_title']}</video:title>
        <video:description>{video_data['seo_description']}</video:description>
        <video:thumbnail_loc>{video_data['thumbnail']['file_path']}</video:thumbnail_loc>
        <video:content_loc>{video_data['video_path']}</video:content_loc>
    </video:video>
</url>
""")
import math
from .functions import logger

def _format_srt_timestamp(seconds: float) -> str:
    """
    Convert seconds (e.g. 3.2) into SRT timestamp "HH:MM:SS,mmm"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - math.floor(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def export_srt_whisper(whisper_json: dict, output_path: str):
    """
    Write an .srt file from Whisper's verbose_json format.
    `whisper_json["segments"]` should be a list of {start,end,text,...}.
    """
    logger.info(f"export_srt_whisper: {output_path}")
    segments = whisper_json.get("segments", [])
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, start=1):
            start_ts = _format_srt_timestamp(seg["start"])
            end_ts   = _format_srt_timestamp(seg["end"])
            text     = seg["text"].strip()
            f.write(f"{idx}\n")
            f.write(f"{start_ts} --> {end_ts}\n")
            f.write(f"{text}\n\n")
def export_srt(audio_text, output_path):
    logger.info(f"export_srt: {output_path}")
    with open(output_path, 'w') as f:
        for i, entry in enumerate(audio_text, 1):
            start = entry['start_time'].replace('.', ',')
            end = entry['end_time'].replace('.', ',')
            f.write(f"{i}\n{start} --> {end}\n{entry['text']}\n\n")

def pick_optimal_thumbnail(video_text,
                           combined_keywords):
    scores = []
    for entry in video_text:
        
        text = entry['text'].lower()
        
        keyword_score = sum(1 for kw in combined_keywords if kw.lower() in text)
        
        clarity_score = 1 if len(text.strip()) > 20 else 0  # basic clarity check
        
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        
        total_score = keyword_score + clarity_score + end_phrase_penalty
        
        scores.append((entry['frame'],
                       total_score,
                       text.strip()))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0] if scores else None
def get_frame_number(file_path):
    file_path = '.'.join(file_path.split('.')[:-1])
    return int(file_path.split('_')[-1])
    

def pick_optimal_thumbnail(whisper_result, keywords, thumbnails_directory,*args,**kwargs):
    scores = []
    dirbase = os.path.basename(os.path.dirname(thumbnails_directory))
    
    thumb_name,thumb_ext = os.path.splitext(os.listdir(thumbnails_directory)[0])
    thubnail_items = os.listdir(thumbnails_directory)
    thubnail_items_length = len(thubnail_items)
    if thubnail_items_length> 35:
        thubnail_items = thubnail_items[35:]
    thubnail_items_length = len(thubnail_items)
    if thubnail_items_length> 35:
        thubnail_items = thubnail_items[:-35]
    
    # Get list of thumbnails from directory
    thumbnails = sorted(
        [f for f in thubnail_items if f.endswith(".jpg")],
        key=lambda x: get_frame_number(x) 
    )
    thumbnails = thumbnails or [os.listdir(thumbnails_directory)[
    # Process each Whisper segment
    for segment in whisper_result["segments"]:
        text = segment["text"].lower().strip()
        start_time = segment["start"]        # Find the closest thumbnail based on start time
        frame_number = math.floor(start_time)
        thumbnail_name = f"{dirbase}_frame_{frame_number}{thumb_ext}"
        
        # Check if thumbnail exists
        if thumbnail_name not in thumbnails:
            continue
        
        # Score the caption
        keyword_score = sum(1 for kw in keywords if kw.lower() in text)
        clarity_score = 1 if len(text) > 20 else 0
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        total_score = keyword_score + clarity_score + end_phrase_penalty
        
        # Store thumbnail path, score, and caption
        thumbnail_path = os.path.join(thumbnails_directory, thumbnail_name)
        scores.append((thumbnail_path, total_score, text))
        print(keywords)
    # Sort by score (highest first)
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    return scores[0] if scores else None



def get_from_list(list_obj=None,length=1):
    list_obj = list_obj or []
    if len(list_obj) >= length:
        list_obj = list_obj[:length]
    return list_obj
def get_seo_data(info,
                 uploader=None,
                 domain=None,
                 categories=None,
                 videos_url=None):
    
    info = create_key_value(info,
                            'categories',
                            categories or {'ai': 'Technology', 'cannabis': 'Health', 'elon musk': 'Business'})
    
    info = create_key_value(info,
                            'uploader',
                            uploader or 'The Daily Dialectics')
    
    info = create_key_value(info,
                            'domain',
                            domain or 'https://thedailydialectics.com')
    
    info = create_key_value(info,
                            'videos_url',
                            videos_url or f"{info['domain']}/videos")
    
    for keyword_key in ['combined_keywords','keywords']:
        keywords = info.get(keyword_key,[])
        if keywords and len(keywords)>0:
            break
    primary_keyword = keywords[0] if keywords and len(keywords)>0 else info['filename']
    seo_title = f"{primary_keyword} - {info['filename']}"
    info['seo_title'] = get_from_list(seo_title,length=70)
    summary = info.get('summary','')
    summary_desc = get_from_list(summary,length=150)
    keywords_str = ', '.join(get_from_list(keywords,length=3))
    seo_desc = f"{summary_desc} Explore {keywords_str}. Visit thedailydialectics.com for more!"
    info['seo_description'] = get_from_list(seo_desc,length=300)
    
    info['seo_tags'] = [kw for kw in keywords if kw.lower() not in ['video','audio','file']]
    video_text = info.get('video_text')
    info['thumbnail']={}
    if video_text and len(video_text)>0:
        thumnail_data = video_text[0]
        info['thumbnail']['file_path']= os.path.join(info['thumbnails_directory'],
                                                     thumnail_data.get("frame"))
        
        info['thumbnail']['alt_text']= thumnail_data.get("text")
    whisper_json = info["whisper_result"]
    thumbnail_score = pick_optimal_thumbnail(whisper_json,
                                               keywords,
                                              info["thumbnails_directory"])
    if thumbnail_score:
        best_frame, score, matched_text = thumbnail_score
        
        info['thumbnail']['file_path']= os.path.join(info['thumbnails_directory'],
                                                     best_frame)
        
        info['thumbnail']['alt_text']= get_from_list(matched_text,length=100)
        basename = os.path.basename(info['thumbnail']['file_path'])
        filename,ext = os.path.splitext(basename)
        prompt = f"Generate SEO metadata for {filename} with the video text info['thumbnail']['alt_text']"
        info['thumbnail']['seo_data']= generate_info_json(info['thumbnail']['file_path'], prompt)
    
    audio = AudioSegment.from_wav(info['audio_path'])
    
    info['duration_seconds'] = len(audio) / 1000
    
    info['duration_formatted'] = format_timestamp(len(audio))
    
    

    export_srt_whisper(
        whisper_json,
        os.path.join(info["info_directory"], "captions.srt")
    )
    
    info['captions_path'] = os.path.join(info['info_directory'],
                                         "captions.srt")
    
    info['schema_markup'] = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": info['seo_title'],
        "description": info['seo_description'],
        "thumbnailUrl": info['thumbnail']['file_path'],
        "duration": f"PT{int(info['duration_seconds'] // 60)}M{int(info['duration_seconds'] % 60)}S",
        "uploadDate": get_time_now_iso(),
        "contentUrl": info['video_path'],
        "keywords": info['seo_tags']
    }
    
    info['social_metadata'] = {
        "og:title": info['seo_title'],
        "og:description": info['seo_description'],
        "og:image": info['thumbnail']['file_path'],
        "og:video": info['video_path'],
        "twitter:card": "player",
        "twitter:title": info['seo_title'],
        "twitter:description": info['seo_description'],
        "twitter:image": info['thumbnail']['file_path']
    }
    
    info['category'] = next((v for k, v in info['categories'].items() if k in ' '.join(info['seo_tags']).lower()), 'General')
    
    info['uploader'] = {"name": info['uploader'],
                        "url": info['domain']}
    
    info['publication_date'] = get_time_now_iso()
    
    video = mp.VideoFileClip(info['video_path'])
    
    info['file_metadata'] = {
        'resolution': f"{video.w}x{video.h}",
        'format': 'MP4',
        'file_size_mb': os.path.getsize(info['video_path']) / (1024 * 1024)
    }
    
    video.close()
    
    update_sitemap(info,
                   f"{info['parent_dir']}/../sitemap.xml")
    
    return info
