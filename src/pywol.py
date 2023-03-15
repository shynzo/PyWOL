from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from wakeonlan import send_magic_packet
from re import fullmatch

import scanner
import json

parser = ArgumentParser(
    description="Wake On Lan through network automatic!",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-l",
    "--load",
    help="load the list of clients from a json file",
    type=str,
    default="clients.json",
)
parser.add_argument(
    "-s",
    "--scan",
    help="scan the network for clients",
    action="store_true",
)
parser.add_argument(
    "-w", "--wake", help="wake up a single client inserting their MAC Address", type=str
)
parser.add_argument(
    "-wl", "--wakelist", help="wake up all clients on the list", action="store_true"
)
args = parser.parse_args()


def load_from_file(file: str = "clients.json") -> dict:
    """Load the list of clients from a json file.

    Args:
        file (str, optional): File to read. Defaults to "clients.json".

    Returns:
        dict: Return all clients of the file.
    """

    with open(file, "r") as f:
        clients: dict = json.load(f)
    return clients


def main():
    """
    Main function of the program.
    """
    clients: dict = {}
    if args.scan:  # If the user want to scan the network
        clients = scanner.scan()  # Scan the network
        print(clients)  # Show the clients
        return

    if args.wake:  # If the user want to wake up a single client
        # Verify if mac address is correct
        match = fullmatch(
            "^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){"
            "5}|([-][a-f0-9]{2}){5}|([s][a-f0-9]{2}){5}))$",
            args.wake,
        )
        if not match:  # If the mac address is not correct
            print("Invalid MAC Address")
            return
        send_magic_packet(args.wake)  # Wake up the client
        return

    if args.wakelist:  # If the user want to wake up all clients on the list
        if args.load:  # If the user want to load the clients from a file
            clients = load_from_file(args.load)  # Load the clients from a file
        for client in clients:  # For each client on the list
            send_magic_packet(client["mac"])  # Wake up the client
        return


if __name__ == "__main__":
    main()
