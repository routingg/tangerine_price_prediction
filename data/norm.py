import pandas as pd
import numpy as np

# 데이터 불러오기
price_data = pd.read_csv('price_data.csv', parse_dates=['date'], date_parser=lambda x: pd.to_datetime(x, format='%Y%m%d'))
weather_data = pd.read_csv('weather_data.csv', parse_dates=['date'])

# date 컬럼의 형식을 동일하게 맞추기
price_df['date'] = pd.to_datetime(price_df['date'], format='%Y%m%d')
weather_df['date'] = pd.to_datetime(weather_df['date'], format='%Y-%m-%d')

# 두 데이터프레임의 날짜 범위를 제한
end_date = min(price_df['date'].max(), weather_df['date'].max())
start_date = pd.to_datetime('130102', format='%y%m%d') # 시작 날짜 설정
price_df = price_df[(price_df['date'] >= start_date) & (price_df['date'] <= end_date)]
weather_df = weather_df[(weather_df['date'] >= start_date) & (weather_df['date'] <= end_date)]

# 모든 날짜를 포함하는 새 데이터프레임 생성
all_dates = pd.date_range(start=start_date, end=end_date)
all_dates_df = pd.DataFrame(all_dates, columns=['date'])

# 날짜를 기준으로 두 데이터프레임을 병합
merge_df = pd.merge(all_dates_df, weather_df, on='date', how='left')
merge_df = pd.merge(merge_df, price_df, on='date', how='left')

# 비가 오지 않은 날의 강수량을 0으로 설정
merge_df['rainFall'].fillna(0, inplace=True)

# 'avgPrice'는 해당 월의 평균 값으로 결측치를 채움
merge_df['avgPrice'] = merge_df.groupby(merge_df['date'].dt.to_period('M'))['avgPrice'].transform(lambda x: x.fillna(x.mean()))

# 'avgPrice'는 소수 첫째 자리에서 올림하여 정수로 변환
merge_df['avgPrice'] = merge_df['avgPrice'].apply(np.ceil).astype('Int64') # NaN이 있는 경우를 고려해 Int64 타입을 사용

# 나머지 결측치는 앞 방향으로 채우기
merge_df.fillna(method ='pad', inplace=True)

# date를 원하는 형식(YYYYMMDD)으로 변환
merge_df['date'] = merge_df['date'].dt.strftime('%Y%m%d')

# 컬럼 순서 변경
merge_df = merge_df[['date', 'avgTemp', 'maxTemp', 'minTemp', 'rainFall', 'avgPrice']]

# 결과를 새 CSV 파일로 저장
merge_df.to_csv('price data.csv', index=False)

print("전처리가 완료되었습니다. 'price data' 파일이 생성되었습니다.")
