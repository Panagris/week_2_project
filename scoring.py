# SCORE_TO_XP[i] gives the number of XP points gained from
# scoring a i/5 on a quiz
SCORE_TO_XP = [0, 0, 0, 100, 200, 300]


def xp_level(xp):
    LEVELS = ["Newbie", "Novice", "Apprentice", "Expert", "Master"]

    # Cap XP at 400 to ensure the next line doesn't go out of bounds
    xp = min(xp, 400)

    # Scoring system kept simple for the sake of demonstration
    # should be a little bit more involved in actuality
    return LEVELS[xp // 100]
