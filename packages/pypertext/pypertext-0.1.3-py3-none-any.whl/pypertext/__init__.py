"""
Pypertext - Create HTML elements in a Pythonic way.

```python
from pypertext import ht, Element

# Create a div element with a class and an id
div = ht.div(id="my-div", classes=["container", "content"], style={"color": "red"})
div + ht.h1("Hello World") + ht.p("This is a paragraph.")
```

Changes
-------
0.1.3 - Added the setup_logging function to configure logging.
0.1.2 - Replaced dict-based elements to class-based elements with the Element class.
"""

import os
import re
import io
import sys
import types
import codecs
import inspect
import logging
import datetime
import contextlib
import typing as t
from abc import ABCMeta
from numbers import Number as _Number

log = logging.getLogger(__name__)

__version__ = "0.1.3"
__license__ = "Apache License 2.0"

# fmt: off
SELF_CLOSING_TAGS = set(["meta", "link", "img", "br", "hr", "input", "area", "base", "col", "embed", "command", 
    "keygen", "param", "source", "track", "wbr", "menuitem", "basefont", "bgsound", "frame", "isindex", "nextid",
    "spacer", "acronym", "applet", "big", "blink", "center", "content", "dir", "element",
    "font", "frameset", "image", "listing", "marquee", "multicol", "nobr",
])
# fmt: on


def _is_function(x: object) -> bool:
    """Return True if x is a function or method."""
    return (
        isinstance(x, (types.FunctionType, types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType))
        or inspect.ismethod(x)
        or inspect.isfunction(x)
    )


def _listify(obj: t.Any) -> t.List[t.Any]:
    """Convert an object to a list."""
    if obj is None:
        return []
    if isinstance(obj, (list, tuple, dict, set)):
        return obj
    return [obj]


def _stringify(value: t.Any, sep: str = " ") -> str:
    """Turn a value or list of values into a string."""
    if isinstance(value, list):
        return sep.join(str(v) for v in _flatten(value))
    return str(value)


def _flatten(lst: t.List[t.Any]) -> t.List[t.Any]:
    """_Flatten a list of lists."""
    if lst is None:
        return []
    if isinstance(lst, str):
        return [lst]
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(_flatten(item))
        else:
            if item is not None:
                result.append(item)
    return result


def _merge_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        for k, v in d.items():
            if k in result:  # found pre-existing key
                if isinstance(v, dict):
                    result[k] = _merge_dicts(result[k], v)
                else:
                    # new value is a list so convert the existing value to a list if it isn't already
                    if not isinstance(result[k], list):
                        result[k] = _listify(result[k])
                    # then extend the list with the new value
                    result[k].extend(_listify(v))
            else:
                result[k] = v
    return result


def _classes_ensure_list(classes: t.Union[str, t.Callable, t.List[str]]) -> t.List[str]:
    """Users can pass a string or a list of strings to the classes attribute. This function ensures that the classes
    attribute is always a list of strings."""
    if _is_function(classes):
        classes = classes()
    if isinstance(classes, str):
        return classes.split()
    return classes


