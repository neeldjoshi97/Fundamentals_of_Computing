"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """

    value_dic = {}
    for element in hand:
        if element in value_dic:
            value_dic[element] = value_dic[element] + element
        else:
            value_dic[element] = element
    max_list = list()
    dummy = list()
    for ind in value_dic.values():
        dummy.append(ind)
    m_value = max(dummy)
    for key in value_dic:
        if value_dic[key] == m_value:
            max_list.append(key)
    # print max_list, m_value
    return m_value


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcome_list = []
    for ind in range(1, num_die_sides + 1):
        outcome_list.append(ind)

    subset = gen_all_sequences(outcome_list, num_free_dice)
    # print subset
    score_list = []
    for each_set in subset:
        dummy_hand = []
        for value in held_dice:
            dummy_hand.append(value)
        for value in each_set:
            dummy_hand.append(value)

        each_score = score(dummy_hand)
        score_list.append(each_score)
        # score list computed
    addition = sum(score_list)
    exp_value = float(addition) / len(score_list)
    # exp_value = round(exp_value, 2)
    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    if len(hand) == 0:
        return set([()])
    dummy_hand = list(hand)

    last_ele = dummy_hand[-1]
    rem_hand = dummy_hand[:-1]
    gen_hand = gen_all_holds(tuple(rem_hand)) # recursion
    dummy_gen_hand = gen_hand.copy()
    for each_tup in dummy_gen_hand:
        each_list = list(each_tup)
        add_list = []
        for each in each_list:
            add_list.append(each)
        add_list.append(last_ele)
        add_list.sort()
        add_tup = tuple(add_list)
        gen_hand.add(add_tup)

    return gen_hand



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_hands = gen_all_holds(hand)
    leng = len(hand)
    exp_dic = {}
    exp_list = []
    for each_choice in all_hands:
        exp_v = expected_value(each_choice, num_die_sides, leng - len(each_choice))
        exp_dic[each_choice] = exp_v
        exp_list.append(exp_v)
    # print exp_dic
    max_exp = max(exp_list)
    max_tup = []
    for tups in exp_dic:
        if exp_dic[tups] == max_exp:
            max_tup.append(tups)
    return (max_exp, max_tup[0])


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)

    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

#run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
