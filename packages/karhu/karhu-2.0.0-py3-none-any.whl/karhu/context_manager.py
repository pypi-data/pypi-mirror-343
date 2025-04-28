import os
from datetime import datetime
import re
from termcolor import colored
from openai import OpenAI

class ContextManager:
    """
    Manages context for the AI assistant with optimized handling of large data.
    Provides summarization, chunking, and selective retrieval capabilities.
    """
    
    def __init__(self, max_context_size=8000, summarization_threshold=10000):
        """Initialize the context manager with configurable size limits"""
        self.current_context = ""
        self.max_context_size = max_context_size
        self.summarization_threshold = summarization_threshold
        self.context_path = os.path.join(os.path.dirname(__file__), "data/.context")
        self.chunks = {}  # Store document chunks for selective retrieval
        self.client = None  # Placeholder for OpenAI client, if needed
        self.setup_summarization_client()
            
    def load_context(self, filename=None):
        """Load context from file"""
        if filename is None:
            filename = self.context_path
            
        try:
            with open(filename, "r", encoding="utf-8") as file:
                self.current_context = file.read()
            return self.current_context
        except FileNotFoundError:
            self.current_context = ""
            return ""
    
    def save_context(self, filename=None):
        """Save context to file"""
        if filename is None:
            filename = self.context_path
            
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.current_context)
    
    def clear_context(self, filename=None):
        """Clear the current context"""
        if filename is None:
            filename = self.context_path
            
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("")
            self.current_context = ""
            self.chunks = {}
            return True
        except Exception as e:
            print(f"Error clearing context: {str(e)}")
            return False

    def setup_summarization_client(self):
        """Setup OpenAI client for summarization operations"""
        try:
            github_token = os.getenv('GITHUB_TOKEN')
            if not github_token:
                return None
            
            self.client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=github_token,
            )
            return self.client
        except Exception as e:
            print(f"Could not setup summarization client: {str(e)}")
            self.client = None
            return None

    def _create_hierarchical_summary(self, content, source_type=None):
        """
        Create a hierarchical summary of content based on its source type
        
        Returns a structured summary with main ideas and supporting details
        """
        # Default summary for when we don't have API access
        default_summary = f"Content ({len(content)} characters) from "
        default_summary += f"{source_type if source_type else 'unknown source'}"
        
        try:
            # If we have a client properly set up
            if hasattr(self, 'client') and self.client:
                # Create a specialized prompt based on source type
                if source_type == "file":
                    system_prompt = """Summarize this file content in a hierarchical format:
                    1. Main Topic/Purpose (1 sentence)
                    2. Key Points (3-5 bullet points)
                    3. Important Details (if any)
                    Include file type information if apparent."""
                
                elif source_type == "web":
                    system_prompt = """Summarize this web content in a hierarchical format:
                    1. Website Topic/Purpose (1 sentence)
                    2. Main Information Points (3-5 bullet points)
                    3. Notable Data or Claims (if any)
                    Indicate if it's an article, documentation, or other content type."""
                
                elif source_type == "search":
                    system_prompt = """Organize these search results in a structured format:
                    1. Overview of Search Topic (1 sentence)
                    2. Main Themes in Results (3-5 themes)
                    3. Specific Findings (bullet points under relevant themes)
                    Note any contradictory information across sources."""
                
                else:
                    system_prompt = """Create a hierarchical summary:
                    1. Main Topic (1 sentence)
                    2. Key Points (3-5 bullet points)
                    3. Supporting Details (if relevant)"""
                
                # Call API to generate summary
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": content[:15000]}
                    ],
                    model="gpt-4o",  # Use a smaller model for summarization
                    temperature=0.3,
                    max_tokens=1000
                )
                               
                # Save the generated summary to a file for inspection
                # with open("hierarchical_summary_output.txt", "w", encoding="utf-8") as summary_file:
                #     summary_file.write(response.choices[0].message.content)
                print(colored(" 📕 Hierarchical summary created successfully", "green"))
                return response.choices[0].message.content
            else:
                # Without client, create a basic structured summary
                return default_summary + "\n- Content was too large to display in full"
                
        except Exception as e:
            print(f"Error creating hierarchical summary: {str(e)}")
            return default_summary


    def add_to_context(self, content, source_type=None, source_name=None, optimize=True):
        """
        Add content to context with smart metadata and optimization
        
        Args:
            content: The content to add
            source_type: Type of content (file, search, web, etc.)
            source_name: Name or identifier of the source
            optimize: Whether to optimize the content
        """
        if not content:
            return

        # Generate timestamp for ordering
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create structured metadata header
        header = f"--- {timestamp} | "
        if source_type:
            header += f"Source: {source_type}"
            if source_name:
                header += f" | {source_name}"
        header += " ---\n"
        
        # Create a summary if content is large
        if optimize and len(content) > self.summarization_threshold:
            # First clean and optimize the text
            optimized_content = self.optimize_content(content)
            
            # Then create a hierarchical summary
            summary = self._create_hierarchical_summary(content, source_type)
            
            # Add both summary and optimized content
            self.current_context += f"{header}[SUMMARY]\n{summary}\n\n"
            self.current_context += f"[FULL CONTENT (Optimized)]\n{optimized_content}\n\n"
            
            # Store the full content in chunks for retrieval if needed
            if source_name:
                self.chunk_document(content, chunk_name=source_name)
        else:
            # For smaller content, add directly
            self.current_context += f"{header}{content}\n\n"
        
        # Manage context size
        self._manage_context_size()
    

    def optimize_content(self, content):
        """Optimize content for context size management"""
        # Basic cleanup
        content = self._clean_text(content)
        
        # If still too large, summarize
        if len(content) > self.summarization_threshold:
            return self._summarize_content(content)
        
        return content
    
    def _clean_text(self, text):
        """Clean text by removing unnecessary whitespace and markup"""
        # Remove redundant spaces, tabs and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common boilerplate text
        text = re.sub(r'Privacy Policy|Terms of Service|Copyright ©.*?202\d', '', text)
        
        # Remove URLs
        text = re.sub(r'https?://\S+', '[URL]', text)
        
        return text.strip()
    
    def _summarize_content(self, content, max_summary_length=2000):
        """Summarize content using AI"""
        if not self.client:
            # If no client, use basic truncation with markers
            return f"{content[:max_summary_length]}... [CONTENT TRUNCATED - {len(content)} chars total]"
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Summarize the following content while preserving key information:"},
                    {"role": "user", "content": content[:15000]}  # First part only if very large
                ],
                model="Mistral-Nemo",  # Use a smaller model for summarization
                temperature=0.3,
                max_tokens=1000
            )
            
            summary = response.choices[0].message.content
            return f"[SUMMARY of {len(content)} chars]: {summary}"
        except Exception:
            # Fallback to basic truncation
            return f"{content[:max_summary_length]}... [CONTENT TRUNCATED - {len(content)} chars total]"
    

    def _manage_context_size(self):
        """Manage context if it exceeds maximum size"""
        if len(self.current_context) <= self.max_context_size:
            return
            
        # Split context into parts
        parts = re.split(r'\n\s*\n', self.current_context)
        
        # Keep most recent parts up to max size
        new_context = ""
        for part in reversed(parts):
            if len(new_context) + len(part) + 2 <= self.max_context_size:
                new_context = part + "\n\n" + new_context
            else:
                break
                
        # Add indicator that content was truncated
        self.current_context = "[CONTEXT TRUNCATED]\n\n" + new_context.strip()
    
    def chunk_document(self, content, chunk_size=5000, chunk_name=None):
        """
        Divide document into retrievable chunks
        
        Args:
            content: Text content to chunk
            chunk_size: Maximum size of each chunk
            chunk_name: Name to identify the document
        """
        if not content:
            return []
                
        # Generate a unique ID for this document
        doc_id = chunk_name or f"doc_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Split content into chunks
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i+chunk_size]
            chunk_id = f"{doc_id}_chunk_{len(chunks)+1}"
            self.chunks[chunk_id] = chunk
            chunks.append(chunk_id)
        
        # Create and store a small metadata section in the context
        chunk_info = f"Document '{doc_id}' split into {len(chunks)} chunks. Use '!chunk {doc_id}_chunk_N' to retrieve part N."
        # Don't add this to context directly, return it
        return {"chunk_ids": chunks, "info": chunk_info}
    
    def get_chunk(self, chunk_id):
        """Retrieve a specific chunk by ID"""
        return self.chunks.get(chunk_id, "Chunk not found")


    def search_context(self, query, max_results=5):
        """Search for relevant parts of the context using proper word boundaries"""
        if not query or not self.current_context:
            return ""
        
        # Normalize and escape the query for regex
        query_escaped = re.escape(query.lower())
        
        # Split context into paragraphs
        paragraphs = re.split(r'\n\s*\n', self.current_context)
        
        # Find paragraphs containing the query as whole words
        results = []
        for para in paragraphs:
            # Using word boundaries \b to match whole words only
            if re.search(r'\b' + query_escaped + r'\b', para.lower()):
                # Highlight the matches in the results
                highlighted = re.sub(r'(?i)\b(' + query_escaped + r')\b', 
                                    r'**\1**', para)
                results.append(highlighted)
                if len(results) >= max_results:
                    break
        
        if not results:
            return ""  # Return empty string to trigger the "No matches found" message
        
        # Build a formatted result
        return "\n\n".join(results)
    
    def get_formatted_context(self, token_limit=None):
        """Get context formatted for the AI, respecting token limits"""
        if not self.current_context:
            return ""
            
        if not token_limit or len(self.current_context) <= token_limit:
            return self.current_context
            
        # If we need to limit tokens, use start and end portions
        start_portion = self.current_context[:token_limit//2]
        end_portion = self.current_context[-token_limit//2:]
        
        return f"{start_portion}\n\n[...Context abbreviated due to length...]\n\n{end_portion}"
    
    

    