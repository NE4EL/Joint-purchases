"""View-функции раздела участий в покупках (данные из SQLite)."""

import sqlite3

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def participations(request: HttpRequest) -> HttpResponse:
    """Список участий со связанными товаром и пользователем (JOIN)."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    participation_list = conn.execute(
        """
        SELECT
            participations.id,
            participations.is_cancelled,
            purchases.product,
            users.name AS user_name
        FROM participations
        JOIN purchases ON participations.purchase_id = purchases.id
        JOIN users ON participations.user_id = users.id
        ORDER BY participations.id
        """,
    ).fetchall()
    conn.close()
    return render(
        request,
        "participations/participation_list.html",
        {"participations": participation_list},
    )


def participation_detail(
    request: HttpRequest,
    participation_id: int,
) -> HttpResponse:
    """Отдельное участие (JOIN, значение передаётся параметром)."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    participation = conn.execute(
        """
        SELECT
            participations.id,
            participations.is_cancelled,
            purchases.product,
            users.name AS user_name
        FROM participations
        JOIN purchases ON participations.purchase_id = purchases.id
        JOIN users ON participations.user_id = users.id
        WHERE participations.id = ?
        """,
        [participation_id],
    ).fetchone()
    conn.close()
    return render(
        request,
        "participations/participation_detail.html",
        {"participation": participation},
        status=404 if participation is None else 200,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    """Статистика: число активных участников по каждой покупке."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    stats = conn.execute(
        """
        SELECT
            purchases.product,
            purchases.min_participants,
            COUNT(participations.id) AS participants_count
        FROM purchases
        LEFT JOIN participations
            ON purchases.id = participations.purchase_id
            AND participations.is_cancelled = 0
        GROUP BY purchases.id, purchases.product
        ORDER BY participants_count DESC
        """,
    ).fetchall()
    conn.close()
    return render(
        request,
        "participations/statistics.html",
        {"statistics": stats},
    )
