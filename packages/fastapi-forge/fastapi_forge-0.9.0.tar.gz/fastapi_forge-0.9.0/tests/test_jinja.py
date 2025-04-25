import pytest

from fastapi_forge.dtos import Model, ModelField
from fastapi_forge.enums import FieldDataTypeEnum
from fastapi_forge.jinja import render_model_to_model, render_model_to_post_test


def _clip_imports(rendered_str: str, split_str: str) -> str:
    return split_str + rendered_str.split(split_str)[1]


def test_render_model() -> None:
    model = Model(
        name="model",
        fields=[
            ModelField(
                name="id",
                type=FieldDataTypeEnum.UUID,
                primary_key=True,
                unique=True,
            ),
            ModelField(
                name="updated_at",
                type=FieldDataTypeEnum.DATETIME,
                default_value="datetime.now(timezone.utc)",
                extra_kwargs={
                    "onupdate": "datetime.now(timezone.utc)",
                },
            ),
        ],
    )

    render = _clip_imports(render_model_to_model(model), "class")
    str_field = """
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    """

    assert str_field in render


@pytest.mark.parametrize(
    "noun, expected",
    [
        ("tooth", "teeth"),
        ("teeth", "teeth"),
        ("person", "people"),
        ("people", "people"),
        ("game_zone", "game-zones"),
        ("user", "users"),
        ("auth_user", "auth-users"),
        ("hardware_setup", "hardware-setups"),
    ],
)
def test_render_post_test(noun: str, expected: str) -> None:
    model = Model(
        name=noun,
        fields=[
            ModelField(
                name="id",
                type=FieldDataTypeEnum.UUID,
                primary_key=True,
                unique=True,
            ),
        ],
    )

    render = render_model_to_post_test(model)
    assert f'URI = "/api/v1/{expected}/"' in render
