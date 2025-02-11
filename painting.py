import pandas as pd
import matplotlib.pyplot as plt

def plot_trade_results(csv_file):
    df = pd.read_csv(csv_file)

    fig, axs = plt.subplots(3, 1, figsize=(12, 6), sharex=True)

    axs[0].plot(df['time_step'], df['best_bid'], label='Best Bid', color='blue')
    axs[0].plot(df['time_step'], df['best_ask'], label='Best Ask', color='red')
    axs[0].set_title('Best Bid & Ask')
    axs[0].legend()

    axs[1].plot(df['time_step'], df['assets'], label='Assets', color='green')
    axs[1].set_title('Assets Over Time')
    axs[1].legend()

    axs[2].plot(df['time_step'], df['total_profit'], label='Total Profit', color='red')
    axs[2].set_title('Total Profit Over Time')
    axs[2].legend()


    plt.xlabel('Time Step')
    plt.tight_layout()
    plt.savefig('trade_results2.png') # Или другой формат, например, .pdf, .svg
    plt.show()
 
if __name__ == "__main__":

    plot_trade_results("trade_results.csv")
