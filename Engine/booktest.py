import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class BookEngine:

    def __init__(self):
        pd.set_option('display.max_columns', 100)
        df = pd.read_csv('https://gist.githubusercontent.com/jaidevd/23aef12e9bf56c618c41/raw/c05e98672b8d52fa0cb94aad80f75eb78342e5d4/books.csv', skipinitialspace=True)
        self.df = df
        df = df[['Title', 'Author', 'Genre', 'Publisher']]
        df = df.fillna("")
        self.indices, self.cosine_sim = self.main(df)

    def main(self, df):
        self.df = df
        df['bag_of_words'] = df[['Genre', 'Publisher', 'Author']].agg(' '.join, axis=1)
        df.set_index('Title', inplace=True)
        df = df.apply(lambda x: x.str.replace(',', ''))
        df.drop(columns=[col for col in df.columns if col != 'bag_of_words'], inplace=True)
        count = CountVectorizer()
        count_matrix = count.fit_transform(df['bag_of_words'])
        indices = pd.Series(df.index)
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        return indices, cosine_sim

    def recommendations(self, title):
        recommended_books = []
        indices = self.indices
        cosine_sim = self.cosine_sim
        df = self.df
        # gettin the index of the movie that matches the title
        idx = indices[indices == title].index[0]

        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

        _indexes = list(score_series.iloc[1:22].index)
        for i in _indexes:
            recommended_books.append(list(df.index)[i])
        return recommended_books



