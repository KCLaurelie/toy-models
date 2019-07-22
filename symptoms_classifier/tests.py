import sys
from symptoms_classifier.symptoms_classifier import *
import pandas as pd
from symptoms_classifier.NLP_text_cleaning import clean_string, text2sentences, preprocess_text, parse_text
from symptoms_classifier.NLP_embedding import fit_text2vec, transform_text2vec, convert_snt2avgtoken, tokenize_sentences
from gensim.models import Word2Vec

spacy_lib = r'C:\Users\K1774755\AppData\Local\Continuum\anaconda3\envs\spacy\Lib\site-packages'
sys.path.append(spacy_lib)
spacy_en_path = os.path.join(spacy_lib, r'en_core_web_sm\en_core_web_sm-2.1.0')


def test_final():
    tweets = TextsToClassify(
        filepath='https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv',
        class_col='airline_sentiment', text_col='text',
        embedding_algo='w2v', embedding_model=None,
        classifier_type='SVM')
    df = tweets.load_data()
    df['tokens_clean'] = tweets.tokenize_text(manually_clean_text=True, update_obj=True)
    # df['tokens_spacy'] = tweets.tokenize_text(manually_clean_text=False, update_obj=True)
    w2v = tweets.train_embedding_model()
    w2v.wv['you']
    emb_x = tweets.embed_text(update_obj=True)
    res = tweets.run_classifier(test_size=0.2)


def quick_embedding_ex(
        data_file='https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv',
        text_col='text',
        class_col='airline_sentiment'):
    data = pd.read_csv(data_file)[[class_col, text_col]]
    data[class_col] = data[class_col].replace({'positive': 1, 'negative': -1, 'neutral': 0})

    sentences = data[text_col]
    y = data[class_col]

    tok_snts = tokenize_sentences(sentences, manually_clean_text=True)  # tokenize sentences
    w2v_model = Word2Vec(tok_snts, size=100, window=5, min_count=4, workers=4)  # train word2vec
    x_emb = convert_snt2avgtoken(sentences, w2v_model, clean_text=True)  # embed sentences
    return [x_emb, y]

def classifier_test():
    data = pd.read_csv(
        "https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv")
    data_clean = data[['airline_sentiment', 'text']].rename(columns={'airline_sentiment': 'class'})
    data_clean['text'] = preprocess_text(data_clean['text'])
    vectorizer = fit_text2vec(data_clean['text'], embedding_algo='word2vec', size=100)
    processed_features = transform_text2vec(data_clean['text'], vectorizer, algo='word2vec')
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(processed_features, data_clean['class'], test_size=0.8,
                                                        random_state=0)

    classifier = classifiers['SVM']
    classifier.fit(x_train, y_train)
    preds = classifier.predict(x_train)
    # test_metrics = gutils.perf_metrics(y_train, preds)

    from sklearn.metrics  import confusion_matrix, classification_report, accuracy_score
    print(confusion_matrix(y_train, preds))
    print(classification_report(y_train, preds))
    print(accuracy_score(y_train, preds))
    return 0


def w2v_test():
    # w2v_model = Word2Vec.load(r'C:\Users\K1774755\Downloads\phd\discharge_summaries_unigram_size100_window5_mincount5')
    w2v_model = Word2Vec.load(
        r'C:\Users\K1774755\Downloads\phd\early_intervention_services_unigram_size100_window5_mincount5')
    w2v_model.wv['attention']
    w2v_model.wv.similar_by_vector(w2v_model.wv['attention'], topn=10)
    w2v_model.wv.similarity('attention', 'concentration')
    vectors = [w2v_model[x] for x in "the patient shows poor concentration".split(' ')]

    sentences = parse_text('C:\\temp\\bla.txt', convert_to_series=True, remove_punctuation=True)
    emb_snt = convert_snt2avgtoken(sentences, w2v_model)


def test0():
    data = pd.read_csv(
        "https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv")
    data_clean = data[['airline_sentiment', 'text']].rename(columns={'airline_sentiment': 'class'})
    txt = data_clean['text'][0:10]
    raw_text = "hi my name is link...I like to fight, And i'm in love with princess zelda.bim. bam.Boum. Bom"
    raw_text = clean_string(raw_text)
    raw_text = text2sentences(raw_text)

    txt = 'C:\\temp\\bla.txt'
    text2sentences(txt)

    clean_text = preprocess_text(txt)
    preprocess_text(txt, remove_stopwords=True, stemmer='snowball', lemmatizer=None)
    # vocab = [["cat", "say", "meow"], ["dog", "say", "woof"]]
    w2v = fit_text2vec(clean_text, min_df=0.00125, max_df=0.7, embedding_algo='tfidf', size=100)
    list(w2v.vocabulary_.keys())[:10]
    processed_features = transform_text2vec(clean_text, w2v, algo='tfidf')

    w2v = fit_text2vec(clean_text, min_df=0.00125, max_df=0.7, embedding_algo='word2vec', size=100)
    list(w2v.wv.vocab)
    return 0
