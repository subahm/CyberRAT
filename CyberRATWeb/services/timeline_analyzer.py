import spacy

class TimeLineAnalysisResults:
    post_containing_dog_name = None
    post_containing_mothers_maiden = None
    posts_containing_city_names = None
    post_containing_street = None
    post_containing_book = None
    account_unreachable = False
    account_private = False

    def __init__(self, time_line_posts):
        if time_line_posts == "account unreachable":
            self.account_unreachable = True
        elif time_line_posts == "account private":
            self.account_private = True
        else:
            self.post_containing_dog_name = scan_for_dog_name(time_line_posts)
            self.post_containing_mothers_maiden = scan_for_mothers_maiden(time_line_posts)
            self.posts_containing_city_names = scan_for_city_names(time_line_posts)
            self.post_containing_street = scan_for_street_name(time_line_posts)
            self.post_containing_book = scan_for_favourite_book(time_line_posts)

#What was the name of your first/current/favorite pet?
def scan_for_dog_name(time_line_posts):
    return generic_scan("dog", time_line_posts)


def scan_for_mothers_maiden(time_line_posts):

    nlp = spacy.load('en_core_web_sm')
    grandma_token = nlp("grandma")

    max = 0
    for post in time_line_posts:
        doc = nlp(post.post_text)

        check_for_multi_words = False
        for ent in doc.ents:
            if " " in ent.text and ent.label_ == "PERSON":
                check_for_multi_words = True

        if check_for_multi_words:

            grandma_similarity = 0
            key_word_found = False
            for token in doc:
                token_similarity = token.similarity(grandma_token)
                if (token_similarity>0.9):
                    grandma_similarity = token_similarity
                    key_word_found = True
                    break
                else:
                    grandma_similarity = grandma_similarity + token_similarity


            if not key_word_found:
                grandma_similarity = grandma_similarity / len(doc)

            if grandma_similarity > max:
                post_containing_mothers_maiden = post
                max = grandma_similarity


    return post_containing_mothers_maiden

# Where did you meet your spouse?
# Where is your favorite place to vacation?
def scan_for_city_names(time_line_posts):

    nlp = spacy.load('en_core_web_sm')

    location_name_posts = []

    for post in time_line_posts:
        doc = nlp(post.post_text)

        for ent in doc.ents:
            if ent.label_ == "GPE":
                location_name_posts.append(post)


    return location_name_posts

# What is the name of the road you grew up on?
def scan_for_street_name(time_line_posts):
    return generic_scan("street", time_line_posts)


# What Is your favorite book?
def scan_for_favourite_book(time_line_posts):
    return generic_scan("book", time_line_posts)

    
def generic_scan(key_word, time_line_posts):
    nlp = spacy.load('en_core_web_sm')
    keyword_token = nlp(key_word)

    max = 0
    for post in time_line_posts:
        doc = nlp(post.post_text)

        if len(doc.ents) > 0:
            key_word_similarity = 0
            key_word_found = False
            for token in doc:
                token_similarity = token.similarity(keyword_token)
                if token_similarity > 0.8:
                    key_word_similarity = token_similarity
                    key_word_found = True
                    break
                else:
                    key_word_similarity = key_word_similarity + token_similarity

            if not key_word_found:
                key_word_similarity = key_word_similarity / len(doc)

            if key_word_similarity > max:
                post_containing_keyword = post
                max = key_word_similarity


    return post_containing_keyword
