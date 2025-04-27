import sys
import docker
from functools import partial


def search_sorter(search_term: str, container) -> int:
    try:
        return f"{container.id} {container.name}".index(search_term)
    except ValueError:
        return -1


def help() -> None:
    print("Usage:")
    print("aliased : docker-nuke <search-term>")
    print("python  : python -m docker-nuke <search-term>")

    print("\n\t<search-term>: partial or whole, name or id")

    print("\nArguments:")
    print("\t--all -a  | Nuke all containers")
    print("\t--help -h | Show this message")


def main() -> None:
    args = sys.argv[1::]

    if len(args) < 1 or "--help" in args or "-h" in args:
        help()
        return

    search_term = " ".join(args)
    client = docker.from_env()

    containers: list = client.containers.list()

    lock: list = []
    if search_term not in ["--all", "-a"]:
        search_key = partial(search_sorter, search_term)
        containers.sort(key=search_key, reverse=True)
        lock = [containers[0]]
    else:
        lock = containers
        print(lock)

    lock_str = "\n".join([f"\t - {l.id} {l.name}" for l in lock])

    print(f"Targets Locked:\n {lock_str}")
    try:
        user_input = input("Fire? (y/N) ")
    except KeyboardInterrupt:
        user_input = "n"

    if user_input.lower() != "y":
        print("X Cancelling launch sequence")
        return

    print("Launching")

    for cont in lock:
        print(f"Killing {cont.name}")
        cont.kill()

        print(f"Removing {cont.name}")
        cont.remove()

    print("All splash")

    # print(", ".join(list(map(lambda c: c.name, containers))))


if __name__ == "__main__":
    main()
