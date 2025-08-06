from rewards.meteor_reward import meteor
from rewards.pylint_reward import pylint_score
from rewards.kfp_linter_reward import kfp_linter_score

def total_reward(generated, reference):
    return 0.5 * meteor(reference, generated) + 0.25 * pylint_score(generated) + 0.25 * kfp_linter_score(generated)
