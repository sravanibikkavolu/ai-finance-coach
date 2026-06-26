from app import calculate_budget


def test_calculate_budget_positive_savings():
    income = 50000.0
    rent = 15000.0
    food = 8000.0
    transport = 3000.0
    other = 4000.0

    result = calculate_budget(income, rent, food, transport, other)

    assert result["total_expenses"] == 30000.0
    assert result["savings"] == 20000.0


def test_calculate_budget_deficit():
    income = 20000.0
    rent = 12000.0
    food = 5000.0
    transport = 2000.0
    other = 3000.0

    result = calculate_budget(income, rent, food, transport, other)

    assert result["total_expenses"] == 22000.0
    assert result["savings"] == -2000.0


def test_calculate_budget_zero_savings():
    income = 10000.0
    rent = 5000.0
    food = 2000.0
    transport = 1500.0
    other = 1500.0

    result = calculate_budget(income, rent, food, transport, other)

    assert result["total_expenses"] == 10000.0
    assert result["savings"] == 0.0


def test_calculate_budget_all_zeros():
    result = calculate_budget(0.0, 0.0, 0.0, 0.0, 0.0)
    assert result["total_expenses"] == 0.0
    assert result["savings"] == 0.0
