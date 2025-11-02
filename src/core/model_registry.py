"""
Complete Model Registry - All Available AI Models
Organized by category for Memory Lane
"""

# Your API Keys (1 concurrent request per key)
API_KEYS = {
    "key1": "1043901e59687190c4eebd9f12f08f2d",
    "key2": "de732f0e5f363e09939178f908d484d7"
}

# Image Generation Models
IMAGE_MODELS = {
    "photoreal": "dreamlike-art/dreamlike-photoreal-2.0",
    "anime": "dreamlike-art/dreamlike-anime-1.0",
    "stable_xl": "stabilityai/stable-diffusion-xl-base-1.0",
    "stable_v15": "stable-diffusion-v1-5/stable-diffusion-v1-5",
    "stable_v14": "CompVis/stable-diffusion-v1-4",
    "kohaku": "KBlueLeaf/Kohaku-XL-Zeta",
    "dreamshaper": "Lykon/DreamShaper",
    "pony": "kitty7779/ponyDiffusionV6XL",
    "noobai": "Laxhar/noobai-XL-1.0"
}

# Video Generation Models
VIDEO_MODELS = {
    "text_to_video": "ali-vilab/text-to-video-ms-1.7b",
    "zeroscope": "cerspense/zeroscope_v2_576w",
    "ltx_video": "Lightricks/LTX-Video-0.9.7-dev"
}

# Audio Generation Models
AUDIO_MODELS = {
    "speech_small": "suno/bark-small",
    "speech_full": "suno/bark",
    "music_small": "facebook/musicgen-stereo-small",
    "music_large": "facebook/musicgen-stereo-large",
    "music_melody": "facebook/musicgen-stereo-melody",
    "music_melody_large": "facebook/musicgen-melody-large"
}

# Text Generation Models
TEXT_MODELS = {
    "gpt4": "openai/gpt-4o",
    "flan_t5": "google/flan-t5-base",
    "arch_router": "katanemo/Arch-Router-1.5B"
}

# Image Understanding Models
IMAGE_UNDERSTANDING = {
    "caption": "Salesforce/blip-image-captioning-base",
    "vqa": "Salesforce/blip-vqa-base",
    "classification": "google/vit-base-patch16-224",
    "zero_shot_classification": "BilelDJ/clip-hugging-face-finetuned",
    "object_detection": "facebook/detr-resnet-50",
    "zero_shot_detection": "google/owlv2-base-patch16-finetuned",
    "segmentation": "sayeed99/segformer-b3-fashion",
    "depth": "vinvino02/glpn-nyu",
    "mask_generation": "facebook/sam-vit-base",
    "feature_extraction": "nomic-ai/nomic-embed-vision-v1"
}

# Video Understanding Models
VIDEO_UNDERSTANDING = {
    "classification": "ahmedabdo/video-classifier"
}

# Text Understanding Models
TEXT_UNDERSTANDING = {
    "sentiment": "AdamCodd/distilbert-base-uncased-finetuned-sentiment-amazon",
    "ner": "dslim/bert-base-NER",
    "summarization": "ainize/bart-base-cnn",
    "qa": "deepset/roberta-base-squad2",
    "translation": "Helsinki-NLP/opus-mt-en-zh",
    "fill_mask": "almanach/camembert-base",
    "similarity": "sentence-transformers/all-MiniLM-L6-v2",
    "feature_extraction": "nomic-ai/nomic-embed-text-v1.5",
    "zero_shot": "facebook/bart-large-mnli"
}

# Audio Understanding Models
AUDIO_UNDERSTANDING = {
    "classification": "aaraki/wav2vec2-base-finetuned-ks",
    "speech_recognition": "facebook/data2vec-audio-base-960h"
}

# Document Understanding Models
DOCUMENT_UNDERSTANDING = {
    "vqa": "cloudqi/CQI_Visual_Question_Awnser_PT_v0"
}

# Model Categories for Memory Lane
MEMORY_LANE_MODELS = {
    "conversation": {
        "primary": "openai/gpt-4o",
        "fallback": "google/flan-t5-base"
    },
    "image_generation": {
        "photoreal": "dreamlike-art/dreamlike-photoreal-2.0",
        "anime": "dreamlike-art/dreamlike-anime-1.0",
        "artistic": "Lykon/DreamShaper"
    },
    "video_generation": {
        "default": "ali-vilab/text-to-video-ms-1.7b",
        "hd": "cerspense/zeroscope_v2_576w"
    },
    "voice": {
        "speech": "suno/bark-small",
        "full": "suno/bark"
    },
    "music": {
        "background": "facebook/musicgen-stereo-small",
        "quality": "facebook/musicgen-stereo-large"
    },
    "understanding": {
        "image_caption": "Salesforce/blip-image-captioning-base",
        "sentiment": "AdamCodd/distilbert-base-uncased-finetuned-sentiment-amazon"
    }
}

# Rate Limit Info
RATE_LIMITS = {
    "concurrent_per_key": 1,
    "total_keys": 2,
    "max_concurrent": 2,
    "hits_per_month": "unlimited"
}

def get_model_for_task(task: str, quality: str = "default") -> str:
    """Get the best model for a specific task"""
    task_map = {
        "conversation": MEMORY_LANE_MODELS["conversation"]["primary"],
        "image": MEMORY_LANE_MODELS["image_generation"].get(quality, 
                MEMORY_LANE_MODELS["image_generation"]["photoreal"]),
        "video": MEMORY_LANE_MODELS["video_generation"].get(quality,
                MEMORY_LANE_MODELS["video_generation"]["default"]),
        "speech": MEMORY_LANE_MODELS["voice"]["speech"],
        "music": MEMORY_LANE_MODELS["music"]["background"]
    }
    return task_map.get(task, MEMORY_LANE_MODELS["conversation"]["primary"])
