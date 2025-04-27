# test.py

from env_config import EnvConfig 

def main():
    env = EnvConfig(
        schema = {
            "TEST": str,
            "TEST2": int,
            "TEST3": float,
            "TEST4": bool,
            "TEST5": list,
            "TEST6": tuple,
            "TEST7": dict,
            "TEST8": set,
        },
        path = ".env"
    )

    print(env.get("TEST2"))




if __name__ == "__main__":
    main()

