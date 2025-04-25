# oblix/connectors/documents/processors.py
import os
import re
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
import json
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class TextChunker:
    """
    Splits text into manageable chunks for embedding and retrieval.
    
    This class provides various strategies for splitting documents into
    smaller chunks suitable for embedding in vector databases. It includes
    methods for splitting by tokens, characters, or semantic units.
    
    Attributes:
        chunk_size (int): Target size for chunks (in tokens or characters)
        chunk_overlap (int): Number of tokens/chars to overlap between chunks
        length_function (callable): Function to measure text length (default: character count)
    """
    
    def __init__(
        self, 
        chunk_size: int = 1024, 
        chunk_overlap: int = 200,
        length_function = None
    ):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size (int): Target size for chunks
            chunk_overlap (int): Overlap between chunks
            length_function (callable): Function to compute text length (default: len)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function or len
        
    def split_by_characters(self, text: str) -> List[str]:
        """
        Split text into chunks based on character count.
        
        Args:
            text (str): Text to split
            
        Returns:
            List[str]: List of text chunks
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            # Find end of current chunk
            end = min(start + self.chunk_size, text_len)
            
            # If we're not at the end, try to find a natural break point
            if end < text_len:
                # Try to find sentence boundary
                sentence_end = max(
                    text.rfind('. ', start, end),
                    text.rfind('? ', start, end),
                    text.rfind('! ', start, end),
                    text.rfind('\n', start, end)
                )
                
                # If found a good break point, use it
                if sentence_end != -1 and sentence_end > start + self.chunk_size // 2:
                    end = sentence_end + 1  # Include the period
            
            # Add the chunk
            chunks.append(text[start:end].strip())
            
            # Move start position for next chunk, accounting for overlap
            start = end - self.chunk_overlap
            
            # Make sure we're making progress
            if start >= text_len or start <= 0:
                break
                
        return chunks
        
    def split_by_tokens(self, text: str, token_counter=None) -> List[str]:
        """
        Split text into chunks based on token count.
        
        Args:
            text (str): Text to split
            token_counter (callable): Function to count tokens (default: word count)
            
        Returns:
            List[str]: List of text chunks
        """
        if not text:
            return []
            
        # Default to simple word counting if no token counter provided
        token_counter = token_counter or (lambda t: len(t.split()))
        
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = []
        current_token_count = 0
        
        for sentence in sentences:
            sentence_tokens = token_counter(sentence)
            
            # If sentence itself exceeds chunk size, split it further
            if sentence_tokens > self.chunk_size:
                # Add any accumulated content first
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_token_count = 0
                
                # Split large sentence using character-based method then append
                sentence_chunks = self.split_by_characters(sentence)
                chunks.extend(sentence_chunks)
                continue
                
            # If adding this sentence would exceed chunk size, finalize current chunk
            if current_token_count + sentence_tokens > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                
                # Start new chunk with overlap from previous chunk
                overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                current_chunk = current_chunk[overlap_start:]
                current_token_count = token_counter(" ".join(current_chunk))
            
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_token_count += sentence_tokens
        
        # Add final chunk if not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

    def split_text(self, text: str, mode: str = 'tokens') -> List[str]:
        """
        Split text into chunks using the specified mode.
        
        Args:
            text (str): Text to split
            mode (str): Splitting mode ('tokens', 'characters')
            
        Returns:
            List[str]: List of text chunks
        """
        if mode == 'tokens':
            return self.split_by_tokens(text)
        elif mode == 'characters':
            return self.split_by_characters(text)
        else:
            raise ValueError(f"Unsupported splitting mode: {mode}")

class BaseDocumentProcessor(ABC):
    """
    Abstract base class for document processors.
    
    Document processors extract text from different file formats and
    prepare it for embedding and retrieval.
    """
    
    @abstractmethod
    def process(self, file_path: str) -> str:
        """
        Process a document and extract its text content.
        
        Args:
            file_path (str): Path to the document
            
        Returns:
            str: Extracted text content
        """
        pass
        
    @abstractmethod
    def supports_format(self, file_path: str) -> bool:
        """
        Check if this processor supports the given file format.
        
        Args:
            file_path (str): Path to the document
            
        Returns:
            bool: True if format is supported, False otherwise
        """
        pass

class TextFileProcessor(BaseDocumentProcessor):
    """Document processor for plain text files."""
    
    def process(self, file_path: str) -> str:
        """Extract text from a plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding if utf-8 fails
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def supports_format(self, file_path: str) -> bool:
        """Check if this processor supports the given file."""
        return file_path.lower().endswith(('.txt', '.md', '.log', '.csv', '.json', '.yml', '.yaml', '.py', '.js', '.html', '.css', '.xml'))

