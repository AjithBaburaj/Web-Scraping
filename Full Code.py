#!/usr/bin/env python
# coding: utf-8

# ### Importing excel sheet(URL)

# In[14]:


import pandas as pd
# Load URLs from input.xlsx file
input_df = pd.read_excel(r"C:\Users\ajith\Downloads\Input.xlsx")
urls = input_df['URL'].tolist()


# ### Extracting article text from URL

# In[20]:


get_ipython().system('pip install readability-lxml')


#Readability is a library that can be used for text extraction.


# In[21]:


import requests
from readability import Document
import re

list_of_article_text=[]

for i, url in enumerate(urls):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using Readability
    doc = Document(response.text)

    # Find the article title and text
    title = doc.title()
    article_text = doc.summary()

    # Remove any HTML tags from the article text
    clean_article_text = re.sub('<.*?>', '', article_text)

    # Remove unwanted notations
    clean_article_text = clean_article_text.replace('\n', '').replace('\r', '').replace('\t', '')

    list_of_article_text.append(title + clean_article_text)

    # Save the article content as a text file with a number as filename
    filename = f"{i+37}.txt"
    with open(f"C:\\Users\\ajith\\OneDrive\\Desktop\\articles\\{filename}", 'w', encoding='utf-8') as file:
        file.write(title + '\n\n' + clean_article_text)

    print(f'Saved article from {url} as {filename}')


# In[22]:


list_of_article_text  # This list is in the format ~ [Article-1 text ,Article-2 text ,.......]


# In[25]:


article_list = list_of_article_text.copy()  #making copy of the list


# ### Removing unwanted notations and punctuations

# In[26]:


for i in range(len(article_list)):
    # Perform multiple text replacements in the current document
    article_list[i] = article_list[i].replace("\n", " ")                 .replace("\xa0", " ")                 .replace("“"," ")                .replace("”", " ")                .replace("’", " ")                .replace("❛", " ")


# ### Tokenization , Normalization

# In[27]:


import string
from nltk.tokenize import word_tokenize

# Punctuation to remove
punctuations = string.punctuation

# List to store the tokenized and normalized sentences
tokenized_list = []

# Loop through each sentence in the list and remove punctuation, then tokenize and normalize
for sentence in article_list:
    sentence = sentence.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(sentence) # Tokenize
    normalized_tokens = [token.lower() for token in tokens]
    tokenized_list.append(normalized_tokens)

print(tokenized_list)  # This list is in the format ~ [[tokenized words from Article-1],[tokenized words from Article-2],....]


# ### Importing stop words

# In[28]:


# Create an empty list to store the words
stop_words = []

# List of file names to read
files = [r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_Auditor.txt",
         r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_Currencies.txt",
         r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_DatesandNumbers.txt",
         r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_Generic.txt",
         r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_GenericLong.txt",
         r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_Geographic.txt",
         r"C:\Users\ajith\OneDrive\Desktop\stop words\StopWords_Names.txt"]

for file_name in files:
    with open(file_name, 'r') as file:
        file_words = file.read().split()
        stop_words.extend(file_words)

stop_words = [word.lower() for word in stop_words]  #changing words into lower case

print(stop_words)


# ### Removing stop words from tokenized list

# In[29]:


filtered_list = [[word for word in sentence if word not in stop_words] for sentence in tokenized_list]

print(filtered_list)


# In[31]:


import nltk

num_of_sentence = []

for article in article_list:
    # Count the number of sentences
    sentences = nltk.sent_tokenize(article)
    num_sentences = len(sentences)
    num_of_sentence.append(num_sentences)
    
print(num_of_sentence)  # This list is in the format ~ [Number of sentence in Article-1,Num pf sentence in Art-2,....]


# ## WORD COUNT

# In[32]:


word_count=[]

for i, filtered_tokens_list in enumerate(filtered_list):
    word_countt = len(filtered_tokens_list)
    word_count.append(word_countt)
print(word_count)


# ## AVG NUMBER OF WORDS PER SENTENCE

# In[33]:


avg_words_per_sentence= []

for word_countt,num_sentences in zip(word_count,num_of_sentence):
    # Calculate average words per sentence
    x = word_countt / num_sentences
    
    avg_words_per_sentence.append(x)
    
print(avg_words_per_sentence)


# ## AVG WORD LENGTH

# In[34]:


avg_word_length=[]

for article in filtered_list:
    total_chars = 0
    total_words = len(article)
    for word in article:
        total_chars += len(word)
    # Calculate average words length
    avg_word_len = total_chars/total_words
    
    avg_word_length.append(avg_word_len)
    
print(avg_word_length) 


