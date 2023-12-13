from typing import Callable, List, TypeVar, Any

# Define a generic type for the elements of the interesting_input list
T = TypeVar("T")


def delta_debug(
    interesting_test: Callable[[List[T]], bool],
    interesting_input: List[T],
    granularity: int = 2,
) -> List[T]:
    assert granularity >= 2, "granularity must be at least 2"
    assert isinstance(interesting_input, list), "interesting_input must be a list."
    assert interesting_test(
        interesting_input
    ), "The initial interesting_input must pass the 'interesting_test'."

    # From now on we represent each input item as a sorted list of their indices.
    interesting_indicies = [i for i in range(len(interesting_input))]

    def reconstruct_from_indicies(indices: List[int]) -> List[T]:
        return [interesting_input[i] for i in indices]

    def _interesting_test(to_check: List[int]) -> bool:
        return interesting_test(reconstruct_from_indicies(to_check))

    while len(interesting_indicies) > 1:
        chunk_size = (len(interesting_indicies) + granularity - 1) // granularity
        subsets = [
            interesting_indicies[i : i + chunk_size]
            for i in range(0, len(interesting_indicies), chunk_size)
        ]
        temp_interesting_indicies = interesting_indicies
        some_subset_is_interesting = False

        for subset in subsets:
            if _interesting_test(subset):
                temp_interesting_indicies = subset
                some_subset_is_interesting = True
                break

        if not some_subset_is_interesting:
            for subset in subsets:
                complement = sorted(set(interesting_indicies) - set(subset))
                if _interesting_test(complement):
                    temp_interesting_indicies = complement
                    some_subset_is_interesting = True
                    break

        if some_subset_is_interesting:
            interesting_indicies = temp_interesting_indicies
            granularity = max(2, granularity - 1)
        else:
            if granularity == len(interesting_indicies):
                break
            granularity = min(len(interesting_indicies), granularity * 2)

    return reconstruct_from_indicies(interesting_indicies)


if __name__ == "__main__":
    import argparse, subprocess, shutil, os

    parser = argparse.ArgumentParser(
        description="Minimize a file using delta debugging."
    )
    parser.add_argument(
        "--interesting", required=True, help="Path to the interesting test script."
    )
    parser.add_argument(
        "--to-minimize", required=True, help="Path to the file to minimize (it is minimized in destructively in place)."
    )
    parser.add_argument(
        "-b", "--bytes", action="store_true", help="Minimize by bytes instead of lines."
    )
    args = parser.parse_args()

    def write_to_minimize(data: List[Any]) -> None:
        with open(args.to_minimize, "wb") as f:
            if args.bytes:
                f.write(bytes(data))
            else:
                for line in data:
                    f.write(line)

    def is_interesting(to_check: List[Any]) -> bool:
        write_to_minimize(to_check)
        result = subprocess.run([args.interesting])
        interesting = result.returncode == 0
        if interesting:
            shutil.copy(
                args.to_minimize, args.to_minimize + ".ddmin_most_interesting_so_far"
            )
        return interesting

    # Read the file as bytes
    with open(args.to_minimize, "rb") as f:
        input_bytes = f.read()

    # Split into lines if not in byte mode, otherwise treat as individual bytes
    input_data: List[Any]
    if args.bytes:
        input_data = list(input_bytes)
    else:
        input_data = input_bytes.splitlines(keepends=True)

    minimized = delta_debug(
        is_interesting,
        input_data,
    )
    write_to_minimize(minimized)
    os.remove(args.to_minimize + ".ddmin_most_interesting_so_far")
