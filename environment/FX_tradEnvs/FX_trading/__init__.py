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
    kwargs={'dataset': 'data/TimeFrame/2004/GBPUSD-2004_H1.xlsx',
            'model' : 'model/scaler.pickle'}
)
register(
    id='FXTrading-v2011',
    entry_point='FX_trading.envs:ForexEnv',
    kwargs={'dataset': 'data/dataset/XM_EURUSD-2011_H1.xlsx',
            'model' : 'model/scaler.pickle'}
)
register(
    id='FXTrading-v2012',
    entry_point='FX_trading.envs:ForexEnv',
    kwargs={'dataset': 'data/dataset/XM_EURUSD-2012_H1.xlsx',
            'model' : 'model/scaler.pickle'}
)
register(
    id='FXTrading-v2013',
    entry_point='FX_trading.envs:ForexEnv',
    kwargs={'dataset': 'data/dataset/XM_EURUSD-2013_H1.xlsx',
            'model' : 'model/scaler.pickle'}
)
register(
    id='FXTrading-v2014',
    entry_point='FX_trading.envs:ForexEnv',
    kwargs={'dataset': 'data/dataset/XM_EURUSD-2014_H1.xlsx',
            'model' : 'model/scaler.pickle'}
)
register(
    id='FXTrading-v2015',
    entry_point='FX_trading.envs:ForexEnv',
    kwargs={'dataset': 'data/dataset/XM_EURUSD-2015_H1.xlsx',
            'model' : 'model/scaler.pickle'}
)