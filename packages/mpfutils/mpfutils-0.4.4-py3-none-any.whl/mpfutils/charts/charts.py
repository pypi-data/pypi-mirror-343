import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Charts:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def plot_line_chart(self, x: str, y: str, title: str = "Line Chart", xlabel: str = "X-axis", ylabel: str = "Y-axis"):
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=self.data, x=x, y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def plot_bar_chart(self, x: str, y: str, title: str = "Bar Chart", xlabel: str = "X-axis", ylabel: str = "Y-axis"):
        plt.figure(figsize=(10, 6))
        sns.barplot(data=self.data, x=x, y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def plot_bump_chart(self, x: str, y: str, title: str = "Bump Chart", xlabel: str = "X-axis", ylabel: str = "Y-axis"):
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=self.data, x=x, y=y, marker="o")

        # sort the data for bump chart
        self.data = self.data.sort_values(by=y, ascending=False)
        for i in range(len(self.data)):
            plt.text(self.data[x].iloc[i], self.data[y].iloc[i], self.data[y].iloc[i], fontsize=9, ha='right')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()