from os import PathLike
from subprocess import PIPE

from reduce_binary import popen_reduce, run_reduce


def protonate(
    in_pdb_file: str | PathLike,
    out_pdb_file: str | PathLike,
    *,
    remove_hydrogen_first=True,
    print_stderr=False,
) -> None:
    """
    Protonate (i.e., add hydrogens) a pdb using reduce and save to an output file.

    Args:
        in_pdb_file: file to protonate.
        out_pdb_file: output file where to save the protonated pdb file.
        remove_hydrogen_first: whether to remove hydrogens first.
        print_stderr: let stderr be printed to the console. Otherwise, it is suppressed.
    """
    stderr = None if print_stderr else PIPE
    if remove_hydrogen_first:
        with open(out_pdb_file, "w") as outfile:
            # To pipe the output directly to the next reduce call, we need to use the subprocess.Popen

            # 1. Remove protons first, in case the structure is already protonated
            proc = popen_reduce(
                ["-Trim", in_pdb_file],
                stdout=PIPE,
                stderr=stderr,
            )

            # 2. Now add them again.
            run_reduce(
                ["-HIS", "-"],
                stdin=proc.stdout,
                stdout=outfile,
                stderr=stderr,
            )
            proc.wait()
    else:
        with open(out_pdb_file, "w") as outfile:
            run_reduce(
                ["-HIS", in_pdb_file],
                stdout=outfile,
                stderr=stderr,
            )
