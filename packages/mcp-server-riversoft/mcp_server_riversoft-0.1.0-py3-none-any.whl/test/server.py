# server.py
import httpx
from datetime import datetime
import pytz
from mcp.server.fastmcp import FastMCP
from pyowm import OWM

openweathermap_api: str = "59473883cd488f7d8fb9cca01660dcd8"
owm = OWM(api_key=openweathermap_api)
uvmgr = owm.uvindex_manager()

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)

def pretty_date(
    datetime_obj: int, offset: int = 8 * 60 * 60
):  # Default to UTC+8 (480 minutes)
    # If an offset is provided, create a timezone based on the offset (minutes)
    if offset:
        offset_timezone = pytz.FixedOffset(offset // 60)  # offset is in minutes
    else:
        offset_timezone = pytz.FixedOffset(8 * 60)  # Default to UTC+8

    # Convert the timestamp into the desired timezone
    date_with_offset = datetime.fromtimestamp(datetime_obj, tz=offset_timezone)

    # Return formatted date string with the offset included
    return date_with_offset.strftime(f"%Y-%m-%d %H:%M:%S UTC{offset//60//60:+03d}")

@mcp.tool()
async def owm_weather_forecast(city: str, country: str):
    """Offer weather forecasts based on city name and country code"""
    print(f"Task on {city}, {country}.")
    print(f"Started at {datetime.now()}")
    
    fore_weather = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={openweathermap_api}"
    headers = {"Content-Type": "application/json"}
    # forecast = requests.get(fore_weather, headers=headers)

    async with httpx.AsyncClient() as client:
        response = await client.get(fore_weather, headers=headers)
        raw = response.json()

        try:
            offset = raw["city"]["timezone"]
            result = (
                f'city: {raw["city"]["name"]}\n' + f'country: {raw["city"]["country"]}\n'
            )
            for timestamp in range(len(raw["list"])):
                result += (
                    f'time: {pretty_date(raw["list"][timestamp]["dt"], offset=offset)}\n'
                    + f'description: {raw["list"][timestamp]["weather"][0]["description"]}\n'
                    + f'temperature range: {round(raw["list"][timestamp]["main"]["temp_min"] - 273.15, 2)} '
                    + f'to {round(raw["list"][timestamp]["main"]["temp_max"] - 273.15, 2)}\n'
                    + f'humidity: {raw["list"][timestamp]["main"]["humidity"]}\n\n'
                )
            UV_index_ls = [
                f"{pretty_date(i.ref_time, offset=offset)}: {i.value}"
                for i in uvmgr.uvindex_forecast_around_coords(
                    lat=raw["city"]["coord"]["lat"], lon=raw["city"]["coord"]["lon"]
                )
            ]
            result += (
                f'sunrise: {pretty_date(raw["city"]["sunrise"], offset=offset)}\n'
                + f'sunset: {pretty_date(raw["city"]["sunset"], offset=offset)}\n'
                + f"UV index: {UV_index_ls}\n"
            )
            result += "以上資訊可能會因為天氣變化快等不可預測因素而有所誤差。建議隨時留意最新的天氣資訊。"
            print(f"Ended at {datetime.now()}")
            return result
        except Exception as err:
            return f"Error fetching weather data: {err}"
        
if __name__ == "__main__":
    mcp.run()