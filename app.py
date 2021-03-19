import streamlit as st 
from gensim.summarization import summarize
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import pdfplumber
import docx2txt

def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("italian"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result
	


def main():
	st.title("INTELLIGENZA ARTIFICIALE ITALIA")
	activity1 = ["Manuale","File (txt, pdf, Docx)"]
	choice = st.sidebar.selectbox("Seleziona come inserire il testo da tradurre",activity1)
	if choice == 'Manuale':
		st.subheader("Crea riassunti con la nostra intelligenza artificiale !")
		raw_text = st.text_area("Inserisci qui il testo da Riassumere","",height=200,max_chars=15000)
		lenI = len(raw_text)
		lenf= 0
		summary_choice = st.selectbox("Algoritmo NLP per il riassunto",["Genism","Sumy Lex Rank"])

		if st.button("Fai il Riassunto"):
			if summary_choice == "Genism":
				summary_result = summarize(raw_text)
				if (len(summary_result)<=3):
					summary_result = "Attenzione il testo inserito potrebbe essere troppo corto, o non riassumibile"
				else: 
					lenf=len(summary_result)
					
			elif summary_choice == "Sumy Lex Rank":
				summary_result = sumy_summarizer(raw_text)
				if (len(summary_result)<=3):
					summary_result = "Attenzione il testo inserito potrebbe essere troppo corto, o non riassumibile"
				else: 
					lenf=len(summary_result)

			st.write(summary_result)
			if (len(summary_result)>=3):
				st.success("Il testo iniziale era di " + str(lenI) + " lettere, il riassunto contiene solo " + str(lenf) +" lettere")
				st.info("L'ottimizzazione è stata di " + str(lenI - lenf ) + " caratteri ")
				st.error("Attenzione, questo programma in alcuni casi potrebbe comunque non evidenziare aspetti importanti del testo ")
				
	if choice == 'File (txt, pdf, Docx)':
		st.subheader("Crea riassunti con la nostra intelligenza artificiale !")	
		raw_textok = ""		
		docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
		if docx_file is not None:
			# Check File Type
			if docx_file.type == "text/plain":
				# raw_text = docx_file.read() # read as bytes
				# st.write(raw_text)
				# st.text(raw_text) # fails
				#st.text(str(docx_file.read(),"utf-8")) # empty
				raw_text = str(docx_file.read(),"utf-8") # works with st.text and st.write,used for futher processing
				# st.text(raw_text) # Works
				raw_textok = raw_text # works
			elif docx_file.type == "application/pdf":
				# raw_text = read_pdf(docx_file)
				# st.write(raw_text)
				try:
					with pdfplumber.open(docx_file) as pdf:
					    pages = pdf.pages
					    for i,pg in enumerate(pages):
						    page = pdf.pages[i]
						    raw_textok = raw_textok + (page.extract_text())
				except:
					st.write("Errore nella Lettura del PDF")
					    
					
			elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
			# Use the right file processor ( Docx,Docx2Text,etc)
				raw_text = docx2txt.process(docx_file) # Parse in the uploadFile Class directory
				raw_textok = raw_text
		
		if(len(raw_textok)<=3):
			st.success("File caricato e letto con successo")
		if( st.checkbox("Leggi testo estratto dal documento sempre con una nostra intelligenza artificiale")):
			st.write(raw_textok)
		lenI = len(raw_textok)
		lenf= 0
		summary_choice = st.selectbox("Algoritmo NLP per il riassunto",["Genism","Sumy Lex Rank"])
		
		if st.button("Fai il Riassunto"):
			if summary_choice == "Genism":
				summary_result = summarize(raw_textok)
				if (len(summary_result)<=3):
					summary_result = "Attenzione il testo inserito potrebbe essere troppo corto, o non riassumibile"
				else: 
					lenf=len(summary_result)
					
			elif summary_choice == "Sumy Lex Rank":
				summary_result = sumy_summarizer(raw_textok)
				if (len(summary_result)<=3):
					summary_result = "Attenzione il testo inserito potrebbe essere troppo corto, o non riassumibile"
				else: 
					lenf=len(summary_result)

			st.write(summary_result)
			if (len(summary_result)>=3):
				st.success("Il testo iniziale era di " + str(lenI) + " lettere, il riassunto contiene solo " + str(lenf) +" lettere")
				st.info("L'ottimizzazione è stata di " + str(lenI - lenf ) + " caratteri ")
				st.error("Attenzione, questo programma in alcuni casi potrebbe comunque non evidenziare aspetti importanti del testo ")



if __name__ == '__main__':
	main()
