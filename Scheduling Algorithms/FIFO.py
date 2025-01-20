import matplotlib.pyplot as plt
import random


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = 0
        self.response_time = 0


def FIFO_scheduling(processes):
    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    gantt_chart = []  # Store the execution order for the Gantt chart
    total_busy_time = 0  # Track CPU busy time for utilization calculation

    for process in processes:
        # Calculate start time based on current time and arrival
        process.start_time = max(current_time, process.arrival_time)

        # Calculate response time (start time - arrival time)
        process.response_time = process.start_time - process.arrival_time

        # Calculate waiting time (queue time before execution)
        process.waiting_time = process.start_time - process.arrival_time

        # Completion time = start time + burst time
        process.completion_time = process.start_time + process.burst_time

        # Turnaround time = completion time - arrival time
        process.turnaround_time = process.completion_time - process.arrival_time

        # Move current time forward
        current_time = process.completion_time
        total_busy_time += process.burst_time  # Increase busy time by burst time

        # Append the process to the Gantt chart for each time unit in its burst time
        gantt_chart.extend([process.pid] * process.burst_time)

    # Calculate CPU utilization as percentage
    cpu_utilization = (total_busy_time / current_time) * 100
    return gantt_chart, cpu_utilization


def print_processes(processes, cpu_utilization):
    print("PID\tArrival\tBurst\tStart\tCompletion\tTurnaround\tWaiting\tResponse")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.start_time}\t"
              f"{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.response_time}")
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
    gnt.set_xlim(0, len(gantt_chart))
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
    gnt.set_xticks(range(len(gantt_chart)))

    plt.show()


def main(process_list):
    
    gantt_chart, cpu_utilization = FIFO_scheduling(process_list)
    print_processes(process_list, cpu_utilization)
    plot_gantt_chart(gantt_chart)

