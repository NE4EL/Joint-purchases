"""View-функции раздела совместных покупок."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.participations import count_active, purchase_status
from models.purchases import find_purchase_by_id
from storage import load_participations, load_purchases, load_users

PURCHASES_FILE = "data/purchases.json"
USERS_FILE = "data/users.json"
PARTICIPATIONS_FILE = "data/participations.json"


def purchases(request: HttpRequest) -> HttpResponse:
    """Страница со списком совместных покупок."""
    items = ""
    for purchase in load_purchases(PURCHASES_FILE):
        text = f"{purchase.product} — {purchase.price} руб."
        items += (
            f'<li class="list-group-item">'
            f'<a href="/purchases/{purchase.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Совместные покупки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Совместные покупки", content))


def purchase_detail(
    request: HttpRequest,
    purchase_id: int,
) -> HttpResponse:
    """Страница отдельной совместной покупки."""
    purchases_list = load_purchases(PURCHASES_FILE)
    purchase = find_purchase_by_id(purchases_list, purchase_id)
    if purchase is None:
        content = """
        <h1 class="text-danger">Покупка не найдена</h1>
        <a href="/purchases/" class="btn btn-outline-secondary">
            ← к списку покупок
        </a>
        """
        return HttpResponse(
            page("Покупка не найдена", content),
            status=404,
        )
    users_list = load_users(USERS_FILE)
    participations_list = load_participations(
        PARTICIPATIONS_FILE,
        purchases_list,
        users_list,
    )
    current = count_active(participations_list, purchase)
    status = purchase_status(participations_list, purchase)
    cost = purchase.participant_cost(5)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{purchase.product}</h5>
            <p class="card-text"><strong>ID:</strong> {purchase.id}</p>
            <p class="card-text">
                <strong>Цена:</strong> {purchase.price} руб.
            </p>
            <p class="card-text">
                <strong>Участников:</strong>
                {current}/{purchase.max_participants}
            </p>
            <p class="card-text">
                <strong>Стоимость участия (комиссия 5%):</strong>
                {cost} руб.
            </p>
            <p class="card-text">
                <span class="badge bg-info">{status}</span>
            </p>
            <a href="/purchases/"
               class="btn btn-outline-secondary">
                ← к списку покупок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(purchase.product, content))
