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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Store, Review
from .forms import ReviewForm
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Store, Review
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Store
from .models import Genre
# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Store
from .models import Like
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import StoreForm  # お店登録用のフォームを作成する
from django.contrib import messages
from .forms import StoreGroupForm
from .models import StoreGroup




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


def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = store.reviews.all()  # お店に関連する全てのレビューを取得

    # おすすめグループを取得
    recommended_groups = store.store_groups.all()

    # ユーザーがこのお店に「いいね」しているかどうかをチェック
    user_has_liked = Like.objects.filter(store=store, user=request.user).exists() if request.user.is_authenticated else False

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

    # インタラクションの記録
    # if request.user.is_authenticated:
    #     UserInteraction.objects.create(
    #         user=request.user,
    #         store=store,
    #         interaction_type='view'
    #     )

    # 閲覧記録を保存
    from django.utils.timezone import now
    if request.user.is_authenticated:
        ViewLog.objects.create(user=request.user, store=store, viewed_at=now())

    sort_order = request.GET.get('sort_order', 'newest')  # デフォルトは新しい順
    if sort_order == 'oldest':
        reviews = Review.objects.filter(store=store).order_by('created_at')  # 古い順
    else:
        reviews = Review.objects.filter(store=store).order_by('-created_at')  # 新しい順


    
    context = {
        'store': store,
        'reviews': reviews,
        'form': form,
        'user_has_liked': user_has_liked,  # 「いいね」状態をテンプレートに渡す
        'recommended_groups': recommended_groups,  # おすすめグループをテンプレートに渡す
        'sort_order': sort_order,
    }
    return render(request, 'stores/store_detail.html', context)



def store_list(request):
    genres = Genre.objects.all()  # ジャンルリストを取得
    stores = Store.objects.all()

    # ジャンルフィルタリング
    genre_query = request.GET.get('genre')

    # ジャンル検索
    if genre_query:
        stores = stores.filter(genre__icontains=genre_query)

    # if genre_query:
    #     stores = Store.objects.filter(genre__name__icontains=genre_query)
    else:
        stores = Store.objects.all()

    return render(request, 'stores/store_list.html', {'stores': stores, 'genres': genres})



@login_required
def some_protected_view(request):
    # ログインが必要なビュー
    return render(request, 'protected_page.html')


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


@login_required
def like_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    
    # すでにユーザーがこの店舗に「いいね」しているか確認
    like, created = Like.objects.get_or_create(user=request.user, store=store)
    print("created",created)
    if created:
        # 新しい「いいね」が作成された場合、「いいね」数をインクリメント
        store.likes += 1
        store.save()
        liked = True
    else:
        # すでに「いいね」している場合、再度インクリメントはしない
        liked = False

    # JSONでいいね数といいねの状態を返す
    return JsonResponse({'likes': store.likes, 'liked': liked})

def settings_page(request):
    if request.method == "POST":
        dark_mode = request.POST.get("dark_mode") == "on"
        request.session['dark_mode'] = dark_mode
        return redirect('settings_page')
    
    return render(request, 'settings.html', {
        'dark_mode': request.session.get('dark_mode', False),
    })


@login_required
def register_store(request):
    if not request.user.is_staff:  # 管理者権限を確認
        return redirect('home')

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            # フォームエラーを出力
            print(form.errors)  # コンソールでエラー内容を確認
    else:
        form = StoreForm()

    return render(request, 'stores/register_store.html', {'form': form})


