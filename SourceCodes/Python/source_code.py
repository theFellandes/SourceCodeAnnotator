import json
import pprint
from time import sleep
from tqdm import tqdm
from urllib.request import urlopen


class Main:
    """Main class for testing source code run."""

    def main(self):
        """The main function of the main class"""
        customers = self.generate_customers()
        self.iterate_customers(customers)

        print("Project Info:")
        # pretty prints the project_info
        project_info = self.get_sample_project_json()
        pprint.pprint(project_info)

    @staticmethod
    def generate_customers() -> dict[str:int]:
        """
        Returns the list of customers

        :returns Dictionary of customers dict[str:int]
        """
        return {"Ali": 1, "Veli": 2, "Mahmut": 3}

    @staticmethod
    def iterate_customers(customers: dict[str:int]):
        """
        Iterates the customers dictionary

        :parameter customers: The dictionary of customers
        """
        for customer_name, customer_id in tqdm(customers.items()):
            sleep(3)
            # Performs some tasks

    @staticmethod
    def get_sample_project_json() -> str:
        """
        Returns the sample project json

        :returns project_info: The sampleproject json info
        """
        with urlopen("https://pypi.org/pypi/sampleproject/json") as resp:
            project_info = json.load(resp)["info"]
        return project_info


if __name__ == "__main__":
    main = Main()
    main.main()
