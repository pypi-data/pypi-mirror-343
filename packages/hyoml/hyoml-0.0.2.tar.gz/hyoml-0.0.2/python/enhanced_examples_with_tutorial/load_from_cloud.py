from python.interface.hyoml import Hyoml

def main():
    h = Hyoml()
    # Simulated cloud content
    cloud_content = """
    user: John Doe
    membership: premium
    """

    parsed = h.parse(cloud_content)
    print(parsed)

if __name__ == "__main__":
    main()
