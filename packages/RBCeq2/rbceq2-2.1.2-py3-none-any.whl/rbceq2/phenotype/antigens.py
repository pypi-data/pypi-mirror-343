from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable

#from icecream import ic


@dataclass(slots=True, frozen=False)
class Antigen(ABC):
    """Abstract base class representing an antigen.

    Attributes:
        given_name (str): The original name provided for the antigen.
        expressed (bool): Indicates whether the antigen is expressed.
        homozygous (bool): Indicates whether the antigen is homozygous.
        antithetical_relationships (dict[str, str]): Relationships mapping the base name
            to a string of antithetical antigen names.
        antithetical_antigen (list[Antigen] | None): A list of antithetical antigen objects,
            initialized in __post_init__.
        base_name (str): The processed base name of the antigen, initialized in __post_init__.
        weak (bool): Flag indicating whether the antigen is weak, determined in __post_init__.
        weight (int): A numerical weight used for ranking antigens, set in __post_init__.
    """
    given_name: str
    expressed: bool  # can freeze if not for this...
    homozygous: bool
    antithetical_antigen: list[Antigen] | None = field(init=False)
    base_name: str = field(init=False)
    weak: bool = field(init=False)
    weight: int = field(init=False)
    antithetical_relationships: dict[str, str]

    def __post_init__(self) -> None:
        """Perform post-initialization tasks.

        This method is automatically called after the object is initialized.
        """
        object.__setattr__(self, "base_name", self._get_base_name())
        object.__setattr__(self, "weak", self._is_weak())
        object.__setattr__(self, "weight", self._set_weight())
        object.__setattr__(self, "antithetical_antigen", self._get_antithetical())

    @abstractmethod
    def _is_weak(self):
        """Determine whether the antigen is considered weak.

        Returns:
            bool: True if the antigen is weak, False otherwise.
        """
        pass

    @abstractmethod
    def _get_base_name(self):
        """Extract the base name of the antigen from its given name.

        Returns:
            str: The base name of the antigen.
        """
        pass

    @abstractmethod
    def _set_weight(self):
        """Determine the weight of the antigen based on its properties.

        Returns:
            int: The weight assigned to the antigen.
        """
        pass

    @abstractmethod
    def name(self):
        """Generate or retrieve the formatted antigen name.

        Returns:
            str: The formatted name of the antigen.
        """
        pass

    def _get_antithetical(self) -> list[Antigen] | None:
        """Retrieve antithetical antigens based on the antigen's relationships.

        Uses the antithetical_relationships dictionary to determine if any
        antithetical antigens exist for the current antigen's base name.

        Returns:
            list[Antigen] | None: A list of antithetical Antigen objects if available,
            otherwise None.
        """
        if self.antithetical_relationships is not None:
            names = self.antithetical_relationships.get(self.base_name)
            if names is not None:
                return [
                    type(self)(
                        given_name=name,
                        expressed="-" not in name,
                        homozygous=False,
                        antithetical_relationships={},
                    )
                    for name in names
                ]
        return None

    def _rank(self, other: Antigen, operator_func: Callable[[int, int], bool]) -> bool:
        """Compare the weight of this antigen with another antigen using a given operator.

        Args:
            other (Antigen): Another antigen to compare with.
            operator_func (Callable[[int, int], bool]): A function that compares two
                integers (e.g., operator.gt or operator.lt).

        Returns:
            bool: The result of applying operator_func to the weights of self and other.
        """
        return operator_func(self.weight, other.weight)

    def __gt__(self, other: Antigen) -> bool:
        """Check if this antigen is greater than another antigen based on weight.

        Args:
            other (Antigen): Another antigen to compare.

        Returns:
            bool: True if this antigen's weight is greater than the other antigen's weight,
            False otherwise.
        """
        return self._rank(other, operator.gt)

    def __lt__(self, other: Antigen) -> bool:
        """Check if this antigen is less than another antigen based on weight.

        Args:
            other (Antigen): Another antigen to compare.

        Returns:
            bool: True if this antigen's weight is less than the other antigen's weight,
            False otherwise.
        """
        return self._rank(other, operator.lt)

    def __eq__(self, other: Antigen) -> bool:
        """Check if two antigens are equal based on their weight.

        Args:
            other (Antigen): Another antigen to compare.

        Returns:
            bool: True if the weights of both antigens are equal, False otherwise.
        """
        return self.weight == other.weight

    def __repr__(self) -> str:
        """Generate a string representation of the antigen.

        The representation excludes the antithetical_relationships attribute and includes
        the antigen's type, given name, antithetical antigen (base names), base name, weak flag,
        homozygous flag, expressed flag, and weight.

        Returns:
            str: A formatted string representation of the antigen.
        """
        anti_ant = (
            [ant.base_name for ant in self.antithetical_antigen]
            if self.antithetical_antigen is not None
            else None
        )
        return (
            "\n"
            f"Antigen(type={type(self)!r}, \n"
            f"Antigen(name={self.given_name!r}, \n"
            f"antithetical_antigen={anti_ant!r}, \n"
            f"base_name={self.base_name!r}, \n"
            f"weak={self.weak!r}, \n"
            f"homozygous={self.homozygous!r}, \n"
            f"expressed={self.expressed!r}, \n"
            f"weight={self.weight!r})"
        )



