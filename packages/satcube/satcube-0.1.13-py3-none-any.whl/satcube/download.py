import pathlib
import ee
import cubexpress
import pandas as pd


def download_data(
    *,                     # keyword-only
    lon: float,
    lat: float,
    cloud_max: int = 40,
    edge_size: int = 2_048,
    start: str,
    end: str,
    output: str = "raw",
    scale: int = 10,
    nworks: int = 4,
    mosaic: bool = True
) -> pd.DataFrame:
    """
    Download a Sentinel cube for (lon, lat) and return its metadata.

    Parameters
    ----------
    lon, lat        Center point in degrees.
    cloud_max       Max cloud cover (%).
    edge_size       Square side length (m).
    start, end      YYYY-MM-DD date range.
    output          Folder for GeoTIFFs.
    scale           Pixel size (m).
    nworks          Parallel workers.
    mosaic          Merge scenes per date.
    auto_init_gee   Call ee.Initialize() if needed.

    Returns
    -------
    pandas.DataFrame
        Scene catalogue used for the request.
    """
    # Filter scenes
    df = cubexpress.cloud_table(
        lon=lon,
        lat=lat,
        edge_size=edge_size,
        scale=scale,
        cloud_max=cloud_max,
        start=start,
        end=end,
    )

    # Build requests + ensure dir
    requests = cubexpress.table_to_requestset(df, mosaic=mosaic)
    pathlib.Path(output).mkdir(parents=True, exist_ok=True)

    # Download cube
    cubexpress.get_cube(requests, output, nworks)
    return df
