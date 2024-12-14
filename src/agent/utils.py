from langchain_community.document_loaders import WebBaseLoader
from agent.state import Section

def load_and_format_urls(url_list):
    """Load web pages from URLs and format them into a readable string.
    
    Args:
        url_list (str or list): Single URL or list of URLs to load and format
        
    Returns:
        str: Formatted string containing metadata and content from all loaded documents,
             separated by '---' delimiters. Each document includes:
             - Title
             - Source URL
             - Description
             - Page content
    """

    loader = WebBaseLoader(url_list)
    docs = loader.load()

    formatted_docs = []
    
    for doc in docs:
        # Format metadata
        metadata_str = (
            f"Title: {doc.metadata.get('title', 'N/A')}\n"
            f"Source: {doc.metadata.get('source', 'N/A')}\n"
            f"Description: {doc.metadata.get('description', 'N/A')}\n"
        )
        
        # Format content (strip extra whitespace and newlines)
        content = doc.page_content.strip()
        
        # Combine metadata and content
        formatted_doc = f"---\n{metadata_str}\nContent:\n{content}\n---"
        formatted_docs.append(formatted_doc)
    
    # Join all documents with double newlines
    return "\n\n".join(formatted_docs)

def read_dictation_file(file_path: str) -> str:
    """Read content from a text file audio-to-text dictation."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""
    
def format_sections(sections: list[Section]) -> str:
    """ Format a list of sections into a string """
    formatted_str = ""
    for idx, section in enumerate(sections, 1):
        formatted_str += f"""
{'='*60}
Section {idx}: {section.name}
{'='*60}
Description:
{section.description}
Main body: 
{section.main_body}

Content:
{section.content if section.content else '[Not yet written]'}

"""