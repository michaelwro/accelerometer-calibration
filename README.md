# Accelerometer Calibration Procedure

A general method for calibrating accelerometer sensors, along with a few helpful scripts

Developed By: Michael Wrona, *B.S. Aerospace Engineering*

**GitHub:** [@michaelwro](https://github.com/michaelwro)

**YouTube:** [@MicWro Engr](https://www.youtube.com/channel/UCIeZzuXHGm7zqSFvT8xGoIQ)

**Blog:** [mwrona.com](https://mwrona.com)

![Calibration result](imgs/Plot_XY.png)

### Pip Install Python3 Dependencies

```bash
$ pip3 install numpy matplotlib pandas  # pip for Windows
```

### Conda Install Python3 Dependencies

```bash
(myenv) $ conda install -c conda-forge numpy matplotlib pandas
```

---

Before following these steps, I highly reccommend watching the video I created about this process. You can watch it [at this link.]()

## Step 1: Output Comma-Separated Data

`record-data.py` expects to read comma-separated accelerometer data from a serial connection. Each sensor is different, so you will need to write your own microcontroller code to output comma-separated accelerometer measurements to a serial port, similar to this format:

```bash
0.0642208,-0.05490976,1.02357024
```

## Step 2: Measure Accelerometer Data

Once you can output comma-separated raw accelerometer measurements over a serial connection, you can begin logging data. The accelerometer must 

## Step 2: Record Measurements to File

Magneto expects your accelerometer 





## Resources

* [Magneto download link](https://sites.google.com/site/sailboatinstruments1/home)
* [YouTube vide]()
* [GitHub code repo](https://github.com/michaelwro/accelerometer-calibration)

