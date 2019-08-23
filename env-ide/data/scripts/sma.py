from datetime import datetime
import backtrader as bt
import tkinter
import matplotlib
from sys import platform as sys_pf
if(sys_pf == "darwin"):
    matplotlib.use("MacOSX")
# import backtrader.plot

# try:
#     #Quick workaround for avoiding the following error while using cerebro.plot
#     #ImportError: Cannot load backend 'TkAgg' which requires the 'tk' interactive framework, as 'headless' is currently running
#     %matplotlib
# except (KeyboardInterrupt, SystemExit):
#     raise
# except Exception as e:
#     print("Ignoring", e)
# import matplotlib.pyplot as plt

print(matplotlib.get_configdir())
print(matplotlib.get_backend())

# Create a subclass of Strategy to define the indicators and logic
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

cerebro.broker.setcommission(
    commission = 0.004
)
# Create a data feed
data = bt.feeds.YahooFinanceData(dataname='MSFT',
                                 fromdate=datetime(2019, 1, 1),
                                 todate=datetime.now().date())
print(data)
cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
print(cerebro.broker.getvalue())
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [16, 10]
cerebro.plot()  # and plot it with a single command
# cerebro.plot(iplot=False)
plt.show()
print("strategy end")
