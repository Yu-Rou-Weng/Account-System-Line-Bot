import gevent
import locust
from locust.env import Environment
from locust.stats import stats_history
from locust.stats import print_stats
import pytest


class UsersTest(locust.TaskSet):

    @locust.task(1)
    def api_get_task(self):
        self.client.get("/", name="GET /api") 
    
    @locust.task(1)
    def api_post_task(self):
        self.client.post("/api/transaction?id=Test&iotype=收入&consume_type=無&amount=8000&time_year=2024&time_month=6&time_date=9&remark=無", name="POST /api")


class SituationTest(locust.HttpUser):
    tasks = [UsersTest]  # Use a list to reference the task set class
    min_wait = 1000
    max_wait = 2000
    host = "http://127.0.0.1:5000/"

def print_detailed_stats(env):
    print("Detailed Stats:")
    for entry in env.stats.entries.values():
        print(f"Request Type: {entry.name} {entry.method}")
        print(f"  Number of Requests: {entry.num_requests}")
        print(f"  Number of Failures: {entry.num_failures}")
        print(f"  Min Response Time: {entry.min_response_time}")
        print(f"  Max Response Time: {entry.max_response_time}")
        print(f"  Avg Response Time: {entry.avg_response_time}")
        print(f"  Median Response Time: {entry.median_response_time}")
        print(f"  95th Percentile Response Time: {entry.get_response_time_percentile(0.95)}")
        print(f"  99th Percentile Response Time: {entry.get_response_time_percentile(0.99)}")
        print(f"  Average Content Size: {entry.avg_content_length}")
        print(f"  Requests per Second: {entry.current_rps}")
        print(f"  Failures per Second: {entry.current_fail_per_sec}")
        print()

def test_smoke():
    print("Smoke test start!")
    env = Environment(user_classes=[SituationTest])
    env.create_local_runner()
    gevent.spawn(stats_history, env.runner)
    env.runner.start(1, spawn_rate=1)  # 1 user, 1 user/second spawn rate
    gevent.spawn_later(5, lambda: env.runner.quit())  # Run for 5 seconds
    env.runner.greenlet.join()

    print_detailed_stats(env)
    assert env.stats.total.avg_response_time < 100
    assert env.stats.total.num_failures == 0
    assert env.stats.total.get_response_time_percentile(0.95) < 200

def test_load():
    print("Load test start!")
    env = Environment(user_classes=[SituationTest])
    env.create_local_runner()
    gevent.spawn(stats_history, env.runner)
    env.runner.start(50, spawn_rate=5)  # 50 users, 5 users/second spawn rate
    gevent.spawn_later(300, lambda: env.runner.quit())  # Run for 5 minutes
    env.runner.greenlet.join()

    print_detailed_stats(env)
    assert env.stats.total.avg_response_time < 100
    assert env.stats.total.num_failures == 0
    assert env.stats.total.get_response_time_percentile(0.95) < 200


def test_stress():
    print("Stress test start!")
    env = Environment(user_classes=[SituationTest])
    env.create_local_runner()
    gevent.spawn(stats_history, env.runner)
    env.runner.start(200, spawn_rate=20)  # 200 users, 20 users/second spawn rate
    gevent.spawn_later(300, lambda: env.runner.quit())  # Run for 5 minutes
    env.runner.greenlet.join()

    print_detailed_stats(env)
    # Stress tests may not have assert conditions since they are looking for breaking points

def test_soak():
    print("Soak test start!")
    env = Environment(user_classes=[SituationTest])
    env.create_local_runner()
    gevent.spawn(stats_history, env.runner)
    env.runner.start(50, spawn_rate=5)  # 50 users, 5 users/second spawn rate
    gevent.spawn_later(600, lambda: env.runner.quit())  # Run for 10 minutes
    env.runner.greenlet.join()

    print_stats(env.stats)
    print_detailed_stats(env)
    assert env.stats.total.avg_response_time < 100
    assert env.stats.total.num_failures == 0
    assert env.stats.total.get_response_time_percentile(0.95) < 200



def test_your_pytest_example():
    env = Environment(user_classes=[SituationTest])
    env.create_local_runner()
    env.create_web_ui("127.0.0.1", 8089)
    gevent.spawn(stats_history, env.runner)
    env.runner.start(1, spawn_rate=1)
    gevent.spawn_later(20, lambda: env.runner.quit())  # Increase runtime to 20 seconds
    env.runner.greenlet.join()

    stats = env.stats

    # Print aggregate stats
    stats = env.stats.total
    print("Aggregate Stats:")
    print(f"Total requests: {stats.num_requests}")
    print(f"Total failures: {stats.num_failures}")
    print(f"Average response time: {stats.avg_response_time}")
    print(f"Median response time: {stats.median_response_time}")
    print(f"Min response time: {stats.min_response_time}")
    print(f"Max response time: {stats.max_response_time}")
    print(f"95th percentile response time: {stats.get_response_time_percentile(0.95)}")
    print(f"99th percentile response time: {stats.get_response_time_percentile(0.99)}")
    print(f"Average content size: {stats.avg_content_length}")
    print(f"Requests per second: {stats.total_rps}")
    print(f"Failures per second: {stats.total_fail_per_sec}")


    assert env.stats.total.avg_response_time < 60
    assert env.stats.total.num_failures == 0
    assert env.stats.total.get_response_time_percentile(0.95) < 100

if __name__ == "__main__":
    pytest.main(["-s", "test_locust.py"])