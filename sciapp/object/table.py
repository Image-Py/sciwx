class Table():
    def __init__(self, df=None):
        self.name = 'Table'
        self.df = df
        self.rg = None
        self.props = None
        if not df is None:
            self.count_range()
        
    @property
    def title(self): return self.name

    @property
    def nbytes(self):
        return self.data.memory_usage().sum()

    @property
    def columns(self):return self.data.columns

    @property
    def index(self):return self.data.index

    @property
    def shape(self): return self.data.shape

    @property
    def data(self): return self.df
    
    @data.setter
    def data(self, df):
        self.df, self.props = df, None
        self.rowmsk, self.colmsk = [],[]
        self.count_range()

    @property
    def style(self):
        props, data = self.props, self.data
        if props is None or set(props)!=set(data.columns):
            ps = [[3, (0,0,0), (0,0,255), 'Text'] for i in data.columns]
            self.props = dict(zip(data.columns, ps))
        return self.props

    def set_style(self, col, **key):
        for i, name in enumerate(['accu', 'tc', 'lc', 'ln']):
            if name in key: self.style[col][i] = key[name]

    def count_range(self):
        rg = list(zip(self.data.min(), self.data.max()))
        self.rg = dict(zip(self.data.columns, rg))

    def select(self, rs=[], cs=[], byidx=False):
        if byidx: rs, cs = self.df.index[rs], self.df.columns[cs]
        self.rowmsk, self.colmsk = rs, cs
        
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    df = pd.DataFrame(np.zeros((10,5)), columns=list('abcde'))
    table = Table(df)
    
