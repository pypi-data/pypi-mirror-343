# from .server import serve
from utils.my_util import test_util
from .__about__ import __version__


def main():
    """Main entry point for the hatch_test package."""
    print(f"Hatch Test Package v{__version__}")
    test_util()
    # serve()


# if __name__ == "__main__":
#     main()
