def convert_congestion(congestion: str):
    return (
        0
        if congestion.lower() == "lower"
        else (1 if congestion.lower() == "medium" else 2)
    )
