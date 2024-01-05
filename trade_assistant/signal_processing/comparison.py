from trade_assistant.model.symbol import Symbol
from trade_assistant.signal_processing.moving_average import MovingAverage
from trade_assistant.signal_processing.resistance_support import SupportResistanceIndicator


def is_reaching_support(
        support_resistance: SupportResistanceIndicator,
        prev_price: Symbol,
        curr_price: Symbol,
        thresh: float,
):
    """
    Should know the direction and velocity (?) and momentum
    """
    direction = prev_price.current - curr_price.current
    support_thresh_price = support_resistance.list_supports[-1] * (1 + thresh)
    decrease_trend = direction < 0
    curr_price_in_thresh = (
        (curr_price.current <= support_thresh_price)
        and (curr_price.current > support_resistance.list_supports[-1])
    )

    return decrease_trend and curr_price_in_thresh


def is_reaching_resistance(
        support_resistance: SupportResistanceIndicator,
        prev_price: Symbol,
        curr_price: Symbol,
        thresh: float,
):
    """
    Should know the direction and velocity (?) and momentum
    """
    direction = prev_price.current - curr_price.current
    resistance_thresh_price = support_resistance.list_resistances[-1] * (1 - thresh)
    increase_trend = direction > 0
    curr_price_in_thresh = (
        (curr_price.current > resistance_thresh_price)
        and (curr_price.current <= support_resistance.list_resistances[-1])
    )

    return increase_trend and curr_price_in_thresh


def is_through_support(
        support_resistance: SupportResistanceIndicator,
        prev_price: Symbol,
        curr_price: Symbol
):
    """
    """
    decrease_trend = curr_price.current < prev_price.current
    through_support = (
        (prev_price.current > support_resistance.list_supports[-1])
        and (curr_price.current <= support_resistance.list_supports[-1])
    )

    return decrease_trend and through_support


def is_through_resistance(
        support_resistance: SupportResistanceIndicator,
        prev_price: Symbol,
        curr_price: Symbol
):
    """
    """
    increase_trend = curr_price.current > prev_price.current
    through_resistance = (
        (prev_price.current <= support_resistance.list_resistances[-1])
        and (curr_price.current > support_resistance.list_resistances[-1])
    )

    return increase_trend and through_resistance


def is_over_moving_average(moving_average: MovingAverage, price: Symbol, compared_by: str = 'close'):
    if compared_by == 'volume':
        return price.volume > moving_average.list_moving_averages[-1]
    elif compared_by == 'close':
        return price.current > moving_average.list_moving_averages[-1]
    elif compared_by == 'lowest':
        return price.lowest > moving_average.list_moving_averages[-1]
    elif compared_by == 'highest':
        return price.highest > moving_average.list_moving_averages[-1]


def is_under_moving_average(moving_average: MovingAverage, price: Symbol, compared_by: str = 'close'):
    if compared_by == 'volume':
        return price.volume < moving_average.list_moving_averages[-1]
    elif compared_by == 'close':
        return price.current < moving_average.list_moving_averages[-1]
    elif compared_by == 'lowest':
        return price.lowest < moving_average.list_moving_averages[-1]
    elif compared_by == 'highest':
        return price.highest < moving_average.list_moving_averages[-1]


