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
        self.start_time = -1
        self.response_time = 0


def SJF_scheduling(processes):
    time = 0
    completed = 0
    n = len(processes)
    gantt_chart = []
    total_busy_time = 0
    while completed < n:
        # Filter available processes that have arrived and are not completed
        available_processes = [p for p in processes if p.arrival_time <= time and p.completion_time == 0]
        
        # Select the process with the shortest burst time among the available processes
        if available_processes:
            current_process = min(available_processes, key=lambda x: x.burst_time)
            gantt_chart.extend([current_process.pid] * current_process.burst_time)

            # Process execution
            current_process.start_time = time if current_process.start_time == -1 else current_process.start_time
            current_process.response_time = time - current_process.arrival_time
            time += current_process.burst_time
            current_process.completion_time = time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

            completed += 1
            total_busy_time += current_process.burst_time
        else:
            gantt_chart.append(-1)  # CPU is idle
            time += 1

    cpu_utilization = (total_busy_time / time) * 100
    return gantt_chart, cpu_utilization


def print_processes(processes, cpu_utilization):
    print("PID\tArrival\tBurst\tStart\tEnd\tResponse\tTurnaround\tWaiting")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.start_time}\t"
              f"{process.completion_time}\t{process.response_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}")
    print(f"\nCPU Utilization: {cpu_utilization:.2f}%\n")


def plot_gantt_chart(gantt_chart):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Process')
    
    process_ids = list(set(pid for pid in gantt_chart if pid != -1))
    gnt.set_yticks(process_ids)
    gnt.set_yticklabels([f'P{pid}' for pid in process_ids])
    gnt.set_xlim(0, len(gantt_chart))
    gnt.set_ylim(0.5, len(process_ids) + 0.5)

    colors = {pid: (random.random(), random.random(), random.random()) for pid in process_ids}

    for i, pid in enumerate(gantt_chart):
        if pid != -1:
            gnt.broken_barh([(i, 1)], (pid - 0.4, 0.8), facecolors=(colors[pid]))

    gnt.set_xticks(range(len(gantt_chart)))
    plt.show()


def main(process_list):

    gantt_chart, cpu_utilization = SJF_scheduling(process_list)
    print_processes(process_list, cpu_utilization)
    plot_gantt_chart(gantt_chart)



