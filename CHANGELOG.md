# 0.0.2

Note that while starlink-python is being developed, its APIs are subject to change heavily.

## Changes

- Alias `spacex.starlink.dish.StarlinkDish` to `spacex.starlink.StarlinkDish`
- Refactor `StarlinkDish` to keep gRPC connection open
- Add `close()` methods and context manager (i.e. `with StarlinkDish() as dish:`)
- Add ability to get status and parse it with `DishStatus` class
  - Determine if the dish is connected or obstructed

## TODO

- Parse more status info
- Get network information

# 0.0.1

- Initial check-in
- Connects to Starlink