from typing import Any, Optional
from taipy import Gui
from taipy.gui.state import State
import pandas as pd


def read_raw(raw_data_path: str) -> pd.DataFrame:
    return pd.read_csv(raw_data_path)

def prepare_base(raw_df: pd.DataFrame) -> pd.DataFrame:
    base_df = raw_df[["URL", "Stars"]]

    base_df["Owner"] = base_df["URL"].str.extract(r"https:\/\/github.com\/(.+)\/.+", expand=True)
    base_df["FullName"] = base_df["URL"].str.replace("https://github.com/", "")
    
    return base_df

raw_df = read_raw("./data/repositories.csv")
base_df = prepare_base(raw_df)

top10_repositories_df = base_df.sort_values(by=["Stars"], ascending=False).head(10)
top10_owners_df = base_df.groupby(["Owner"]) \
    .sum() \
    .reset_index() \
    .sort_values(by=["Stars"], ascending=False) \
    .head(10)
owners = top10_owners_df["Owner"].sort_values(key=lambda owner: owner.str.lower()).unique().tolist()

selected_owner: Optional[str] = None

def on_repository_owner_change(state: State, var_name: str, value: Any) -> None:
    new_base_df = state.base_df[state.base_df["Owner"] == value]
    state.top10_repositories_df = new_base_df.sort_values(by=["Stars"], ascending=False).head(10)

def on_change(state, var, val) -> None:
    print(f"Value changed: {state} - {var} - {val}")

page = """
# Top GitHub Repositories

<|Filters|expandable|

Repository Owner
<|{selected_owner}|selector|lov={owners}|dropdown|on_change=on_repository_owner_change|>

|>


<|Overview|expandable|
<|layout

<|
## Top 10 Owners
<|{top10_owners_df}|chart|type=bar|x=Owner|y=Stars|on_change=on_change|>
|>

<|
## Top 10 Respositories
<|{top10_repositories_df}|chart|type=bar|x=FullName|y=Stars|>
|>

|>
|>
"""

if __name__ == "__main__":
    Gui(page).run(debug=True, use_reloader=True)