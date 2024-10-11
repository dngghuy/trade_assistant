import pandas as pd
import pytest
import numpy as np
from trade_assistant.metrics.metrics import SharpeRatio


@pytest.mark.parametrize(
    "returns, interval, risk_free_rate, expected_sharpe_ratio",
    [
        # Test case 1: Basic example with positive returns
        (pd.Series([0.01, 0.02, -0.01, 0.03, 0.015]), 252, 0.06, -50.30217779),
        # Test case 2: All zero returns
        (pd.Series([0.0, 0.0, 0.0, 0.0, 0.0]), 252, 0.06, -1 * np.inf),
        # Test case 3:  Negative returns
        (pd.Series([-0.01, -0.02, -0.01, -0.03, -0.015]), 252, 0.06, -146.0972279),
        # Test case 4:  Different interval (monthly)
        (pd.Series([0.01, 0.02, -0.01, 0.03, 0.015]), 12, 0.06, -10.97683511),
        # Test case 5: Different risk-free rate
        (pd.Series([0.01, 0.02, -0.01, 0.03, 0.015]), 252, 0.03, -18.19440473),
    ],
)
def test_sharpe_ratio(returns, interval, risk_free_rate, expected_sharpe_ratio):
    sharpe_ratio_calculator = SharpeRatio(interval, risk_free_rate)
    calculated_sharpe_ratio = sharpe_ratio_calculator.calculate(returns)
    assert calculated_sharpe_ratio == pytest.approx(expected_sharpe_ratio, rel=1e-6)
