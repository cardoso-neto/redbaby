from typing import Optional

from bson.objectid import ObjectId as BsonObjectId


def get_root_dir(path: str) -> Optional[str]:
    """
    Get the root folder name from a path-like string.

    >>> get_root_dir("/foo/bar/baz")
    "foo"
    """
    without_surrounding_slashes = path.strip("/")
    breadcrumbs = without_surrounding_slashes.split("/")
    root_folder = breadcrumbs[0]
    if not root_folder:
        return None
    return root_folder


class PyObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (cls, BsonObjectId, str)) or not BsonObjectId.is_valid(v):
            raise TypeError("Invalid ObjectId.")
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            type="string",
            examples=["5eb7cf5a86d9755df3a6c593", "5eb7cfb05e32e07750a1756a"],
        )


def parse_sort(sort: str) -> list[tuple[str, int]]:
    """

    >>> parse_sort("-date,-count,+app")
    [("date", -1), ("count", -1), ("app", 1)]
    """
    return [
        (field_order[1:], -1 if field_order[0] == "-" else 1)
        for field_order in sort.split(",")
    ]
