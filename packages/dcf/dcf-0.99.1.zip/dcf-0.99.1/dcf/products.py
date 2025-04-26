# -*- coding: utf-8 -*-

# dcf
# ---
# A Python library for generating discounted cashflows.
#
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.7, copyright Friday, 14 January 2022
# Website:  https://github.com/sonntagsgesicht/dcf
# License:  Apache License 2.0 (see LICENSE file)


try:
    import businessdate as bd
except ImportError:
    bd = None

from dcf import CashFlowList
from dcf.plans import annuity, outstanding

TODAY = 0.0
MATURITY = 10
BOND_TENOR = 1
SWAP_TENOR = 3 / 12


def _payment_dates(origin, num, frequency, *,
                   roll=None, convention=None, holidays=None):
    if isinstance(origin, float):
        pay_dates = [origin + step / frequency for step in range(num + 1)]
    else:
        start = bd.BusinessDate(origin)
        step = bd.BusinessPeriod(f"{12 // frequency}m")
        end = start + step * num
        pay_dates = bd.BusinessSchedule(start, end, step, roll=roll)
        pay_dates = pay_dates.first_stub_long()
        pay_dates.adjust(convention, holidays)
    return pay_dates


def mortgage(amount=None, fixed_rate=None, *,
             num=None, redemption_rate=None,
             annuity_amount=None, frequency=12, origin=None):
    redemption = annuity(
        num=num,
        amount=amount,
        fixed_rate=fixed_rate / frequency,
        redemption_rate=redemption_rate / frequency,
        annuity_amount=annuity_amount
    )
    out = outstanding(
        redemption,
        amount=amount
    )
    pay_dates = _payment_dates(
        origin,
        len(redemption),
        frequency,
        roll=origin
    )

    cashflows = CashFlowList.from_rate_cashflows(
        pay_dates,
        amount_list=out,
        fixed_rate=fixed_rate,
        day_count=1 / frequency
    )
    cashflows += CashFlowList.from_fixed_cashflows(
        pay_dates,
        amount_list=redemption
    )
    return cashflows


def bullet(amount=None, fixed_rate=None, *,
           num=None, frequency=12, origin=None):
    pay_dates = _payment_dates(
        origin,
        num,
        frequency,
        roll=origin
    )
    cashflows = CashFlowList.from_rate_cashflows(
        pay_dates,
        amount_list=amount,
        fixed_rate=fixed_rate,
        day_count=1 / frequency
    )
    cashflows += CashFlowList.from_fixed_cashflows(
        pay_dates[-1:],
        amount_list=amount
    )
    return cashflows


def bond(maturity_date, *,
         notional_amount=100.0, origin=None, day_count=None,
         fixed_rate=0.0, frequency=1,
         convention=None, holidays=None):

    pay_dates = _payment_dates(
        origin,
        None,
        frequency=frequency,
        roll=maturity_date,
        convention=convention,
        holidays=holidays
    )

    start = pay_dates[0]
    end = pay_dates[-1]

    principal = CashFlowList.from_fixed_cashflows(
        [start.adjust(convention, holidays)],
        notional_amount
    )
    redemption = CashFlowList.from_fixed_cashflows(
        [end.adjust(convention, holidays)],
        notional_amount
    )

    if not fixed_rate:
        return -principal + redemption

    interest = CashFlowList.from_rate_cashflows(
        pay_dates[1:],
        notional_amount,
        origin=start,
        fixed_rate=fixed_rate,
        day_count=day_count
    )
    return -principal + interest + redemption


def irs():
    return


def asset_swap():
    return
