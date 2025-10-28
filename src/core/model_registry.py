"""
Complete Model Registry - All 30+ Bytez AI Models
Centralized configuration and management
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ModelType(Enum):
    """Model type categories"""
    TEXT_TO_IMAGE = "text-to-image"
    TEXT_TO_VIDEO = "text-to-video"
    TEXT_TO_SPEECH = "text-to-speech"
    TEXT_TO_AUDIO = "text-to-audio"
    IMAGE_ANALYSIS = "image-analysis"
    VIDEO_ANALYSIS = "video-analysis"
    AUDIO_ANALYSIS = "audio-analysis"
    TEXT_GENERATION = "text-generation"
    TEXT_CLASSIFICATION = "text-classification"
    VISUAL_QA = "visual-qa"


@dataclass
class ModelConfig:
    """Configuration for a single model"""
    id: str
    name: str
    type: ModelType
    bytez_id: str
    rate_limit: int  # requests per minute
    min_tier: str  # minimum tier required
    nsfw_capable: bool = False
    description: str = ""
    

class ModelRegistry:
    """
    Central registry for all AI models
    """
    
    def __init__(self):
        self.models = self._initialize_models()
    
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Initialize all 30+ models"""
        
        models = {}
        
        # ==================== TEXT-TO-IMAGE MODELS ====================
        
        models["dreamlike-photoreal"] = ModelConfig(
            id="dreamlike-photoreal",
            name="Dreamlike Photoreal",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id=os.getenv("BYTEZ_IMAGE_DREAMLIKE_PHOTOREAL", "dreamlike-art/dreamlike-photoreal-2.0"),
            rate_limit=10,
            min_tier="free",
            description="Photorealistic image generation"
        )
        
        models["stable-diffusion-xl"] = ModelConfig(
            id="stable-diffusion-xl",
            name="Stable Diffusion XL",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id=os.getenv("BYTEZ_IMAGE_STABLE_DIFFUSION_XL", "stabilityai/stable-diffusion-xl-base-1.0"),
            rate_limit=10,
            min_tier="free",
            description="High-quality general purpose image generation"
        )
        
        models["dreamlike-anime"] = ModelConfig(
            id="dreamlike-anime",
            name="Dreamlike Anime",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id=os.getenv("BYTEZ_IMAGE_DREAMLIKE_ANIME", "dreamlike-art/dreamlike-anime-1.0"),
            rate_limit=10,
            min_tier="free",
            description="Anime-style image generation"
        )
        
        models["nsfw-gen"] = ModelConfig(
            id="nsfw-gen",
            name="NSFW Generator",
            type=ModelType.TEXT_TO_IMAGE,
            bytez_id=os.getenv("BYTEZ_IMAGE_NSFW_GEN", "UnfilteredAI/NSFW-gen-v2.1"),
            rate_limit=5,
            min_tier="prime",
            nsfw_capable=True,
            description="Adult content generation (Prime+)"
        )
        
        # ==================== TEXT-TO-VIDEO MODELS ====================
        
        models["text-to-video-ms"] = ModelConfig(
            id="text-to-video-ms",
            name="Text-to-Video MS",
            type=ModelType.TEXT_TO_VIDEO,
            bytez_id=os.getenv("BYTEZ_TEXT_TO_VIDEO_MS", "ali-vilab/text-to-video-ms-1.7b"),
            rate_limit=5,
            min_tier="basic",
            description="Basic video generation"
        )
        
        models["zeroscope"] = ModelConfig(
            id="zeroscope",
            name="Zeroscope V2",
            type=ModelType.TEXT_TO_VIDEO,
            bytez_id=os.getenv("BYTEZ_TEXT_TO_VIDEO_ZEROSCOPE", "cerspense/zeroscope_v2_576w"),
            rate_limit=5,
            min_tier="pro",
            description="High-quality video generation"
        )
        
        models["ltx-video"] = ModelConfig(
            id="ltx-video",
            name="LTX Video",
            type=ModelType.TEXT_TO_VIDEO,
            bytez_id=os.getenv("BYTEZ_TEXT_TO_VIDEO_LTX", "Lightricks/LTX-Video-0.9.7-dev"),
            rate_limit=3,
            min_tier="lifetime",
            description="Premium video generation (Lifetime only)"
        )
        
        # ==================== TEXT-TO-SPEECH MODELS ====================
        
        models["bark-small"] = ModelConfig(
            id="bark-small",
            name="Bark Small",
            type=ModelType.TEXT_TO_SPEECH,
            bytez_id=os.getenv("BYTEZ_TTS_BARK_SMALL", "suno/bark-small"),
            rate_limit=10,
            min_tier="basic",
            description="Fast text-to-speech"
        )
        
        models["bark"] = ModelConfig(
            id="bark",
            name="Bark",
            type=ModelType.TEXT_TO_SPEECH,
            bytez_id=os.getenv("BYTEZ_TTS_BARK", "suno/bark"),
            rate_limit=5,
            min_tier="pro",
            description="High-quality text-to-speech"
        )
        
        # ==================== TEXT-TO-AUDIO MODELS ====================
        
        models["musicgen-small"] = ModelConfig(
            id="musicgen-small",
            name="MusicGen Small",
            type=ModelType.TEXT_TO_AUDIO,
            bytez_id=os.getenv("BYTEZ_AUDIO_MUSICGEN_SMALL", "facebook/musicgen-stereo-small"),
            rate_limit=10,
            min_tier="pro",
            description="Music generation"
        )
        
        models["musicgen-large"] = ModelConfig(
            id="musicgen-large",
            name="MusicGen Large",
            type=ModelType.TEXT_TO_AUDIO,
            bytez_id=os.getenv("BYTEZ_AUDIO_MUSICGEN_LARGE", "facebook/musicgen-stereo-large"),
            rate_limit=5,
            min_tier="lifetime",
            description="High-quality music generation"
        )
        
        # ==================== IMAGE ANALYSIS MODELS ====================
        
        models["blip-caption"] = ModelConfig(
            id="blip-caption",
            name="BLIP Image Captioning",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_IMAGE_TO_TEXT_BLIP", "Salesforce/blip-image-captioning-base"),
            rate_limit=20,
            min_tier="free",
            description="Image captioning and description"
        )
        
        models["detr-detection"] = ModelConfig(
            id="detr-detection",
            name="DETR Object Detection",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_OBJECT_DETECTION", "facebook/detr-resnet-50"),
            rate_limit=20,
            min_tier="free",
            description="Object detection in images"
        )
        
        models["vit-classification"] = ModelConfig(
            id="vit-classification",
            name="ViT Image Classification",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_IMAGE_CLASSIFICATION_VIT", "google/vit-base-patch16-224"),
            rate_limit=20,
            min_tier="free",
            description="Image classification"
        )
        
        models["clip-zero-shot"] = ModelConfig(
            id="clip-zero-shot",
            name="CLIP Zero-Shot Classification",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_ZERO_SHOT_IMAGE_CLASSIFICATION", "BilelDJ/clip-hugging-face-finetuned"),
            rate_limit=20,
            min_tier="free",
            description="Zero-shot image classification"
        )
        
        models["nomic-vision"] = ModelConfig(
            id="nomic-vision",
            name="Nomic Vision Embeddings",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_IMAGE_FEATURE_EXTRACTION", "nomic-ai/nomic-embed-vision-v1"),
            rate_limit=30,
            min_tier="free",
            description="Image feature extraction"
        )
        
        models["segformer"] = ModelConfig(
            id="segformer",
            name="Segformer Segmentation",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_IMAGE_SEGMENTATION", "sayeed99/segformer-b3-fashion"),
            rate_limit=15,
            min_tier="basic",
            description="Image segmentation"
        )
        
        models["depth-estimation"] = ModelConfig(
            id="depth-estimation",
            name="Depth Estimation",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_DEPTH_ESTIMATION", "vinvino02/glpn-nyu"),
            rate_limit=15,
            min_tier="basic",
            description="Depth map generation"
        )
        
        models["sam-mask"] = ModelConfig(
            id="sam-mask",
            name="SAM Mask Generation",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_MASK_GENERATION", "facebook/sam-vit-base"),
            rate_limit=10,
            min_tier="pro",
            description="Segmentation mask generation"
        )
        
        models["owl-detection"] = ModelConfig(
            id="owl-detection",
            name="OWL Zero-Shot Detection",
            type=ModelType.IMAGE_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_ZERO_SHOT_OBJECT_DETECTION", "google/owlv2-base-patch16-finetuned"),
            rate_limit=15,
            min_tier="basic",
            description="Zero-shot object detection"
        )
        
        # ==================== VIDEO ANALYSIS ====================
        
        models["video-classifier"] = ModelConfig(
            id="video-classifier",
            name="Video Classifier",
            type=ModelType.VIDEO_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_VIDEO_CLASSIFIER", "ahmedabdo/video-classifier"),
            rate_limit=10,
            min_tier="basic",
            description="Video content classification"
        )
        
        # ==================== AUDIO ANALYSIS ====================
        
        models["audio-classification"] = ModelConfig(
            id="audio-classification",
            name="Audio Classification",
            type=ModelType.AUDIO_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_AUDIO_CLASSIFICATION", "aaraki/wav2vec2-base-finetuned-ks"),
            rate_limit=15,
            min_tier="free",
            description="Audio content classification"
        )
        
        models["speech-recognition"] = ModelConfig(
            id="speech-recognition",
            name="Speech Recognition",
            type=ModelType.AUDIO_ANALYSIS,
            bytez_id=os.getenv("BYTEZ_SPEECH_RECOGNITION", "facebook/data2vec-audio-base-960h"),
            rate_limit=15,
            min_tier="free",
            description="Automatic speech recognition"
        )
        
        # ==================== TEXT MODELS ====================
        
        models["flan-t5"] = ModelConfig(
            id="flan-t5",
            name="FLAN-T5",
            type=ModelType.TEXT_GENERATION,
            bytez_id=os.getenv("BYTEZ_TEXT_FLAN_T5", "google/flan-t5-base"),
            rate_limit=30,
            min_tier="free",
            description="Text generation"
        )
        
        models["sentence-similarity"] = ModelConfig(
            id="sentence-similarity",
            name="Sentence Similarity",
            type=ModelType.TEXT_CLASSIFICATION,
            bytez_id=os.getenv("BYTEZ_SIMILARITY_MINILM", "sentence-transformers/all-MiniLM-L6-v2"),
            rate_limit=50,
            min_tier="free",
            description="Sentence similarity comparison"
        )
        
        models["nomic-text"] = ModelConfig(
            id="nomic-text",
            name="Nomic Text Embeddings",
            type=ModelType.TEXT_CLASSIFICATION,
            bytez_id=os.getenv("BYTEZ_FEATURE_EXTRACTION_NOMIC", "nomic-ai/nomic-embed-text-v1.5"),
            rate_limit=50,
            min_tier="free",
            description="Text feature extraction"
        )
        
        models["zero-shot-classification"] = ModelConfig(
            id="zero-shot-classification",
            name="Zero-Shot Classification",
            type=ModelType.TEXT_CLASSIFICATION,
            bytez_id=os.getenv("BYTEZ_ZERO_SHOT_CLASSIFICATION", "facebook/bart-large-mnli"),
            rate_limit=40,
            min_tier="free",
            description="Zero-shot text classification"
        )
        
        models["sentiment-analysis"] = ModelConfig(
            id="sentiment-analysis",
            name="Sentiment Analysis",
            type=ModelType.TEXT_CLASSIFICATION,
            bytez_id=os.getenv("BYTEZ_TEXT_CLASSIFICATION_SENTIMENT", "AdamCodd/distilbert-base-uncased-finetuned-sentiment-amazon"),
            rate_limit=40,
            min_tier="free",
            description="Sentiment analysis"
        )
        
        models["ner"] = ModelConfig(
            id="ner",
            name="Named Entity Recognition",
            type=ModelType.TEXT_CLASSIFICATION,
            bytez_id=os.getenv("BYTEZ_TOKEN_CLASSIFICATION_NER", "dslim/bert-base-NER"),
            rate_limit=40,
            min_tier="free",
            description="Named entity recognition"
        )
        
        models["summarization"] = ModelConfig(
            id="summarization",
            name="Text Summarization",
            type=ModelType.TEXT_GENERATION,
            bytez_id=os.getenv("BYTEZ_SUMMARIZATION", "ainize/bart-base-cnn"),
            rate_limit=15,
            min_tier="free",
            description="Text summarization"
        )
        
        models["question-answering"] = ModelConfig(
            id="question-answering",
            name="Question Answering",
            type=ModelType.TEXT_GENERATION,
            bytez_id=os.getenv("BYTEZ_QUESTION_ANSWERING", "deepset/roberta-base-squad2"),
            rate_limit=25,
            min_tier="free",
            description="Question answering"
        )
        
        models["translation"] = ModelConfig(
            id="translation",
            name="Translation (EN-ZH)",
            type=ModelType.TEXT_GENERATION,
            bytez_id=os.getenv("BYTEZ_TRANSLATION_EN_ZH", "Helsinki-NLP/opus-mt-en-zh"),
            rate_limit=20,
            min_tier="free",
            description="English to Chinese translation"
        )
        
        models["fill-mask"] = ModelConfig(
            id="fill-mask",
            name="Fill Mask",
            type=ModelType.TEXT_GENERATION,
            bytez_id=os.getenv("BYTEZ_FILL_MASK", "almanach/camembert-base"),
            rate_limit=30,
            min_tier="free",
            description="Fill masked text"
        )
        
        # ==================== VISUAL QA ====================
        
        models["blip-vqa"] = ModelConfig(
            id="blip-vqa",
            name="BLIP Visual QA",
            type=ModelType.VISUAL_QA,
            bytez_id=os.getenv("BYTEZ_VISUAL_QA", "Salesforce/blip-vqa-base"),
            rate_limit=15,
            min_tier="free",
            description="Visual question answering"
        )
        
        models["document-qa"] = ModelConfig(
            id="document-qa",
            name="Document QA",
            type=ModelType.VISUAL_QA,
            bytez_id=os.getenv("BYTEZ_DOCUMENT_QA", "cloudqi/CQI_Visual_Question_Awnser_PT_v0"),
            rate_limit=15,
            min_tier="basic",
            description="Document question answering"
        )
        
        return models
    
    def get_model(self, model_id: str) -> Optional[ModelConfig]:
        """Get model configuration by ID"""
        return self.models.get(model_id)
    
    def get_models_by_type(self, model_type: ModelType) -> List[ModelConfig]:
        """Get all models of a specific type"""
        return [m for m in self.models.values() if m.type == model_type]
    
    def get_models_for_tier(self, tier: str) -> List[ModelConfig]:
        """Get all models available for a tier"""
        tier_order = ["free", "basic", "pro", "prime", "super", "lifetime"]
        tier_index = tier_order.index(tier) if tier in tier_order else 0
        
        return [
            m for m in self.models.values()
            if tier_order.index(m.min_tier) <= tier_index
        ]
    
    def get_nsfw_models(self) -> List[ModelConfig]:
        """Get all NSFW-capable models"""
        return [m for m in self.models.values() if m.nsfw_capable]
    
    def list_all_models(self) -> Dict[str, ModelConfig]:
        """Get all models"""
        return self.models


# Global registry instance
_registry = None


def get_model_registry() -> ModelRegistry:
    """Get global model registry instance"""
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
