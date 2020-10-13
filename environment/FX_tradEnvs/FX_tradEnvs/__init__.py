from gym.envs.registration import register

register(
    id='FXTrading-v0',
    entry_point='FX_tradEnvs.envs:ForexEnv_test',
    kwargs={'dataset': 'data/Test_data/sin_dataset.xlsx'}
)
register(
    id='FXTrading-v1',
    entry_point='FX_tradEnvs.envs:ForexEnv',
    kwargs={'dataset': 'data/TimeFrame/2004/GBPUSD-2004_H1.xlsx'}
)

