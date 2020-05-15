import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class MovieEngine:

    def __init__(self):
        pd.set_option('display.max_columns', 100)
        df = pd.read_csv('static/dataset/Movie.csv',skipinitialspace=True)
        self.df = df
        df = df[['Title', 'Genres', 'Director', 'Writers', 'Cast', 'Short Summary', 'Runtime', 'Rating', 'Movie Poster']]
        df = df.fillna("")
        df['Cast'] = df['Cast'].apply(lambda x: x.replace(' ', '')).apply(lambda x: x.replace('|', ' '))
        df['Genres'] = df['Genres'].apply(lambda x: x.replace(' ', '')).apply(lambda x: x.replace('|', ' '))
        df['Director'] = df['Director'].apply(lambda x: x.replace(' ', ''))
        df['Writers'] = df['Writers'].apply(lambda x: x.replace(' ', ''))
        self.indices, self.cosine_sim = self.main(df)

    def main(self, df):
        self.df = df
        for index, row in df.iterrows():
            row['Director'] = ''.join(row['Director']).lower()
            row['Cast'] = ''.join(row['Cast']).lower()
            row['Writers'] = ''.join(row['Writers']).lower()

        df['Key_words'] = ""
        for index, row in df.iterrows():
            summary = row['Short Summary']
            r = Rake()
            r.extract_keywords_from_text(summary)
            key_words_dict_scores = r.get_word_degrees()
            row['Key_words'] = list(key_words_dict_scores.keys())
        df.drop(columns=['Short Summary'], inplace=True)
        df.set_index('Title', inplace=True)
        df['bag_of_words'] = df[['Genres', 'Director', 'Writers', 'Cast', 'Key_words']].agg(' '.join, axis=1)
        df.drop(columns=[col for col in df.columns if col != 'bag_of_words'], inplace=True)
        count = CountVectorizer()
        count_matrix = count.fit_transform(df['bag_of_words'])

        return pd.Series(df.index), cosine_similarity(count_matrix, count_matrix)

    def recommendations(self, title):
        if title in self.df.index:
            pass
        else:
            return True
            
        indices = self.indices
        cosine_sim = self.cosine_sim
        df = self.df
        recommended_movies = []
        idx = indices[indices == title].index[0]

        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
        top_10_indexes = list(score_series.iloc[:32].index)

        for i in top_10_indexes:
            recommended_movies.append(list(df.index)[i])
        return recommended_movies


