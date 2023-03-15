import subprocess
import json
from re import fullmatch


def save_to_file(clients_list: dict, file: str = "clients.json") -> bool:
    """Save the list of clients to a json file.

    Args:
        clients_list (dict): List of clients.
        file (str, optional): File name or path to save file. Defaults to 'clients.json'.

    Returns:
        bool: Return True if the file is saved correctly, False otherwise.
    """

    try:
        with open(file, "w") as f:
            json.dump(clients_list, f, indent=4)  # Save the clients to a file
        return True
    except:
        return False


def scan() -> dict:
    """Scan the network for clients.

    Returns:
        dict: Return all MAC Address clients found.
    """

    result = subprocess.run(
        ["arp", "-a"], capture_output=True
    )  # Search all clients using arp command on Windows
    result = result.stdout.decode("utf-8", errors="ignore")  # Decode the result
    result = result.replace("\r", "")  # Remove \r from the result
    result = result.split("\n")  # Split the result by \n
    result.remove("")  # Remove empty elements
    clients: dict = {}  # Create a dictionary for clients
    for line in result:
        if line:
            line = line.split(" ")  # Split the line by spaces
            line = [x for x in line if x]  # Remove empty elements
            # regex for ip address
            _ip = fullmatch(
                "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                line[0],
            )
            # regex for mac address
            _mac = fullmatch(
                "^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){"
                "5}|([-][a-f0-9]{2}){5}|([s][a-f0-9]{2}){5}))$",
                line[1],
            )
            if not _ip or not _mac:  # If the line is not an ip address or a mac address
                continue  # Skip the line
            clients[line[0]] = line[1]  # Add the client to the dictionary
    saved = save_to_file(clients)  # Save the clients to a file
    if not saved:
        print(
            "Error while saving the list of clients. Check the permissions of the file or the path."
        )
    return clients  # Return the clients
