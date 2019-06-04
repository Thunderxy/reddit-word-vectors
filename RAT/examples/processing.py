from RAT.pushshift.load_data import Content
from RAT.similarity.text_preprocessing import get_sentences


my_file = Content('askreddit_comments.json.gz')
my_comments = my_file.load_comments()

for i in get_sentences(my_comments[0:1000]):
    print(i)
