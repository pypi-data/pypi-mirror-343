"""Module for raw at-time-of-loading validation of config files

The purpose of this module is mostly to facilitate loading of a stricter subset
of Gold configuration, as defined by the models in the `refined` sibling module.

Since Grevling allows many parts of the input to be callables, validation of
their outputs must necessarily be delayed.
"""


from __future__ import annotations

from functools import partial

from typing import Any, List, Dict, Optional, Union, Literal, Callable, Tuple, Type
from typing_extensions import Self

from pydantic import BaseModel, Field

from .. import util, api
from ..render import render
from . import refined


# Numbers can usually be either ints or floats. Note that Pydantic will coerce
# floats to ints or vice-versa depending on which type is listed first in this
# union. To prevent this, models which make use of scalars should use the
# `smart_unions` config option.
Scalar = Union[int, float]

Constant = Union[
    str,
    None,
    Scalar,
    bool,
]


class RegexCaptureSchema(BaseModel):
    """A capture pattern defined using regular expressions."""

    capture_type: Literal["regex"] = "regex"
    pattern: str
    mode: Literal["first", "last", "all"] = "last"
    multiline: bool = False

    @staticmethod
    def from_str(pattern: str) -> RegexCaptureSchema:
        """Grevling allows captures to be defined as pure strings, in which case
        they are interpreted as regular expressions. Use this constructor to
        convert a string to a *RegexCaptureSchema*.
        """
        return RegexCaptureSchema(pattern=pattern)


class SimpleCaptureSchema(BaseModel):
    """'Simple' captures are easier to configure than regular expressions,
    which are easy to get wrong. They support only a subset of features, and are
    compiled to a regex when used.
    """

    capture_type: Literal["simple"] = "simple"
    kind: Literal["integer", "float"] = Field(alias="type")
    name: str
    prefix: str
    skip_words: int = 0
    flexible_prefix: bool = False
    mode: Literal["first", "last", "all"] = "last"


# Captures should conform to this type when written in the config file
CaptureSchema = Union[
    str,
    SimpleCaptureSchema,
    RegexCaptureSchema,
    List[
        Union[
            str,
            SimpleCaptureSchema,
            RegexCaptureSchema,
        ]
    ],
]


class FileMapBaseSchema(BaseModel):
    """Superclass for all filemap schemas (normal pre and post, as well as
    templates). The only difference is whether the *template* attribute defaults
    to true or not. Recommended usage today is to just use prefiles and
    postfiles, and to explicitly mark which files are templates. Thus, the
    splitting of the two classes here is just to facilitate legacy configs.
    """

    source: str
    target: Optional[str] = None
    mode: Literal["simple", "glob"] = "simple"
    template: bool

    @classmethod
    def from_any(cls: Type[Self], source: Union[str, Dict]) -> Self:
        """Convert an object with 'any' type to a filemap schema. Most
        importantly, convert strings by interpreting them as source
        filenames.
        """
        if isinstance(source, str):
            return cls.model_validate({"source": source})
        return cls.model_validate(source)

    def refine(self) -> refined.FileMapSchema:
        return refined.FileMapSchema.model_validate(self.model_dump())

    def render(self, context: api.Context) -> Self:
        """Perform template substitution in the *source* and *target*
        attributes.
        """
        return self.model_copy(
            update={
                "source": render(self.source, context),
                "target": render(self.target, context) if self.target else None,
            }
        )


class TemplateSchema(FileMapBaseSchema):
    template: Literal[True] = True


class FileMapSchema(FileMapBaseSchema):
    template: bool = False


