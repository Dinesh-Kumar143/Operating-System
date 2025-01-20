from tabulate import tabulate


class Process:
    def __init__(self, pid, arrival_time, execution_time, resource_info, quantum_size):
        self.pid = pid  # Process ID
        self.arrival_time = arrival_time  # Arrival time of the process
        # Simulated instruction list
        self.execution_time = list(range(execution_time))
        # 0 for no resource needed, 1 for resource needed
        self.resource_info = resource_info
        self.quantum_size = quantum_size  # Time quantum for Round Robin scheduling
        self.finish_time = None  # Time when the process finishes
        # PSW Resume Info (Program Status Word)
        self.psw_resume_info_num = None
        self.psw_resume_info_address = None  # Memory address for resuming the process
        self.state = 'Ready'  # Initial state is 'Ready'
        self.pc = 0  # Program Counter (current instruction index)
        self.ir = 0  # Instruction Register (holds the current instruction)
        self.processed_instructions = 0  # Number of processed instructions


def print_pcb(process):
    """Prints the Process Control Block (PCB) information."""
    print(f"\nProcess ID = {process.pid}")
    print(f"Arrival Time = {process.arrival_time}")
    print(f"Execution Time = {len(process.execution_time)}")
    print(f"Resource Information = {process.resource_info}")
    print(
        f"Finish Time = {process.finish_time if process.finish_time is not None else 'In Progress'}")
    print(f"PSW Resume Info Number = {process.psw_resume_info_num}")
    print(f"PSW Resume Info Address = {process.psw_resume_info_address}")
    print(
        f"Scheduling Algorithm = Round Robin (Quantum size = {process.quantum_size})")
    print(f"State = {process.state}")
    print(f"PC = {process.pc + 1}")
    print(f"IR = {process.ir + 2}")
    print(f"No of Processed Instructions = {process.processed_instructions}")
    print("----------------------------------------")


def process_summary_table(processes):
    """Prints the final table of process details after execution."""
    table = []
    headers = ["Process ID", "Arrival Time", "Execution Time", "Finish Time", "PSW Resume Info Num",
               "PSW Resume Info Address", "State", "Processed Instructions"]

    for process in processes:
        table.append([
            process.pid,
            process.arrival_time,
            len(process.execution_time),
            process.finish_time if process.finish_time is not None else "In Progress",
            process.psw_resume_info_num,
            process.psw_resume_info_address,
            process.state,
            process.processed_instructions
        ])

    print("\nFinal Process Table:")
    print(tabulate(table, headers=headers))


def round_robin_scheduler(processes):
    """Implements the Round Robin scheduling algorithm."""
    time = 0  # Global time counter
    blocked_queue = []  # Queue for blocked processes

    while processes or blocked_queue:
        active_processes = processes.copy()  # Copy list to iterate without modifying

        for process in active_processes:
            if process.state == 'Blocked':
                continue  # Skip blocked processes

            if process.resource_info:  # Check if resource is required
                # Update PSW Resume Info before blocking
                process.psw_resume_info_num = process.pc
                process.psw_resume_info_address = f"{process.pid}[{process.pc}]"
                process.state = 'Blocked'  # Mark process as blocked
                blocked_queue.append(process)
                processes.remove(process)
                print(f"\n{process.pid} is blocked due to resource issue.")
                continue  # Move to the next process

            print(f"\nRunning {process.pid}")
            process.state = 'Running'  # Process is now running
            quantum_size = process.quantum_size  # Use process-specific quantum size

            # Execute for quantum size or until process finishes
            for _ in range(quantum_size):
                if process.pc < len(process.execution_time):
                    # Update IR to current instruction
                    process.ir = process.execution_time[process.pc]
                    process.processed_instructions += 1
                    print_pcb(process)

                    process.pc += 1  # Increment program counter
                    time += 1  # Increment global time
                else:
                    process.finish_time = time  # Set finish time
                    process.state = 'Terminated'  # Mark process as terminated
                    processes.remove(process)
                    print(
                        f"{process.pid} has terminated. Finish Time = {process.finish_time}.")
                    break  # Stop executing this process

            # Update PSW Resume Info for non-terminated processes
            if process.state != 'Terminated':
                process.psw_resume_info_num = process.pc
                process.psw_resume_info_address = f"{process.pid}[{process.pc}]"

            # Mark process as ready for the next round if not terminated or blocked
            if process.state != 'Terminated' and process not in blocked_queue:
                process.state = 'Ready'

        # Handle blocked processes
        if not processes and blocked_queue:
            print("\nHandling blocked processes...")
            unblocked_processes = []
            for process in blocked_queue:
                # Simulate resource availability and unblock process
                process.resource_info = False
                process.state = 'Ready'
                unblocked_processes.append(process)
                print(f"{process.pid} is unblocked and ready to resume.")

            # Move unblocked processes back to the active list
            processes.extend(unblocked_processes)
            blocked_queue.clear()

        # Exit if all processes are handled
        if not processes and not blocked_queue:
            print("\nAll processes have been terminated or handled.")
            break


def main():
    processes = []  # List of processes
    num_processes = int(input("Enter the number of processes (max 5): "))

    if num_processes > 5:
        print("Error: Number of processes cannot be more than 5")
        return

    for i in range(num_processes):
        pid = f"P{i}"  # Process ID
        arrival_time = i  # Simplified arrival time
        execution_time = int(
            input(f"Enter execution time for process {pid} (between 10 and 12): "))
        if execution_time < 10 or execution_time > 12:
            print("Error: Execution time must be between 10 and 12.")
            return
        resource_info = int(
            input(f"Does process {pid} need a resource (0 for No, 1 for Yes)? "))
        quantum_size = int(input("Enter Quantum size (<= 3 and != 0): "))
        if quantum_size > 3 or quantum_size == 0:
            print("Error: Quantum size must be <= 3 and != 0")
            return

        # Create and add process to the list
        process = Process(pid, arrival_time, execution_time,
                          resource_info, quantum_size)
        processes.append(process)

    # Print the initial process table
    print("\nProcess Table:")
    print("ID    Arrival    Execution Time")
    for process in processes:
        print(
            f"{process.pid}      {process.arrival_time}          {len(process.execution_time)}")

    # Call the scheduler
    round_robin_scheduler(processes)

    # process_summary_table(processes)


if __name__ == "__main__":
    main()
