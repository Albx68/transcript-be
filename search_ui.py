import gradio as gr
import os
from dotenv import load_dotenv
from test_vector_search import perform_vector_search
import random
import time
import itertools
import re

# Load environment variables
load_dotenv()

def format_score(score):
    """Helper function to format score value"""
    if isinstance(score, (int, float)):
        return f"{score:.4f}"
    return str(score)

def format_datetime(dt):
    """Helper function to format datetime objects"""
    if isinstance(dt, str):
        return dt
    try:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(dt)

def get_loading_messages():
    """Return cycling loading messages for search phases"""
    return {
        'init': itertools.cycle([
            "Initializing search engine...", 
            "Warming up the neural networks...",
            "Preparing semantic search..."
        ]),
        'search': itertools.cycle([
            "Searching through documents...",
            "Analyzing semantic meanings...",
            "Computing relevance scores...",
            "Matching your query..."
        ]),
        'format': itertools.cycle([
            "Formatting results...",
            "Preparing output...",
            "Organizing findings..."
        ])
    }

def format_result(result: dict, query: str) -> str:
    """Format a single result with highlighting and proper spacing"""
    lines = []
    
    # Format header with bold
    lines.append("\n" + "━" * 50)
    lines.append(f"**📄 Document**")
    lines.append("━" * 50)
    
    for key, value in result.items():
        if key == 'metadata':
            lines.append("\n**📋 Metadata:**")
            for meta_key, meta_value in value.items():
                lines.append(f"  • {meta_key}: {meta_value}")
        elif key == 'transcript_text':
            # Highlight search terms in transcript
            highlighted_text = highlight_text(str(value), query)
            lines.append(f"\n**📝 Transcript:**")
            lines.append(highlighted_text)
        else:
            lines.append(f"\n**{key}:** {value}")
    
    return "\n".join(lines)

def highlight_text(text: str, query: str) -> str:
    """Highlight search terms using ASCII formatting"""
    if not text or not query:
        return text
    
    # Split query into terms
    terms = [term.strip().lower() for term in query.split() if len(term.strip()) > 2]
    
    # Highlight each term
    highlighted = text
    for term in terms:
        pattern = re.compile(f'({re.escape(term)})', re.IGNORECASE)
        highlighted = pattern.sub(r'*\1*', highlighted)
    
    return highlighted

def search_documents(query: str, progress=gr.Progress()):
    """
    Perform vector search and return formatted results
    
    Args:
        query: Search query string
        progress: Gradio progress indicator
    """
    try:
        if not query.strip():
            return "Please enter a search query."
            
        loading_messages = get_loading_messages()
        current_progress = 0.0
        
        # Animated initialization phase
        for _ in range(3):
            current_progress = min(0.2, current_progress + 0.07)
            progress(current_progress, desc=next(loading_messages['init']))
            time.sleep(0.3)
        
        # Animated search phase
        search_progress_steps = [0.3, 0.4, 0.5, 0.6]
        for step in search_progress_steps:
            current_progress = max(current_progress, step)
            progress(current_progress, desc=next(loading_messages['search']))
            time.sleep(0.4)
            
        results = perform_vector_search(query)
        
        # Animated formatting phase
        for _ in range(2):
            current_progress = min(0.8, current_progress + 0.1)
            progress(current_progress, desc=next(loading_messages['format']))
            time.sleep(0.2)
            
        print('gradio results:', results)

        # Format results with highlighting
        output_lines = []
        for idx, result in enumerate(results, 1):
            formatted_result = format_result(result, query)
            output_lines.append(formatted_result)
        
        progress(1.0, desc="Search complete! 🎉")
        time.sleep(0.5)
        
        if not output_lines:
            return "No matching documents found."
            
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Document Search", theme=gr.themes.Soft(), css="""
    .output-text { 
        font-size: 0.9em !important;
        font-family: monospace !important;
        background-color: transparent !important;
    }
    textarea.output-text {
        font-size: 0.9em !important;
        line-height: 1.4 !important;
        white-space: pre-wrap !important;
        background: transparent !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
    }
""") as demo:
    gr.Markdown("""
    # 🔍 Semantic Document Search
    Enter your search query below to find relevant documents using AI-powered semantic search.
    """)
    
    with gr.Row():
        query_input = gr.Textbox(
            label="Search Query",
            placeholder="Enter your search query here...",
            lines=2
        )
    
    with gr.Row():
        search_button = gr.Button("🔍 Search", variant="primary")
    
    with gr.Row():
        output = gr.Textbox(
            label="Search Results",
            lines=15,
            show_copy_button=True,
            elem_classes=["output-text"]
        )
    
    # Add example queries
    gr.Examples(
        examples=[
            "Find conversations with experts in oauth",
            "How does one implement lazy loading?",
            "What is the strongest pokemon type",
        ],
        inputs=query_input,
        label="Example Queries"
    )
    
    # Handle the search button click
    search_button.click(
        fn=search_documents,
        inputs=query_input,
        outputs=output,
        api_name="search"
    )
    
    # Add error handling for empty queries
    query_input.change(
        lambda x: gr.update(interactive=bool(x.strip())),
        inputs=query_input,
        outputs=search_button
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    ) 