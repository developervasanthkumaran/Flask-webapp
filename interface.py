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
    if bres == True:
      br.append(['No Results Found'])
    else:
      br.append(bres)
    mres = mf.recommendations(m_val)
    if mres == True:
      mr.append(['No Results Found'])
    else:
      mr.append(mres)
    return [mr, br]
  
