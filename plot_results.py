#!/usr/bin/python3


from matplotlib import pyplot as plt
import json


def read_data(file):
    data = []
    with open(file) as rfile:
        rjson = rfile.read()
        rdata = json.loads(rjson)
        intervals = rdata["intervals"]
        # only plot the first 9 points
        n_datapts = 0
        for interval in intervals:
            data.append(interval["sum"]["bits_per_second"])
            if n_datapts >= 9:
                break
            n_datapts += 1
    return data


def plot(data_closed, data_public):
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(data_closed, label="isolated network", color="blue")
    ax2.plot(data_public, label="public network", color="green")
    ax.set_title("iperf3 bandwith test on isolated network and public network")
    ax.set_xlabel("interval number")
    ax.set_ylabel("gigabits per second")
    ax.legend(loc=2)
    ax.yaxis.offsetText.set_visible(False)
    ax2.yaxis.offsetText.set_visible(False)
    ax2.legend(loc=4)
    plt.show()


def main():
    data_closed = read_data("results_closed_network.json")
    data_public = read_data("results_public_network.json")
    plot(data_closed, data_public)


if __name__ == "__main__":
    main()