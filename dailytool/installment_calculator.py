"""
分期计算器
"""


def installment_calculator(total_price, down_payment_ratio, installment_periods, annual_interest_rate):
    down_payment_amount = total_price * down_payment_ratio / 100
    principal = total_price - down_payment_amount
    monthly_interest_rate = annual_interest_rate / 12 / 100
    monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -installment_periods)

    return down_payment_amount, monthly_payment


if __name__ == "__main__":
    total_price = float(input("请输入商品总价："))
    down_payment_ratio = float(input("请输入首付比例（百分比）："))
    installment_periods = int(input("请输入分期期数（月）："))
    annual_interest_rate = float(input("请输入年利率（百分比）："))

    down_payment_amount, monthly_payment = installment_calculator(total_price, down_payment_ratio, installment_periods,
                                                                  annual_interest_rate)
    print("首付金额：%.2f" % down_payment_amount)
    print("每月还款金额：%.2f" % monthly_payment)
