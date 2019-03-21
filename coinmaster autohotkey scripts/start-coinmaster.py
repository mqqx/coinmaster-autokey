import datetime
import time

PURCHASES = ["min", "caf", "sho", "far", "com", "bak", "bus", "hou", "cin", "pow", "res", "war", "fac", "rai", "hos",
             "hot", "tra", "sup", "mus", "fas", "cas", "sch", "the", "bar", "piz", "gam", "pol", "flo", "dep", "boo",
             "ban", "pos", "wor", "cru", "mov", "amu", "spo", "oil", "shu", "sat"]

UPGRADES = ["v", "cli", "sol", "cri", "v", "dep", "mul", "cli", "v", "sol", "cri", "dep"]
SINGLE_UPGRADES = ["dis", "coi"]
COMMAND_INTERVALS = [10, 15, 30, 45, 60, 90]

INITIAL_REFACTOR_CODE = 4190
INITIAL_REFACTOR_CODE_DATE = datetime.date(2019, 3, 21)
MAX_ROUNDS = 3

__purchases_current_index__ = 0
__upgrades_current_index__ = 0
__single_upgrades_current_index__ = 0
__current_round__ = 1
__current_round_command_count__ = 0
__current_refactor_code__ = INITIAL_REFACTOR_CODE
__should_buy_max_all__ = True


def main():
    send_text("started script")
    time.sleep(1)
    while True:
        restart()
        if check_stop_value():
            set_stop_value()
            send_text("stopped script")
            break


def restart():
    send_text("!b m all")
    count = 1

    while __current_round__ <= MAX_ROUNDS:
        time.sleep(0.96)
        if check_stop_value():
            return

        send_count_spam(count)

        # send next buy/upgrade command
        check_and_send_next_command(count)

        # send guild raid/open crates
        send_additional_commands(count)

        count += 1

    set_variables()
    refactor()


# Use the GLOBALS directly. If not set, use False as the default.
def check_stop_value():
    return store.GLOBALS.get("STOP", False)


def set_stop_value():
    # Reset the global variable, otherwise the next script will be aborted immediately.
    store.set_global_value("STOP", False)


def send_count_spam(count):
    if count % 2 == 0:
        count_as_string = str(count)
        send_text(count_as_string)


def check_and_send_next_command(count):
    global __should_buy_max_all__
    send_next_single_upgrade(count)

    command_interval_index = min(__current_round__ - 1, len(COMMAND_INTERVALS) - 1)
    is_time_for_next_command = count % COMMAND_INTERVALS[command_interval_index] == 0

    if is_time_for_next_command:
        # buys and upgrades should be sent in a 2:1 ratio (2 buys, 1 upgrade)
        if __current_round__ == 1:
            # in the first round every now and then buy max all is used to prevent unrecognized commands
            if __current_round_command_count__ % 7 == 0 and __should_buy_max_all__:
                send_text("!b m all")
                __should_buy_max_all__ = False
            else:
                send_next_command(3)
                __should_buy_max_all__ = True

        # buys and upgrades should be sent in a 4:1 ratio (4 buys, 1 upgrade)
        elif __current_round__ == 2:
            send_next_command(5)
        else:
            send_next_upgrade_command()


def send_next_command(update_modulo_interval):
    if __current_round_command_count__ % update_modulo_interval == 0:
        send_next_upgrade_command()
    else:
        send_next_buy_command()


def send_next_buy_command():
    global __purchases_current_index__
    if __purchases_current_index__ == len(PURCHASES):
        __purchases_current_index__ = 0
        prepare_next_round()
        # in dem fall kann neue runde direkt beginnen
        send_next_upgrade_command()
    else:
        send_text("!b max " + PURCHASES[__purchases_current_index__])
        __purchases_current_index__ += 1
        increment_current_round_command_count()


def send_next_upgrade_command():
    global __upgrades_current_index__
    if __upgrades_current_index__ == len(UPGRADES):
        __upgrades_current_index__ = 0
        if __current_round__ >= 3:
            prepare_next_round()

    send_text("!upgrade max " + UPGRADES[__upgrades_current_index__])
    __upgrades_current_index__ += 1
    increment_current_round_command_count()


def prepare_next_round():
    global __current_round__
    global __current_round_command_count__
    __current_round__ += 1
    __current_round_command_count__ = 0


def increment_current_round_command_count():
    global __current_round_command_count__
    __current_round_command_count__ += 1


def send_next_single_upgrade(count):
    global __single_upgrades_current_index__
    if __single_upgrades_current_index__ < 3 and count % 5 == 0:
        send_text("!upgrade max " + SINGLE_UPGRADES[__single_upgrades_current_index__])
        __single_upgrades_current_index__ += 1


def send_additional_commands(count):
    if count % 300 == 0:
        send_text("!guild raid")
    elif count % 287 == 0:
        send_text("!swap")
        send_text("!crate all")
        send_text("!swap")


def get_current_refactor_code():
    today = datetime.date.today()
    diff = today - INITIAL_REFACTOR_CODE_DATE
    days_since_refactor_code_date = diff.days
    return INITIAL_REFACTOR_CODE + (10 * days_since_refactor_code_date)


def set_variables():
    global __purchases_current_index__
    global __upgrades_current_index__
    global __single_upgrades_current_index__
    global __current_round__
    global __current_round_command_count__
    global __current_refactor_code__

    __purchases_current_index__ = 0
    __upgrades_current_index__ = 0
    __single_upgrades_current_index__ = 0
    __current_round__ = 1
    __current_round_command_count__ = 0
    __current_refactor_code__ = get_current_refactor_code()


def refactor():
    for i in range(-20, 20, 10):
        send_refactor_command_and_sleep(i)


def send_refactor_command_and_sleep(_diff_to_current_ref_code_):
    send_text("!refactor city " + str(__current_refactor_code__ + _diff_to_current_ref_code_))
    time.sleep(3)


def send_text(_text_to_send):
    keyboard.send_keys(_text_to_send)
    keyboard.send_keys("<enter>")
    time.sleep(0.1)


main()
