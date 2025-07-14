import os

if "tests" in os.getcwd():
    os.chdir("..")
    __import__("sys").path.append("../src")

if __name__ == "__main__":
    __import__("sys").path.append("./src")
    import weatherquery as wq

    wq.debug()
