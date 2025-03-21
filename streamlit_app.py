import streamlit as st
from pypdf import PdfWriter
from io import BytesIO

def merge_pdfs(pdf_files):
    """Merges a list of PDF files into a single PDF using PdfWriter."""
    merger = PdfWriter()
    for pdf_file in pdf_files:
        try:
            merger.append(pdf_file)
        except Exception as e:
            st.error(f"Error merging {pdf_file.name}: {e}")
            return None

    output_buffer = BytesIO()
    try:
        merger.write(output_buffer)
    except Exception as e:
        st.error(f"Error writing merged PDF: {e}")
        return None

    output_buffer.seek(0)
    return output_buffer

def frontend():
    """Handles the frontend logic using Streamlit."""
    st.title("PDF Merger Application")

    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        st.write("Uploaded files:")
        for file in uploaded_files:
            st.write(file.name)

        if st.button("Merge PDFs"):
            with st.spinner("Merging PDFs..."):
                merged_pdf = merge_pdfs(uploaded_files)

            if merged_pdf:
                st.success("PDFs merged successfully!")
                st.session_state.merged_pdf_data = merged_pdf #store the merged pdf data in session state.

                st.download_button(
                    label="Download Merged PDF (Button 1)",
                    data=st.session_state.merged_pdf_data,
                    file_name="merged_pdf.pdf",
                    mime="application/pdf",
                    key = "download_button1" #added key
                )
            else:
                st.error("PDF merging failed. Please check the uploaded files.")

        # Add a second download button (only if merged_pdf_data exists)
        if 'merged_pdf_data' in st.session_state:
            st.download_button(
                label="Download Merged PDF (Button 2)",
                data=st.session_state.merged_pdf_data,
                file_name="merged_pdf.pdf",
                mime="application/pdf",
                key = "download_button2" #added key
            )

if __name__ == "__main__":
    frontend()
