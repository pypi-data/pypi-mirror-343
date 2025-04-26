import typing as t


def construct_filtered_dict(
    func: t.Callable[[t.Any], bool] = bool,
    /,
    **kwargs: t.Any,
) -> dict[str, t.Any]:
    return {k: v for k, v in kwargs.items() if func(v)}
