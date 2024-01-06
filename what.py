overlay: str|None = "scsent"

match overlay:
    case "scent":
        print("scent")
    case None:
        print("none")