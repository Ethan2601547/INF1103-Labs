#supplier class

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if supplier_id.strip() == "" or name.strip() == "":
            raise ValueError("Supplier ID and name cannot be empty.")
        if "@" not in contact_email:
            raise ValueError("Contact email must contain '@'.")
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    @property
    def supplier_id(self) -> str: return self.__supplier_id
    @property
    def name(self) -> str: return self.__name
    @property
    def contact_email(self) -> str: return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Email: {self.__contact_email}")