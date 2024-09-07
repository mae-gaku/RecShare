from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import qrcode
from .models import Store
from .models import StoreGroup
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from .models import Store, Dish
from .forms import StoreForm
from django.shortcuts import render, redirect
from .forms import StoreForm, DishForm


def home(request):
    return render(request, 'stores/home.html')


def store_group_list(request, group_id):
    print(f"Received request for group_id: {group_id}")  # デバッグ用
    group = get_object_or_404(StoreGroup, id=group_id)
    stores = group.stores.all()
    return render(request, 'stores/store_group_list.html', {'group': group, 'stores': stores})

def store_list(request):
    stores = Store.objects.all()
    return render(request, 'stores/store_list.html', {'stores': stores})


def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    return render(request, 'stores/store_detail.html', {'store': store})

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

def register_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store_list')  # 保存後のリダイレクト先
    else:
        form = DishForm()
    return render(request, 'stores/register_dish.html', {'form': form})


# def register_store_with_dishes(request):
#     DishInlineFormSet = inlineformset_factory(Store, Dish, fields=('name', 'description', 'price'), extra=3)
#     if request.method == 'POST':
#         form = StoreForm(request.POST)
#         if form.is_valid():
#             created_store = form.save()
#             formset = DishInlineFormSet(request.POST, instance=created_store)
#             if formset.is_valid():
#                 formset.save()
#                 return redirect('store_list')
#     else:
#         form = StoreForm()
#         formset = DishInlineFormSet()
#     return render(request, 'stores/register_store_with_dishes.html', {'form': form, 'formset': formset})
# from .forms import StoreForm, DishFormSet
# def register_store_with_dishes(request):
#     if request.method == 'POST':
#         store_form = StoreForm(request.POST)
#         formset = DishFormSet(request.POST)

#         if store_form.is_valid() and formset.is_valid():
#             store = store_form.save()
#             dishes = formset.save(commit=False)
#             for dish in dishes:
#                 dish.store = store  # Storeに関連付ける
#                 dish.save()
#             return redirect('store_list')  # 適切なリダイレクト先に変更してください
#     else:
#         store_form = StoreForm()
#         formset = DishFormSet()

#     return render(request, 'stores/register_store_with_dishes.html', {
#         'store_form': store_form,
#         'formset': formset
#     })