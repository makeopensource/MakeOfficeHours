"""Database functions relating to courses"""

from abc import ABC, abstractmethod


class ICourses(ABC):
    """Class containing database methods for course management"""

    @abstractmethod
    def create_course(self, name, semester, url) -> int:
        """Create a new course with the specified information

        :param name: name of the course, e.g. "CSE 116: Intro to Computer Science II"
        :param semester: identifier of this specified offering, e.g. "f26"
        :param url: unique url for this course, e.g. "cse116-f26"
        :return: the generated course_id for this course
        """
        raise NotImplementedError()

    @abstractmethod
    def get_course(self, identifier) -> dict[str, str]:
        """
        Retrieve database info for the specified course.

        :param identifier: the course id or url to look up
        :return: database info for this course
        """
        raise NotImplementedError()

    @abstractmethod
    def get_courses(self) -> list[dict[str, str]]:
        """
        Retrieve database info for all courses

        :return: All courses in the form of dicts
        """
        raise NotImplementedError()
