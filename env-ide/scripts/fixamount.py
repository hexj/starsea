import tushare as ts
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def get_fixed_amt_rates(stocks):
    df = stocks.loc[:, ['date', 'close']]
    df['index'] = np.arange(1, len(df) + 1)
    df['amt_p-rec'] = 1.0/df['close']  # 价格倒数 p-rec
    df['amt_sum-vol'] = df['amt_p-rec'].cumsum()  # 定额总量，价格倒数累加求和
    df['amt_p'] = (df['index'])/df['amt_sum-vol']  # 定额平均单价 = 总价/总量
    df['amt_p_s1'] = df['amt_p'].shift(fill_value=df['close'].values[0])
    df['rates'] = df['close']/df['amt_p_s1']
    df = df.loc[:, ['date', 'close', 'amt_p', 'rates']]
    return df

def init_font(): #/usr/share/fonts/SimHei.ttf
    font_name = 'SimHei'
    plt.rcParams['font.family'] = font_name  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['font.sans-serif'].append(font_name)
    plt.rcParams['figure.figsize'] = 16, 8
    import matplotlib.font_manager
    matplotlib.font_manager._rebuild()
    print(matplotlib.font_manager.findfont(font_name))

def main():
    init_font()
    ETF_300 = ts.get_k_data('sh000300', start='2019-01-01')
    df = get_fixed_amt_rates(ETF_300)
    rate = df["close"].iloc[-1]/df["amt_p"].iloc[-1]
    df1 = df.loc[:, ['date', 'rates']]
    df.rename(columns={'close': '收盘价', 'amt_p': '平均持仓成本', 'rates':'定额投收益率'}, inplace=True)
    df.plot(x='date', subplots=True)
    plt.title('到结束日期收益率={:.2%}'.format(rate-1))
    plt.show()

if __name__ == '__main__':
    main()
