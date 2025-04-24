import os
import tempfile
from datetime import datetime
import argparse
from pathlib import Path

from musa_develop.check.shell_executor import BaseShellExecutor
from musa_develop.utils import InventoryGenerator


class AnsibleExecutor(BaseShellExecutor):
    def __init__(self):
        super().__init__()

    def __call__(self, inventory_file, playbook):
        print(f"ansible-playbook -i {inventory_file} {playbook}")
        os.system(f"ansible-playbook -i {inventory_file} {playbook} -v")


CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
PLAYBOOK_TEMPLATE = os.path.join(CURRENT_FOLDER, "playbook", "playbook_template.yaml")
RESET_PLAYBOOK_TEMPLATE = os.path.join(
    CURRENT_FOLDER, "playbook", "reset_docker_swarm_playbook.yaml"
)
INIT_CLUSTER_PLAYBOOK_TEMPLATE = os.path.join(
    CURRENT_FOLDER, "playbook", "init_docker_swarm_playbook.yaml"
)
DOCKER_STACK_TEMPLATE = os.path.join(CURRENT_FOLDER, "service", "stack_template.yaml")
START_SERVICE_PLAYBOOK = os.path.join(
    CURRENT_FOLDER, "playbook", "start_service_playbook.yaml"
)


def generate_playbook(template_path: str, command: str):
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"错误：模板文件 {template_path} 不存在")
        return

    # 执行参数替换
    modified_content = template.replace("{musa_develop_command}", command)

    # 生成输出文件名
    temp_dir = tempfile.gettempdir()  # 返回系统标准临时目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"generated_playbook_{timestamp}.yml"
    output_path = os.path.join(temp_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(modified_content)
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(
        prog="musa-develop-ansible",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
        description="",
    )
    parser.add_argument(
        "--hostfile",
        type=Path,
        help="输入文件路径，格式：IP 用户名 密码\n"
        "示例：\n"
        "192.168.5.150 ggn 000000\n"
        "192.168.5.149 ggn 000000",
    )
    parser.add_argument(
        "--init-cluster",
        dest="init_cluster",
        action="store_true",
        default=False,
        help="init cluster according to hostfile",
    )
    parser.add_argument(
        "--reset-cluster",
        dest="reset_cluster",
        action="store_true",
        default=False,
        help="clear cluster configuration",
    )
    parser.add_argument(
        "--generate-stack-yaml",
        dest="generate_stack_yaml",
        action="store_true",
        default=False,
        help="cp stack yaml to /tmp",
    )

    parser.add_argument(
        "--task",
        dest="task",
        type=str,
        help="specify model name",
    )
    return parser.parse_known_args()


def main():
    args, unknown_args = parse_args()
    if args.hostfile:
        if not args.hostfile.exists():
            print(f"输入文件不存在: {args.hostfile}")
        try:
            generator = InventoryGenerator()
            inventory_path = generator.generate_temp_inventory(args.hostfile)
        except Exception as e:
            print(f"[错误] {str(e)}")
            return 1

    ansible = AnsibleExecutor()
    if args.reset_cluster:
        ansible(inventory_path, RESET_PLAYBOOK_TEMPLATE)
        return 0
    if args.generate_stack_yaml:
        os.system(f"cp {DOCKER_STACK_TEMPLATE} /tmp")

    if args.init_cluster:
        # setup base musa env in cluster
        # 0. get full command
        # musa_develop_args = " ".join(sys.argv[1:])
        # full_command = "musa-develop " + musa_develop_args + " --auto-install"
        full_command = "musa-develop --demo vllm-musa --auto-install"
        # 1. generate playbook
        playbook_file = generate_playbook(PLAYBOOK_TEMPLATE, full_command)
        # 2. ansible-playbook
        ansible(inventory_path, playbook_file)

        # init docker swarm cluster
        ansible(inventory_path, INIT_CLUSTER_PLAYBOOK_TEMPLATE)
        return 0

    if args.task:
        ansible(inventory_path, START_SERVICE_PLAYBOOK)


if __name__ == "__main__":
    main()
