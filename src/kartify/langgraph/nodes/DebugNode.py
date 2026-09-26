import os


def _debug_logging_enabled() -> bool:
    return os.getenv("DEBUG_LOGGERS_ENABLED", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

def debug_node(name, fn):
    def wrapper(state):
        debug_enabled = _debug_logging_enabled()
   
        print(f"\n===== RUNNING NODE: {name} =====")

        result = fn(state)
        if debug_enabled:
            print(f"STATE AFTER {name}:")
            for key, value in result.items():
                print(f"  {key}: {value}")
            print("================================\n")

        return result

    return wrapper