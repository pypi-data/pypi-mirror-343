import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import seaborn as sns
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Step 1: Text Preprocessing (Tokenization, Stopword Removal, Lemmatization)
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    # Remove stopwords and non-alphabetic words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
    return ' '.join(tokens)

d['Processed Document'] = d['product'].apply(preprocess_text)

# Step 2: Word Frequency Analysis using CountVectorizer
vectorizer = CountVectorizer(max_features=10)
X = vectorizer.fit_transform(d['Processed Document'])
word_freq = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
word_freq = word_freq.sum(axis=0).sort_values(ascending=False)

# Step 3: Sentiment Analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

d['Sentiment'] = d['product'].apply(get_sentiment)

# Step 4: Topic Modeling using LDA (Latent Dirichlet Allocation)
lda = LatentDirichletAllocation(n_components=2, random_state=42)
lda.fit(X)



# 1. Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(d['Processed Document']))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Processed Documents')
plt.tight_layout()
plt.show()

# 2. Bar Chart for Word Frequencies
plt.figure(figsize=(8, 6))
word_freq.head(10).plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Top 10 Word Frequencies')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


# 3. Sentiment Analysis Pie Chart
sentiment_counts = d['Sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')).value_counts()
plt.figure(figsize=(8, 6))
sentiment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Sentiment Analysis')
plt.ylabel('')
plt.tight_layout()
plt.show()



# 4. Topic Modeling Bar Chart (Topic Distribution)
topic_distribution = lda.transform(X)
topic_keywords = [', '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-6:-1]]) for topic in lda.components_]
topic_df = pd.DataFrame(topic_distribution, columns=['Topic 1', 'Topic 2'])

plt.figure(figsize=(8, 6))
sns.barplot(x=topic_df.columns, y=topic_df.mean().values, palette='viridis')
plt.title('Topic Modeling - Topic Distribution')
plt.ylabel('Average Proportion')
plt.tight_layout()
plt.show()

