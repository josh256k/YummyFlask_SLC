from .recipe import Recipe
class Category(object):
    """docstring for Category"""

    def __init__(self, title):
        self.title = title
        self.categories={}

    def add_category(self, title):
        """ add category method"""
        if title not in self.categories and title != "" and title != " ":
            self.categories[title] = Category(title)
            return True
        return False

    def edit_category(self, title, new_title):
        """ edit category method"""
        if title in self.categories and new_title != "" and new_title !=" ":
            self.categories[new_title] = self.categories.pop(title)
            return True
        return False

    def delete_category(self, title):
        """ delete category method"""
        if title in self.categories:
            self.categories.pop(title)
            return True
        return False
    