class NumericAntigen(Antigen):
    """A concrete Antigen subclass representing numeric antigens."""
    def _is_weak(self):
        """Determine if the NumericAntigen is weak based on its given name.

        Returns:
            bool: True if 'w' or 'weak' is found in the given name, False otherwise.
        """
        return "w" in self.given_name or "weak" in self.given_name

    def _get_base_name(self):
        """Extract the base name from the given name by removing certain characters.

        Characters removed include '-', '+', and 'w'.

        Returns:
            str: The base name of the NumericAntigen.
        """
        translation_table = str.maketrans("", "", "-+w")
        return self.given_name.translate(translation_table)  # .replace("var", "")

    def _set_weight(self):
        """Set the weight of the NumericAntigen based on its given name.

        Returns:
            int: The weight of the antigen. A lower number indicates a stronger antigen.
                 Returns 1 if the antigen is strong, 2 if it is weak, and 3 if it has a '-'
                 modifier.
        """
        if (
            "w" not in self.given_name
            and "weak" not in self.given_name
            and "-" not in self.given_name
        ):
            return 1
        elif "w" in self.given_name or "weak" in self.given_name:
            return 2
        elif "-" in self.given_name:
            return 3
  
    @property
    def name(self):
        """Generate the name for the NumericAntigen.

        If the antigen is weak, append a 'w' to the base name. If the antigen is not
        expressed, prepend a '-' to the base name.

        Returns:
            str: The formatted name of the NumericAntigen.
        """
        name = self.base_name if not self.weak else f"{self.base_name}w"

        return name if self.expressed else f"-{name}"


class AlphaNumericAntigen(Antigen):
    """A concrete Antigen subclass representing alphanumeric antigens."""

    def _is_weak(self):
        """Determine if the AlphaNumericAntigen is weak based on its given name.

        Returns:
            bool: True if '+w' or 'weak' is present in the given name, False otherwise.
        """
        return "+w" in self.given_name or "weak" in self.given_name

    def _get_base_name(self):
        """Extract the base name from the given name by removing specific characters.

        Characters removed include '-', '+', and 'w'. Additionally, the substring 'var'
        is removed.

        Returns:
            str: The base name of the AlphaNumericAntigen.
        """
        translation_table = str.maketrans("", "", "-+w")
        return self.given_name.translate(translation_table).replace("var", "")

    def _set_weight(self):
        """Set the weight of the AlphaNumericAntigen based on its given name.

        Returns:
            int: The weight assigned to the antigen. Returns 1 if strong, 2 if weak, and 3
            if a '-' modifier is present.
        """
        if (
            "+w" not in self.given_name
            and "weak" not in self.given_name
            and "-" not in self.given_name
        ):
            return 1
        elif "+w" in self.given_name or "weak" in self.given_name:
            return 2
        elif "-" in self.given_name:
            return 3
  
    @property
    def name(self) -> str:
        """Generate the name for the AlphaNumericAntigen.

        For special cases containing substrings like 'common', 'partial', 'altered', or
        'var', the given name is returned directly. Otherwise, a suffix is generated
        based on whether the antigen is weak and/or expressed.

        Returns:
            str: The formatted name of the AlphaNumericAntigen.
        """
        if any(
            special_case in self.given_name.lower()
            for special_case in ["common", "partial", "altered", "var"]
        ):
            return self.given_name

        def generate_name(suffix: str) -> str:
            """Helper function to generate the name with a given suffix.

            Args:
                suffix (str): The suffix to append or replace in the base name.

            Returns:
                str: The formatted allele name.
            """
            return (
                f"{self.base_name}{suffix}"
                if "(" not in self.given_name
                else self.base_name.replace(")", f"{suffix})")
            )

        # Determine the suffix based on the allele's state
        if self.weak:
            name_expressed = generate_name("+w")
            name_not_expressed = generate_name("-")
        else:
            name_expressed = generate_name("+")
            name_not_expressed = generate_name("-")

        # Return the appropriate name based on whether the allele is expressed
        return name_expressed if self.expressed else name_not_expressed


