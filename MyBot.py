from penguin_game import *

attack_flag = False


def get_the_closest_iceberg(game, from_iceberg):
    icebergs = game.get_neutral_icebergs()
    closest = icebergs[0]
    for iceberg in icebergs:
        if from_iceberg.get_turns_till_arrival(iceberg) < from_iceberg.get_turns_till_arrival(
                closest) and closest is not from_iceberg:
            closest = iceberg
    return closest


def get_all_my_penguins(game):
    penguins = 0
    for icebergs in game.get_my_icebergs():
        penguins += icebergs.penguin_amount
    return penguins


def it_is_time_to_attack(game):
    enemy_icepital = get_the_enemy_icepital(game)
    enemy_penguins = enemy_icepital.penguin_amount
    enemy_penguins += enemy_icepital.penguins_per_turn * get_my_icepital(game).get_turns_till_arrival(enemy_icepital)
    my_penguins = get_all_my_penguins(game)
    return my_penguins > enemy_penguins and amount_of_attacking_iceberg(game, get_my_icepital(game))[
        1] < my_penguins - enemy_penguins


def upgrade_icepital(game):
    my_icepital = get_my_icepital(game)
    if my_icepital.can_upgrade():
        my_icepital.upgrade()


def get_my_icepital(game):
    for iceberg in game.get_my_icebergs():
        if iceberg.is_icepital:
            return iceberg


def get_the_enemy_icepital(game):
    for iceberg in game.get_enemy_icebergs():
        if iceberg.is_icepital:
            return iceberg


def attack_with_all_power(game):
    my_icebergs = game.get_my_icebergs()
    for iceberg in my_icebergs:
        iceberg.send_penguins(get_the_enemy_icepital(game), iceberg.penguin_amount)


def get_weakest_enemy_iceberg(game):
    enemy_icebegs = game.get_enemy_icebergs()
    smallest = enemy_icebegs[0]
    for enemy_icebeg in enemy_icebegs:
        if smallest.penguin_amount > enemy_icebeg.penguin_amount:
            smallest = enemy_icebeg
    return smallest


def attack_the_weakest_iceberg(game, target):
    target_amount = target.penguin_amount + 5 + target.penguins_per_turn * get_my_icepital(game).get_turns_till_arrival(
        target)
    our_icebergs = game.get_my_icebergs()
    amount = target_amount / len(our_icebergs)
    for iceberg in our_icebergs:
        if iceberg.penguin_amount < amount:
            return
    for iceberg in our_icebergs:
        iceberg.send_penguins(target, amount)


def upgrade_all_icebergs_to_level_2(game):
    our_icebergs = game.get_my_icebergs()
    for iceberg in our_icebergs:
        if iceberg.can_upgrade() and iceberg.level == 1:
            iceberg.upgrade()


#doesnt work
# def send_penguin_to_save_me(game, target):
#     icebergs = game.get_my_icebergs
#     amount_of_attackers = amount_of_attacking_iceberg(game, target)[1] - amount_of_attacking_iceberg(game, target)[0] * target.penguins_per_turn
#     amount = amount_of_attackers // len(game.get_my_icebergs()) + 2
#     while amount_of_attackers > 0:
#         for iceberg in icebergs:
#             if iceberg != target:
#                 if iceberg.penguin_amount > amount*2:
#                     iceberg.send_penguins(target, amount*2)
#                     amount_of_attackers -= amount*2
#                 elif iceberg.penguin_amount > amount:
#                     iceberg.send_penguins(target, amount)
#                     amount_of_attackers -= amount

def send_penguin_to_save_me(game,target):
    icepital = get_my_icepital(game)
    icebergs = game.get_my_icebergs()
    for iceberg in icebergs:
        if iceberg != icepital:
            iceberg.send_penguins(target,iceberg.penguin_amount - 1)



def amount_of_attacking_iceberg(game, target):
    enemy_penguin_groups = game.get_enemy_penguin_groups()
    total_amount_of_fers_attacking_me = 0
    smallest_turns_till_arraivel = 0
    if len(enemy_penguin_groups) == 0:
        return 0, 0
    for group in enemy_penguin_groups:
        if group.destination == target:
            total_amount_of_fers_attacking_me += group.penguin_amount
            if group.source.get_turns_till_arrival(target) < smallest_turns_till_arraivel:
                smallest_turns_till_arraivel = group.get_turns_till_arrival(target)
    return smallest_turns_till_arraivel, total_amount_of_fers_attacking_me

def am_i_safe(game):
    icepital = get_my_icepital(game)
    icebergs = game.get_my_icebergs()
    is_there_icepital = False
    smallest_turns_till_arraivel = amount_of_attacking_iceberg(game, icepital)[0]
    total_amount_of_fers_attacking_me = amount_of_attacking_iceberg(game, icepital)[1]
    for iceberg in icebergs:
        if iceberg.is_icepital:
            is_there_icepital = True
    #if there is no icepital there is no penguin_amount and it crashes ---- fix this
    if len(game.get_enemy_penguin_groups()) is 0 or is_there_icepital == False or total_amount_of_fers_attacking_me < icepital.penguin_amount + (icepital.penguins_per_turn * smallest_turns_till_arraivel):
        return False
    else:
        return True


def save_me(game):
    icepital = get_my_icepital(game)
    send_penguin_to_save_me(game, icepital)


#doesnt work
# def defense_everything(game):
#     total_amount_of_fers_attacking_me = 0
#     smallest_turns_till_arraivel = 0
#     icebergs = game.get_my_icebergs()
#     for iceberg in icebergs:
#         total_amount_of_fers_attacking_me = amount_of_attacking_iceberg(game,iceberg)[1]
#         smallest_turns_till_arraivel = amount_of_attacking_iceberg(game,iceberg)[0]
#         if total_amount_of_fers_attacking_me != 0:
#             send_penguin_to_save_me(game,iceberg)


def do_turn(game):
    if game.turn == 1:
        upgrade_icepital(game)
    elif game.turn == 7:
        closest = get_the_closest_iceberg(game, get_my_icepital(game))
        get_my_icepital(game).send_penguins(closest, 11)
    elif game.turn == 18:
        closest = get_the_closest_iceberg(game, get_my_icepital(game))
        get_my_icepital(game).send_penguins(closest, 11)

    global attack_flag
    if am_i_safe(game):
        save_me(game)
    elif not attack_flag:
        if it_is_time_to_attack(game):
            attack_with_all_power(game)
            attack_flag = True
    else:
        upgrade_all_icebergs_to_level_2(game)

    if game.turn > 30 and not attack_flag:
        attack_the_weakest_iceberg(game, get_weakest_enemy_iceberg(game))
