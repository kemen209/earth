# era5_electromagnetic_impact_2025-09_grib.py
import os
import time
import cdsapi

MONTH = "09"
YEAR = "2025"
OUTDIR = "era5_electromagnetic_impact_grib_202509"
os.makedirs(OUTDIR, exist_ok=True)

# 数据集
dataset = "reanalysis-era5-single-levels"

# 影响电磁传播的变量
VARIABLES = [
    "2m_temperature",  # 2米温度
    "2m_relative_humidity",  # 2米相对湿度
    "10m_u_component_of_wind",  # 10米风速-东西分量
    "10m_v_component_of_wind",  # 10米风速-南北分量
    "mean_sea_level_pressure",  # 海平面气压
    "total_cloud_cover",  # 总云量
    "total_precipitation",  # 总降水
]

HOURS = [f"{h:02d}:00" for h in range(24)]

def fetch_day(day):
    fn = os.path.join(OUTDIR, f"era5_elec_{YEAR}{MONTH}{day:02d}.grib")
    if os.path.exists(fn) and os.path.getsize(fn) > 0:
        print(f"[SKIP] {fn} already exists.")
        return
    req = {
        "product_type": ["reanalysis"],
        "variable": VARIABLES,
        "year": YEAR,
        "month": MONTH,
        "day": f"{day:02d}",
        "time": HOURS,
        "data_format": "grib",
        "download_format": "unarchived"
    }
    c = cdsapi.Client()
    for attempt in range(5):
        try:
            print(f"[REQ] {fn} (attempt {attempt+1})")
            print(req)
            c.retrieve(dataset, req, fn)
            if os.path.exists(fn) and os.path.getsize(fn) > 0:
                print(f"[OK ] {fn}")
                return
        except Exception as e:
            print(f"[ERR] {e}")
        time.sleep(10 * (attempt + 1))  # back-off
    raise RuntimeError(f"Failed to download {fn} after retries.")


def main():
    for d in range(1, 31):  # Download 2025年9月的30天
        fetch_day(d)
    # Optional: Merge all files into one large GRIB file (useful for continuous use)
    os.system(
        f"cat {OUTDIR}/era5_elec_{YEAR}{MONTH}*.grib > {OUTDIR}/era5_elec_{YEAR}{MONTH}.grib")
    print(f"[DONE] merged: {OUTDIR}/era5_elec_{YEAR}{MONTH}.grib")


if __name__ == "__main__":
    main()
