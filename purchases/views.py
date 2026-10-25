"""View-функции раздела совместных покупок (данные из SQLite)."""

import sqlite3

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def purchases(request: HttpRequest) -> HttpResponse:
    """Страница со списком совместных покупок из базы данных."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    purchase_list = conn.execute(
        """
        SELECT
            id,
            product,
            price,
            min_participants,
            max_participants
        FROM purchases
        ORDER BY product
        """,
    ).fetchall()
    conn.close()
    return render(
        request,
        "purchases/purchase_list.html",
        {"purchases": purchase_list},
    )


def purchase_detail(
    request: HttpRequest,
    purchase_id: int,
) -> HttpResponse:
    """Страница отдельной покупки (значение передаётся параметром)."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    purchase = conn.execute(
        """
        SELECT
            id,
            product,
            price,
            min_participants,
            max_participants
        FROM purchases
        WHERE id = ?
        """,
        [purchase_id],
    ).fetchone()
    conn.close()
    return render(
        request,
        "purchases/purchase_detail.html",
        {"purchase": purchase},
        status=404 if purchase is None else 200,
    )


def search(request: HttpRequest) -> HttpResponse:
    """Подбор покупок в пределах заданного бюджета (параметр цены)."""
    max_price = request.GET.get("max_price")
    purchase_list = []
    if max_price:
        try:
            limit = float(max_price)
        except ValueError:
            limit = None
        if limit is not None:
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            purchase_list = conn.execute(
                """
                SELECT
                    id,
                    product,
                    price,
                    max_participants
                FROM purchases
                WHERE price <= ?
                ORDER BY price
                """,
                [limit],
            ).fetchall()
            conn.close()
    return render(
        request,
        "purchases/purchase_search.html",
        {"purchases": purchase_list, "max_price": max_price},
    )
