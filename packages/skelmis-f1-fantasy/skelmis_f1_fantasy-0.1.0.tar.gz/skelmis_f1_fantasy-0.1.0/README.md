F1 Fantasy API Client
---

A mildy janky implementation letting you browser the F1 fantasy data set. Certain values are guaranteed to be wrong and methods missing due to a lack of public methods. This is a best guess implementation, and I'd love any feedback.


### Basic Usage

- Navigate to https://fantasy.formula1.com
- Open dev tools for your browser (typically F12)
- Click `Network`
- Login
- Look for a request to `/services/session/login`
- Click `Response`
- Copy the value of `GUID` and `Token`.
- See below example.

```python
import asyncio

from skelmis import fantasy


async def main():
    client = fantasy.Client(
        user_guid="GUID HERE",
        token="TOKEN HERE"
    )
    race_id = await client.get_current_race_id()
    data = await client.get_my_teams(race_id)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
```