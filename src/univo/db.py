"""
For MVP it fakes a database with a list of categories and pictograms.
In the future, it should connect to a real database."""

categories = ["food", "beverages", "feelings", "actions"]
pictograms = {
    "food": [("apple", "apple.png"), ("bread", "bread.png")],
    "beverages": [("water", "water.png"), ("juice", "juice.png")],
    "feelings": [("happy", "happy.png"), ("sad", "sad.png"), ("tired", "tired.png")],
    "actions": [("drink", "drink.png"), ("eat", "eat.png"), ("sleep", "sleep.png")]
}

def get_categories():
    return categories

def get_pictograms(category):
    return pictograms.get(category, [])