class CommandSchema(BaseModel):
    """Model schema for commands: anything that can be an element of the
    'script' list in a Grevling config file. This represents any command
    that can be run as part of a Grevling case.
    """

    command: Optional[Union[str, List[str]]] = None
    name: Optional[str] = None
    capture: CaptureSchema = []
    capture_output: bool = True
    capture_walltime: bool = True
    retry_on_fail: bool = False
    env: Dict[str, str] = {}
    container: Optional[str] = None
    container_args: Union[str, List[str]] = []
    allow_failure: bool = False
    workdir: Optional[str] = None

    @staticmethod
    def from_any(source: Union[str, List[str], CommandSchema, Dict]) -> CommandSchema:
        """Convert an object with 'any' type to a CommandSchema. Most
        importantly, this interprets raw strings and lists of strings as
        commands with only the *command* attribute set.
        """
        if isinstance(source, CommandSchema):
            return source
        if isinstance(source, Dict):
            return CommandSchema.model_validate(source)
        return CommandSchema.model_validate({"command": source})

    def render(self, context: api.Context):
        """Perform template substitution in the attributes that require it."""

        # If commands are provided as strings instead of lists, templates must
        # be rendered in shell mode for proper quoting.
        cmd_render_mode = "shell" if isinstance(self.command, str) else None
        cargs_render_mode = "shell" if isinstance(self.container_args, str) else None

        return self.model_copy(
            update={
                "command": render(self.command, context, mode=cmd_render_mode),
                "container_args": render(self.container_args, context, mode=cargs_render_mode),
                "workdir": render(self.workdir, context),
                "env": render(self.env, context),
            }
        )

    def refine_capture(self) -> List[Dict]:
        """Convert the *capture* attribute so that it can be loaded by the
        refined models.
        """

        # Convert to list if not already a list
        raw_captures = self.capture if isinstance(self.capture, list) else [self.capture]

        # Strings should be interpreted as regex capture patterns
        return [
            RegexCaptureSchema.from_str(pattern).model_dump()
            if isinstance(pattern, str)
            else pattern.model_dump()
            for pattern in raw_captures
        ]

    def refine(self) -> refined.CommandSchema:
        return refined.CommandSchema.model_validate(
            {
                **self.model_dump(),
                "capture": self.refine_capture(),
            }
        )


class UniformParameterSchema(BaseModel):
    """Model for uniformly sampled parameters"""

    kind: Literal["uniform"] = Field(alias="type")
    interval: Tuple[Scalar, Scalar]
    num: int

    def refine(self) -> refined.UniformParameterSchema:
        return refined.UniformParameterSchema.model_validate(self.model_dump())


class GradedParameterSchema(BaseModel):
    """Model for geometrically sampled parameters (parameter spaces that are
    denser on one side than another).
    """

    kind: Literal["graded"] = Field(alias="type")
    interval: Tuple[Scalar, Scalar]
    num: int
    grading: Scalar

    def refine(self) -> refined.GradedParameterSchema:
        return refined.GradedParameterSchema.model_validate(self.model_dump())


# Parameter specifications in the config file should conform to this type
ParameterSchema = Union[
    List[Scalar],
    List[str],
    UniformParameterSchema,
    GradedParameterSchema,
]


class PlotCategorySchema(BaseModel):
    """Model for specifying that a parameter should behave as a category in
    plots.
    """

    mode: Literal["category"]
    argument: Optional[Literal["color", "line", "marker"]] = Field(alias="style", default=None)


class PlotIgnoreSchema(BaseModel):
    """Model for specifying that a parameter should be ignored in plots."""

    mode: Literal["ignore"]
    argument: Optional[Union[Scalar, str]] = Field(alias="value", default=None)


# Parameter plot modes in the config file should conform to this type
PlotModeSchema = Union[
    Literal["fixed", "variate", "category", "ignore", "mean"],
    PlotCategorySchema,
    PlotIgnoreSchema,
]


class PlotStyleSchema(BaseModel):
    """Model for specifying plot styles (lists of colors, lines and marker
    options.)
    """

    color: Optional[Union[str, List[str]]] = None
    line: Optional[Union[str, List[str]]] = None
    marker: Optional[Union[str, List[str]]] = None

    def refine(self) -> refined.PlotStyleSchema:
        def fix(x):
            return [x] if isinstance(x, str) else x

        return refined.PlotStyleSchema.model_validate(
            {
                "color": fix(self.color),
                "line": fix(self.line),
                "marker": fix(self.marker),
            }
        )


