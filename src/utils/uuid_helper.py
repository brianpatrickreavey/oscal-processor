import uuid
from threading import Lock

class UUIDRegistry:
    """
    Helper for registering and generating unique UUIDs for OSCAL elements.
    """
    def __init__(self):
        self._uuids = set()
        self._lock = Lock()

    def register_uuid(self, uuid_str):
        """Register an existing UUID (from imported data)."""
        with self._lock:
            self._uuids.add(uuid_str)

    def register_uuids(self, uuid_list):
        """Bulk register a list of UUIDs."""
        with self._lock:
            self._uuids.update(uuid_list)

    def generate_uuid(self):
        """Generate a new UUID, ensuring it is unique among registered UUIDs."""
        while True:
            new_uuid = str(uuid.uuid4())
            with self._lock:
                if new_uuid not in self._uuids:
                    self._uuids.add(new_uuid)
                    return new_uuid

    def all_uuids(self):
        """Return a copy of all registered UUIDs."""
        with self._lock:
            return set(self._uuids)

# Singleton instance for convenience
uuid_registry = UUIDRegistry()
