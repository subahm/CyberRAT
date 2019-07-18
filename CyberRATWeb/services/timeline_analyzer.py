import spacy
from CyberRatv1.CyberRATWeb.scrapers.timeline_post import TimelinePost


# test image/ text for dog and then nlp for names
def scan_for_dog_name(time_line_posts):

    nlp = spacy.load('en_core_web_sm')
    dog_token = nlp("dog")

    max = 0
    for post in time_line_posts:
        doc = nlp(post.post_text)

        if len(doc.ents) > 0:

            dog_similarity = 0
            for token in doc:
                dog_similarity = dog_similarity + token.similarity(dog_token)

            dog_similarity = dog_similarity/len(doc)

            if dog_similarity > max:
                probable_post_containing_dog_name = doc.text
                max = dog_similarity


    return probable_post_containing_dog_name

def scan_for_mothers_maiden(time_line_posts):

    nlp = spacy.load('en_core_web_sm')
    grandma_token = nlp("grandma")

    max = 0
    for post in time_line_posts:
        doc = nlp(post.post_text)

        check_for_multi_words = False
        for ent in doc.ents:
            if " " in ent.text:
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

            print(grandma_similarity)

            if grandma_similarity > max:
                probable_post_containing_mothers_maiden = doc.text
                max = grandma_similarity


    return probable_post_containing_mothers_maiden

# any streets or raods you grew up on

# places you may live

# Where is your favorite place to vacation?

# What is your favorite food?

# What was the first company that you worked for?