class PlotSchema(BaseModel):
    """Model for specifying a plot."""

    filename: str
    fmt: Union[str, List[str]] = Field(alias="format")
    xaxis: Optional[str] = None
    yaxis: Union[str, List[str]] = Field(alias="yaxis")
    ylim: Optional[Tuple[Scalar, Scalar]] = None
    xlim: Optional[Tuple[Scalar, Scalar]] = None
    kind: Optional[Literal["scatter", "line"]] = Field(alias="type", default=None)
    legend: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    xmode: Literal["linear", "log"] = "linear"
    ymode: Literal["linear", "log"] = "linear"
    title: Optional[str] = None
    grid: bool = True
    parameters: Dict[str, PlotModeSchema] = {}
    style: PlotStyleSchema = PlotStyleSchema()

    def refine_fmt(self) -> List[str]:
        return self.fmt if isinstance(self.fmt, list) else [self.fmt]

    def refine_yaxis(self) -> List[str]:
        return self.yaxis if isinstance(self.yaxis, list) else [self.yaxis]

    def refine_parameters(self) -> Dict[str, Dict]:
        """Convert the *parameters* attribute so that it can be loaded by the
        refined models.
        """
        return {
            name: {"mode": value} if isinstance(value, str) else value.model_dump()
            for name, value in self.parameters.items()
        }

    def refine(self) -> refined.PlotSchema:
        return refined.PlotSchema.model_validate(
            {
                **self.model_dump(),
                "fmt": self.refine_fmt(),
                "yaxis": self.refine_yaxis(),
                "style": self.style.refine(),
                "parameters": self.refine_parameters(),
            }
        )


class SettingsSchema(BaseModel):
    """Model for specifying case settings."""

    storagedir: str = ".grevlingdata"
    logdir: Union[Callable, str] = "${g_index}"
    ignore_missing_files: bool = Field(alias="ignore-missing-files", default=False)

    def refine_logdir(self) -> Callable[[api.Context], str]:
        """Convert the *logdir* attribute to a callable so that it can be loaded
        by refined models.
        """
        logdir = self.logdir
        if isinstance(logdir, str):
            return lambda ctx: render(logdir, ctx)
        return lambda ctx: logdir(**ctx)

    def refine(self) -> refined.SettingsSchema:
        return refined.SettingsSchema.model_validate(
            {
                **self.model_dump(),
                "logdir": self.refine_logdir(),
            }
        )


ScriptSchema = Union[
    Callable,
    List[
        Union[
            str,
            List[str],
            CommandSchema,
        ]
    ],
]


