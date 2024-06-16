import threading  
import time  
  
import psutil  
import pytest  
import requests  
  
  
# 定义测试用例  
@pytest.mark.performance  
def test_performance():  
    # 设置测试参数  
    url = 'http://127.0.0.1:5000/'  
    num_threads = 20  
    num_requests = 200  
    timeout = 5  
  
    # 初始化测试结果  
    response_times = []  
    errors = 0  
    successes = 0  
  
    # 定义测试函数  
    def test_func():  
        nonlocal errors, successes  
        for _ in range(num_requests):  
            try:  
                start_time = time.time()  
                requests.get(url, timeout=timeout)  
                end_time = time.time()  
                response_time = end_time - start_time  
                response_times.append(response_time)  
                successes += 1  
            except requests.exceptions.RequestException:  
                errors += 1  
  
    # 创建测试线程  
    threads = []  
    for _ in range(num_threads):  
        t = threading.Thread(target=test_func)  
        threads.append(t)  
  
    # 启动测试线程  
    for t in threads:  
        t.start()  
  
    # 等待测试线程结束  
    for t in threads:  
        t.join()  
  
    # 计算测试结果  
    total_requests = num_threads * num_requests  
    throughput = successes / (sum(response_times) or 1)  
    concurrency = num_threads  
    error_rate = errors / (total_requests or 1)  
    cpu_usage = psutil.cpu_percent()  
    memory_usage = psutil.virtual_memory().percent  
  
    # 输出测试结果  
    print(f'總請求數：{total_requests}')  
    print(f'總時間：{sum(response_times):.2f}s')  
    print(f'吞吐量：{throughput:.2f} requests/s')  
    print(f'併發率：{concurrency}')  
    print(f'錯誤率：{error_rate:.2%}')  
    print(f'CPU使用率：{cpu_usage:.2f}%')  
    print(f'記憶體使用率：{memory_usage:.2f}%')  
  
    # 将测试结果写入文件  
    with open('performance_test_result.txt', 'w') as f:  
        f.write(f'總請求數：{total_requests}\n')  
        f.write(f'總時間：{sum(response_times):.2f}s\n')  
        f.write(f'吞吐量：{throughput:.2f} requests/s\n')  
        f.write(f'併發率：{concurrency}\n')  
        f.write(f'錯誤率：{error_rate:.2%}\n')  
        f.write(f'CPU使用率：{cpu_usage:.2f}%\n')  
        f.write(f'記憶體使用率：{memory_usage:.2f}%\n')