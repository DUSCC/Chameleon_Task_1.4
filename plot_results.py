#!/usr/bin/python3

from matplotlib import pyplot as plt
import json


def read_data():
    data = []
    with open("results_closed_network.json") as rfile:
        rjson = rfile.read()
        rdata = json.loads(rjson)
        intervals = rdata["intervals"]
        for interval in intervals:
            data.append(interval["sum"]["bits_per_second"])
    return data


def plot(data):
    plt.plot(data)
    plt.xlabel("interval number")
    plt.ylabel("bits per second")
    plt.show()


def main():
    data = read_data()
    plot(data)


if __name__ == "__main__":
    main()