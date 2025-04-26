# BusRadar24
A package to get the location of busses, currently only in Bonn

## How to use
```python
import busradar24
# To get the location/data for a bus/tram line, use it as following (example for line 600)
busradar24.get_information("600") # Will output a dictionary
# To get the list of all existing bus lines (and their corresponding id's), do the following
busradar24.bus_lines # Will output a dictionary
```

More following later on
