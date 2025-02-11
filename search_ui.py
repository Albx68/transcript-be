import gradio as gr
import os
from dotenv import load_dotenv
from test_vector_search import perform_vector_search

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
            
        progress(0.2, desc="Initializing search...")
        
        # Perform the vector search
        progress(0.4, desc="Searching documents...")
        results = perform_vector_search(query)
        
        progress(0.8, desc="Formatting results...")
        print('gradio results:', results)

        # Convert results to string representation
        output_lines = []
        for idx, result in enumerate(results, 1):
            output_lines.append(f"=== Document {idx} ===")
            for key, value in result.items():
                if key == 'metadata':
                    output_lines.append(f"metadata:")
                    for meta_key, meta_value in value.items():
                        output_lines.append(f"  {meta_key}: {meta_value}")
                else:
                    output_lines.append(f"{key}: {value}")
            output_lines.append("=" * 50)
        
        progress(1.0, desc="Complete!")
        
        if not output_lines:
            return "No matching documents found."
            
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Document Search", theme=gr.themes.Soft()) as demo:
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
            show_copy_button=True
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