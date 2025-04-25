import os
import sys
import time
import json
import signal
import subprocess
import threading
import requests
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)


# 配置日志
def setup_logger():
    import logging
    from logging.handlers import RotatingFileHandler

    logger = logging.getLogger("TaskAgent")
    logger.setLevel(logging.INFO)

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 文件输出，自动轮转
    file_handler = RotatingFileHandler(
        'agent.log', maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


class TaskAgent:
    def __init__(self,
                 scheduler_url: str,
                 agent_id: str,
                 heartbeat_interval: int = 30,
                 max_concurrent_tasks: int = 5,
                 http_port: int = 8080,
                 pull_mode: bool = True,
                 push_mode: bool = True):
        """
        初始化任务代理

        :param scheduler_url: 调度服务器URL
        :param agent_id: 代理ID
        :param heartbeat_interval: 心跳间隔(秒)
        :param max_concurrent_tasks: 最大并发任务数
        :param http_port: HTTP服务端口
        :param pull_mode: 是否启用主动拉取模式
        :param push_mode: 是否启用被动接收模式
        """
        self.scheduler_url = scheduler_url
        self.agent_id = agent_id
        self.heartbeat_interval = heartbeat_interval
        self.max_concurrent_tasks = max_concurrent_tasks
        self.http_port = http_port
        self.pull_mode = pull_mode
        self.push_mode = push_mode

        self.running_tasks: Dict[str, dict] = {}  # task_id -> task info
        self.pending_tasks: List[dict] = []  # 等待执行的任务队列
        self.processes: Dict[str, subprocess.Popen] = {}  # task_id -> process
        self.task_timeouts: Dict[str, float] = {}  # task_id -> timeout seconds
        self.task_start_times: Dict[str, float] = {}  # task_id -> start timestamp

        self.heartbeat_thread: Optional[threading.Thread] = None
        self.monitor_thread: Optional[threading.Thread] = None
        self.task_pull_thread: Optional[threading.Thread] = None

        self.stop_event = threading.Event()
        self.work_dir = Path("agent_workspace")
        self.dependency_cache = Path("dependency_cache")

        # 创建工作目录和缓存目录
        self.work_dir.mkdir(exist_ok=True)
        self.dependency_cache.mkdir(exist_ok=True)

        # 注册信号处理
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, signum, frame):
        """处理终止信号"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()

    def start(self):
        """启动代理"""
        logger.info(f"Starting agent {self.agent_id}")

        # 注册心跳
        if not self.register_with_scheduler():
            logger.error("Failed to register with scheduler, exiting...")
            return False

        # 启动心跳线程
        self.heartbeat_thread = threading.Thread(
            target=self.heartbeat_loop, daemon=True
        )
        self.heartbeat_thread.start()

        # 启动监控线程
        self.monitor_thread = threading.Thread(
            target=self.monitor_loop, daemon=True
        )
        self.monitor_thread.start()

        # 启动任务拉取线程
        if self.pull_mode:
            self.task_pull_thread = threading.Thread(
                target=self.task_pull_loop, daemon=True
            )
            self.task_pull_thread.start()

        # 启动任务执行循环
        threading.Thread(
            target=self.task_execution_loop, daemon=True
        ).start()

        return True

    def stop(self):
        """停止代理"""
        logger.info("Stopping agent...")
        self.stop_event.set()

        # 停止所有运行中的任务
        for task_id, process in self.processes.items():
            try:
                process.terminate()
                logger.info(f"Terminated task {task_id}")
            except Exception as e:
                logger.error(f"Error terminating task {task_id}: {e}")

        # 等待线程结束
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        if self.task_pull_thread:
            self.task_pull_thread.join(timeout=5)

        logger.info("Agent stopped")

    def register_with_scheduler(self) -> bool:
        """向调度器注册"""
        try:
            response = requests.post(
                f"{self.scheduler_url}/register",
                json={
                    "agent_id": self.agent_id,
                    "timestamp": int(time.time()),
                    "max_concurrent": self.max_concurrent_tasks,
                    "http_port": self.http_port if self.push_mode else None,
                    "push_mode": self.push_mode
                },
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to register with scheduler: {e}")
            return False

    def heartbeat_loop(self):
        """心跳循环"""
        while not self.stop_event.is_set():
            try:
                self.send_heartbeat()
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

            # 等待下一次心跳
            self.stop_event.wait(self.heartbeat_interval)

    def send_heartbeat(self):
        """发送心跳"""
        try:
            running_tasks = [
                {
                    "task_id": task_id,
                    "status": "running",
                    "start_time": self.task_start_times.get(task_id, 0),
                    "timeout": self.task_timeouts.get(task_id, 0)
                }
                for task_id in self.running_tasks
            ]

            response = requests.post(
                f"{self.scheduler_url}/heartbeat",
                json={
                    "agent_id": self.agent_id,
                    "timestamp": int(time.time()),
                    "running_tasks": running_tasks,
                    "pending_tasks": len(self.pending_tasks),
                    "status": "active",
                    "capacity": self.max_concurrent_tasks - len(self.running_tasks)
                },
                timeout=10
            )

            if response.status_code != 200:
                logger.warning(f"Heartbeat failed with status {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending heartbeat: {e}")

    def monitor_loop(self):
        """监控循环，检查超时任务"""
        while not self.stop_event.is_set():
            current_time = time.time()

            # 检查运行中的任务
            for task_id, start_time in list(self.task_start_times.items()):
                timeout = self.task_timeouts.get(task_id, 0)

                if timeout > 0 and (current_time - start_time) > timeout:
                    logger.warning(f"Task {task_id} has timed out, terminating...")
                    self.terminate_task(task_id)
                    # 上报任务失败
                    self.report_task_status(task_id, "failed", "timeout")

            # 检查进程状态
            for task_id, process in list(self.processes.items()):
                if process.poll() is not None:  # 进程已结束
                    return_code = process.returncode
                    status = "completed" if return_code == 0 else "failed"
                    logger.info(f"Task {task_id} has {status} with return code {return_code}")

                    # 清理资源
                    self.cleanup_task(task_id)

                    # 上报状态
                    self.report_task_status(
                        task_id,
                        status,
                        f"Process exited with code {return_code}"
                    )

            # 每秒检查一次
            self.stop_event.wait(1)

    def task_pull_loop(self):
        """任务拉取循环"""
        while not self.stop_event.is_set():
            try:
                # 从调度器获取任务
                tasks = self.fetch_tasks()

                for task in tasks:
                    self.add_task(task)

                # 短暂休眠避免频繁请求
                self.stop_event.wait(5)
            except Exception as e:
                logger.error(f"Error in task pull loop: {e}")
                self.stop_event.wait(10)  # 出错后等待更长时间

    def task_execution_loop(self):
        """任务执行循环"""
        while not self.stop_event.is_set():
            try:
                # 检查是否有空闲槽位和等待任务
                if len(self.running_tasks) < self.max_concurrent_tasks and self.pending_tasks:
                    task = self.pending_tasks.pop(0)
                    self.execute_task(task)

                    # 短暂休眠
                    self.stop_event.wait(1)
            except Exception as e:
                logger.error(f"Error in task execution loop: {e}")
                self.stop_event.wait(5)

    def add_task(self, task: dict):
        """添加任务到队列"""
        if task["task_id"] in self.running_tasks or any(t["task_id"] == task["task_id"] for t in self.pending_tasks):
            logger.warning(f"Task {task['task_id']} already exists")
            return

        self.pending_tasks.append(task)
        logger.info(f"Added task {task['task_id']} to queue, queue size: {len(self.pending_tasks)}")

        # 如果有空闲槽位，立即执行
        if len(self.running_tasks) < self.max_concurrent_tasks:
            self.execute_task(self.pending_tasks.pop(0))

    def fetch_tasks(self) -> List[dict]:
        """从调度器获取分配给此代理的任务"""
        try:
            response = requests.get(
                f"{self.scheduler_url}/tasks",
                params={"agent_id": self.agent_id},
                timeout=10
            )

            if response.status_code == 200:
                return response.json().get("tasks", [])
            else:
                logger.warning(f"Failed to fetch tasks: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error fetching tasks: {e}")
            return []

    def execute_task(self, task: dict):
        """执行任务"""
        task_id = task["task_id"]

        try:
            # 检查并发限制
            if len(self.running_tasks) >= self.max_concurrent_tasks:
                logger.warning(f"Cannot execute task {task_id}, reached max concurrent limit")
                self.pending_tasks.insert(0, task)  # 放回队列头部
                return

            # 记录任务开始
            self.running_tasks[task_id] = task
            self.task_start_times[task_id] = time.time()
            self.task_timeouts[task_id] = task.get("timeout", 0)

            # 创建任务工作目录
            task_dir = self.work_dir / task_id
            task_dir.mkdir(exist_ok=True)

            # 1. 从OSS拉取代码
            self.download_code(task["code_url"], task_dir)

            # 2. 写入种子文件
            self.write_seed_file(task.get("seed_data"), task_dir)

            # 3. 安装依赖
            if "requirements" in task:
                self.install_dependencies(task["requirements"], task_dir)

            # 4. 启动进程
            command = task["command"]
            process = self.start_process(command, task_dir)
            self.processes[task_id] = process

            # 上报任务开始
            self.report_task_status(task_id, "started", "Task started successfully")

            logger.info(f"Task {task_id} started successfully")
        except Exception as e:
            logger.error(f"Failed to start task {task_id}: {e}")
            self.cleanup_task(task_id)
            self.report_task_status(task_id, "failed", str(e))

    def download_code(self, code_url: str, dest_dir: Path):
        """从OSS下载代码"""
        # 这里简化实现，实际应该使用OSS SDK
        logger.info(f"Downloading code from {code_url} to {dest_dir}")

        # 模拟下载过程
        time.sleep(1)

        # 创建示例文件
        (dest_dir / "main.py").write_text("print('Hello from task!')")
        logger.info("Code downloaded successfully")

    def write_seed_file(self, seed_data: Optional[dict], task_dir: Path):
        """写入种子文件"""
        if not seed_data:
            return

        seed_file = task_dir / "seed.json"
        with seed_file.open("w") as f:
            json.dump(seed_data, f)
        logger.info(f"Seed file written to {seed_file}")

    def install_dependencies(self, requirements: List[str], task_dir: Path):
        """安装依赖"""
        logger.info(f"Installing dependencies: {requirements}")

        # 检查缓存
        cache_file = self.dependency_cache / "installed_deps.txt"
        installed_deps = set()

        if cache_file.exists():
            installed_deps = set(cache_file.read_text().splitlines())

        # 安装新依赖
        new_deps = [dep for dep in requirements if dep not in installed_deps]

        if new_deps:
            # 模拟pip安装过程
            logger.info(f"Installing new dependencies: {new_deps}")
            time.sleep(2)

            # 更新缓存
            installed_deps.update(new_deps)
            cache_file.write_text("\n".join(installed_deps))

        logger.info("Dependencies installed successfully")

    def start_process(self, command: str, work_dir: Path) -> subprocess.Popen:
        """启动进程"""
        logger.info(f"Starting process: {command} in {work_dir}")

        # 拆分命令
        if isinstance(command, str):
            command = command.split()

        # 在工作目录中启动进程
        process = subprocess.Popen(
            command,
            cwd=str(work_dir),
            stdout=open(str(work_dir / "stdout.log"), "w"),
            stderr=open(str(work_dir / "stderr.log"), "w"),
            preexec_fn=os.setsid  # 创建新的进程组
        )

        return process

    def terminate_task(self, task_id: str):
        """终止任务"""
        if task_id in self.processes:
            process = self.processes[task_id]
            try:
                # 终止整个进程组
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                logger.info(f"Terminated task {task_id}")
            except Exception as e:
                logger.error(f"Error terminating task {task_id}: {e}")

            self.cleanup_task(task_id)

    def cleanup_task(self, task_id: str):
        """清理任务资源"""
        if task_id in self.processes:
            del self.processes[task_id]
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        if task_id in self.task_start_times:
            del self.task_start_times[task_id]
        if task_id in self.task_timeouts:
            del self.task_timeouts[task_id]

        # 检查是否有等待任务可以执行
        if self.pending_tasks and len(self.running_tasks) < self.max_concurrent_tasks:
            next_task = self.pending_tasks.pop(0)
            self.execute_task(next_task)

    def report_task_status(self, task_id: str, status: str, message: str):
        """向调度器上报任务状态"""
        try:
            response = requests.post(
                f"{self.scheduler_url}/task_status",
                json={
                    "agent_id": self.agent_id,
                    "task_id": task_id,
                    "status": status,
                    "message": message,
                    "timestamp": int(time.time())
                },
                timeout=10
            )

            if response.status_code != 200:
                logger.warning(f"Failed to report task status: {response.status_code}")
        except Exception as e:
            logger.error(f"Error reporting task status: {e}")

    def restart_task(self, task_id: str):
        """重启任务"""
        if task_id in self.running_tasks:
            logger.info(f"Restarting task {task_id}")
            self.terminate_task(task_id)
            task = self.running_tasks[task_id]
            self.add_task(task.copy())  # 重新加入队列
        else:
            logger.warning(f"Cannot restart task {task_id}: not found")


# 全局Agent实例
agent: TaskAgent = Optional[TaskAgent]


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "running_tasks": len(agent.running_tasks),
        "max_concurrent": agent.max_concurrent_tasks,
        "pending_tasks": len(agent.pending_tasks)
    })


@app.route('/task', methods=['POST'])
def receive_task():
    """接收新任务接口"""
    if not agent.push_mode:
        return jsonify({"error": "Push mode not enabled"}), 400

    try:
        data = request.get_json()
        task = data["task"]
        agent.add_task(task)
        return jsonify({"status": "accepted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/control', methods=['POST'])
def control_task():
    """控制任务接口"""
    try:
        data = request.get_json()
        command = data["command"]
        task_id = data.get("task_id")

        if command == "restart":
            if task_id:
                agent.restart_task(task_id)
                return jsonify({"status": "restarted"})
            else:
                return jsonify({"error": "task_id required"}), 400
        elif command == "stop":
            if task_id:
                agent.terminate_task(task_id)
                return jsonify({"status": "stopped"})
            else:
                return jsonify({"error": "task_id required"}), 400
        else:
            return jsonify({"error": "invalid command"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_agent():
    """启动Agent"""
    global agent

    # 示例配置 - 实际使用时应该从配置文件或环境变量读取
    SCHEDULER_URL = "http://scheduler.example.com/api"
    AGENT_ID = f"agent-{os.getpid()}"

    agent = TaskAgent(
        scheduler_url=SCHEDULER_URL,
        agent_id=AGENT_ID,
        heartbeat_interval=30,
        max_concurrent_tasks=5,
        http_port=8080,
        pull_mode=True,
        push_mode=True
    )

    try:
        if agent.start():
            # 启动Flask应用
            app.run(host='0.0.0.0', port=agent.http_port)
    except KeyboardInterrupt:
        agent.stop()
    except Exception as e:
        logger.error(f"Agent crashed: {e}")
        agent.stop()


if __name__ == "__main__":
    run_agent()