def register_store_group(request):
    if request.method == 'POST':
        form = StoreGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # 登録後にリダイレクト
    else:
        form = StoreGroupForm()

    return render(request, 'stores/register_store_group.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Store, StoreGroup

def store_group(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    store_groups = StoreGroup.objects.filter(stores=store)
    return render(request, 'store_group.html', {'store': store, 'store_groups': store_groups})


from django.shortcuts import render
from .models import Store
# from .utils import predict_next_stores
from .models import Store

from django.shortcuts import render
from .models import Store, ViewLog
# from prophet import Prophet
import pandas as pd
from django.contrib.auth.decorators import login_required

def record_view(user, store):
    if user.is_authenticated:
        ViewLog.objects.create(user=user, store=store)


#######################Prophetの場合########################################

# @login_required
# def predicted_stores(request):
#     user = request.user
    
#     # ユーザーの閲覧履歴を取得
#     logs = ViewLog.objects.filter(user=user).values('viewed_at', 'store__name')
    
#     if logs.count() < 2:
#         # 閲覧履歴が2件未満の場合、おすすめ店舗をNoneに設定
#         recommended_stores = None
#     else:
#         # DataFrameを作成
#         df = pd.DataFrame(logs)
#         df.columns = ['ds', 'y']  # Prophetの期待する列名
#         df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)  # タイムゾーンを削除

#         # ストア名をカテゴリに変換して数値にマッピング
#         df['y'] = df['y'].astype('category')
#         category_to_store = dict(enumerate(df['y'].cat.categories))
#         store_to_category = {v: k for k, v in category_to_store.items()}

#         # Prophet用にカテゴリの数値をセット
#         df['y'] = df['y'].cat.codes

#         # モデルを適用
#         model = Prophet()
#         model.fit(df)

#         # 予測後にカテゴリ値をストア名に戻す
#         future = model.make_future_dataframe(periods=100)  # 必要に応じて予測期間を増やす
#         forecast = model.predict(future)
    
#         # カテゴリコードをストア名に変換し、スコア上位5件を取得
#         forecast['store_name'] = forecast['yhat'].apply(lambda x: category_to_store.get(round(x), 'Unknown'))
#         top_forecast = forecast.sort_values(by='yhat', ascending=False).drop_duplicates(subset=['store_name']).head(5)

#         # ストア名をリスト化
#         recommended_store_names = top_forecast['store_name'].tolist()

#         # データベースクエリで名前を用いる
#         recommended_stores = Store.objects.filter(name__in=recommended_store_names)

#     return render(request, 'stores/ai_recommendations.html', {'stores': recommended_stores})


# @login_required
# def predicted_stores(request):
#     user = request.user
    
#     # ユーザーの閲覧履歴を取得
#     logs = ViewLog.objects.filter(user=user).values('viewed_at', 'store__name')
    
#     if logs.count() < 2:
#         # 閲覧履歴が2件未満の場合、おすすめ店舗をNoneに設定
#         recommended_stores = None
#     else:
#         # DataFrameを作成
#         df = pd.DataFrame(logs)
#         df.columns = ['ds', 'y']  # Prophetの期待する列名
#         df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)  # タイムゾーンを削除

#         # ストア名をカテゴリに変換して数値にマッピング
#         df['y'] = df['y'].astype('category')
#         category_to_store = dict(enumerate(df['y'].cat.categories))
#         store_to_category = {v: k for k, v in category_to_store.items()}

#         # Prophet用にカテゴリの数値をセット
#         df['y'] = df['y'].cat.codes
#         print("df", df)
#         # モデルを適用
#         model = Prophet()
#         model.fit(df)

#         # すべての店舗に対して推論を行う
#         stores = Store.objects.all()  # 登録されている全てのお店
#         store_scores = []

#         for store in stores:
#             # 各店舗について、予測用のデータを生成
#             store_name = store.name
#             # 店舗の名前を数値にマッピング
#             store_code = store_to_category.get(store_name, -1)  # マッピングがない場合は-1
            
#             # if store_code != -1:  # 有効な店舗コードがある場合に予測
#             store_df = pd.DataFrame({'ds': pd.to_datetime('today'), 'y': [store_code]})
#             store_df['y'] = store_df['y'].astype('category')
#             store_df['y'] = store_df['y'].cat.codes
#             forecast = model.predict(store_df)

#             # 予測結果を格納
#             store_scores.append({
#                 'store': store,
#                 'score': forecast['yhat'].values[0]  # 予測スコア
#             })
#         print("!store_scores", store_scores)
#         # スコアを基に降順で並べ替え
#         store_scores = sorted(store_scores, key=lambda x: x['score'], reverse=True)

#         # 上位5件のお店を取得
#         top_stores = [store_score['store'] for store_score in store_scores[:5]]

#         # レコメンド店舗を取得
#         recommended_stores = top_stores

#     return render(request, 'stores/ai_recommendations.html', {'stores': recommended_stores})


#########################################################################


#######################XGboostの場合########################################


# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# import xgboost as xgb
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render



# @login_required
# def predicted_stores(request):
#     user = request.user

#     # 履歴データを取得
#     logs = ViewLog.objects.filter(user=user).values('viewed_at', 'store__genre')

#     if logs.count() < 2:
#         # 閲覧履歴が2件未満の場合、レコメンド結果をNoneに設定
#         return render(request, 'stores/ai_recommendations.html', {'stores': None})

#     # DataFrame を作成
#     df = pd.DataFrame(logs)
#     df.columns = ['timestamp', 'genre_name']
#     df['timestamp'] = pd.to_datetime(df['timestamp'])

#     # 特徴量を作成
#     df['day_of_week'] = df['timestamp'].dt.dayofweek
#     df['hour'] = df['timestamp'].dt.hour
#     df['genre_code'] = df['genre_name'].astype('category').cat.codes

#     # モデル学習用データの準備
#     features = df[['day_of_week', 'hour', 'genre_code']]
#     labels = df['genre_name'].astype('category')
#     genre_to_code = dict(enumerate(labels.cat.categories))
#     y = labels.cat.codes

#     # XGBoost モデルの学習
#     model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
#     model.fit(features, y)

#     # 推論データの準備
#     now = pd.Timestamp.now()
#     current_day_of_week = now.dayofweek
#     current_hour = now.hour

#     # 全店舗データを取得
#     stores = Store.objects.all()

#     # ジャンルカテゴリを生成
#     genres = [store.genre if store.genre else "unknown" for store in stores]
#     genre_categories = pd.Series(genres).astype('category')
#     genre_to_code = dict(enumerate(genre_categories.cat.categories))

#     # 店舗特徴量を作成
#     store_features = [
#         {
#             'day_of_week': current_day_of_week,
#             'hour': current_hour,
#             'genre_code': genre_categories.cat.codes[i]
#         }
#         for i, store in enumerate(stores)
#     ]
#     store_features_df = pd.DataFrame(store_features)
#     # print("store_features_df", store_features_df)

#     # 推論スコアを計算
#     store_scores = model.predict_proba(store_features_df)[:, 1]

#     # 上位 5 件の店舗を選出
#     store_score_pairs = zip(stores, store_scores)
#     # print("AAAA", sorted(store_score_pairs, key=lambda x: x[1], reverse=True))
#     top_stores = sorted(store_score_pairs, key=lambda x: x[1], reverse=True)[:5]
#     recommended_stores = [store for store, score in top_stores]

#     # 結果をレンダリング
#     return render(request, 'stores/ai_recommendations.html', {'stores': recommended_stores})


# ############################################################################



#######################LightBGMの場合########################################

# import lightgbm as lgb

# @login_required
# def predicted_stores(request):
#     user = request.user

#     # 履歴データを取得
#     logs = ViewLog.objects.filter(user=user).values('viewed_at', 'store__genre')

#     if logs.count() < 2:
#         # 閲覧履歴が2件未満の場合、レコメンド結果をNoneに設定
#         return render(request, 'stores/ai_recommendations.html', {'stores': None})

#     # DataFrame を作成
#     df = pd.DataFrame(logs)
#     df.columns = ['timestamp', 'genre_name']
#     df['timestamp'] = pd.to_datetime(df['timestamp'])

#     # 特徴量を作成
#     df['day_of_week'] = df['timestamp'].dt.dayofweek
#     df['hour'] = df['timestamp'].dt.hour
#     df['genre_code'] = df['genre_name'].astype('category').cat.codes

#     # モデル学習用データの準備
#     features = df[['day_of_week', 'hour', 'genre_code']]
#     labels = df['genre_name'].astype('category')
#     y = labels.cat.codes

#     # LightGBMモデルの学習
#     train_data = lgb.Dataset(features, label=y)
#     params = {
#         'objective': 'multiclass',
#         'num_class': len(labels.cat.categories),
#         'metric': 'multi_logloss'
#     }
#     model = lgb.train(params, train_data, num_boost_round=100)

#     # 推論データの準備
#     now = pd.Timestamp.now()
#     current_day_of_week = now.dayofweek
#     current_hour = now.hour

#     # 全店舗データを取得
#     stores = Store.objects.all()

#     # ジャンルカテゴリを生成
#     genres = [store.genre if store.genre else "unknown" for store in stores]
#     genre_categories = pd.Series(genres).astype('category')
#     genre_to_code = dict(enumerate(genre_categories.cat.categories))

#     # 店舗特徴量を作成
#     store_features = [
#         {
#             'day_of_week': current_day_of_week,
#             'hour': current_hour,
#             'genre_code': genre_categories.cat.codes[i]
#         }
#         for i, store in enumerate(stores)
#     ]
#     store_features_df = pd.DataFrame(store_features)

#     # 推論スコアを計算
#     store_scores = model.predict(store_features_df)
#     store_scores = store_scores[:, 1]  # クラス1の確率を使用

#     # 上位 5 件の店舗を選出
#     store_score_pairs = zip(stores, store_scores)
#     top_stores = sorted(store_score_pairs, key=lambda x: x[1], reverse=True)[:5]
#     recommended_stores = [store for store, score in top_stores]

#     # 結果をレンダリング
#     return render(request, 'stores/ai_recommendations.html', {'stores': recommended_stores})

# @login_required
# def map_page(request):
#     return render(request, 'stores/map.html')


from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Store

@login_required
def map_page(request):
    stores = Store.objects.all().values('name', 'latitude', 'longitude')
    stores_json = json.dumps(list(stores), cls=DjangoJSONEncoder)
    return render(request, 'stores/map.html', {'stores': stores_json})



from django.shortcuts import render
from .models import ViewLog, Store
from llm.llm_service import get_llm
from django.contrib.auth.models import User



import json
from django.core.serializers.json import DjangoJSONEncoder
from llama_index.core import VectorStoreIndex, Document


import json
from django.core.serializers.json import DjangoJSONEncoder
# from langchain.llms import LlamaCpp
# from langchain_community.llms import LlamaCpp

def analyze_user_preferences(user):
    llm = get_llm()

    # デバッグ：llm の状態確認
    print("llm", llm)

    # ViewLog データを取得
    view_logs = ViewLog.objects.filter(user=user).select_related('store')

    # ViewLog を JSON フォーマットに変換
    view_logs_data = [
        {
            "store_name": log.store.name,
            "genre": log.store.genre,
            "description": log.store.description,
            "viewed_at": log.viewed_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for log in view_logs
    ]
    view_logs_json = json.dumps(view_logs_data, cls=DjangoJSONEncoder, ensure_ascii=False)

    # プロンプトを生成
    prompt = f"""
    あなたはユーザーの履歴を分析するアシスタントです。
    以下はユーザーが訪れたお店の履歴です。この履歴を基に、ユーザーが好むジャンルやお店の特徴を分析してください。
    好きなジャンルやお店の特徴を簡潔にリスト形式で出力してください。

    【履歴】:
    {view_logs_json}
    """

    # デバッグ：生成されたプロンプトの確認
    print("Debug: Prompt format:", prompt)

    # LLM にプロンプトを渡して推論
    try:
        response = llm(prompt)  # LangChain ではプロンプトを直接渡す
        print("Debug: Response:", response)

        # 推論結果を整形して返す
        result = response.strip()
        print("LLM Result:", result)
        return result
    except Exception as e:
        print(f"Error during LLM chat: {e}")
        return "エラーが発生しました。詳細を確認してください。"


# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from llama_cpp import Llama  # LlamaCPP のインポート

# def analyze_user_preferences(user):
#     # Llama モデルのロード
#     llm = get_llm()

#     # デバッグ：llm の状態確認
#     print("llm", llm)

#     # ViewLog データを取得
#     view_logs = ViewLog.objects.filter(user=user).select_related('store')

#     # ViewLog を JSON フォーマットに変換
#     view_logs_data = [
#         {
#             "store_name": log.store.name,
#             "genre": log.store.genre,
#             "description": log.store.description,
#             "viewed_at": log.viewed_at.strftime("%Y-%m-%d %H:%M:%S"),
#         }
#         for log in view_logs
#     ]
#     view_logs_json = json.dumps(view_logs_data, cls=DjangoJSONEncoder, ensure_ascii=False)

#     # プロンプトを生成
#     prompt = f"""
#     あなたはユーザーの履歴を分析するアシスタントです。
#     以下はユーザーが訪れたお店の履歴です。この履歴を基に、ユーザーが好むジャンルやお店の特徴を分析してください。
#     好きなジャンルやお店の特徴を簡潔にリスト形式で出力してください。

#     【履歴】:
#     {view_logs_json}
#     """

#     # デバッグ：生成されたプロンプトの確認
#     print("Debug: Prompt format:", prompt)

#     # LLM にプロンプトを渡して推論
#     try:
#         response = llm(prompt, max_tokens=300, temperature=0.7)  # 適切な呼び出し方法に修正
#         print("Debug: Response:", response)

#         # 推論結果を整形して返す
#         if "choices" in response and response["choices"]:
#             result = response["choices"][0]["text"].strip()
#             print("LLM Result:", result)
#             return result
#         else:
#             print("分析結果が取得できませんでした。")
#             return "分析結果が取得できませんでした。"
#     except Exception as e:
#         print(f"Error during LLM chat: {e}")
#         return "エラーが発生しました。詳細を確認してください。"


# お店データベースを作成
def create_store_database():
    stores = Store.objects.all()
    store_data = [
        {
            "id": store.id,
            "name": store.name,
            "genre": store.genre,
            "description": store.description,
            "address": store.address,
            "hours": store.hours,
        }
        for store in stores
    ]
    print("store_data", store_data)
    nodes = [Document(text=json.dumps(data)) for data in store_data]

    # ドキュメントの読み込み
    # documents = SimpleDirectoryReader("./data").load_data()
    # from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    # embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu")

    from langchain_huggingface import HuggingFaceEmbeddings
    print("embedding")
    model_name = "intfloat/multilingual-e5-large"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    return VectorStoreIndex(nodes, embed_model=embedding_model)

# レコメンドを作成
def recommend_stores(preferences, store_index):
    query_engine = store_index.as_query_engine(similarity_top_k=5)
    return query_engine.query(preferences)

# レコメンドの統合ビュー
@login_required
def predicted_stores(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    # 1. ユーザーの好みを分析
    preferences = analyze_user_preferences(user)

    # 2. お店データベースを構築
    store_index = create_store_database()

    # 3. レコメンド結果を取得
    recommended_stores = recommend_stores(preferences, store_index)

    # 4. 結果をテンプレートに渡す
    return render(request, "recommendations.html", {
        "user": user,
        "preferences": preferences,
        "recommended_stores": recommended_stores,
    })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def user_points(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  # ない場合は作成

    return render(request, 'user_points.html', {'profile': profile})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, UserProfile, UserPointHistory

@login_required
def scan_qr_code(request):
    store_id = request.GET.get('store_id')
    if not store_id:
        messages.error(request, "無効なQRコードです。")
        return redirect('user_points')

    try:
        store = Store.objects.get(unique_id=store_id)
    except Store.DoesNotExist:
        messages.error(request, "店舗が見つかりません。")
        return redirect('user_points')

    # すでにこの店舗でポイントを獲得しているか確認
    if UserPointHistory.objects.filter(user=request.user, store=store).exists():
        messages.warning(request, "この店舗のQRコードはすでにスキャンしています。")
        return redirect('user_points')

    # ユーザーのポイントを増やし、履歴を追加
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.points += 1
    profile.save()

    UserPointHistory.objects.create(user=request.user, store=store)

    messages.success(request, f"{store.name} のQRコードをスキャンしました！1ポイント獲得！")
    return redirect('user_points')
