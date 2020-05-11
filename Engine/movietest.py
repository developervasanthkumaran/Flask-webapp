import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class MovieEngine:

    def __init__(self):
        pd.set_option('display.max_columns', 100)
        df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7', skipinitialspace=True)
        self.df = df
        df = df[['Title', 'Genre', 'Director', 'Actors', 'Plot']]
        df = df.fillna("")
        df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
        df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))
        df['Director'] = df['Director'].map(lambda x: x.split(' '))
        self.indices, self.cosine_sim = self.main(df)
        
    def main(self, df):
        self.df = df
        for index, row in df.iterrows():
            row['Actors'] = [x.lower().replace(' ', '') for x in row['Actors']]
            row['Director'] = ''.join(row['Director']).lower()

        df['Key_words'] = ""
        for index, row in df.iterrows():
            plot = row['Plot']
            r = Rake()
            r.extract_keywords_from_text(plot)
            key_words_dict_scores = r.get_word_degrees()
            row['Key_words'] = list(key_words_dict_scores.keys())

        df.drop(columns=['Plot'], inplace=True)

        df.set_index('Title', inplace=True)

        df['bag_of_words'] = ''
        columns = df.columns
        for index, row in df.iterrows():
            words = ''
            for col in columns:
                if col != 'Director':
                    words = words + ' '.join(row[col]) + ' '
                else:
                    words = words + row[col] + ' '
            row['bag_of_words'] = words

        df.drop(columns=[col for col in df.columns if col != 'bag_of_words'], inplace=True)
        count = CountVectorizer()
        count_matrix = count.fit_transform(df['bag_of_words'])
        return pd.Series(df.index), cosine_similarity(count_matrix, count_matrix)

    def recommendations(self, title):
        indices = self.indices
        cosine_sim = self.cosine_sim
        df = self.df
        recommended_movies = []

        idx = indices[indices == title].index[0]

        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
        top_10_indexes = list(score_series.iloc[1:22].index)

        for i in top_10_indexes:
            recommended_movies.append(list(df.index)[i])
        return recommended_movies


