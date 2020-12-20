from gym.envs.registration import register

register(
    id='FXTrading-v0',
    entry_point='FX_trading.envs:ForexEnv_test',
    kwargs={'dataset': 'data/Test_data/sin_dataset.xlsx'}
)
register(
    id='FXTrading-v1',
    entry_point='FX_trading.envs:ForexEnv_test2',
    kwargs={'dataset': 'data/Test_data/sin_dataset.xlsx'}
)
register(
    id='FXTrading-v2',
    entry_point='FX_trading.envs:ForexEnv_test3',
    kwargs={'dataset': 'data/TimeFrame/2004/GBPUSD-2004_H1.xlsx'}
)
register(
    id='FXTrading-v99',
    entry_point='FX_trading.envs:ForexEnv',
    kwargs={'dataset': 'data/dataset/XM_EURUSD-2011_H1.xlsx'}
)