class AlphaNumericAntigenABO(AlphaNumericAntigen):
    """An AlphaNumericAntigen subclass for ABO blood group antigens."""

    @property
    def name(self):
        """Return the name for the AlphaNumericAntigenABO.

        For ABO antigens, the given name is returned directly without modification.

        Returns:
            str: The original given name.
        """
        return self.given_name

    def _get_base_name(self):
        """Determine the base name for an ABO antigen based on the given name.

        The base name is determined by checking the starting character(s) of the
        given name. It must start with 'A', 'B', 'CIS', or 'O'. If none match, a
        ValueError is raised.

        Returns:
            str: The base name for the ABO antigen.

        Raises:
            ValueError: If the given name does not start with a recognized ABO type.
        """
        if self.given_name.upper().startswith("A"):
            return "A"
        elif self.given_name.upper().startswith("B"):
            return "B"
        elif self.given_name.upper().startswith("CIS"):
            return "cis"
        elif self.given_name.upper().startswith("O"):
            return "O"
        else:
            raise ValueError(f"ABO given name wrong: {self.given_name}")


class AlphaNumericAntigenXG(AlphaNumericAntigen):
    """An AlphaNumericAntigen subclass for XG blood group antigens."""
    @property
    def name(self):
        """Generate the name for the AlphaNumericAntigenXG.

        Returns:
            str: The given name with parentheses and plus signs removed, with 'CD99'
            appended.
        """
        return (
            self.given_name.replace("(", "").replace(")", "").replace("+", "") + "CD99"
        )



class AlphaNumericAntigenMNS(AlphaNumericAntigen):
    """An AlphaNumericAntigen subclass for MNS blood group antigens."""
    def _get_base_name(self):
        """Extract the base name for the AlphaNumericAntigenMNS by removing specific
        characters and substrings.

        Characters removed include '-', '+', and 'w'. Additionally, substrings like
        'partial', 'alteredGPB', 'alteredU/GPB', and 'var' are removed. The result is
        then stripped of leading and trailing whitespace.

        Returns:
            str: The base name for the MNS antigen.
        """
        translation_table = str.maketrans("", "", "-+w")
        return (
            self.given_name.translate(translation_table)
            .replace("partial", "")
            .replace("alteredGPB", "")
            .replace("alteredU/GPB", "")
            .replace("var", "")
            .strip()
        )


class AlphaNumericAntigenVel(AlphaNumericAntigen):
    """An AlphaNumericAntigen subclass for Vel blood group antigens."""
    def _get_base_name(self):
        """Extract the base name for the AlphaNumericAntigenVel by removing specific
        characters and substrings.

        Characters removed include '-', '+', and 'w'. Additionally, substrings like 'var',
        'strong', and 'STRONG' are removed.

        Returns:
            str: The base name for the Vel antigen.
        """
        translation_table = str.maketrans("", "", "-+w")
        return (
            self.given_name.translate(translation_table)
            .replace("var", "")
            .replace("strong", "")
            .replace("STRONG", "")
        )

    def _set_weight(self):
        """Set the weight for the AlphaNumericAntigenVel based on its given name.

        For Vel antigens, if 'STRONG' is present in the given name (case-insensitive),
        the weight is set to 1. Otherwise, the weight is determined by the presence of
        '+w', 'weak', or '-' modifiers.

        Returns:
            int: The weight assigned to the Vel antigen.
        """
        if "STRONG" in self.given_name.upper():
            return 1
        elif (
            "+w" not in self.given_name
            and "weak" not in self.given_name
            and "-" not in self.given_name
        ):
            return 2
        elif "+w" in self.given_name or "weak" in self.given_name:
            return 3
        elif "-" in self.given_name:
            return 4
        

    @property
    def name(self):
        """Return the name for the AlphaNumericAntigenVel.

        For Vel antigens, the given name is returned directly without modification.

        Returns:
            str: The original given name.
        """
        return self.given_name
