# link video: https://www.youtube.com/watch?v=vwFR2bXXzTw&ab_channel=JCharisTech%26J-Secur1ty
import json
import streamlit as st
import xmltodict
import pandas as pd
import docx2txt
from PIL import Image
from PyPDF2 import PdfFileReader
import pdfplumber

def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()

    return all_page_text


def read_pdf_with_pdfplumber(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        return page.extract_text()

@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img


def main():
    st.title("File Upload")
    menu = ["Image", "Dataset", "DocumentFiles", "Json", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Image":
        st.subheader("Image")
        image_file = st.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'])
        if image_file is not None:
            file_details = {"Filename": image_file.name, "FileType": image_file.type, "FileSize": image_file.size}
            st.write(file_details)

            img = load_image(image_file)
            st.image(img, width=300, height=300)

    elif choice == "Dataset":
        st.subheader("Dataset")
        data_file = st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx'])
        if st.button("Process"):
            if data_file is not None:
                file_details = {"Filename": data_file.name,
                                "FileType": data_file.type,
                                "FileSize": data_file.size}
                st.write(file_details)

                try:
                    df = pd.read_csv(data_file)
                    n = df.isnull().sum()
                    # df = df.convert_dtypes()
                    a = df.dtypes
                    st.write("Data Type", a)
                    st.write("Celulas Vazias", n)
                    st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
                    st.dataframe(df)

                except Exception as e:
                    print(e)
                    df = pd.read_excel(data_file)
                    # st.dataframe(df)
                    n = df.isnull().sum()
                    a = df.dtypes
                    st.write("Data Type", a)
                    st.write("Celulas Vazias", n)
                    st.table(df)

    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles")
        docx_file = st.file_uploader("Upload File", type=['txt', 'docx', 'pdf'])
        if st.button("Process"):
            if docx_file is not None:
                file_details = {"Filename": docx_file.name, "FileType": docx_file.type, "FileSize": docx_file.size}
                st.write(file_details)
                # Check File Type
                if docx_file.type == "text/plain":
                    st.text(str(docx_file.read(), "utf-8"))  # empty
                    raw_text = str(docx_file.read(),
                                   "utf-8")  # works with st.text and st.write,used for futher processing

                    st.write(raw_text)  # works
                elif docx_file.type == "application/pdf":
                    try:
                        with pdfplumber.open(docx_file) as pdf:
                            page = pdf.pages[0]
                            st.write(page.extract_text())
                    except:
                        st.write("None")

                elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    raw_text = docx2txt.process(docx_file)  # Parse in the uploadFile Class directory
                    st.write(raw_text)

    else:
        st.subheader("About")
        st.info("Built with Streamlit")
        st.info("Alecio Nunes TI/BI")
        st.text("Alécio Engenheiro de Computação")

if __name__ == '__main__':
    main()




