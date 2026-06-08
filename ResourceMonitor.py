import psutil
import time
import matplotlib.pyplot as plt
import numpy as np
import signal
import socket
import sys

def find_pid_by_port(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == 'LISTEN':
            return conn.pid
    return None

def smooth(data, window_size=5):
    if len(data) < window_size:
        return data
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def plot_data(timestamps, cpu_usages, mem_usages, save=True):
    timestamps = np.array(timestamps)
    cpu_usages = np.array(cpu_usages)
    mem_usages = np.array(mem_usages)


    cpu_smoothed = smooth(cpu_usages, window_size=5)
    mem_smoothed = smooth(mem_usages, window_size=5)
    t_smoothed = timestamps[:len(cpu_smoothed)]

    cpu_thresholds = [np.mean(cpu_smoothed[:i+1]) + 10 * np.std(cpu_smoothed[:i+1]) for i in range(len(cpu_smoothed))]
    mem_thresholds = [np.mean(mem_smoothed[:i+1]) + 10 * np.std(mem_smoothed[:i+1]) for i in range(len(mem_smoothed))]

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.plot(t_smoothed, cpu_smoothed, label='CPU Usage (smoothed)')
    plt.plot(t_smoothed, cpu_thresholds, 'r--', label='μ + 10σ (dynamic)')
    plt.title('CPU Usage Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Usage (%)')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(t_smoothed, mem_smoothed, color='orange', label='Memory Usage (smoothed)')
    plt.plot(t_smoothed, mem_thresholds, 'r--', label='μ + 10σ (dynamic)')
    plt.title('Memory Usage Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Memory Usage (MB)')
    plt.legend()

    plt.tight_layout()

    if save:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"monitor_{timestamp}.png"
        plt.savefig(filename)
        print(f"📊 Plot saved as '{filename}'")

    plt.show()

def monitor_process(port, interval=0.2):
    pid = find_pid_by_port(port)
    if pid is None:
        print(f"No process found on port {port}")
        return

    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print(f"Process {pid} does not exist")
        return

    timestamps = []
    cpu_usages = []
    mem_usages = []

    print(f"Monitoring process PID={pid} on port {port}... (Press Ctrl+C to stop)")

    def handler(signum, frame):
        print("\n⏹️ Stopping and generating plots...")
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        np.savez(f"monitor_data_{timestamp_str}.npz",
                 timestamps=np.array(timestamps),
                 cpu_usages=np.array(cpu_usages),
                 mem_usages=np.array(mem_usages))
        print(f"💾 Data saved as 'monitor_data_{timestamp_str}.npz'")
        plot_data(timestamps, cpu_usages, mem_usages)
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    while True:
        try:
            cpu = p.cpu_percent(interval=None)
            time.sleep(interval)
            cpu = p.cpu_percent(interval=None)
            mem = p.memory_info().rss / 1024 / 1024  # MB

            timestamps.append(time.time())
            cpu_usages.append(cpu)
            mem_usages.append(mem)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            finalize_and_analyze(
                timestamps,
                cpu_usages,
                mem_usages,
                reason="target process ended or access denied"
            )
            break

if __name__ == "__main__":
    port = int(input("Enter port to monitor: "))
    monitor_process(port, interval=0.2)
