from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import qrcode
from .models import Store
from .models import StoreGroup
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from .models import Store
from .forms import StoreForm
from django.shortcuts import render, redirect
from .forms import StoreForm


def home(request):
    stores = Store.objects.all()  # `stores`をhome.htmlに渡す
    return render(request, 'stores/home.html', {'stores': stores})

def store_group_list(request, group_id):
    print(f"Received request for group_id: {group_id}")  # デバッグ用
    group = get_object_or_404(StoreGroup, id=group_id)
    stores = group.stores.all()
    return render(request, 'stores/store_group_list.html', {'group': group, 'stores': stores})

def store_list(request):
    stores = Store.objects.all()
    return render(request, 'stores/store_list.html', {'stores': stores})

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Store, Review

def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    reviews = Review.objects.filter(store=store)
    return render(request, 'store_detail.html', {'store': store, 'reviews': reviews})


def recommendations(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    recommended_stores = store.recommended_stores.all()
    return render(request, 'stores/recommendations.html', {'store': store, 'recommended_stores': recommended_stores})

def generate_qr_code(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(store.website)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

from django.shortcuts import render


from django.shortcuts import render, get_object_or_404
from .models import Store

def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    return render(request, 'stores/store_detail.html', {'store': store})


def register_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store_list')  # 保存後のリダイレクト先
    else:
        form = StoreForm()
    return render(request, 'stores/register_store.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Store, Review
from .forms import ReviewForm

def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = store.reviews.all()  # お店に関連する全てのレビューを取得

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.store = store
            review.user = request.user  # ログインしているユーザーを関連付け
            review.save()
            return redirect('store_detail', store_id=store.id)
    else:
        form = ReviewForm()

    context = {
        'store': store,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'stores/store_detail.html', context)


from .models import Genre
def store_list(request):
    genres = Genre.objects.all()  # ジャンルリストを取得
    stores = Store.objects.all()

    # ジャンルフィルタリング
    genre_query = request.GET.get('genre')

    # ジャンル検索
    if genre_query:
        stores = Store.objects.filter(genre__name__icontains=genre_query)
    else:
        stores = Store.objects.all()

    return render(request, 'stores/store_list.html', {'stores': stores, 'genres': genres})

# views.py
from django.contrib.auth.decorators import login_required

@login_required
def some_protected_view(request):
    # ログインが必要なビュー
    return render(request, 'protected_page.html')


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # ログイン後のリダイレクト先を指定
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


