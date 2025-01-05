# import pandas as pd
# from prophet import Prophet
# from .models import UserInteraction, Store

# def predict_next_stores(user_id, top_n=5):
#     # ユーザーのインタラクションデータを取得
#     interactions = UserInteraction.objects.filter(user_id=user_id).order_by('-timestamp')
#     print("interactions", interactions)
#     if not interactions.exists():
#         return Store.objects.none()  # データがない場合は空のクエリセットを返す

#     df = pd.DataFrame(interactions)
#     df['timestamp'] = pd.to_datetime(df['timestamp'])  # 'timestamp'を使用
#     df = df.groupby('created_at').size().reset_index(name='count')

#     # Prophet用にデータを整形
#     df = df.rename(columns={'created_at': 'ds', 'count': 'y'})

#     # モデルの作成と学習
#     model = Prophet()
#     model.fit(df)

#     # 将来の予測データフレーム作成
#     future = model.make_future_dataframe(periods=30)  # 30日先を予測
#     forecast = model.predict(future)

#     # 予測結果から上位の店舗を取得
#     next_stores = forecast[['ds', 'yhat']].nlargest(top_n, 'yhat')

#     # インタラクションが多かった店舗を返す
#     predicted_store_ids = df.loc[df['ds'].isin(next_stores['ds']), 'store_id'].unique()
#     return Store.objects.filter(id__in=predicted_store_ids)


import pandas as pd
from .models import UserInteraction
from prophet import Prophet

def predict_next_stores(user_id):
    interactions = UserInteraction.objects.filter(user_id=user_id).order_by('-timestamp')
    print("interactions", interactions)
    if not interactions.exists():
        return []

    data = [{'store_id': i.store.id, 'timestamp': i.timestamp} for i in interactions]
    df = pd.DataFrame(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'])  # 修正箇所
    df = df.groupby('store_id').count().reset_index()
    df.columns = ['store_id', 'interaction_count']

    df['ds'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
    df['y'] = df['interaction_count']

    model = Prophet()
    model.fit(df[['ds', 'y']])

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    predicted_store_ids = df['store_id'].tolist()  # 修正ポイント: ここで確認
    print("Predicted Store IDs:", predicted_store_ids)  # デバッグ用
    from .models import Store
    return Store.objects.filter(id__in=predicted_store_ids)
