"""
Finance assistant tools for the CloudiQS Agentic AI Bakery.

Provides burn rate calculations, runway projections, financial summaries,
and revenue forecasting. All data is mock/simulated for demo purposes.
"""

from datetime import datetime, timedelta

from strands import tool


@tool
def calculate_burn_rate(monthly_expenses: float, monthly_revenue: float) -> dict:
    """Calculate the monthly burn rate for the company.

    Burn rate is the rate at which a company spends its cash reserves.
    Gross burn is total monthly spending; net burn accounts for revenue.

    Args:
        monthly_expenses: Total monthly operating expenses in dollars.
        monthly_revenue: Total monthly revenue in dollars.

    Returns:
        A dict with gross burn rate, net burn rate, revenue offset,
        and a health assessment.
    """
    if monthly_expenses < 0:
        return {"error": "Monthly expenses cannot be negative."}
    if monthly_revenue < 0:
        return {"error": "Monthly revenue cannot be negative."}

    gross_burn = monthly_expenses
    net_burn = monthly_expenses - monthly_revenue
    revenue_offset_percent = (
        (monthly_revenue / monthly_expenses * 100) if monthly_expenses > 0 else 0.0
    )

    if net_burn <= 0:
        health = "Profitable"
        assessment = (
            "The company is generating more revenue than it spends. "
            "Net cash position is positive."
        )
    elif revenue_offset_percent >= 75:
        health = "Near Breakeven"
        assessment = (
            "Revenue covers over 75% of expenses. The company is approaching "
            "profitability and burn is well-managed."
        )
    elif revenue_offset_percent >= 50:
        health = "Moderate Burn"
        assessment = (
            "Revenue covers a significant portion of expenses. Focus on "
            "increasing revenue and controlling costs to reach profitability."
        )
    elif revenue_offset_percent >= 25:
        health = "Elevated Burn"
        assessment = (
            "Revenue covers only a quarter of expenses. Consider cost "
            "optimization and accelerating revenue growth."
        )
    else:
        health = "High Burn"
        assessment = (
            "Revenue covers less than 25% of expenses. Immediate attention "
            "needed to either reduce costs or increase revenue significantly."
        )

    return {
        "gross_burn_rate": round(gross_burn, 2),
        "net_burn_rate": round(max(net_burn, 0), 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "monthly_revenue": round(monthly_revenue, 2),
        "revenue_offset_percent": round(revenue_offset_percent, 1),
        "is_profitable": net_burn <= 0,
        "monthly_cash_change": round(-net_burn, 2),
        "health_status": health,
        "assessment": assessment,
        "message": (
            f"Gross burn: ${gross_burn:,.2f}/mo. Net burn: ${max(net_burn, 0):,.2f}/mo. "
            f"Revenue covers {revenue_offset_percent:.1f}% of expenses. "
            f"Status: {health}."
        ),
    }


@tool
def calculate_runway(current_cash: float, monthly_burn_rate: float) -> dict:
    """Calculate the financial runway based on current cash and burn rate.

    Runway is the number of months a company can operate before running
    out of cash at the current burn rate.

    Args:
        current_cash: Current total cash and cash equivalents in dollars.
        monthly_burn_rate: Net monthly burn rate in dollars (positive number
                           representing cash spent per month after revenue).

    Returns:
        A dict with runway in months, projected end date, and recommendations.
    """
    if current_cash < 0:
        return {"error": "Current cash cannot be negative."}
    if monthly_burn_rate < 0:
        return {"error": "Monthly burn rate should be a positive number representing net cash outflow."}

    if monthly_burn_rate == 0:
        return {
            "current_cash": round(current_cash, 2),
            "monthly_burn_rate": 0.0,
            "runway_months": float("inf"),
            "message": "Burn rate is zero. The company is not consuming cash reserves.",
            "recommendations": ["Maintain current trajectory and reinvest profits."],
        }

    runway_months = current_cash / monthly_burn_rate
    now = datetime.utcnow()
    projected_end = now + timedelta(days=runway_months * 30.44)

    if runway_months >= 24:
        urgency = "Comfortable"
        recommendations = [
            "Strong cash position. Consider strategic investments for growth.",
            "Evaluate opportunities for market expansion.",
            "Consider building a war chest for acquisitions.",
        ]
    elif runway_months >= 18:
        urgency = "Healthy"
        recommendations = [
            "Good runway. Continue monitoring burn rate trends.",
            "Begin planning for next funding round if applicable.",
            "Focus on metrics that drive valuation.",
        ]
    elif runway_months >= 12:
        urgency = "Adequate"
        recommendations = [
            "Start fundraising conversations within 3 months.",
            "Identify areas for cost optimization.",
            "Accelerate path to profitability initiatives.",
        ]
    elif runway_months >= 6:
        urgency = "Warning"
        recommendations = [
            "URGENT: Begin fundraising immediately.",
            "Implement cost reduction measures across non-essential spending.",
            "Review headcount plans and discretionary spending.",
            "Explore bridge financing options.",
        ]
    else:
        urgency = "Critical"
        recommendations = [
            "CRITICAL: Cash reserves dangerously low.",
            "Emergency board meeting recommended.",
            "Freeze all non-essential hiring and spending.",
            "Explore emergency funding, bridge loans, or revenue acceleration.",
            "Prepare contingency plans including potential restructuring.",
        ]

    milestones = {}
    for pct, label in [(75, "75% cash remaining"), (50, "50% cash remaining"),
                        (25, "25% cash remaining"), (10, "10% cash remaining")]:
        months_to = (current_cash * (1 - pct / 100)) / monthly_burn_rate
        milestone_date = now + timedelta(days=months_to * 30.44)
        milestones[label] = {
            "months_from_now": round(months_to, 1),
            "projected_date": milestone_date.strftime("%Y-%m-%d"),
            "remaining_cash": round(current_cash * pct / 100, 2),
        }

    return {
        "current_cash": round(current_cash, 2),
        "monthly_burn_rate": round(monthly_burn_rate, 2),
        "runway_months": round(runway_months, 1),
        "projected_cash_out_date": projected_end.strftime("%Y-%m-%d"),
        "urgency": urgency,
        "milestones": milestones,
        "recommendations": recommendations,
        "message": (
            f"Current runway: {runway_months:.1f} months "
            f"(projected cash-out: {projected_end.strftime('%B %Y')}). "
            f"Urgency level: {urgency}."
        ),
    }


@tool
def get_financial_summary(period: str = "current_quarter") -> dict:
    """Get a financial summary for the specified reporting period.

    Returns key financial metrics including revenue, expenses, profit margins,
    and period-over-period comparisons.

    Args:
        period: The reporting period - one of "current_month", "last_month",
                "current_quarter", "last_quarter", "ytd", or "last_year".

    Returns:
        A dict with the full financial summary including revenue breakdown,
        expense categories, and key ratios.
    """
    valid_periods = {
        "current_month", "last_month", "current_quarter",
        "last_quarter", "ytd", "last_year",
    }
    if period not in valid_periods:
        period = "current_quarter"

    summaries = {
        "current_month": {
            "period_label": "October 2026",
            "revenue": {
                "total": 2_850_000,
                "recurring": 2_450_000,
                "services": 320_000,
                "other": 80_000,
            },
            "expenses": {
                "total": 2_100_000,
                "personnel": 1_200_000,
                "infrastructure": 380_000,
                "sales_marketing": 280_000,
                "general_admin": 160_000,
                "rd": 80_000,
            },
            "prior_period_revenue": 2_680_000,
            "headcount": 142,
        },
        "last_month": {
            "period_label": "September 2026",
            "revenue": {
                "total": 2_680_000,
                "recurring": 2_320_000,
                "services": 290_000,
                "other": 70_000,
            },
            "expenses": {
                "total": 2_050_000,
                "personnel": 1_180_000,
                "infrastructure": 360_000,
                "sales_marketing": 275_000,
                "general_admin": 155_000,
                "rd": 80_000,
            },
            "prior_period_revenue": 2_510_000,
            "headcount": 138,
        },
        "current_quarter": {
            "period_label": "Q4 2026 (Oct - projected)",
            "revenue": {
                "total": 8_200_000,
                "recurring": 7_100_000,
                "services": 880_000,
                "other": 220_000,
            },
            "expenses": {
                "total": 6_300_000,
                "personnel": 3_600_000,
                "infrastructure": 1_120_000,
                "sales_marketing": 850_000,
                "general_admin": 480_000,
                "rd": 250_000,
            },
            "prior_period_revenue": 7_500_000,
            "headcount": 142,
        },
        "last_quarter": {
            "period_label": "Q3 2026",
            "revenue": {
                "total": 7_500_000,
                "recurring": 6_500_000,
                "services": 800_000,
                "other": 200_000,
            },
            "expenses": {
                "total": 5_900_000,
                "personnel": 3_400_000,
                "infrastructure": 1_050_000,
                "sales_marketing": 790_000,
                "general_admin": 430_000,
                "rd": 230_000,
            },
            "prior_period_revenue": 6_800_000,
            "headcount": 138,
        },
        "ytd": {
            "period_label": "YTD 2026 (Jan - Oct)",
            "revenue": {
                "total": 25_800_000,
                "recurring": 22_100_000,
                "services": 2_950_000,
                "other": 750_000,
            },
            "expenses": {
                "total": 20_500_000,
                "personnel": 11_800_000,
                "infrastructure": 3_600_000,
                "sales_marketing": 2_750_000,
                "general_admin": 1_550_000,
                "rd": 800_000,
            },
            "prior_period_revenue": 19_200_000,
            "headcount": 142,
        },
        "last_year": {
            "period_label": "FY 2025",
            "revenue": {
                "total": 24_000_000,
                "recurring": 20_000_000,
                "services": 3_200_000,
                "other": 800_000,
            },
            "expenses": {
                "total": 21_000_000,
                "personnel": 12_000_000,
                "infrastructure": 3_800_000,
                "sales_marketing": 2_800_000,
                "general_admin": 1_600_000,
                "rd": 800_000,
            },
            "prior_period_revenue": 16_500_000,
            "headcount": 125,
        },
    }

    data = summaries[period]
    revenue = data["revenue"]["total"]
    expenses = data["expenses"]["total"]
    net_income = revenue - expenses
    gross_margin = ((revenue - data["expenses"].get("infrastructure", 0)) / revenue * 100) if revenue > 0 else 0
    net_margin = (net_income / revenue * 100) if revenue > 0 else 0
    prior_rev = data["prior_period_revenue"]
    revenue_growth = ((revenue - prior_rev) / prior_rev * 100) if prior_rev > 0 else 0
    revenue_per_employee = revenue / data["headcount"] if data["headcount"] > 0 else 0

    return {
        "period": period,
        "period_label": data["period_label"],
        "revenue": data["revenue"],
        "expenses": data["expenses"],
        "net_income": net_income,
        "key_metrics": {
            "gross_margin_percent": round(gross_margin, 1),
            "net_margin_percent": round(net_margin, 1),
            "revenue_growth_percent": round(revenue_growth, 1),
            "revenue_per_employee": round(revenue_per_employee, 2),
            "headcount": data["headcount"],
            "recurring_revenue_percent": round(
                data["revenue"]["recurring"] / revenue * 100, 1
            ) if revenue > 0 else 0,
            "burn_multiple": round(
                expenses / revenue, 2
            ) if revenue > 0 else None,
        },
        "message": (
            f"Financial summary for {data['period_label']}: "
            f"Revenue ${revenue:,.0f}, Expenses ${expenses:,.0f}, "
            f"Net Income ${net_income:,.0f} "
            f"(margin {net_margin:.1f}%, growth {revenue_growth:.1f}%)."
        ),
    }


@tool
def forecast_revenue(
    current_mrr: float,
    growth_rate: float,
    months: int = 12,
) -> dict:
    """Forecast future revenue based on current MRR and expected growth rate.

    Projects month-by-month revenue using compound growth. Useful for
    financial planning, board presentations, and fundraising materials.

    Args:
        current_mrr: Current Monthly Recurring Revenue in dollars.
        growth_rate: Expected month-over-month growth rate as a percentage
                     (e.g. 10.0 for 10% monthly growth).
        months: Number of months to forecast (1-36, default 12).

    Returns:
        A dict with month-by-month projections, ARR calculations,
        and cumulative revenue totals.
    """
    if current_mrr < 0:
        return {"error": "Current MRR cannot be negative."}
    if months < 1 or months > 36:
        months = min(max(months, 1), 36)

    growth_decimal = growth_rate / 100.0
    now = datetime.utcnow()

    monthly_projections = []
    cumulative_revenue = 0.0
    mrr = current_mrr

    for i in range(months):
        month_date = now + timedelta(days=30.44 * (i + 1))
        mrr_at_month = current_mrr * ((1 + growth_decimal) ** (i + 1))
        arr_at_month = mrr_at_month * 12
        cumulative_revenue += mrr_at_month

        monthly_projections.append({
            "month": i + 1,
            "date": month_date.strftime("%Y-%m"),
            "mrr": round(mrr_at_month, 2),
            "arr": round(arr_at_month, 2),
            "cumulative_revenue": round(cumulative_revenue, 2),
        })

    ending_mrr = monthly_projections[-1]["mrr"]
    ending_arr = monthly_projections[-1]["arr"]
    total_revenue = cumulative_revenue
    mrr_growth_total = ending_mrr - current_mrr
    mrr_growth_multiple = ending_mrr / current_mrr if current_mrr > 0 else 0

    # Identify key milestones
    milestones = []
    arr_thresholds = [1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000]
    current_arr = current_mrr * 12
    for threshold in arr_thresholds:
        if current_arr < threshold:
            for proj in monthly_projections:
                if proj["arr"] >= threshold:
                    milestones.append({
                        "milestone": f"${threshold / 1_000_000:.0f}M ARR",
                        "projected_month": proj["month"],
                        "projected_date": proj["date"],
                    })
                    break

    return {
        "current_mrr": round(current_mrr, 2),
        "current_arr": round(current_arr, 2),
        "growth_rate_percent": growth_rate,
        "forecast_months": months,
        "ending_mrr": round(ending_mrr, 2),
        "ending_arr": round(ending_arr, 2),
        "total_revenue_over_period": round(total_revenue, 2),
        "mrr_growth": {
            "absolute": round(mrr_growth_total, 2),
            "multiple": round(mrr_growth_multiple, 2),
        },
        "milestones": milestones,
        "monthly_projections": monthly_projections,
        "message": (
            f"Revenue forecast: Starting at ${current_mrr:,.0f} MRR with "
            f"{growth_rate}% monthly growth over {months} months. "
            f"Ending MRR: ${ending_mrr:,.0f} "
            f"(${ending_arr:,.0f} ARR). "
            f"Total revenue over period: ${total_revenue:,.0f}."
        ),
    }
