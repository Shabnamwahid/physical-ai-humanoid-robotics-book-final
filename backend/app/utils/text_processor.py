from typing import List
import re


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> List[str]:
    """
    Split text into overlapping chunks of specified size.

    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    # Split text into sentences to avoid breaking sentences across chunks
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding the sentence would exceed chunk size
        if len(current_chunk) + len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())

            # If the sentence itself is longer than chunk_size, split it
            if len(sentence) > chunk_size:
                # Split long sentence into smaller parts
                sentence_chunks = split_long_sentence(sentence, chunk_size)
                for sc in sentence_chunks[:-1]:  # Add all but the last chunk
                    chunks.append(sc)
                current_chunk = sentence_chunks[-1]  # Start new chunk with last part
            else:
                current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence

    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Ensure chunks don't exceed the size limit
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= chunk_size:
            final_chunks.append(chunk)
        else:
            # If still too long, force split by characters
            final_chunks.extend(force_chunk_by_size(chunk, chunk_size, overlap))

    # Apply overlap if specified
    if overlap > 0:
        final_chunks = apply_overlap(final_chunks, overlap)

    return final_chunks


def split_long_sentence(sentence: str, max_length: int) -> List[str]:
    """
    Split a long sentence into smaller parts.

    Args:
        sentence: Long sentence to split
        max_length: Maximum length for each part

    Returns:
        List of sentence parts
    """
    if len(sentence) <= max_length:
        return [sentence]

    # Split by words to avoid breaking words
    words = sentence.split()
    parts = []
    current_part = ""

    for word in words:
        if len(current_part + " " + word) <= max_length:
            current_part += " " + word if current_part else word
        else:
            if current_part:
                parts.append(current_part)
            current_part = word

    if current_part:
        parts.append(current_part)

    return parts


def force_chunk_by_size(text: str, chunk_size: int, overlap: int = 0) -> List[str]:
    """
    Force split text into chunks of specified size.

    Args:
        text: Input text to chunk
        chunk_size: Size of each chunk
        overlap: Number of characters to overlap

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap if overlap < chunk_size else end

    return chunks


def apply_overlap(chunks: List[str], overlap: int) -> List[str]:
    """
    Apply overlap between consecutive chunks.

    Args:
        chunks: List of text chunks
        overlap: Number of characters to overlap

    Returns:
        List of text chunks with overlap applied
    """
    if overlap <= 0 or len(chunks) <= 1:
        return chunks

    result = [chunks[0]]

    for i in range(1, len(chunks)):
        prev_chunk = chunks[i-1]
        curr_chunk = chunks[i]

        # Take the last 'overlap' characters from the previous chunk
        overlap_text = prev_chunk[-overlap:] if len(prev_chunk) >= overlap else prev_chunk

        # Create new chunk with overlap
        new_chunk = overlap_text + curr_chunk
        result.append(new_chunk)

    return result


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing.

    Args:
        text: Input text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def extract_key_sentences(text: str, num_sentences: int = 3) -> List[str]:
    """
    Extract key sentences from text (first few sentences).

    Args:
        text: Input text
        num_sentences: Number of sentences to extract

    Returns:
        List of key sentences
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences[:num_sentences] if len(sentences) >= num_sentences else sentences