import matplotlib.pyplot as plt
import random


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = -1
        self.response_time = 0


def SRT_scheduling(processes):
    n = len(processes)
    time = 0
    completed = 0
    prev = -1
    min_remaining_time = float('inf')
    shortest = 0
    is_found = False
    gantt_chart = []  # To store the process execution order at each time
    total_busy_time = 0  # To calculate CPU utilization

    while completed != n:
        for i in range(n):
            if processes[i].arrival_time <= time and processes[i].remaining_time > 0:
                if processes[i].remaining_time < min_remaining_time:
                    min_remaining_time = processes[i].remaining_time
                    shortest = i
                    is_found = True
                elif processes[i].remaining_time == min_remaining_time:
                    if processes[i].arrival_time < processes[shortest].arrival_time:
                        shortest = i

        if not is_found:
            time += 1
            gantt_chart.append(-1)  # No process is being executed
            continue

        if prev != shortest:
            prev = shortest

        # Log the process being executed
        gantt_chart.append(processes[shortest].pid)

        # Check if it's the first time the process starts
        if processes[shortest].start_time == -1:
            processes[shortest].start_time = time
            processes[shortest].response_time = time - \
                processes[shortest].arrival_time

        processes[shortest].remaining_time -= 1
        total_busy_time += 1  # Increment busy time since a process is being executed

        min_remaining_time = processes[shortest].remaining_time
        if min_remaining_time == 0:
            min_remaining_time = float('inf')

        if processes[shortest].remaining_time == 0:
            completed += 1
            is_found = False

            finish_time = time + 1
            processes[shortest].completion_time = finish_time
            processes[shortest].turnaround_time = finish_time - \
                processes[shortest].arrival_time
            processes[shortest].waiting_time = processes[shortest].turnaround_time - \
                processes[shortest].burst_time

        time += 1

    cpu_utilization = (total_busy_time / time) * \
        100  # CPU utilization percentage
    return gantt_chart, cpu_utilization


def print_processes(processes, cpu_utilization):
    print("PID\tArrival\tBurst\tStart\tEnd\tResponse\tTurnaround\tWaiting")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.start_time}\t"
              f"{process.completion_time}\t{process.response_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}")
    print(f"\nCPU Utilization: {cpu_utilization:.2f}%\n")


def plot_gantt_chart(gantt_chart):
    fig, gnt = plt.subplots()

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Process')

    # Setting ticks on y-axis
    process_ids = list(set(pid for pid in gantt_chart if pid != -1))
    gnt.set_yticks(process_ids)
    gnt.set_yticklabels([f'P{pid}' for pid in process_ids])

    # Setting the chart limits
    gnt.set_xlim(0, len(gantt_chart)+0.5)
    gnt.set_ylim(0.5, len(process_ids) + 0.5)

    # Creating a random color for each process
    colors = {pid: (random.random(), random.random(), random.random())
              for pid in process_ids}

    # Plotting the Gantt chart
    for i, pid in enumerate(gantt_chart):
        if pid != -1:
            gnt.broken_barh([(i, 1)], (pid - 0.4, 0.8),
                            facecolors=(colors[pid]))

    # Setting the x-axis ticks to show each minute (each time unit)
    # Mark every time unit on the x-axis
    gnt.set_xticks(range(len(gantt_chart)+1))

    plt.show()


def main(process_list):

    gantt_chart, cpu_utilization = SRT_scheduling(process_list)
    print_processes(process_list, cpu_utilization)
    plot_gantt_chart(gantt_chart)
