影响电磁传播的气象数据主要与**大气中的温度、湿度、风速、气压、云层**等因素相关。以下是针对电磁传播影响最直接的气象要素，并提供了**ERA5**中相关数据的下载脚本。

### 影响电磁传播的主要气象要素

1. **温度（2m温度、500 hPa温度）**
   - 电磁波在不同气温下的传播速度不同，影响折射率。
2. **湿度（2m湿度、相对湿度）**
   - 湿度影响电磁波的吸收与传播路径，尤其在微波频段。
3. **风速（10m风速）**
   - 风速对电磁波传播的影响较小，但强风可影响传播稳定性。
4. **气压（海平面气压）**
   - 气压变化直接影响电波的折射，尤其是低频和中频电波。
5. **云层/降水（总云量、降水量）**
   - 云层对电磁波的传播有遮挡作用，降水会导致信号衰减。

------

### 下载脚本

以下是**ERA5（逐小时，全球，2025年9月）**相关气象数据（影响电磁传播的要素）的下载脚本，按需下载 **2米温度、2米湿度、10米风速、海平面气压、总云量、总降水** 等变量。

**注意：脚本不能工作，请直接到网站下载：https://cds.climate.copernicus.eu/api-how-to **


```python
# era5_grib.py
import os, time
import cdsapi

MONTH = "09"
YEAR = "2025"
OUTDIR = "era5_grib_202509"
os.makedirs(OUTDIR, exist_ok=True)

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
        "product_type": "reanalysis",
        "variable": VARIABLES,
        "year": YEAR,
        "month": MONTH,
        "day": [f"{day:02d}"],
        "time": HOURS,
        "format": "grib",
    }
    c = cdsapi.Client()
    for attempt in range(5):
        try:
            print(f"[REQ] {fn} (attempt {attempt+1})")
            c.retrieve("reanalysis-era5-single-levels", req, fn)
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
    # os.system(f"cat {OUTDIR}/era5_elec_{YEAR}{MONTH}*.grib > {OUTDIR}/era5_elec_{YEAR}{MONTH}.grib")
    print(f"[DONE] merged: {OUTDIR}/era5_elec_{YEAR}{MONTH}.grib")

if __name__ == "__main__":
    main()
```

### 如何运行：

1. **安装依赖**：

   ```bash
   pip install cdsapi
   ```

2. **配置CDS API 密钥**：在 `~/.cdsapirc` 中填写你的 **CDS API key**。具体步骤见[官方文档](https://cds.climate.copernicus.eu/api-how-to)。

3. **运行脚本**：

   ```bash
   python era5_grib.py
   ```

### 主要气象变量：

- **2m_temperature**：2米高度的温度数据
- **2m_relative_humidity**：2米高度的相对湿度数据
- **10m_u_component_of_wind**、**10m_v_component_of_wind**：10米高度的风速（分量）
- **mean_sea_level_pressure**：海平面气压
- **total_cloud_cover**：云层覆盖总量
- **total_precipitation**：总降水量

### 合并和验证：

- 下载完后，脚本会把单日的文件合并成一个大文件（`era5_elec_202509.grib`），方便进一步处理。

- 合并后的文件可以通过 **wgrib2** 工具来验证和查看：

  ```bash
  wgrib2 era5_elec_202509.grib -s | head  # 查看文件头信息，确认变量是否完整
  ```

### 后续处理：

- **转换为 NetCDF**：如果你想方便进行分析，可以使用 `wgrib2` 或 Python 中的 `cfgrib` 库将 GRIB2 转换为 NetCDF 格式，进一步结合 `xarray` 进行处理。

如果有任何其他需求（如区域裁剪、特殊变量、或其他时效），可以告诉我，我会调整脚本给你。