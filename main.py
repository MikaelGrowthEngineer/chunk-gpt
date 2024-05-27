import streamlit as st
import math
import pyperclip

# Initialize session state for parts copied
if 'copied_parts' not in st.session_state:
    st.session_state.copied_parts = {}

def main():
    st.title("ChatGPT Splitter")
    st.subheader("Effortlessly split your ChatGPT prompts with ChatGPT Splitter - the ultimate solution for seamless conversations!")
    
    st.markdown("### Instructions")
    # Instructions with a copy button
    st.markdown("""
    <div style="background-color: #FFF8DC; padding: 10px; border-radius: 5px;margin-bottom:10px;">
    The length of the content I need to send is too big to be sent all at once. 
    I will follow this rule when sending you the content:
    
    [START PART 1/X]
    This is the first part out of a total of X.
    [END PART 1/X]
    
    You can simply respond with "Acknowledged receipt of part 1 of X".
    
    And when I tell you "ALL PARTS SENT", then you can continue processing the data and answering my requests.
    
    Once I have confirmed that all parts have been sent, please proceed with processing the data and fulfilling my requests promptly.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Copy Instructions"):
        pyperclip.copy("The length of the content I need to send is too big to be sent all at once.\n\nI will follow this rule when sending you the content:\n\n[START PART 1/X]\nThis is the first part out of a total of X.\n[END PART 1/X]\n\nYou can simply respond with 'Acknowledged receipt of part 1 of X'.\n\nAnd when I tell you 'ALL PARTS SENT', then you can continue processing the data and answering my requests.\n\nOnce I have confirmed that all parts have been sent, please proceed with processing the data and fulfilling my requests promptly.")
        st.success("Instructions copied to clipboard!")

    st.markdown("---")

    # Text area to input the long prompt
    long_prompt = st.text_area("Enter the long prompt to be split", height=200)

    # Number input to choose the max length for each split part
    max_length = st.number_input("Choose the max length for each split part:", min_value=100, value=15000)

    # Button to split the prompt
    if st.button("Split into parts"):
        if long_prompt:
            parts = split_prompt(long_prompt, max_length)
            st.session_state.parts = parts
        else:
            st.error("Please enter a long prompt to split.")
    
    if 'parts' in st.session_state:
        for i, part in enumerate(st.session_state.parts, 1):
            st.markdown(f"### Part {i}/{len(st.session_state.parts)}")
            text = f"[START PART {i}/{len(st.session_state.parts)}]\n{part}\n[END PART {i}/{len(st.session_state.parts)}]"
            st.text_area(f'Part {i}', value=text, height=200, key=f'text_area_{i}')
            if st.button(f"Copy Part {i}", key=f"copy_button_{i}"):
                pyperclip.copy(text)
                st.session_state.copied_parts[f'part_{i}'] = True
            
            if st.session_state.copied_parts.get(f'part_{i}', False):
                st.success(f"Part {i} copied to clipboard!")

def split_prompt(text, max_length):
    """Function to split the text into parts with max length"""
    part_length = max_length
    num_parts = math.ceil(len(text) / part_length)
    return [text[i:i + part_length] for i in range(0, len(text), part_length)]

if __name__ == "__main__":
    main()
