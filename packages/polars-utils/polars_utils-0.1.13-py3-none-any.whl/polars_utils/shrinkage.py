from typing import Optional
import polars as pl
from polars import _typing as pt


from polars_utils import into_expr
from polars_utils.stats import mean
from polars_utils.weights import Weight


def reliability(
    estimates: pl.Expr,
    *,
    variances: pt.IntoExprColumn,
    w: Optional[Weight] = None,
    mu: Optional[pl.Expr] = None,
):
    # point around which we compute variance
    mu = estimates.pipe(mean, w=w) if mu is None else mu

    # calculate reliability
    signal_variance = ((estimates - mu).pow(2) - variances).pipe(mean, w=w)
    return signal_variance / into_expr(variances).add(signal_variance)


def shrink(
    estimates: pl.Expr,
    *,
    variances: Optional[pt.IntoExprColumn] = None,
    w: Optional[Weight] = None,
    mu: Optional[pl.Expr] = None,  # mean to shrink to
    rho: Optional[pl.Expr] = None,  # reliability
) -> pl.Expr:
    """
    https://libgen.li/adsa82270d055f6ee991539ac0533036e0dO9ZBZS4G
    """

    # point we shrink to
    if mu is None:
        mu = estimates.pipe(mean, w=w)

    # reliability
    if rho is None:
        if variances is None:
            raise ValueError("Must pass either variances or reliabilities.")

        rho = reliability(estimates, variances=variances, w=w, mu=mu)

    # shrink towards mean based on reliability
    return estimates.mul(rho) + mu.mul(1 - rho)