class PDFProcessor(BaseDocumentProcessor):
    """Document processor for PDF files."""
    
    def process(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            # Import here to avoid dependency if not used
            import PyPDF2
            
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            
            # If we couldn't extract any text, return an error message
            if not text.strip():
                logger.warning(f"No text could be extracted from PDF file {file_path}")
                return f"This PDF file doesn't contain extractable text. It may be scanned or image-based."
                
            return text
        except ImportError:
            error_msg = "PyPDF2 not installed. Please install it to process PDF files."
            logger.error(error_msg)
            print(f"ERROR: {error_msg}")
            # Install instructions
            print("To install PyPDF2, run: pip install PyPDF2")
            return f"[Error: {error_msg} - {file_path}]"
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {e}")
            return f"[Error processing PDF: {str(e)} - {file_path}]"
    
    def supports_format(self, file_path: str) -> bool:
        """Check if this processor supports the given file."""
        return file_path.lower().endswith('.pdf')

class DocxProcessor(BaseDocumentProcessor):
    """Document processor for Microsoft Word documents."""
    
    def process(self, file_path: str) -> str:
        """Extract text from a Word document."""
        try:
            # Import here to avoid dependency if not used
            import docx
            
            doc = docx.Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except ImportError:
            logger.error("python-docx not installed. Please install it to process DOCX files.")
            return f"[Error: python-docx not installed. Please install it to process DOCX files. - {file_path}]"
        except Exception as e:
            logger.error(f"Error processing DOCX file {file_path}: {e}")
            return f"[Error processing DOCX: {str(e)} - {file_path}]"
    
    def supports_format(self, file_path: str) -> bool:
        """Check if this processor supports the given file."""
        return file_path.lower().endswith('.docx')

class DocumentProcessor:
    """
    Main document processor that handles various file formats.
    
    This class manages a collection of format-specific processors and
    delegates processing to the appropriate one based on file extension.
    """
    
    def __init__(self):
        """Initialize with a set of document processors."""
        self.processors = [
            TextFileProcessor(),
            PDFProcessor(),
            DocxProcessor()
        ]
    
    def process_document(self, file_path: str) -> str:
        """
        Process a document and extract its text content.
        
        Args:
            file_path (str): Path to the document
            
        Returns:
            str: Extracted text content
            
        Raises:
            ValueError: If no suitable processor is found
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        for processor in self.processors:
            if processor.supports_format(file_path):
                return processor.process(file_path)
                
        raise ValueError(f"Unsupported document format: {file_path}")
    
    def chunk_document(self, text: str, chunk_size: int = 1024, chunk_overlap: int = 200) -> List[str]:
        """
        Split document text into chunks for embedding.
        
        Args:
            text (str): Document text to chunk
            chunk_size (int): Size of each chunk
            chunk_overlap (int): Overlap between chunks
            
        Returns:
            List[str]: List of text chunks
        """
        chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return chunker.split_text(text)
    
    def process_and_chunk(self, file_path: str, chunk_size: int = 768, chunk_overlap: int = 150) -> List[str]:
        """
        Process a document and split it into chunks.
        
        Args:
            file_path (str): Path to the document
            chunk_size (int): Size of each chunk (reduced from 1024 to 768 for more granular chunks)
            chunk_overlap (int): Overlap between chunks (increased from 200 to 150 for better context)
            
        Returns:
            List[str]: List of text chunks
        """
        text = self.process_document(file_path)
        return self.chunk_document(text, chunk_size, chunk_overlap)