"""
Complete Model Registry - All 35 Bytez Models
"""

from enum import Enum
from typing import Dict, List
from dataclasses import dataclass


class ModelType(Enum):
    """Model categories"""
    TEXT_TO_IMAGE = "text-to-image"
    TEXT_TO_VIDEO = "text-to-video"
    TEXT_TO_AUDIO = "text-to-audio"
    IMAGE_ANALYSIS = "image-analysis"
    VIDEO_ANALYSIS = "video-analysis"
    AUDIO_ANALYSIS = "audio-analysis"
    TEXT_PROCESSING = "text-processing"
    VISUAL_QA = "visual-qa"


@dataclass
class Model:
    """Model configuration"""
    id: str
    name: str
    type: ModelType
    bytez_id: str
    min_tier: str = "free"
    nsfw: bool = False


class ModelRegistry:
    """Registry of all 35 AI models"""
    
    MODELS = {
        # TEXT-TO-IMAGE (4 models)
        "dreamlike-photoreal": Model(
            id="dreamlike-photoreal",
            name="Dreamlike Photoreal",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id="dreamlike-art/dreamlike-photoreal-2.0",
            min_tier="free"
        ),
        "stable-diffusion-xl": Model(
            id="stable-diffusion-xl",
            name="Stable Diffusion XL",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id="stabilityai/stable-diffusion-xl-base-1.0",
            min_tier="free"
        ),
        "dreamlike-anime": Model(
            id="dreamlike-anime",
            name="Dreamlike Anime",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id="dreamlike-art/dreamlike-anime-1.0",
            min_tier="free"
        ),
        "nsfw-gen": Model(
            id="nsfw-gen",
            name="NSFW Generator",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id="UnfilteredAI/NSFW-gen-v2.1",
            min_tier="prime",
            nsfw=True
        ),
        
        # TEXT-TO-VIDEO (3 models)
        "text-to-video-ms": Model(
            id="text-to-video-ms",
            name="Text-to-Video MS",
            type=ModelType.TEXT_TO_VIDEO,
            bytez_id="ali-vilab/text-to-video-ms-1.7b",
            min_tier="basic"
        ),
        "zeroscope": Model(
            id="zeroscope",
            name="Zeroscope V2",
            type=ModelType.TEXT_TO_VIDEO,
            bytez_id="cerspense/zeroscope_v2_576w",
            min_tier="pro"
        ),
        "ltx-video": Model(
            id="ltx-video",
            name="LTX Video",
            type=ModelType.TEXT_TO_VIDEO,
            bytez_id="Lightricks/LTX-Video-0.9.7-dev",
            min_tier="lifetime"
        ),
        
        # TEXT-TO-AUDIO (4 models)
        "bark-small": Model(
            id="bark-small",
            name="Bark Small TTS",
            type=ModelType.TEXT_TO_AUDIO,
            bytez_id="suno/bark-small",
            min_tier="basic"
        ),
        "bark": Model(
            id="bark",
            name="Bark TTS",
            type=ModelType.TEXT_TO_AUDIO,
            bytez_id="suno/bark",
            min_tier="pro"
        ),
        "musicgen-small": Model(
            id="musicgen-small",
            name="MusicGen Small",
            type=ModelType.TEXT_TO_AUDIO,
            bytez_id="facebook/musicgen-stereo-small",
            min_tier="pro"
        ),
        "musicgen-large": Model(
            id="musicgen-large",
            name="MusicGen Large",
            type=ModelType.TEXT_TO_AUDIO,
            bytez_id="facebook/musicgen-stereo-large",
            min_tier="lifetime"
        ),
        
        # IMAGE ANALYSIS (9 models)
        "blip-caption": Model(
            id="blip-caption",
            name="BLIP Image Captioning",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="Salesforce/blip-image-captioning-base",
            min_tier="free"
        ),
        "detr-detection": Model(
            id="detr-detection",
            name="DETR Object Detection",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="facebook/detr-resnet-50",
            min_tier="free"
        ),
        "vit-classification": Model(
            id="vit-classification",
            name="ViT Classification",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="google/vit-base-patch16-224",
            min_tier="free"
        ),
        "clip-zero-shot": Model(
            id="clip-zero-shot",
            name="CLIP Zero-Shot",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="BilelDJ/clip-hugging-face-finetuned",
            min_tier="free"
        ),
        "nomic-vision": Model(
            id="nomic-vision",
            name="Nomic Vision Embeddings",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="nomic-ai/nomic-embed-vision-v1",
            min_tier="free"
        ),
        "segformer": Model(
            id="segformer",
            name="Segformer Segmentation",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="sayeed99/segformer-b3-fashion",
            min_tier="basic"
        ),
        "depth-estimation": Model(
            id="depth-estimation",
            name="Depth Estimation",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="vinvino02/glpn-nyu",
            min_tier="basic"
        ),
        "sam-mask": Model(
            id="sam-mask",
            name="SAM Mask Generation",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="facebook/sam-vit-base",
            min_tier="pro"
        ),
        "owl-detection": Model(
            id="owl-detection",
            name="OWL Zero-Shot Detection",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id="google/owlv2-base-patch16-finetuned",
            min_tier="basic"
        ),
        
        # VIDEO ANALYSIS (1 model)
        "video-classifier": Model(
            id="video-classifier",
            name="Video Classifier",
            type=ModelType.VIDEO_ANALYSIS,
            bytez_id="ahmedabdo/video-classifier",
            min_tier="basic"
        ),
        
        # AUDIO ANALYSIS (2 models)
        "audio-classification": Model(
            id="audio-classification",
            name="Audio Classification",
            type=ModelType.AUDIO_ANALYSIS,
            bytez_id="aaraki/wav2vec2-base-finetuned-ks",
            min_tier="free"
        ),
        "speech-recognition": Model(
            id="speech-recognition",
            name="Speech Recognition",
            type=ModelType.AUDIO_ANALYSIS,
            bytez_id="facebook/data2vec-audio-base-960h",
            min_tier="free"
        ),
        
        # TEXT PROCESSING (10 models)
        "flan-t5": Model(
            id="flan-t5",
            name="FLAN-T5",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="google/flan-t5-base",
            min_tier="free"
        ),
        "sentence-similarity": Model(
            id="sentence-similarity",
            name="Sentence Similarity",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="sentence-transformers/all-MiniLM-L6-v2",
            min_tier="free"
        ),
        "nomic-text": Model(
            id="nomic-text",
            name="Nomic Text Embeddings",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="nomic-ai/nomic-embed-text-v1.5",
            min_tier="free"
        ),
        "zero-shot-classification": Model(
            id="zero-shot-classification",
            name="Zero-Shot Classification",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="facebook/bart-large-mnli",
            min_tier="free"
        ),
        "sentiment-analysis": Model(
            id="sentiment-analysis",
            name="Sentiment Analysis",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="AdamCodd/distilbert-base-uncased-finetuned-sentiment-amazon",
            min_tier="free"
        ),
        "ner": Model(
            id="ner",
            name="Named Entity Recognition",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="dslim/bert-base-NER",
            min_tier="free"
        ),
        "summarization": Model(
            id="summarization",
            name="Text Summarization",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="ainize/bart-base-cnn",
            min_tier="free"
        ),
        "question-answering": Model(
            id="question-answering",
            name="Question Answering",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="deepset/roberta-base-squad2",
            min_tier="free"
        ),
        "translation": Model(
            id="translation",
            name="Translation EN-ZH",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="Helsinki-NLP/opus-mt-en-zh",
            min_tier="free"
        ),
        "fill-mask": Model(
            id="fill-mask",
            name="Fill Mask",
            type=ModelType.TEXT_PROCESSING,
            bytez_id="almanach/camembert-base",
            min_tier="free"
        ),
        
        # VISUAL QA (2 models)
        "blip-vqa": Model(
            id="blip-vqa",
            name="BLIP Visual QA",
            type=ModelType.VISUAL_QA,
            bytez_id="Salesforce/blip-vqa-base",
            min_tier="free"
        ),
        "document-qa": Model(
            id="document-qa",
            name="Document QA",
            type=ModelType.VISUAL_QA,
            bytez_id="cloudqi/CQI_Visual_Question_Awnser_PT_v0",
            min_tier="basic"
        ),
    }
    
    @classmethod
    def get_model(cls, model_id: str) -> Model:
        """Get model by ID"""
        return cls.MODELS.get(model_id)
    
    @classmethod
    def get_models_by_type(cls, model_type: ModelType) -> List[Model]:
        """Get all models of a type"""
        return [m for m in cls.MODELS.values() if m.type == model_type]
    
    @classmethod
    def get_models_for_tier(cls, tier: str) -> List[Model]:
        """Get models available for tier"""
        tier_order = ["free", "basic", "pro", "prime", "super", "lifetime"]
        tier_index = tier_order.index(tier) if tier in tier_order else 0
        
        return [
            m for m in cls.MODELS.values()
            if tier_order.index(m.min_tier) <= tier_index
        ]
    
    @classmethod
    def count_models(cls) -> int:
        """Total model count"""
        return len(cls.MODELS)