# ## COMPLEX WORD COUNT

# In[35]:


get_ipython().system('pip install syllables')


# In[36]:


import syllables

complex_word_counts = []

def count_syllables(word):
    return syllables.estimate(word)

for article in filtered_list:
    complex_word_count = 0
    for word in article:
        num_syllables = count_syllables(word)
        if num_syllables > 2:
            complex_word_count += 1
    complex_word_counts.append(complex_word_count)

print(complex_word_counts)


# ## SYLLABLE PER WORD

# In[37]:


import syllables

syllables_per_word = []

for article in filtered_list:
    total_syllables = 0
    total_words = len(article)
    for word in article:
        syllable_count = syllables.estimate(word)
        total_syllables += syllable_count
        avg_syllables_per_word = total_syllables / total_words
    syllables_per_word.append(avg_syllables_per_word)

print(syllables_per_word)


# ## PERSONAL PRONOUNS

# In[38]:


import re

# Define the regex pattern for personal pronouns
pronoun_pattern = r'\b(i|we|my|ours|us)\b'

personal_pronouns_list = []

for article in filtered_list:
    personal_pronouns_count = 0
    for word in article:
        personal_pronouns_count += len(re.findall(pronoun_pattern, word, re.IGNORECASE))
    personal_pronouns_list.append(personal_pronouns_count)


print(personal_pronouns_list)


# ## AVG SENTENCE LENGTH,PERCENTAGE OF COMPLEX WORDS,FOG INDEX

# In[39]:


avg_sentence_len = []
pct_of_complex_words = []
fog_index = []

for i in range(len(word_count)):
    num_of_words = word_count[i]
    num_of_sentences = num_of_sentence[i]
    num_of_complex_words = complex_word_counts[i]
    
    avg_sentence_leng = num_of_words / num_of_sentences
    pct_complex_words = num_of_complex_words / num_of_words
    fog_indexx = 0.4 * (avg_sentence_leng + pct_complex_words)
    
    avg_sentence_len.append(avg_sentence_leng)      
    pct_of_complex_words.append(pct_complex_words)    
    fog_index.append(fog_indexx)                   


# ### importing positive and negative words

# In[40]:


positive_words = []
negative_words = []

with open(r"C:\Users\ajith\OneDrive\Desktop\pos,neg dict\positive-words.txt", 'r') as file:
    # Read the contents of the file and split it into words
    file_words = file.read().split()
    # Append the words to the list
    positive_words.extend(file_words)

with open(r"C:\Users\ajith\OneDrive\Desktop\pos,neg dict\negative-words.txt", 'r') as file:
    # Read the contents of the file and split it into words
    file_words = file.read().split()
    # Append the words to the list
    negative_words.extend(file_words)
    
positive_words = [word.lower() for word in positive_words]  #changing into lower case
negative_words = [word.lower() for word in negative_words]  #changing into lower case


# ## POSITIVE,NEGATIVE,POLARITY AND SUBJECTIVITY SCORES

# In[41]:


positive_scores = []
negative_scores = []
polarity_scores = []
subjectivity_scores = []

for i, article in enumerate(filtered_list):
    # Calculate positive score
    pos_score = sum([1 if word in positive_words else 0 for word in article])
    positive_scores.append(pos_score)
    
    # Calculate negative score
    neg_score = sum([1 if word in negative_words else 0 for word in article])
    negative_scores.append(neg_score)
    
    # Calculate polarity score
    pol_score = (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)
    polarity_scores.append(pol_score)
    
    # Calculate subjectivity score
    subj_score = (pos_score + neg_score) / (word_count[i] + 0.000001)
    subjectivity_scores.append(subj_score)


# In[42]:


#posite_score_for_each_article
positive_scores #[score of Article-1, Article-2 ,.....]


# In[43]:


#negative_score_for_each_article
negative_scores


# In[44]:


#polarity_score_for_each_article
polarity_scores


# In[45]:


#subjectivity_score_for_each_article
subjectivity_scores


# In[46]:


#average_sentence_length_in_each_article
avg_sentence_len


# In[47]:


#percentage_of_complex_words_for_each_article
pct_of_complex_words


# In[48]:


#fog_index_for_each_article
fog_index


# In[49]:


#average_words_per_sentence_in_each_article
avg_words_per_sentence


# In[50]:


#comples_words_counts_in_each_article
complex_word_counts


# In[51]:


#word_count_in_each_article
word_count


# In[52]:


#syllables_per_word_in_each_article
syllables_per_word


# In[53]:


#personal_pronouns_in_each_article
personal_pronouns_list


# In[54]:


#average_word_length_in_each_article
avg_word_length


# In[ ]:




