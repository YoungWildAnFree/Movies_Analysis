class Movie(object):

    # 初始化，设置电影名称、平均评分、豆瓣ID，上映年份
    def __init__(self, name, rating, id_number, year):
        self.name = name
        self.rating = rating
        self.id_number = id_number
        self.year = year
        self.weighted_ratings = []
        self.amount = 0

    # 设置评分星级分布
    def set_weighted_ratings(self, weighted_ratings):
        assert type(weighted_ratings) == list
        self.weighted_ratings = weighted_ratings

    # 设置评分人数
    def set_amount(self, amount):
        self.amount = amount
