"""View-функции раздела участий в покупках."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.participations import find_participation_by_id
from storage import load_participations, load_purchases, load_users

PURCHASES_FILE = "data/purchases.json"
USERS_FILE = "data/users.json"
PARTICIPATIONS_FILE = "data/participations.json"


def _load_all() -> list:
    """Загрузить участия со связями на покупки и пользователей."""
    purchases_list = load_purchases(PURCHASES_FILE)
    users_list = load_users(USERS_FILE)
    return load_participations(
        PARTICIPATIONS_FILE,
        purchases_list,
        users_list,
    )


def participations(request: HttpRequest) -> HttpResponse:
    """Страница со списком участий."""
    items = ""
    for item in _load_all():
        state = "отменено" if item.is_cancelled else "активно"
        badge = "bg-secondary" if item.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/participations/{item.id}/">
                {item.user.name} — {item.purchase.product}
            </a>
            <span class="badge {badge}">{state}</span>
        </li>
        """
    content = f"""
    <h1>Участия в покупках</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Участия в покупках", content))


def participation_detail(
    request: HttpRequest,
    participation_id: int,
) -> HttpResponse:
    """Страница отдельного участия."""
    participation = find_participation_by_id(
        _load_all(),
        participation_id,
    )
    if participation is None:
        content = """
        <h1 class="text-danger">Участие не найдено</h1>
        <a href="/participations/"
           class="btn btn-outline-secondary">
            ← к списку участий
        </a>
        """
        return HttpResponse(
            page("Участие не найдено", content),
            status=404,
        )
    cancelled = participation.is_cancelled
    state = "отменено" if cancelled else "активно"
    badge = "bg-secondary" if cancelled else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Участие №{participation.id}</h5>
            <p class="card-text">
                Товар: {participation.purchase.product}
            </p>
            <p class="card-text">
                Пользователь: {participation.user.name}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{state}</span>
            </p>
            <a href="/participations/"
               class="btn btn-outline-secondary">
                ← к списку участий
            </a>
        </div>
    </div>
    """
    title = f"Участие №{participation.id}"
    return HttpResponse(page(title, content))
