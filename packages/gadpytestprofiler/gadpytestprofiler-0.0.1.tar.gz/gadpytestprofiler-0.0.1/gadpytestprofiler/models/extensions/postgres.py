import pydantic


class Explain(pydantic.BaseModel):
    class Plan(pydantic.BaseModel):
        class Buffer(pydantic.BaseModel):
            hit: int | None = pydantic.Field(None, alias="Shared Hit Blocks")
            read: int | None = pydantic.Field(None, alias="Shared Read Blocks")
            write: int | None = pydantic.Field(None, alias="Shared Written Blocks")

        type: str = pydantic.Field(..., alias="Node Type")
        name: str | None = pydantic.Field(None, alias="Relation Name")
        alias: str | None = pydantic.Field(None, alias="Alias")
        startup: float | None = pydantic.Field(None, alias="Startup Cost")
        total: float | None = pydantic.Field(None, alias="Total Cost")

        plan_rows: int | None = pydantic.Field(None, alias="Plan Rows")
        plan_width: int | None = pydantic.Field(None, alias="Plan Width")

        actual_rows: int | None = pydantic.Field(None, alias="Actual Rows")
        actual_loops: int | None = pydantic.Field(None, alias="Actual Loops")
        actual_startup_time: float | None = pydantic.Field(None, alias="Actual Startup Time")
        actual_total_time: float | None = pydantic.Field(None, alias="Actual Total Time")

        buffers: Buffer | None = pydantic.Field(None, alias="Buffers")
        plans: list["Plan"] = pydantic.Field(default_factory=list, alias="Plans")

        filter: str | None = pydantic.Field(None, alias="Filter")
        index: str | None = pydantic.Field(None, alias="Index Cond")
        join: str | None = pydantic.Field(None, alias="Join Type")

        class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True

    plan: Plan = pydantic.Field(..., alias="Plan")
    planning: float | None = pydantic.Field(None, alias="Planning Time")
    execution: float | None = pydantic.Field(None, alias="Execution Time")

    class Config:
        allow_population_by_field_name = True
