# pyre-strict
from libcst.codemod import CodemodTest
from libcst.codemod.commands.strip_strings_from_types import StripStringsCommand


class TestStripStringsCodemod(CodemodTest):

    TRANSFORM = StripStringsCommand

    def test_noop(self) -> None:
        before = """
            foo: str = ""

            class Class:
                pass

            def foo(a: Class, **kwargs: str) -> Class:
                t: Class = Class()  # This is a comment
                bar = ""
                return t
        """
        after = """
            foo: str = ""

            class Class:
                pass

            def foo(a: Class, **kwargs: str) -> Class:
                t: Class = Class()  # This is a comment
                bar = ""
                return t
        """

        self.assertCodemod(before, after)

    def test_non_async(self) -> None:
        before = """
            class Class:
                pass

            def foo(a: "Class", **kwargs: "str") -> "Class":
                t: "Class" = Class()  # This is a comment
                return t
        """
        after = """
            from __future__ import annotations

            class Class:
                pass

            def foo(a: Class, **kwargs: str) -> Class:
                t: Class = Class()  # This is a comment
                return t
        """

        self.assertCodemod(before, after)

    def test_async(self) -> None:
        before = """
            class Class:
                pass

            async def foo(a: "Class", **kwargs: "str") -> "Class":
                t: "Class" = Class()  # This is a comment
                return t
        """
        after = """
            from __future__ import annotations

            class Class:
                pass

            async def foo(a: Class, **kwargs: str) -> Class:
                t: Class = Class()  # This is a comment
                return t
        """

        self.assertCodemod(before, after)

    def test_recursive(self) -> None:
        before = """
            class Class:
                pass

            def foo(a: List["Class"]):
                pass

            def bar(a: List[Optional["Class"]]):
                pass

            def baz(a: "List[Class]"):
                pass
        """
        after = """
            from __future__ import annotations

            class Class:
                pass

            def foo(a: List[Class]):
                pass

            def bar(a: List[Optional[Class]]):
                pass

            def baz(a: List[Class]):
                pass
        """

        self.assertCodemod(before, after)

    def test_literal(self) -> None:
        before = """
            from typing_extensions import Literal

            class Class:
                pass

            def foo(a: Literal["one", "two", "three"]):
                pass

            def bar(a: Union["Class", Literal["one", "two", "three"]]):
                pass
        """
        after = """
            from __future__ import annotations
            from typing_extensions import Literal

            class Class:
                pass

            def foo(a: Literal["one", "two", "three"]):
                pass

            def bar(a: Union[Class, Literal["one", "two", "three"]]):
                pass
        """

        self.assertCodemod(before, after)
