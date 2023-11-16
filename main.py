from broker import Broker

if __name__ == "__main__":
    server = Broker("0.0.0.0", 1883)
    server.start()
