import streamlit as st
import openai
from typing import Dict

def setup_page():
    """Configure the Streamlit page with a title and description"""
    st.title("AI Prompt Enhancer")
    st.write("Enter your prompt details below to get an enhanced version optimized for AI responses.")

def get_user_inputs() -> Dict[str, str]:
    """Collect user inputs using Streamlit form elements"""
    # Create input fields
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    role = st.text_area("Role (Who should AI act as?):", 
                        help="Example: You are an experienced business consultant")
    context = st.text_area("Context (What's the background?):", 
                          help="Example: I'm preparing a business plan for a startup")
    task = st.text_area("Task (What do you want AI to do?):", 
                        help="Example: Review my business plan and provide feedback")
    
    return {
        "api_key": api_key,
        "role": role,
        "context": context,
        "task": task
    }

def enhance_prompt(inputs: Dict[str, str]) -> str:
    """Use OpenAI to enhance the user's prompt"""
    try:
        client = openai.OpenAI(api_key=inputs["api_key"])
        
        # Create a system message to guide the enhancement
        enhancement_prompt = f"""
        Please enhance the following prompt components to create a comprehensive and effective prompt.
        Add structure, specific instructions for response format, and explicit request for assumption clarification.

        Original Components:
        Role: {inputs["role"]}
        Context: {inputs["context"]}
        Task: {inputs["task"]}

        Create an enhanced prompt that:
        1. Maintains the original role, context, and task
        2. Adds specific instructions for response format
        3. Explicitly requests assumption clarification
        4. Includes any necessary additional context or specifications
        5. Structures the output in a clear, organized way
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert prompt engineer."},
                {"role": "user", "content": enhancement_prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main application function"""
    # Setup the page
    setup_page()
    
    # Get user inputs
    inputs = get_user_inputs()
    
    # Add a submit button
    if st.button("Enhance Prompt"):
        # Validate inputs
        if not all([inputs["api_key"], inputs["role"], inputs["context"], inputs["task"]]):
            st.error("Please fill in all fields")
            return
        
        # Show a spinner while processing
        with st.spinner("Enhancing your prompt..."):
            enhanced_prompt = enhance_prompt(inputs)
        
        # Display the enhanced prompt
        st.subheader("Enhanced Prompt:")
        st.write(enhanced_prompt)
        
        # Add a copy button
        st.code(enhanced_prompt, language="text")

if __name__ == "__main__":
    main()