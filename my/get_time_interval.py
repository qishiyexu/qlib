import qlib
from qlib.config import REG_US
from qlib.data import D

# 初始化 Qlib
qlib.init(provider_uri='~/.qlib/qlib_data/us_data', region=REG_US)

# 打印可用的交易日历范围
try:
    calendar = D.calendar(freq='day')
    print(f"数据集时间范围：{calendar[0]} 至 {calendar[-1]}")
    print(f"总共交易日数：{len(calendar)}")
except Exception as e:
    print(f"错误：{e}")

_start_time=calendar[0]
_end_time=calendar[-1]

# 打印可用的股票代码
try:
    instruments = D.instruments(market='all')
    stocks = D.list_instruments(instruments, start_time=_start_time, end_time=_end_time, as_list=True)
    print(f"最近可用股票数：{len(stocks)}")
    print(f"样本股票代码：{stocks[:5]}")
except Exception as e:
    print(f"获取股票列表错误：{e}")



print("\n--- 获取可用的工具/股票 ---")
try:
    instruments_config = D.instruments(market='all')
    print(f"✓ instruments 配置对象获取成功")
    
    # 获取列表形式的工具
    inst_list = D.list_instruments(
        instruments=instruments_config,
        start_time=_start_time,
        end_time=_end_time,
        as_list=True
    )
    
    print(f"✓ 在 {_start_time} 至 {_end_time} 期间可用的工具数：{len(inst_list)}")
    
    if len(inst_list) > 0:
        print(f"  样本工具代码：{inst_list[:10]}")
    else:
        print("  ⚠️ 未发现任何工具！")
        
except Exception as e:
    print(f"✗ 获取工具列表失败：{e}")
    import traceback
    traceback.print_exc()

print("\n--- 查询某个 ticker 的交易日数 ---")
target_stock = "AAPL"

try:
    # 3. 加载该股票从 1980年 到 2030年 之间的所有收盘价 ($close)
    #    这会覆盖绝大多数可能的交易区间
    df = D.features([target_stock], ['$close'], start_time='1980-01-01', end_time='2030-01-01')

    if not df.empty:
        # 4. 提取时间索引的最小值和最大值
        #    索引通常是 (instrument, datetime) 的 MultiIndex
        dates = df.index.get_level_values('datetime')
        start_date = dates.min()
        end_date = dates.max()
        
        print(f"================ {target_stock} 数据统计 ================")
        print(f"开始日期: {start_date.strftime('%Y-%m-%d')}")
        print(f"结束日期: {end_date.strftime('%Y-%m-%d')}")
        print(f"总交易日数: {len(df)}")
        print(f"====================================================")
    else:
        print(f"未找到 {target_stock} 的数据。请检查代码是否正确（如区分大小写）。")

except Exception as e:
    print(f"查询出错: {e}")


print("\n--- 尝试加载基准指数 ---")
benchmark_codes = ['^GSPC', 'GSPC', '^NDX', 'NDX', '^DJI', 'DJI']

for code in benchmark_codes:
    try:
        # 尝试将其作为工具加载数据
        df = D.features(
            instruments=[code],
            fields=['$close'],
            start_time=_start_time,
            end_time=_end_time,
            freq='day'
        )
        if df is not None and len(df) > 0:
            print(f"✓ {code:10s} 可用 ({len(df)} 行数据)")
        else:
            print(f"✗ {code:10s} 返回空数据")
    except Exception as e:
        error_msg = str(e)[:50]
        print(f"✗ {code:10s} 报错：{error_msg}")