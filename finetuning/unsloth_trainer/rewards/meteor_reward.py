from nltk.translate.meteor_score import single_meteor_score

def meteor(reference, hypothesis):
    return single_meteor_score(reference, hypothesis)
