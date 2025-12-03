import gradio as gr
from main_agent import run_agent
import logging

# Setup minimal logging for Hugging Face
logging.basicConfig(level=logging.INFO)

def process_request(message: str) -> str:
    """
    Process user input and return disaster resource recommendations.
    """
    try:
        if not message or not message.strip():
            return "Error: Please provide a message describing your situation."
        
        response = run_agent(message)
        return response
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return f"Error processing your request. Please try again."

def create_interface():
    """
    Create Gradio interface for the Disaster Resource Agent.
    """
    with gr.Blocks(title="Disaster Resource Connector") as interface:
        gr.Markdown("# 🆘 Disaster Resource Connector")
        gr.Markdown("""
        This agent helps you find essential resources during disaster situations including:
        - Shelter locations
        - Food and water distribution points
        - Medical aid stations
        - Government assistance programs (FEMA, etc.)
        
        Simply describe your situation and the resources you need.
        """)
        
        with gr.Row():
            with gr.Column():
                message_input = gr.Textbox(
                    label="Describe your situation",
                    placeholder="e.g., 'I need shelter after the hurricane' or 'Where can I find medical help?'",
                    lines=3
                )
                submit_btn = gr.Button("Find Resources", variant="primary")
            
            with gr.Column():
                response_output = gr.Textbox(
                    label="Available Resources",
                    lines=8,
                    interactive=False
                )
        
        submit_btn.click(process_request, inputs=message_input, outputs=response_output)
        message_input.submit(process_request, inputs=message_input, outputs=response_output)
        
        # Examples
        gr.Examples(
            examples=[
                ["I need shelter after the hurricane"],
                ["Where can I find food and water?"],
                ["Medical assistance needed urgently"],
                ["How do I apply for FEMA aid?"]
            ],
            inputs=message_input,
            outputs=response_output,
            fn=process_request,
            cache_examples=True
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
