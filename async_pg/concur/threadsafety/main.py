import threading

import config_util


def do_something():
    port = config_util.get("port")
    print(port)


def main():
    config_util.load_config("config.yml")
    port = config_util.get("port")
    print(port)

    t = threading.Thread(target=do_something, daemon=True)
    t.start()
    t.join()
    
    port = config_util.get("port")
    print(port)


if __name__ == "__main__":
    main()
