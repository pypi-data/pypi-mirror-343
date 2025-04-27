"""
JCL Parser package for parsing and analyzing JCL (Job Control Language) files
"""

from .jcl_parser import JCLParser
from .interface import JCLInterface
from .logger import logger, LogLevel
from extractors.job_extractor import extract_jobs
from extractors.step_extractor import extract_steps
from extractors.proc_extractor import extract_procedures
from extractors.comment_extractor import extract_comments
from extractors.base_extractor import BaseExtractor

# Package metadata
__version__ = "0.1.0"
__package_name__ = "legacylens_jcl_parser"

__all__ = ['JCLParser', 'JCLInterface', 'logger', 
           'LogLevel','extract_jobs', 'extract_steps', 'extract_procedures', 
           'extract_comments', 'BaseExtractor']