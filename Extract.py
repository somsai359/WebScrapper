from flask import Flask,request
import logging
app = Flask(__name__)
 
from pdfminer.high_level import extract_text
    
import nltk
import requests
 
 
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)
SKILLS_DB = [
    'machine learning',
    'data science',
    'word',
    'excel',
    'english',
    'java',
    'sql',
    'c',
    'react',
    'javascript',
    'git'
]
 
 
 
def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
    app.logger.info(word_tokens)
    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    # we create a set to keep the results in.
    found_skills = set()
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)
    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)
    return str(found_skills)
 
 
 
def parse_resume(file_url):
    text=extract_text_from_pdf(file_url)
    skills = extract_skills(text)
    return skills
 
 
@app.route("/skillFromResume",methods=['POST','GET'])
def get_skills():
    if(request.method=='POST'):
        return parse_resume("uploads/"+request.form['file_name'])
 
    else:
        return "Only post requests are allowed"
