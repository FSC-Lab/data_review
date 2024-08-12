# F450 Flight Data Analysis

- The bag files are in this [google_drive](https://drive.google.com/drive/u/0/folders/1oCRPpMkX4U8UqFsCuI7HKh1kR6G_lI7w).

- bags_0726 is the most recent flight tests with different forms of UDE implementations.

- run src/bag_load/run ros_bag_f450_test_load.py to load the bag file

- run the following scripts to show the flight data

| File  |      Content      |
|:----------:|:-------------:|
|src/data_display/flight_review_ude_ai_0726.ipynb| acceleration based UDE on F450 |
|src/data_display/flight_review_ude_vb_0726.ipynb| velocity based UDE in body-fixed frame on F450 |
|src/data_display/flight_review_ude_vi_0726.ipynb| velocity based UDE in inertial frame on F450 |