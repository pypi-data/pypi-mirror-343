
# MetaRagTool/__init__.py

# Core RAG components
from .RAG.MetaRAG import MetaRAG
from .RAG.DocumentStructs import ChunkingMethod, MyDocument, MyParagraph, MySentence, MyChunk

# Configuration
from .Utils.MetaRagConfig import MetaRagConfig, get_baseline_config, get_best_config

# Encoders
from .Encoders.MyEncoder import MyEncoder
from .Encoders.SentenceTransformerEncoder import SentenceTransformerEncoder
# Add other encoder imports if available, e.g., from .Encoders.MyReranker import MyReranker

# LLMs
from .LLM.LLMIdentity import LLMIdentity
from .LLM.GoogleGemini import Gemini
from .LLM.OpenaiGpt import OpenaiGpt # Assuming this exists based on file names
from .LLM.JudgeLLM import JudgeLLM

# Evaluation
from .Evaluation.Evaluator import test_retrival, judged, full_test_find_in, full_test_find_in_multiHop

# Utilities
from .Utils import Constants
from .Utils import MyUtils
from .Utils import DataLoader
from .Utils import GradioApps # If GradioApps contains reusable components/functions


# Define what gets imported with 'from MetaRagTool import *'
__all__ = [
    'MetaRAG',
    'MetaRagConfig',
    'ChunkingMethod',
    'MyDocument',
    'MyParagraph',
    'MySentence',
    'MyChunk',
    'MyEncoder',
    'SentenceTransformerEncoder',
    # 'MyReranker', # Uncomment if exists and needed
    'LLMIdentity',
    'Gemini',
    'OpenaiGpt',
    'JudgeLLM',
    'test_retrival',
    'judged',
    'full_test_find_in',
    'full_test_find_in_multiHop',
    'Constants',
    'MyUtils',
    'DataLoader',
    'GradioApps', # Uncomment if needed
    'get_baseline_config',
    'get_best_config',
    '__version__'
]

print("MetaRagTool package initialized.")


__version__ = "0.1.5"