class CaseSchema(BaseModel):
    """Root model for specifying a Grevling case."""

    parameters: Dict[str, ParameterSchema] = {}

    p_script: ScriptSchema = Field(alias="script", default=[])

    p_containers: Dict[str, Union[str, List[str]]] = Field(alias="containers", default={})
    p_evaluate: Union[Callable, Dict[str, str]] = Field(alias="evaluate", default={})
    constants: Dict[str, Constant] = {}
    p_where: Union[Callable, str, List[str]] = Field(alias="where", default=[])
    types: Dict[str, str] = {}

    p_templates: Union[Callable, List[Union[str, TemplateSchema]]] = Field(alias="templates", default=[])
    p_prefiles: Union[Callable, List[Union[str, FileMapSchema]]] = Field(alias="prefiles", default=[])
    p_postfiles: Union[Callable, List[Union[str, FileMapSchema]]] = Field(alias="postfiles", default=[])

    plots: List[PlotSchema] = []

    settings: SettingsSchema = SettingsSchema()

    def refine_parameters(self) -> Dict[str, Union[Dict, refined.ParameterSchema]]:
        """Convert the *parameters* attribute so that raw lists are converted to
        objects when refining.
        """
        parameters: dict[str, Union[dict, refined.ParameterSchema]] = {}
        for name, schema in self.parameters.items():
            if isinstance(schema, list):
                parameters[name] = {
                    "kind": "listed",
                    "values": schema,
                }
            else:
                parameters[name] = schema.refine()
        return parameters

    def refine_script(self) -> Callable[[api.Context], List[refined.CommandSchema]]:
        """Convert the *script* attribute to a callable so that it is accepted
        by the refined model.
        """
        p_script = self.p_script
        if isinstance(p_script, list):
            return lambda ctx: [CommandSchema.from_any(schema).render(ctx).refine() for schema in p_script]
        return lambda ctx: [CommandSchema.from_any(schema).refine() for schema in p_script(**ctx)]

    def refine_evaluate(self) -> Callable[[api.Context], Dict[str, Any]]:
        """Convert the *evaluate* attribute to a callable so that it is accepted
        by the refined model.
        """
        p_evaluate = self.p_evaluate
        if isinstance(p_evaluate, dict):
            return partial(util.evaluate, evaluables=p_evaluate)
        return lambda ctx: p_evaluate(**ctx)

    def refine_where(self) -> Callable[[api.Context], bool]:
        """Convert the *where* attribute to a callable so that it is accepted
        by the refined model."""
        p_where = self.p_where
        if isinstance(p_where, str):
            return partial(util.all_truthy, conditions=[p_where])
        if isinstance(p_where, list):
            return partial(util.all_truthy, conditions=p_where)
        return lambda ctx: p_where(**ctx)

    @staticmethod
    def refine_filemap(schemas, schema_converter):
        """Helper method for converting filemaps to refined models."""
        if isinstance(schemas, list):
            return lambda ctx: [schema_converter(schema).render(ctx).refine() for schema in schemas]
        return lambda ctx: [schema_converter(schema).refine() for schema in schemas(**ctx)]

    def templates_callable(self) -> Callable[[api.Context], List[FileMapSchema]]:
        """Convert the *templates* attribute to a callable."""
        return CaseSchema.refine_filemap(self.p_templates, lambda schema: TemplateSchema.from_any(schema))

    def prefiles_callable(self) -> Callable[[api.Context], List[FileMapSchema]]:
        """Convert the *prefiles* attribute to a callable."""
        return CaseSchema.refine_filemap(self.p_prefiles, lambda schema: FileMapSchema.from_any(schema))

    def refine_prefiles(self) -> Callable[[api.Context], List[FileMapSchema]]:
        """Combine the *templates* and *prefiles* attributes into a callable
        so that it's accepted by the refined model.
        """
        prefiles = self.prefiles_callable()
        templates = self.templates_callable()
        return lambda ctx: [*prefiles(ctx), *templates(ctx)]

    def refine_postfiles(self) -> Callable[[api.Context], List[FileMapSchema]]:
        """Convert the *postfiles* attribute to a callable so that it's accepted
        by the refined model.
        """
        return CaseSchema.refine_filemap(self.p_postfiles, lambda schema: FileMapSchema.from_any(schema))

    def refine_plots(self) -> List[refined.PlotSchema]:
        """Refine all the plots in the *plots* attribute."""
        return [plot.refine() for plot in self.plots]

    def refine(self) -> refined.CaseSchema:
        return refined.CaseSchema.model_validate(
            {
                **self.model_dump(),
                "parameters": self.refine_parameters(),
                "script": self.refine_script(),
                "evaluate": self.refine_evaluate(),
                "where": self.refine_where(),
                "prefiles": self.refine_prefiles(),
                "postfiles": self.refine_postfiles(),
                "settings": self.settings.refine(),
                "plots": self.refine_plots(),
            }
        )
