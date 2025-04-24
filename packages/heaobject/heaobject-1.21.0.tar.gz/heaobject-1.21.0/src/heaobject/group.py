"""
Defines the following reserved groups for desktop objects, for use in the group attribute of its shares and invites:

NONE_GROUP: 'system|none' -- for objects that have no particular group-level permissions.
TEST_GROUP: 'system|test' -- for use in testing HEA.

Furthermore, all groups beginning with 'system|' are reserved for system use.
"""

NONE_GROUP = 'system|none'
TEST_GROUP = 'system|test'


def is_system_group(id_: str) -> bool:
    """
    Returns whether the given string is a system group or not.

    :param id_: The string to check.
    :return: True or False.
    """
    return id_ in (NONE_GROUP, TEST_GROUP)