class Element(metaclass=ABCMeta):
    """
    Base class for all elements.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.tag: str = "div"
        """The tag name of the element."""
        self.children = []
        """List of children elements."""
        self.attributes = {}
        """Dictionary of attributes."""
        # Add children
        if args:
            self.__add__(args)
        # Add attributes
        if kwargs:
            if "classes" in kwargs:
                classes = kwargs.pop("classes")
                self.attributes["classes"] = _classes_ensure_list(classes)
            self.attributes.update(kwargs)

    def __add__(self, other) -> "Element":
        """Add children or attributes to the element using the + operator."""
        if isinstance(other, dict):
            self.set_attrs(**other)
            return self
        other = _listify(other)
        num_t = (_Number, datetime.date, datetime.datetime, datetime.timedelta)
        for obj in other:
            # None
            if obj is None:
                continue
            # Number, Date, Datetime, timedelta
            if isinstance(obj, num_t):
                obj = str(obj)
            # String
            if isinstance(obj, str):
                self.children.append(obj)
            # bytes
            elif isinstance(obj, bytes):
                self.children.append(obj.decode("utf-8"))
            # Dict and TypeDict are treated as attributes
            # note: t.is_typeddict(obj) is available in Python 3.10+
            elif isinstance(obj, dict) or t.is_typeddict(obj):
                self.set_attrs(**obj)
            # Pydantic model
            elif hasattr(obj, "model_dump"):
                self.set_attrs(**obj.model_dump())
            # Element
            elif isinstance(obj, Element):
                self.children.append(obj)
            # Renderable as an element-like object, e.g. Element, str, etc. This
            # is usually a class with a get_element method
            elif hasattr(obj, "get_element"):
                self.children.append(obj)
            # Rich display: https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display
            elif hasattr(obj, "_repr_html_"):
                self.children.append(obj._repr_html_())
            # Iterable
            elif hasattr(obj, "__iter__"):
                for subobj in obj:
                    self + subobj
            # Function or method
            elif _is_function(obj):
                # function is evaluated when rendered
                self.children.append(obj)
            # Unknown
            else:
                log.debug(
                    "%r not an `Element` or string (type %s). Coercing to string." % (obj, type(obj)),
                )
                try:
                    # try to coerce to string
                    self.children.append(str(obj))
                except Exception:
                    raise TypeError(
                        f"Failed to add type {type(obj)} as a child. "
                        "Only `Element`, str, and iterables of these are allowed."
                    )
        return self

    def __iadd__(self, other):
        """
        Add children to this element with += operator. Returns the left element.

        Args:
            other: The children to add to the element. Can be a string, number, list, tuple, dict, Element,
                or any class that defines a get_element method.

        Example:
            Add children to an element using the += operator.

            ```python
            form = ht.form()
            form += ht.input(type="text", name="name")
            form += ht.button(type="submit")
            ```
        """
        self.__add__(other)
        return self

    def set_attrs(self, **kwargs) -> "Element":
        """
        Set attributes for the element. If there are duplicate keys, use the last value. `classes` key is merged into
        a single classes list.

        Args:
            **kwargs: Attributes to set for the element.
        """
        if "classes" in kwargs:
            classes = kwargs.pop("classes")
            self.add_classes(classes)
        self.attributes.update(kwargs)
        return self

    def merge_attrs(self, **kwargs) -> "Element":
        """
        Merge attributes with the existing attributes. If there are duplicate keys, combine them into a list.

        Args:
            **kwargs: Attributes to merge with the existing attributes.

        Example:
            Merge attributes with an element.

            ```python
            ht.div(classes=["container"]).merge_attrs(id="my-div", classes=["content"])
            ```
        """
        if "classes" in kwargs:
            classes = kwargs.pop("classes")
            self.add_classes(classes)
        self.attributes = _merge_dicts(self.attributes, kwargs)
        return self

    def has_classes(self, *classes: str) -> bool:
        """
        Check if the element has all of the given classes.

        Args:
            *classes (str): The classes to check for.

        Returns:
            bool: True if the element has all of the given classes, False otherwise.
        """
        classes = self.attributes.get("classes", [])
        if _is_function(classes):
            classes = classes()
        classes = _flatten(classes)
        classes = map(str, classes)
        return all(str(c) in classes for c in classes)

    def add_classes(self, *classes: str) -> "Element":
        """
        Add classes to the element.

        Args:
            *classes (str): The classes to add to the element.

        Returns:
            Element: The element with the added classes.

        Example:
            Add classes to an element.

            ```python
            ht.div().add_classes("container", "row")
            ```
        """
        current_classes = self.attributes.get("classes", [])
        current_classes = _classes_ensure_list(current_classes)
        new_classes = current_classes + list(classes)
        new_classes = list(set(_flatten(new_classes)))
        self.attributes["classes"] = new_classes
        return self

    def remove_classes(self, *classes: str) -> "Element":
        """
        Remove classes from the element.

        Args:
            *classes (str): The classes to remove from the element.

        Returns:
            Element: The element with the removed classes.

        Example:
            Remove classes from an element.

            ```python
            ht.div().remove_classes("container", "row")
            ```
        """
        current_classes = self.attributes.get("classes", [])
        current_classes = _classes_ensure_list(current_classes)
        for c in classes:
            try:
                current_classes.remove(c)
            except ValueError:
                pass
        self.attributes["classes"] = list(set(_flatten(current_classes)))
        return self

    def __call__(self, *args, **kwargs) -> "Element":
        """
        Add children or attributes to the element.

        Args:
            *args: Children elements.
            **kwargs: Attributes.

        Returns:
            Element: The element with the added children and attributes.

        Example:
            Add children and attributes to an element.

            ```python
            ht.div("Hello")("World", style="color: red;")
            ```
        """
        self + args
        self.set_attrs(**kwargs)
        return self

    def append(self, *args):
        """
        Add children to the element.

        Args:
            *args: Children elements.

        Returns:
            Element: The element with the added children.

        Example:
            Add children to an element.

            ```python
            ht.div().append("Hello world")
            ```
        """
        self + args
        return self

    def extend(self, *args):
        """
        Add children to the element.

        Args:
            *args: Children elements.

        Returns:
            Element: The element with the added children.

        Example:
            Add children to an element.

            ```python
            ht.div().extend("Hello", "world")
            ```
        """
        for arg in args:
            self + arg

    def insert(self, index: int, *args):
        """
        Insert children at the given index.

        Args:
            index (int): The index at which to insert the
            *args: Children elements.

        Returns:
            Element: The element with the inserted children

        Example:
            Insert children at a specific index.

            ```python
            ht.div("World").insert(0, "Hello")
            ```
        """
        self.children.insert(index, *args)
        return self

    def to_string(self) -> str:
        """
        Return the HTML element as a string.

        Returns:
            (str): The HTML element as a string.

        Example:
            Convert an element to a string.

            ```python
            ht.div("Hello world").to_string()
            # '<div>Hello world</div>'
            ```
        """
        return ht.render_element(self)

    def pipe(self, function: t.Callable, *args, **kwargs):
        """
        A structured way to apply a sequence of user-defined functions.

        Args:
            function (Callable): The function to apply to the element.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            The result of the function.

        Example:
            Apply a function to an element.

            ```python
            def add_classes(element, prefix: str):
                elment.add_classes(f"{prefix}-class")
                return element

            ht.div("Hello world").pipe(add_classes, "my-prefix")
            ```
        """
        return function(self, *args, **kwargs)

    def __str__(self) -> str:
        """
        Return the HTML element as a string.

        Returns:
            (str): The HTML element as a string.
        """
        return self.to_string()

    def _repr_html_(self) -> str:
        """
        Return the HTML element as a string for Jupyter notebooks.
        https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display
        """
        return self.to_string()


class _MetaTagType(type):
    def __getattr__(self, __name: str) -> Element:
        """Return a new instance of ht with the given tag name."""
        el = Element()
        el.tag = __name
        return el


class ht(metaclass=_MetaTagType):
    """
    HTML factory class.

    This class is used to create HTML elements in a Pythonic way. It is a factory class that returns an Element, so you
    can call it with the tag name and any attributes or children you want to add to the element and it will return an
    Element instance.

    Example:
        Generate HTML elements using the ht class:

        ```python
        ht.div(id="my-div", classes=["container", "content"], style={"color": "red"})
        ht.button(type="submit", classes=["btn", "btn-primary"])
        ht.h1("Hello World")
        ```
    """

    def __call__(self, tag, *args: t.Any, **kwds: t.Any) -> Element:
        el = Element(*args, **kwds)
        el.tag = tag
        return el

    @classmethod
    def render_element(cls, element: t.Union[Element, str, None]) -> str:
        """
        Return the HTML element as a string.
        """
        if _is_function(element):
            element = element()

        # In the event that the returned value is a function, method, or coroutine
        # then recursively call ht.render_element until we get a string
        if _is_function(element):
            element = ht.render_element(element)

        # `get_element` is a special method that can be implemented by classes and
        # should return an Element
        if hasattr(element, "get_element"):
            if _is_function(element.get_element):
                element = element.get_element()

        if element is None:
            return ""

        if isinstance(element, (str, _Number, bool)):
            return str(element)

        if not isinstance(element, Element):
            raise TypeError(
                f"element must be an instance of `Element` or str or have a `get_element` method that returns an instance of `Element`, got type {type(element)}: {element}"
            )

        tag: str = element.tag
        attrs: t.Mapping = element.attributes
        children: t.List = element.children

        # replace underscores with dashes in tag name
        tag = tag.replace("_", "-")
        # parse attributes
        _attrs: t.List[t.Any] = []
        attrs_str: str = ""

        if attrs is not None:
            for k, v in attrs.items():
                if k == "classes":
                    klass = [attrs.get("classes", [])]
                    if _is_function(klass[0]):
                        klass[0] = klass[0]()
                    if len(klass) > 0:
                        v = " ".join(list(set(_flatten(klass))))
                        if len(v) > 0:
                            _attrs.append(f'class="{v}"')
                    continue
                if k == "for_":
                    k = "for"
                # prop keys with underscores are converted to dashes
                k = k.replace("_", "-")
                # evaluate values that are callable functions
                if _is_function(v):
                    try:
                        v = v()
                    except Exception:
                        log.error("Error evaluating function: %r" % v, exc_info=True)
                # style attribute with dict value should be converted to string
                # e.g. {"color": "red"} -> "color: red;"
                if k == "style" and isinstance(v, dict):
                    v = "; ".join([f"{k}: {_stringify(v)}" for k, v in v.items()])
                if isinstance(v, bool):
                    # boolean value only adds the key if True
                    if v:
                        _attrs.append(k)
                else:
                    if v is None:
                        # None value is skipped
                        continue
                    if isinstance(v, (list, tuple)):
                        # list or tuple values are converted to space-separated strings
                        v = _stringify(v)
                    # all other value types converted to string
                    if not isinstance(v, str):
                        v = str(v)
                    # handle the case where value contains double quotes by using
                    # single quotes
                    if '"' in v:
                        _attrs.append(f"{k}='{v}'")
                    else:
                        _attrs.append(f'{k}="{v}"')
            attrs_str = " ".join(_attrs)
        # if attrs is not empty, prepend a space
        if len(attrs_str) > 0:
            attrs_str = " " + attrs_str
        if tag in SELF_CLOSING_TAGS:
            # self-closing tags have no children
            return f"<{tag}{attrs_str}/>"
        else:
            # process non-self-closing tags
            innerHTML: str = ""
            if children is None:
                innerHTML = ""
            elif isinstance(children, (str, _Number, bool)):
                innerHTML = str(children)
            elif isinstance(children, Element):  # ht class instance
                try:
                    innerHTML = ht.render_element(children)
                except Exception:
                    log.error("Error rendering element: %r" % children, exc_info=True)
            elif hasattr(children, "get_element"):
                # Any class instance with a get_element method
                innerHTML = children.get_element()
            elif _is_function(children):
                # evaluate function and render the result
                try:
                    result = children()
                except Exception:
                    log.error("Error evaluating function: %r" % children, exc_info=True)
                innerHTML += str(result)
            elif isinstance(children, (list, tuple)):
                for child in children:
                    innerHTML += ht.render_element(child)
            return f"<{tag}{attrs_str}>{innerHTML}</{tag}>"

    @classmethod
    def render_document(
        cls,
        body: Element,
        head: t.List[Element] = None,
        title: str = None,
        body_kwargs: dict = None,
        head_kwargs: dict = None,
        html_kwargs: dict = None,
    ) -> str:
        """
        Render a full HTML document.

        Args:
            body (Element): Document body.
            head (list[Element]): A list of elements to include in the head tag.
            title (str): Document title.
            body_kwargs (dict): Body tag attributes.
            head_kwargs (dict): Head tag attributes.
            html_kwargs (dict): HTML tag attributes.

        Returns:
            The HTML document as a string.

        Example:
            Render an HTML document.

            ```python
            ht.render_document(ht.div("Hello world"))
            # <!DOCTYPE html><html><head>...</head><body><div>Hello world</div></body></html>
            ```
        """
        if not isinstance(body, (Element, str)):
            if not hasattr(body, "get_element"):
                raise TypeError(
                    "body must be an instance of `Element` or str or have a `get_element` method that returns an `Element` element"
                )

        head = head or []
        body_kwargs = body_kwargs or {}
        head_kwargs = head_kwargs or {}
        html_kwargs = html_kwargs or {}

        if not isinstance(head, list):
            raise TypeError("head must be a list of `Element` elements")

        _head = [
            ht.meta(charset="utf-8"),
            ht.meta(name="viewport", content="width=device-width, initial-scale=1"),
            ht.meta(http_equiv="X-UA-Compatible", content="IE=edge"),
        ]
        _head.extend(head)
        if title is not None:
            _head.append(ht.title(title))
        html = [
            "<!DOCTYPE html>",
            ht.render_element(
                ht.html(
                    ht.head(_head, **head_kwargs),
                    ht.body(body, **body_kwargs),
                    **html_kwargs,
                )
            ),
        ]
        return "".join(html)


def dict2css(style: t.Mapping[str, t.Mapping[str, str]]) -> str:
    """
    Convert a dict to a CSS string.

    Args:
        style (Mapping[str, Mapping[str, str]]): A dict of dicts, where the keys of the outer dict are the CSS selectors
            and the keys of the inner dicts are the CSS properties.

    Returns:
        str: The CSS string.

    Example:
        Convert a dict to a CSS string:

        ```python
        dict2css({"body": {"background-color": "red", "color": "white"}})
        # 'body{background-color: red;color: white;}'

        dict2css({"body": "background-color: red;"})
        # 'body{background-color: red;}'

        dict2css({"@media (max-width: 600px)": dict2css({"body": "background-color: red;"})})
        # nested media query
        ```
    """
    _style = ""
    for selector, properties in style.items():
        if isinstance(properties, str):
            _style += f"{selector}{{{properties}}}"
            continue
        _style += f"{selector}{{"
        for prop, value in properties.items():
            if value.endswith("}"):
                _style += f"{prop}:{value}"
            else:
                _style += f"{prop}:{value};"
        _style += "}"
    return _style


class Document(Element):
    """
    HTML document that can be used as an ASGI application.

    This class is a subclass of Element and can be used to create an HTML document. It can also be used to return an
    HTML response in an ASGI application.

    Attributes:
        page_title (str): The title of the page.
        headers (dict): Response headers.
        status_code (int): Response status code.
        title (Element): The title element.
        head (Element): The head element.
        body (Element): The body element.
        html (Element): The html element.
    """

    def __init__(
        self,
        *args,
        page_title: str = None,
        headers: dict = None,
        status_code: int = 200,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.page_title: str = page_title
        self.headers: dict = headers
        """Response headers."""
        self.status_code: int = status_code
        """Response status code."""
        self.title = ht.title()
        """Document title."""
        self.head: Element = ht.head(
            ht.meta(charset="utf-8"),
            ht.meta(name="viewport", content="width=device-width, initial-scale=1"),
            ht.meta(http_equiv="X-UA-Compatible", content="IE=edge"),
            self.title,
        )
        """The head element."""
        self.body = ht.body()
        """The body element."""
        self.html = ht.html(self.head, self.body)
        """The html element."""

    def get_element(self) -> Element:
        """
        Return the document as an Element, starting with the `<html>` tag.

        Returns:
            Element: The document as an Element.
        """
        self.title.children = [self.page_title]
        self.body.children = self.children
        self.body.attributes = self.attributes
        return self.html

    def to_string(self) -> str:
        """Return the HTML document as a string."""
        doc = super().to_string()
        return "<!DOCTYPE html>" + doc

    async def __call__(self, scope, receive, send):
        """
        ASGI application interface using Starlette.
        """
        try:
            from starlette.responses import HTMLResponse  # noqa: F401
        except ImportError:
            raise ImportError("starlette is not installed. Please install it with `pip install starlette`.")

        assert scope["type"] == "http"

        response = HTMLResponse(self.to_string(), headers=self.headers, status_code=self.status_code)
        await response(scope, receive, send)


def config(key: str, cast: t.Callable = None, default: t.Any = None) -> t.Any:
    """
    Get a configuration value from environment variables.

    Args:
        key (str): Environment variable name.
        cast (Callable): Type to cast the value to.
        default (Any): Default value if the environment variable is not found.

    Example:

        Read an environment variable:

        ```python
        from pypertext import config

        DEBUG = config("DEBUG", cast=bool, default=False)
        ```
    """
    if key in os.environ:
        value = os.environ[key]
        if cast is None or value is None:
            return value
        elif cast is bool and isinstance(value, str):
            mapping = {"true": True, "1": True, "false": False, "0": False}
            value = value.lower()
            if value not in mapping:
                raise ValueError(f"Config '{key}' has value '{value}'. Not a valid bool.")
            return mapping[value]
        try:
            return cast(value)
        except (TypeError, ValueError):
            raise ValueError(f"Config '{key}' has value '{value}'. Not a valid {cast.__name__}.")

    try:
        return cast(default)
    except (TypeError, ValueError):
        return default


def _walk_to_root(path: str) -> t.Iterator[str]:
    """
    Yield directories starting from the given directory up to the root
    """
    if not os.path.exists(path):
        raise IOError("Starting path not found")

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_dotenv(filename: str = ".env", raise_error_if_not_found: bool = False, usecwd: bool = False) -> str:
    """
    Search in increasingly higher folders for the given file. Returns path to the file if found, or an empty
    string otherwise.

    Args:
        filename (str): The name of the file to search for. Defaults to ".env".
        raise_error_if_not_found (bool): If True, raises an IOError if the file is not found. Defaults to False.
        usecwd (bool): If True, uses the current working directory as the starting point for the search. Defaults to False.

    Returns:
        str: The path to the file if found, or an empty string if not found.
    """

    def _is_interactive():
        """Decide whether this is running in a REPL or IPython notebook"""
        try:
            main = __import__("__main__", None, None, fromlist=["__file__"])
        except ModuleNotFoundError:
            return False
        return not hasattr(main, "__file__")

    if usecwd or _is_interactive() or getattr(sys, "frozen", False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path = os.getcwd()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_back is not None and (
            frame.f_code.co_filename == current_file or not os.path.exists(frame.f_code.co_filename)
        ):
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError("File not found")

    return ""


def load_dotenv(dotenv_path: str = None, override: bool = True, encoding: str = "utf-8") -> None:
    """
    Load environment variables from a .env file into os.environ.

    Args:
        dotenv_path (str): Path to the .env file. If not provided, will default to searching for .env in the current
            directory and all parent directories.
        override (bool): Whether to override existing environment variables.
        encoding (str): The encoding of the .env file. Defaults to 'utf-8'.

    Example:
        Load environment variables from a .env file:

        ```python
        from pypertext import load_dotenv

        load_dotenv()  # Load from the default .env file in the current directory
        load_dotenv("config.env")  # Load from a specific file
        ```
    """
    if dotenv_path is None:
        dotenv_path = find_dotenv()

    envvars = {}

    _whitespace = re.compile(r"[^\S\r\n]*", flags=re.UNICODE)
    _export = re.compile(r"(?:export[^\S\r\n]+)?", flags=re.UNICODE)
    _single_quoted_key = re.compile(r"'([^']+)'", flags=re.UNICODE)
    _unquoted_key = re.compile(r"([^=\#\s]+)", flags=re.UNICODE)
    _single_quoted_value = re.compile(r"'((?:\\'|[^'])*)'", flags=re.UNICODE)
    _double_quoted_value = re.compile(r'"((?:\\"|[^"])*)"', flags=re.UNICODE)
    _unquoted_value = re.compile(r"([^\r\n]*)", flags=re.UNICODE)
    _double_quote_escapes = re.compile(r"\\[\\'\"abfnrtv]", flags=re.UNICODE)
    _single_quote_escapes = re.compile(r"\\[\\']", flags=re.UNICODE)

    @contextlib.contextmanager
    def _get_stream() -> t.Iterator[t.IO[str]]:
        if dotenv_path and os.path.isfile(dotenv_path):
            with open(dotenv_path, encoding=encoding) as stream:
                yield stream
        else:
            yield io.StringIO("")

    _double_quote_map = {
        r"\\": "\\",
        r"\'": "'",
        r"\"": '"',
        r"\a": "\a",
        r"\b": "\b",
        r"\f": "\f",
        r"\n": "\n",
        r"\r": "\r",
        r"\t": "\t",
        r"\v": "\v",
    }

    def _double_quote_escape(m: t.Match[str]) -> str:
        return _double_quote_map[m.group()]

    nexport = len("export ")
    with _get_stream() as stream:
        for line in stream:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[nexport:]
            key, value = line.split("=", 1)
            key = key.strip()
            key = _single_quoted_key.sub(r"\1", key)
            key = _unquoted_key.sub(r"\1", key)
            key = _whitespace.sub("", key)
            key = _export.sub("", key)
            key = key.strip()
            if not key:
                continue

            if _single_quoted_value.match(value):
                value = _single_quoted_value.sub(r"\1", value)
                value = _single_quote_escapes.sub(r"\1", value)
            elif _double_quoted_value.match(value):
                value = _double_quoted_value.sub(r"\1", value)
                value = codecs.decode(value.encode("utf-8"), "unicode_escape")
            elif _unquoted_value.match(value):
                value = _unquoted_value.sub(r"\1", value)
                value = _double_quote_escapes.sub(_double_quote_escape, value)
                value = _whitespace.sub("", value)
            else:
                raise ValueError(f"Line {line} does not match format KEY=VALUE")
            envvars[key] = value

    for k, v in envvars.items():
        if k in os.environ and not override:
            continue
        if v is not None:
            os.environ[k] = v


def setup_logging(level: int = None, file: str = None, disable_stdout: bool = False):
    """Setup logging.

    Args:
        level (int, optional): The logging level. Defaults to logging.INFO.
        file (str, optional): The path to the log file. Defaults to None.
        disable_stdout (bool, optional): Whether to disable stdout logging. Defaults to False.
    
    Example:

        Setup logging to a file and disable stdout logging:

        ```python
        import logging
        from pypertext import setup_logging

        setup_logging(level=logging.DEBUG)
        setup_logging(file="logs/app.log", disable_stdout=True)
        setup_logging(level="DEBUG", file="logs/app.log", disable_stdout=True)
        ```
    """
    if level is None:
        level = logging.INFO
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    if file is None and disable_stdout:
        return
    handlers = []
    if not disable_stdout:
        handlers.append(logging.StreamHandler())
    if file is not None:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        handlers.append(logging.FileHandler(file))
    logging.basicConfig(
        level=level,
        format="%(asctime)s|%(levelname)s|%(name)s|%(message)s",
        handlers=handlers,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
