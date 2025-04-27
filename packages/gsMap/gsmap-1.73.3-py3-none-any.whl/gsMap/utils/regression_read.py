import os

import numpy as np
import pandas as pd


# Fun for reading gwas data
def _read_sumstats(fh, alleles=False, dropna=False):
    """
    Parse gwas summary statistics.
    """
    print(f"Reading summary statistics from {fh} ...")
    sumstats = ps_sumstats(fh, alleles=alleles, dropna=dropna)
    print(f"Read summary statistics for {len(sumstats)} SNPs.")

    m = len(sumstats)
    sumstats = sumstats.drop_duplicates(subset="SNP")
    if m > len(sumstats):
        print(f"Dropped {m - len(sumstats)} SNPs with duplicated rs numbers.")

    return sumstats


def ps_sumstats(fh, alleles=False, dropna=True):
    """
    Parses .sumstats files. See docs/file_formats_sumstats.txt.
    """
    dtype_dict = {"SNP": str, "Z": float, "N": float, "A1": str, "A2": str}
    compression = get_compression(fh)
    usecols = ["SNP", "Z", "N"]
    if alleles:
        usecols += ["A1", "A2"]

    try:
        x = read_csv(fh, usecols=usecols, dtype=dtype_dict, compression=compression)
    except (AttributeError, ValueError) as e:
        raise ValueError("Improperly formatted sumstats file: " + str(e.args)) from e

    if dropna:
        x = x.dropna(how="any")

    return x


def get_compression(fh):
    """
    Determin the format of compression used with read_csv?
    """
    if fh.endswith("gz"):
        compression = "gzip"
    elif fh.endswith("bz2"):
        compression = "bz2"
    else:
        compression = None
    # -
    return compression


def read_csv(fh, **kwargs):
    """
    Read the csv data
    """
    return pd.read_csv(fh, sep=r"\s+", na_values=".", **kwargs)


# Fun for reading loading LD scores
def which_compression(fh):
    """
    Given a file prefix, figure out what sort of compression to use.
    """
    if os.access(fh + ".bz2", 4):
        suffix = ".bz2"
        compression = "bz2"
    elif os.access(fh + ".gz", 4):
        suffix = ".gz"
        compression = "gzip"
    elif os.access(fh + ".parquet", 4):
        suffix = ".parquet"
        compression = "parquet"
    elif os.access(fh + ".feather", 4):
        suffix = ".feather"
        compression = "feather"
    elif os.access(fh, 4):
        suffix = ""
        compression = None
    else:
        raise OSError(f"Could not open {fh}[./gz/bz2/parquet/feather]")
    # -
    return suffix, compression


def _read_ref_ld_v2(ld_file):
    suffix = ".l2.ldscore"
    file = ld_file
    first_fh = f"{file}1{suffix}"
    s, compression = which_compression(first_fh)
    print(f"Reading ld score annotations from {file}[1-22]{suffix}.{compression}")
    ref_ld = pd.concat(
        [pd.read_feather(f"{file}{chr}{suffix}{s}") for chr in range(1, 23)], axis=0
    )
    # set first column as index
    ref_ld.rename(columns={"index": "SNP"}, inplace=True)
    ref_ld.set_index("SNP", inplace=True)
    return ref_ld


def _read_M_v2(ld_file, n_annot, not_M_5_50):
    suffix = ".l2.M"
    if not not_M_5_50:
        suffix += "_5_50"
    M_annot = np.array(
        [
            np.loadtxt(
                f"{ld_file}{chr}{suffix}",
            )
            for chr in range(1, 23)
        ]
    )
    assert M_annot.shape == (22, n_annot)
    return M_annot.sum(axis=0).reshape((1, n_annot))


# Fun for reading M annotations
def _read_M(ld_file, n_annot, not_M_5_50):
    """
    Read M (--M, --M-file, etc).
    """
    M_annot = M(ld_file, common=(not not_M_5_50))

    try:
        M_annot = np.array(M_annot).reshape((1, n_annot))
    except ValueError as e:
        raise ValueError(
            "# terms in --M must match # of LD Scores in --ref-ld.\n" + str(e.args)
        ) from e
    return M_annot


def M(fh, common=False):
    """
    Parses .l{N}.M files, split across num chromosomes.
    """
    suffix = ".l2.M"
    if common:
        suffix += "_5_50"
    # -
    M_array = []
    for i in range(1, 23):
        M_current = pd.read_csv(f"{fh}{i}" + suffix, header=None)
        M_array.append(M_current)

    M_array = pd.concat(M_array, axis=1).sum(axis=1)
    # -
    return np.array(M_array).reshape((1, len(M_array)))


def _check_variance_v2(M_annot, ref_ld):
    ii = ref_ld.var() == 0
    if ii.all():
        raise ValueError("All LD Scores have zero variance.")
    elif not ii.any():
        print("No partitioned LD Scores have zero variance.")
    else:
        ii_snp = ii_m = np.array(~ii)
        print(f"Removing {sum(ii)} partitioned LD Scores with zero variance.")
        ref_ld = ref_ld.iloc[:, ii_snp]
        M_annot = M_annot[:, ii_m]
    return M_annot, ref_ld


def _read_w_ld(w_file):
    suffix = ".l2.ldscore"
    file = w_file
    first_fh = f"{file}1{suffix}"
    s, compression = which_compression(first_fh)
    #
    w_array = []
    print(f"Reading ld score annotations from {file}[1-22]{suffix}.{compression}")

    for chr in range(1, 23):
        file_chr = f"{file}{chr}{suffix}{s}"
        #
        if compression == "parquet":
            x = pd.read_parquet(file_chr)
        elif compression == "feather":
            x = pd.read_feather(file_chr)
        else:
            x = pd.read_csv(file_chr, compression=compression, sep="\t")

        x = x.sort_values(by=["CHR", "BP"])

        columns_to_drop = ["MAF", "CM", "Gene", "TSS", "CHR", "BP"]
        columns_to_drop = [col for col in columns_to_drop if col in x.columns]
        x = x.drop(columns_to_drop, axis=1)

        w_array.append(x)
    #
    w_ld = pd.concat(w_array, axis=0)
    w_ld.columns = ["SNP", "LD_weights"]

    return w_ld
