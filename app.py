import streamlit as st
import datetime 
import requests
import json

def safe_json_response(response):
    """レスポンスが有効なJSONかどうかを確認し、安全にJSONを取得する"""
    try:
        if response.text.strip():
            return response.json()
        else:
            return {"error": f"Empty response: HTTP {response.status_code}"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON response: {response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
    st.title('ユーザー登録画面')
    with st.form(key='user'):
        # user_id: int = random.randint(0, 10)
        username: str = st.text_input('ユーザー名', max_chars=12)
        data = {
            # 'user_id': user_id,
            'username': username
        }
        submit_button = st.form_submit_button(label='ユーザー登録')

    if submit_button:
        url = 'http://127.0.0.1:8000/users'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        response_data = safe_json_response(res)
        if res.status_code == 200:
            st.success('ユーザー登録完了')
        elif res.status_code == 400:
            # HTTP 400エラーの場合、detailメッセージを直接表示
            error_detail = response_data.get('detail', 'ユーザー登録エラーが発生しました')
            st.error(error_detail)
        else:
            st.error(f'エラーが発生しました: {response_data}')
        st.json(response_data)

elif page == 'rooms':
    st.title('会議室登録画面')

    with st.form(key='room'):
        # room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            # 'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')

    if submit_button:
        url = 'http://127.0.0.1:8000/rooms'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        response_data = safe_json_response(res)
        if res.status_code == 200:
            st.success('会議室登録完了')
        elif res.status_code == 400:
            # HTTP 400エラーの場合、detailメッセージを直接表示
            error_detail = response_data.get('detail', '会議室登録エラーが発生しました')
            st.error(error_detail)
        else:
            st.error(f'エラーが発生しました: {response_data}')
        st.json(response_data)

elif page == 'bookings':
    st.title('会議室予約画面')
    # ユーザー一覧取得
    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users_data = safe_json_response(res)
    users = users_data if isinstance(users_data, list) else []
    # ユーザー名をキー、ユーザーIDをバリュー
    users_name = {}
    for user in users:
        users_name[user['username']] = user['user_id']

    # 会議室一覧の取得
    url_rooms = 'http://127.0.0.1:8000/rooms'
    res = requests.get(url_rooms)
    rooms_data = safe_json_response(res)
    rooms = rooms_data if isinstance(rooms_data, list) else []
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }

    st.write('### 会議室一覧')
    for room in rooms:
        st.write(f"**{room['room_name']}** - 定員: {room['capacity']}名 (ID: {room['room_id']})")

    url_bookings = 'http://127.0.0.1:8000/bookings'
    res = requests.get(url_bookings)
    bookings_data = safe_json_response(res)
    bookings = bookings_data if isinstance(bookings_data, list) else []

    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['username']

    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity'],
        }

    st.write('### 予約一覧')
    for booking in bookings:
        username = users_id.get(booking['user_id'], 'Unknown')
        room_name = rooms_id.get(booking['room_id'], {}).get('room_name', 'Unknown')
        start_time = datetime.datetime.fromisoformat(booking['start_datetime']).strftime('%Y/%m/%d %H:%M')
        end_time = datetime.datetime.fromisoformat(booking['end_datetime']).strftime('%Y/%m/%d %H:%M')
        
        st.write(f"**予約番号:** {booking['booking_id']}")
        st.write(f"**予約者:** {username}")
        st.write(f"**会議室:** {room_name}")
        st.write(f"**予約人数:** {booking['booked_num']}名")
        st.write(f"**時間:** {start_time} ～ {end_time}")
        st.write("---")


    with st.form(key='booking'):
        username: str = st.selectbox('予約者名', users_name.keys())
        room_name: str = st.selectbox('会議室名', rooms_name.keys())
        booked_num: int = st.number_input('予約人数', step=1, min_value=1)
        date = st.date_input('日付: ', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻: ', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('終了時刻: ', value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label='予約登録')

    if submit_button:
        user_id: int = users_name[username]
        room_id: int = rooms_name[room_name]['room_id']
        capacity: int = rooms_name[room_name]['capacity']

        data = {
            'user_id': user_id,
            'room_id': room_id,
            'booked_num': booked_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        # 定員より多い予約人数の場合
        if booked_num > capacity:
            st.error(f'{room_name}の定員は、{capacity}名です。{capacity}名以下の予約人数のみ受け付けております。')
        # 開始時刻 >= 終了時刻
        elif start_time >= end_time:
            st.error('開始時刻が終了時刻を越えています')
        elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
            st.error('利用時間は9:00~20:00になります。')
        else:
            # 会議室予約
            url = 'http://127.0.0.1:8000/bookings'
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            if res.status_code == 200:
                st.success('予約完了しました')            
            elif res.status_code == 404:
                response_data = safe_json_response(res)
                if isinstance(response_data, dict) and response_data.get('detail') == 'Already booked':
                    st.error('指定の時間にはすでに予約が入っています。')
                else:
                    st.error(f'予約エラー: {response_data}')
