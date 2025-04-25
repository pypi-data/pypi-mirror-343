import sys
from importlib import import_module
from itertools import chain
from pkgutil import iter_modules, walk_packages
from typing import List, Optional, Type

from lcmutils.typing import LCMType

SIDE_EFFECT_PACKAGES = {"antigravity", "lib2to3", "this", "unittest", "venv"}


class LCMTypeRegistry:
    """
    Registry of LCM types. Key-value pairs are stored as (fingerprint, class).
    """

    def __init__(self, *classes: tuple[LCMType]) -> None:
        self._registry: dict[bytes, LCMType] = {}

        for cls in classes:
            self.register(cls)

    def register(self, cls: LCMType) -> None:
        """
        Register an LCM type class.

        Args:
            cls (LCMType): LCM class to register.
        """
        self._registry[cls._get_packed_fingerprint()] = cls

    @property
    def types(self) -> list[LCMType]:
        """
        Get the list of registered LCM types.

        Returns:
            list[LCMType]: List of registered LCM types.
        """
        return list(self._registry.values())

    def clear(self) -> None:
        """
        Clear the registry.
        """
        self._registry.clear()

    def get(self, fingerprint: bytes) -> LCMType | None:
        """
        Get the LCM class associated with a fingerprint.

        Args:
            fingerprint (bytes): Fingerprint to look up.

        Returns:
            LCMType | None: LCM type class associated with the fingerprint, or None if no class is registered for the fingerprint.
        """
        return self._registry.get(fingerprint, None)

    def detect(self, data: bytes) -> Type[LCMType]:
        """
        Detect the LCM type class associated with LCM message data.

        Args:
            data (bytes): LCM message data.

        Returns:
            Type[LCMType]: LCM type class associated with the data.
        """
        fingerprint = data[:8]
        cls = self.get(fingerprint)
        return cls

    def decode(self, data: bytes) -> LCMType | None:
        """
        Decode data into an LCM type instance, if its class is registered.

        Args:
            data (bytes): LCM data to decode.

        Returns:
            LCMType | None: Decoded instance, or None if the class is not registered.
        """
        cls = self.detect(data)

        if cls is None:
            return None

        return cls.decode(data)

    def discover(self, module_name: str) -> None:
        """
        Discover LCM type classes in a Python package or module by name.

        Args:
            module_name (str): Package or module to discover.
        """
        module = import_module(module_name)

        # Add all LCM types from the module itself
        for name in dir(module):
            cls = getattr(module, name)
            if isinstance(cls, type) and issubclass(cls, LCMType):
                self.register(cls)

        # If it's a package, recursively process all submodules
        if hasattr(module, "__path__"):
            for _, submodule_name, _ in walk_packages(
                module.__path__, prefix=f"{module_name}."
            ):
                try:
                    submodule = import_module(submodule_name)
                    for name in dir(submodule):
                        cls = getattr(submodule, name)
                        if isinstance(cls, type) and issubclass(cls, LCMType):
                            self.register(cls)
                except ImportError:
                    # Skip modules that can't be imported, but don't fail the entire discovery
                    pass

    def discover_all(self, skip: Optional[List[str]] = None) -> None:
        """
        Discover all LCM types in all installed packages and modules.

        This function iterates through all installed packages and modules in sys.path, and attempts to discover LCM types in each one. It skips packages that are known to have side effects.
        """
        # Collect the set of packages to skip
        if skip is None:
            skip = SIDE_EFFECT_PACKAGES
        else:
            skip = set(skip).union(SIDE_EFFECT_PACKAGES)

        # Iterate through all installed packages and modules
        pkg_gen = chain(iter_modules(), iter_modules(sys.path))
        for pkg in pkg_gen:
            # Skip packages that are in the skip list or are private/internal
            if pkg.name.startswith("_") or pkg.name in SIDE_EFFECT_PACKAGES:
                continue

            # Try to discover LCM types in the package
            try:
                self.discover(pkg.name)
            except Exception:
                # Skip packages that fail for any reason
                pass


__all__ = ["LCMTypeRegistry"]
