# Import Dependencies
import pandas as pd

# List for use later when checking letter matches
letter_spacing = ["L1", "L2", "L3", "L4", "L5"]
allowed_guesses_df = pd.read_table(
    "wordle-allowed-guesses.txt", delimiter=" ", header=None)
possible_words_df = pd.read_table(
    "wordle-answers-alphabetical.txt", delimiter=" ", header=None)
words_df_static = pd.concat(
    [allowed_guesses_df, possible_words_df]).reset_index(drop=True)
words_df_static = words_df_static.rename(columns={0: "word"})

# Function to narrow down word list if letter is in the correct place


def letter_correct(letter, position, words_df):
    words_df = words_df.loc[words_df[position] == letter, :]
    return words_df

# Function to narrow down word list if letter is not in the word


def letter_missing(letter, words_df):
    for position in ["L1", "L2", "L3", "L4", "L5"]:
        words_df = words_df.loc[words_df[position] != letter, :]
    return words_df

# Function to narrow down word list if letter is in the wrong place


def letter_misplaced(letter, position, words_df):
    words_df = words_df.loc[words_df[position] != letter, :]
    space_list = ["L1", "L2", "L3", "L4", "L5"]
    space_list.remove(position)
    words_df = words_df.loc[(words_df[space_list[0]] == letter) | (words_df[space_list[1]] == letter) | (
        words_df[space_list[2]] == letter) | (words_df[space_list[3]] == letter), :]
    return words_df


# Function to 'play the game': THE MAIN ALGORITHM
def next_guess(words_df):

    scoredict = {}
    for index, row in words_df.iterrows():
        for position in letter_spacing:
            if row[position] in scoredict:
                scoredict[row[position]] += 1
            else:
                scoredict[row[position]] = 1
    score_table = pd.Series(data=scoredict).to_frame().reset_index().rename(
        columns={'index': 'letter', 0: 'totalcount'})

    # Score each word based on letter frequency to choose the best guess. We do this by merging each individual letter to the score
    # table, then adding them into a final score to append to our word table. If a letter is a duplicate, we do not add that score
    # since the information added is likely to be none or very little, and we would gain more for having better variety
    score_list = []
    for index, row in words_df.iterrows():
        score = 0
        letter1_score = [
            row["L1"], score_table.loc[score_table["letter"] == row["L1"], "totalcount"].values[0]]
        letter2_score = [
            row["L2"], score_table.loc[score_table["letter"] == row["L2"], "totalcount"].values[0]]
        letter3_score = [
            row["L3"], score_table.loc[score_table["letter"] == row["L3"], "totalcount"].values[0]]
        letter4_score = [
            row["L4"], score_table.loc[score_table["letter"] == row["L4"], "totalcount"].values[0]]
        letter5_score = [
            row["L5"], score_table.loc[score_table["letter"] == row["L5"], "totalcount"].values[0]]
        score = letter1_score[1]
        if letter2_score[0] != letter1_score[0]:
            score = score + letter2_score[1]
        if (letter3_score[0] != letter1_score[0] and letter3_score[0] != letter2_score[0]):
            score = score + letter3_score[1]
        if (letter4_score[0] != letter1_score[0] and letter4_score[0] != letter2_score[0] and letter4_score[0] != letter3_score[0]):
            score = score + letter4_score[1]
        if (letter5_score[0] != letter1_score[0] and letter5_score[0] != letter2_score[0] and letter5_score[0] != letter3_score[0] and letter5_score[0] != letter4_score[0]):
            score = score + letter5_score[1]
        score_list.append(score)

    # Add Previous calcuations to word list
    words_df['Frequency_Score'] = score_list

    # Choose best guess and create a dataframe split by letter, similar to word list
    maxid = words_df.Frequency_Score.idxmax()
    bestguess = words_df.iloc[maxid, :].values[0]

    return bestguess


# function to runthruogh the inputs from user
def input_unravel(input_dict):
    for item in input_dict.values():
        if item[0] == "correct":
            words_df = letter_correct(item[1], item[2], words_df)
        elif item[0] == "missing":
            words_df = letter_missing(item[1], words_df)
        else:
            words_df = letter_misplaced(item[1], item[2], words_df)

    words_df = words_df.reset_index(drop=True)

    return next_guess(words_df)
