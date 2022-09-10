"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided # has the BuildInfo class

# Constants
SIM_TIME = 10000000000.0
class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._cookies_now = 0.0
        self._time_now = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return '\n' + 'Time: ' + str(self._time_now) + '\n' + 'Current Cookies: ' + str(self._cookies_now) + '\n' + 'CPS: ' + str(self._cps) + '\n' + 'Total Cookies: ' + str(self._total_cookies)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cookies_now

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time_now

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        dummy_list = list(self._history)
        return dummy_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._cookies_now >= cookies:
            return 0.0
        delta_time = (cookies - self._cookies_now) / self._cps
        delta_time = math.ceil(delta_time)
        return delta_time

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time_now += time
            extra_cookies = self._cps * time
            self._cookies_now += extra_cookies
            self._total_cookies += extra_cookies

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies_now >= cost:
            self._cookies_now -= cost
            self._cps += additional_cps
            tup = (self._time_now, item_name, cost, self._total_cookies)
            self._history.append(tup)


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    info = build_info.clone()
    c_s = ClickerState()

    # looping over time
    while c_s.get_time() <= duration:

        item_name = strategy(c_s.get_cookies(), c_s.get_cps(), c_s.get_history(), duration - c_s.get_time(), info)
        if item_name == None:
            break

        cost = info.get_cost(item_name)
        cps = info.get_cps(item_name)
        time_to_wait = c_s.time_until(cost)

        if time_to_wait + c_s.get_time() > duration:
            time_left = duration - c_s.get_time()
            c_s.wait(time_left)
            return c_s

        c_s.wait(time_to_wait)
        c_s.buy_item(item_name, cost, cps)
        info.update_item(item_name)

    time_left = duration - c_s.get_time()
    c_s.wait(time_left)

    return c_s


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    tup = history[-1]
    time = tup[0]
    info1 = build_info
    items = info1.build_items()
    items_costs = {}
    for each in items:
        items_costs[each] = info1.get_cost(each)
    time_needed = items_costs['Cursor'] / cps
    time_needed = math.ceil(time_needed)
    if time + time_needed > SIM_TIME:
        values = []
        for key in items_costs:
            values.append(items_costs[key])
        cheapest_value = min(values)
        for key in items_costs:
            if items_costs[key] == cheapest_value:
                return str(key)
    return 'Cursor'

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    tup = history[-1]
    time = tup[0]
    info1 = build_info
    items = info1.build_items()
    items_costs = {}
    for each in items:
        items_costs[each] = info1.get_cost(each)
    time_needed = math.ceil(items_costs['Cursor'] / cps)
    if time + time_needed > SIM_TIME:
        values = [None]
        for key in items_costs:
            if items_costs[key] <= cookies + time_left * cps:
                values.append(items_costs[key])
        exp_value = max(values)
        for key in items_costs:
            if items_costs[key] == exp_value:
                return str(key)

    return 'Cursor'

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    info1 = build_info
    items = info1.build_items()
    items_costs = {}
    items_cps = {}
    items_ratio = {}
    ratio_list = []
    for each in items:
        items_costs[each] = info1.get_cost(each)
        items_cps[each] = info1.get_cps(each)
        items_ratio[each] = items_costs[each] / items_cps[each]
        ratio_list.append(items_ratio[each])
    min_ratio = min(ratio_list)
    for each in items_ratio:
        if items_ratio[each] == min_ratio:
            exp_item = each

    return exp_item

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    print
    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    print
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    print
    run_strategy("Best", SIM_TIME, strategy_best)

run()
