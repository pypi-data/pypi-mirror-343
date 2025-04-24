class MissingDependencyError(Exception):
    """Exception raised when a required dependency is missing."""

    def __init__(self, package_name: str):
        self.package_name = package_name
        super().__init__(f"Missing required dependency: {package_name}. \n Please install it using 'pip install"
                         f" {package_name}' or 'pip 'install swc_utils[extras]'.")
