import pickle
import pandas as pd

def obj_to_dict(obj):
    """将对象或字典转为字典"""
    if isinstance(obj, dict):
        return obj
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    elif hasattr(obj, 'to_dict'):  # 如果有to_dict方法
        return obj.to_dict()
    else:
        return {}
    
def flatten_position_data(data):
    records = []
    
    for timestamp, day_data in data.items():
        day_dict = obj_to_dict(day_data)
        position = day_dict.get('position', {})
        
        if not isinstance(position, dict):
            position = obj_to_dict(position)
        
        for ticker, info in position.items():
            if ticker not in ['cash', 'now_account_value', '_settle_type']:
                info_dict = obj_to_dict(info)
                
                def safe_get(d, key, default=0, dtype=float):
                    if isinstance(d, dict):
                        val = d.get(key, default)
                    else:
                        val = getattr(d, key, default)
                    return dtype(val) if val is not None else default
                
                records.append({
                    'date': timestamp,
                    'ticker': ticker,
                    'amount': safe_get(info_dict, 'amount', 0, float),
                    'price': safe_get(info_dict, 'price', 0, float),
                    'weight': safe_get(info_dict, 'weight', 0, float),
                    'count_day': safe_get(info_dict, 'count_day', 0, int)
                })
    
    return pd.DataFrame(records)

print("========================== [port_analysis_1day] ==============================")
with open('C:\\Don\\code\\qlib\\mlruns\\314554406726719244\\16dce9fb79374039a2f8671072331cfe\\artifacts\\portfolio_analysis\\port_analysis_1day.pkl', 'rb') as f:
    backtest_data = pickle.load(f)
    print(backtest_data)

print("========================== [positions_normal_1day] ==============================")
with open('C:\\Don\\code\\qlib\\mlruns\\314554406726719244\\16dce9fb79374039a2f8671072331cfe\\artifacts\\portfolio_analysis\\positions_normal_1day.pkl','rb') as f:
    analysis = pickle.load(f)
    df = flatten_position_data(analysis)
    print(df)  
    df.to_csv('portfolio_positions.csv', index=False)

print("========================== [report_normal_1day] ==============================")
with open('C:\\Don\\code\\qlib\\mlruns\\314554406726719244\\16dce9fb79374039a2f8671072331cfe\\artifacts\\portfolio_analysis\\report_normal_1day.pkl','rb') as f:
    analysis = pickle.load(f)
    print(analysis)  