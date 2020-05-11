class interface:
  def __init__(self, book_o, movie_o):
    self.book_o = book_o
    self.movie_o = movie_o  
    

  def controller(self, m_val, b_val):
    bf = self.book_o
    mf = self.movie_o
    br = ["Books"]
    mr = ["Movies"]
    bres = bf.recommendations(b_val)
    br.append(bres)
    mres = mf.recommendations(m_val)
    mr.append(mres)
    return [mr, br]
  
