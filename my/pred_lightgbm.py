import qlib
import pandas as pd
import yaml
from qlib.utils import init_instance_by_config
from qlib.data import D

# 1. 加载修改后的配置
config_path = 'examples/benchmarks/LightGBM/workflow_config_lightgbm_test.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# 2. 初始化 Qlib
qlib.init(provider_uri=config['qlib_init']['provider_uri'], region=config['qlib_init']['region'])

# 3. 从 task 中提取 dataset 配置
dataset_config = config['task']['dataset']

# 4. 初始化数据集
dataset = init_instance_by_config(dataset_config)

# 5. 初始化模型
model_config = config['task']['model']
model = init_instance_by_config(model_config)

# 6. 训练模型
print("训练模型中...")
model.fit(dataset)
print("训练完成。\n")

# 7. 预测
pred_score = model.predict(dataset)

# 8. 查询 AAPL 在 2020-11-10 的预测 (用于预测 2020-11-11)
signal_date = '2020-11-10'    
target_stock = 'AAPL'

try:
    score = pred_score.loc[(target_stock, signal_date)].item()
    close_price = D.features([target_stock], ['$close'], start_time=signal_date, end_time=signal_date).item()
    
    print(f"========== 2020-11-11 预测报告 ==========")
    print(f"信号生成日期: {signal_date} (周二)")
    print(f"预测目标日期: 2020-11-11 (周三)")
    print(f"------- 模型预测 -------")
    print(f"预测评分 (Score): {score:.6f}")
    print(f"前日({signal_date})收盘价: ${close_price:.2f}")
    predicted_price = close_price * (1 + score)
    print(f"预测2020-11-11价格约: ${predicted_price:.2f}")
    print(f"隐含涨幅: {score*100:.2f}%")
    print(f"=========================================")
    
except KeyError as e:
    print(f"错误: 找不到数据")
    print(f"详情: {e}")