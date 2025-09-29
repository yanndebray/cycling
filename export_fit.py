import pandas as pd
import garmin_fit_sdk as garmin
import glob

def fit2df(fit_file):
    stream = garmin.Stream.from_file(fit_file)
    decoder = garmin.Decoder(stream)
    m, errors = decoder.read()
    df = pd.DataFrame(m['record_mesgs'])
    # Only keep timestamp, position_lat, position_long, distance, enhanced_speed, enhanced_altitude
    df = df[['timestamp', 'position_lat', 'position_long', 'distance', 'enhanced_speed', 'enhanced_altitude']]
    degPerSemicircle = 180 / (2**31)
    df['position_lat'] = df['position_lat'] * degPerSemicircle
    df['position_long'] = df['position_long'] * degPerSemicircle
    return df

if __name__ == "__main__":
    l = glob.glob("*.fit")
    df = fit2df(l[1])
    df.to_csv("garmin.csv",index=None)
