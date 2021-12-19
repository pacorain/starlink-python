Note that while starlink-python is being developed, its APIs are subject to change heavily.

# 0.1.0

- Prepare to publish to PyPI
- Write some tests (though nearly not enough)
- Also write hardware_test.py for new hardware or firmware releases that may break functionality in the future.

## TODO:
- I discovered that a lot of the stuff I was looking for (such as public IP address) are stored in the router. I should make a StarlinkRouter class.
- Write more tests to make sure the right gRPC calls are being made to get data.

# 0.0.3
- Parsed the rest of `DishGetStatusResponse` into `DishStatus` properties
- Created `DishAlert` enum for alerts
- Created `OutageReason` enum for outages

# 0.0.2

- Alias `spacex.starlink.dish.StarlinkDish` to `spacex.starlink.StarlinkDish`
- Refactor `StarlinkDish` to keep gRPC connection open
- Add `close()` methods and context manager (i.e. `with StarlinkDish() as dish:`)
- Add ability to get status and parse it with `DishStatus` class
  - Determine if the dish is connected or obstructed

# 0.0.1

- Initial check-in
- Connects to Starlink