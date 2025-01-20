import subprocess; 

# while True:
#         print("\nScheduling Algorithms\n Choose an algorithm.")
#         print("1. FIFO")
#         print("2. SRT (Shortest Remaining Time)")
#         print("3. SJF (Shortest Job First)")
#         print("4. HRRN (Highest Response Ratio Next)")
#         print("5. Exit")
        
#         choice = input("Enter your choice: ")
        
#         if choice == '1':
#             subprocess.run(["python", "FIFO.py"])
#         elif choice == '2':
#             subprocess.run(["python", "SRT.py"])
#         elif choice == '3':
#             subprocess.run(["python", "SJF.py"])
#         elif choice == '4':
#             subprocess.run(["python", "HRRN.py"])
#         elif choice == '5':
#             print("Exiting program.")
#             break
#         else:
#             print("Invalid choice. Please select a valid option.")
import FIFO
import SRT
import SJF
import HRRN
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

process_list = []
num_processes = int(input("Enter the number of processes: "))
for i in range(num_processes):
    arrival_time = int(input(f"Enter arrival time for process {i+1}: "))
    burst_time = int(input(f"Enter burst time for process {i+1}: "))
    process_list.append(Process(i+1, arrival_time, burst_time))

FIFO.main(process_list)
SRT.main(process_list)
SJF.main(process_list)
HRRN.main(process_list)